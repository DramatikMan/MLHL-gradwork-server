import base64
import io

from PIL import Image
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from starlite import (
    Body,
    HTTPException,
    Provide,
    RequestEncodingType,
    ResponseSpec,
    UploadFile,
    get,
    post,
)
from starlite.controller import Controller as Base
from starlite.status_codes import (
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from gwserver import model, tasks
from gwserver.api.schema import IMAGE, UID, error
from gwserver.api.schema.error import ApiException
from gwserver.core import config
from gwserver.core.database import DB


class Controller(Base):
    @get(
        path="{uid:int}",
        dependencies={"db": Provide(DB)},
        responses={
            HTTP_404_NOT_FOUND: ResponseSpec(
                model=error.NOT_FOUND,
                description="Image not found",
            )
        },
    )
    async def get_image(self, uid: UID, db: Session) -> IMAGE:
        record = db.get(model.Image, uid)

        if record is None:
            raise ApiException(error.NOT_FOUND)

        return IMAGE(
            uid=record.uid,
            path=record.path,
            category=record.category.title,
        )

    @post(
        content_media_type="image/jpeg",
        dependencies={"db": Provide(DB)},
        responses={
            HTTP_422_UNPROCESSABLE_ENTITY: ResponseSpec(
                model=error.IMAGE_CHECK_FAILURE,
                description="Could not parse the payload as a JPEG image of size (224, 224)",
            ),
        },
    )
    async def post_image(
        self,
        db: Session,
        data: UploadFile = Body(media_type=RequestEncodingType.MULTI_PART),
    ) -> IMAGE:
        content = await data.read()

        try:
            image = Image.open(io.BytesIO(content), formats=("JPEG",))
            assert image.size == (224, 224)
        except Exception:
            raise ApiException(error.IMAGE_CHECK_FAILURE)

        stmt = select(func.count()).select_from(model.Image)
        count = db.scalar(stmt)

        if count is None:
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Image count scalar returned "None".',
            )

        path = f"{config.S3_USER_DATA_SUBPATH}/{count + 1}.jpg"
        record = model.Image(path=path)

        db.add(record)
        db.commit()
        db.refresh(record)

        tasks.upload.send(path=path, content=base64.b64encode(content).decode())

        return IMAGE(
            uid=record.uid,
            path=record.path,
        )
