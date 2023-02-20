import base64

import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from gwserver.core import config
from gwserver.core.s3 import s3

rabbitmq_broker = RabbitmqBroker(host=config.RABBITMQ_HOST)
dramatiq.set_broker(rabbitmq_broker)


@dramatiq.actor
def upload(path: str, content: str) -> None:
    s3.upload(path, base64.b64decode(content.encode("utf-8")))
