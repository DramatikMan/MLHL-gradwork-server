import base64
import imghdr
import io

import dramatiq
import sqlalchemy as sa
from litestar import post, status_codes
from litestar.datastructures import UploadFile
from litestar.enums import RequestEncodingType
from litestar.params import Body
from PIL import Image as PIL

from gwserver import tasks
from gwserver.core import config
from gwserver.model import Image as Mapper
from gwserver.schema.error.base import DynamicAPIError
from gwserver.schema.response import Image as ResponseOne

BadImage = DynamicAPIError(
    name="BadImage",
    status_code=status_codes.HTTP_400_BAD_REQUEST,
    description="Expected a square JPEG image",
)


ImageOpenFailure = DynamicAPIError(
    name="ImageOpenFailure",
    status_code=status_codes.HTTP_422_UNPROCESSABLE_ENTITY,
    description="Failed to open the payload with Pillow",
)


@post(
    content_media_type="image/jpeg",
    responses=BadImage.response | ImageOpenFailure.response,
)
async def handler(
    session: sa.orm.Session,
    data: UploadFile = Body(media_type=RequestEncodingType.MULTI_PART),
) -> ResponseOne:
    content = await data.read()

    if (what := imghdr.what(io.BytesIO(content))) != "jpeg":
        if what is None:
            raise BadImage("Expected JPEG image", extra={"type": None})

        got = what.upper()
        raise BadImage(f"Expected JPEG image, got {got} instead", extra={"type": got})

    try:
        image = PIL.open(io.BytesIO(content), formats=("JPEG",))
    except Exception as ex:
        raise ImageOpenFailure(str(ex))

    if not (width := image.size[0]) == (height := image.size[1]):
        raise BadImage(
            f"Expected a square image, got size ({width}, {height}) instead",
            extra={"size": [width, height]},
        )

    stmt = sa.select(sa.func.count()).select_from(Mapper)
    count: int | None = session.scalar(stmt)

    if count is None:
        raise RuntimeError("Could not count currently existing images.")

    path = f"{config.S3_USER_DATA_SUBPATH}/{count + 1}.jpg"
    record = Mapper(path=path)

    if image.size[0] != 224:
        buffer = io.BytesIO()
        image.resize((224, 224)).save(buffer, format="JPEG")
        buffer.seek(0)
        content = buffer.read()

    content_string = base64.b64encode(content).decode()
    session.add(record)
    session.commit()
    session.refresh(record)

    parallel = (
        tasks.upload.message(path, content_string),
        tasks.predict.message(record.uid, content_string),
    )

    dramatiq.group(parallel).run()  # type: ignore[no-untyped-call]

    return ResponseOne.parse_obj(
        {
            "uid": record.uid,
            "path": record.path,
        }
    )
