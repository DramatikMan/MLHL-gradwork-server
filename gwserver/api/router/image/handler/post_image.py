import base64
import io

import dramatiq
import sqlalchemy as sa
from litestar.datastructures import UploadFile
from litestar.enums import RequestEncodingType
from litestar.exceptions import HTTPException
from litestar.params import Body
from PIL import Image as PIL

from gwserver import tasks
from gwserver.core import config
from gwserver.model import Image as Mapper
from gwserver.schema.response import Image as ResponseOne


async def handler(
    session: sa.orm.Session,
    data: UploadFile = Body(media_type=RequestEncodingType.MULTI_PART),
) -> ResponseOne:
    content = await data.read()

    try:
        image = PIL.open(io.BytesIO(content), formats=("JPEG",))
    except Exception as ex:
        raise HTTPException(detail=str(ex), status_code=422)

    if not image.size[0] == image.size[1]:
        raise HTTPException(detail="Expected a square JPEG image.", status_code=400)

    stmt = sa.select(sa.func.count()).select_from(Mapper)
    count: int | None = session.scalar(stmt)

    if count is None:
        raise HTTPException(
            detail="Could not count currently existing images.",
            status_code=500,
        )

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
