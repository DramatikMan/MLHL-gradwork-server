import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from gwserver.core import config

from .predict import predict
from .upload import upload

rabbitmq_broker = RabbitmqBroker(host=config.RABBITMQ_HOST)
dramatiq.set_broker(rabbitmq_broker)


__all__ = ("upload", "predict")
