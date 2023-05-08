import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from gwserver.core import config

from .predict import predict as task_predict
from .upload import upload as task_upload

rabbitmq_broker = RabbitmqBroker(url=config._RABBITMQ_URL)  # type: ignore[no-untyped-call]
dramatiq.set_broker(rabbitmq_broker)

predict = dramatiq.actor(task_predict)
upload = dramatiq.actor(task_upload)

__all__ = ("upload", "predict")
