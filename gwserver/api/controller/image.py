import base64
import io

import sqlalchemy as sa
import starlite as s
from PIL import Image
from starlite import status_codes

from gwserver import model, tasks
from gwserver.api.schema import IMAGE, UID, error
from gwserver.api.schema.error import ApiException
from gwserver.core import config
from gwserver.core.database import DB


class Controller(s.Controller):
    @s.get(
        path="{uid:int}",
        dependencies={"db": s.Provide(DB)},
        responses={
            status_codes.HTTP_404_NOT_FOUND: s.ResponseSpec(
                model=error.NOT_FOUND,
                description="Image not found",
            )
        },
    )
    async def get_image(self, uid: UID, db: sa.orm.Session) -> IMAGE:
        record = db.get(model.Image, uid)

        if record is None:
            raise ApiException(error.NOT_FOUND)

        return IMAGE(
            uid=record.uid,
            path=record.path,
            category=record.category.title,
        )

    @s.post(
        content_media_type="image/jpeg",
        dependencies={"db": s.Provide(DB)},
        responses={
            status_codes.HTTP_422_UNPROCESSABLE_ENTITY: s.ResponseSpec(
                model=error.IMAGE_CHECK_FAILURE,
                description="Could not parse the payload as a JPEG image of size (224, 224)",
            ),
        },
    )
    async def post_image(
        self,
        db: sa.orm.Session,
        data: s.UploadFile = s.Body(media_type=s.RequestEncodingType.MULTI_PART),
    ) -> IMAGE:
        content = await data.read()

        try:
            image = Image.open(io.BytesIO(content), formats=("JPEG",))
            assert image.size == (224, 224)
        except Exception:
            raise ApiException(error.IMAGE_CHECK_FAILURE)

        stmt = sa.select(sa.func.count()).select_from(model.Image)
        count = db.scalar(stmt)

        if count is None:
            raise s.HTTPException(
                status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR,
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
