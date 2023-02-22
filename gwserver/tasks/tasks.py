import base64
import random

import dramatiq
import sqlalchemy as sa
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from gwserver import model
from gwserver.core import config
from gwserver.core.database import DB
from gwserver.core.s3 import s3

rabbitmq_broker = RabbitmqBroker(host=config.RABBITMQ_HOST)
dramatiq.set_broker(rabbitmq_broker)


@dramatiq.actor
def upload(path: str, content: str) -> None:
    s3.upload(path, base64.b64decode(content.encode("utf-8")))


@dramatiq.actor
def predict(uid: int, content: str) -> None:
    db = DB.make_session()

    try:
        stmt = (
            sa.update(model.Image)
            .where(model.Image.uid == uid)
            .values(category_uid=random.randint(1, 15))  # * placeholder random classifier
        )

        db.execute(stmt)
        db.commit()
    except Exception as e:
        raise RuntimeError(f"Failed to classify image [uid = {uid}]:\n{e}")
    finally:
        db.close()
