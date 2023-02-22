import base64
import io

import dramatiq
import sqlalchemy as sa
import starlite as s
from PIL import Image
from starlite import status_codes

from gwserver import model, tasks
from gwserver.api.schema import IMAGE, UID
from gwserver.core import config
from gwserver.core.database import DB


class Controller(s.Controller):
    @s.get(path="{uid:int}", dependencies={"db": s.Provide(DB)})
    async def get_image(self, uid: UID, db: sa.orm.Session) -> IMAGE:
        record = db.get(model.Image, uid)

        if record is None:
            raise s.HTTPException(detail="Image not found by UID.", status_code=404)

        return IMAGE(
            uid=record.uid,
            path=record.path,
            category=record.category.title,
        )

    @s.post(content_media_type="image/jpeg", dependencies={"db": s.Provide(DB)})
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
            raise s.HTTPException(
                detail="Expected a JPEG image of size (224, 224).",
                status_code=422,
            )

        stmt = sa.select(sa.func.count()).select_from(model.Image)
        count = db.scalar(stmt)

        if count is None:
            raise s.HTTPException(
                detail='Image count scalar returned "None".',
                status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        path = f"{config.S3_USER_DATA_SUBPATH}/{count + 1}.jpg"
        record = model.Image(path=path)

        db.add(record)
        db.commit()
        db.refresh(record)

        content_string = base64.b64encode(content).decode()

        dramatiq.group(
            (
                tasks.upload.message(path, content_string),
                tasks.predict.message(record.uid, content_string),
            )
        ).run()

        return IMAGE(
            uid=record.uid,
            path=record.path,
        )
