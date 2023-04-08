import base64
import io

import dramatiq
import sqlalchemy as sa
from litestar import status_codes
from litestar.datastructures import UploadFile
from litestar.enums import RequestEncodingType
from litestar.params import Body
from PIL import Image as PIL

from gwserver import tasks
from gwserver.core import config
from gwserver.model import Image as Mapper
from gwserver.schema.error.base import DynamicAPIError
from gwserver.schema.response import Image as ResponseOne

ImageOpenFailure = DynamicAPIError(
    name="ImageOpenFailure",
    status_code=status_codes.HTTP_422_UNPROCESSABLE_ENTITY,
    description="Failed to open the payload as a JPEG image",
)

ImageNotSquare = DynamicAPIError(
    name="ImageNotSquare",
    status_code=status_codes.HTTP_400_BAD_REQUEST,
    description="Expected a square JPEG image",
)


async def handler(
    session: sa.orm.Session,
    data: UploadFile = Body(media_type=RequestEncodingType.MULTI_PART),
) -> ResponseOne:
    content = await data.read()

    try:
        image = PIL.open(io.BytesIO(content), formats=("JPEG",))
    except Exception as ex:
        raise ImageOpenFailure(str(ex))

    if not (width := image.size[0]) == (height := image.size[1]):
        raise ImageNotSquare(f"Expected a square JPEG image, got ({width}, {height}) instead")

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
