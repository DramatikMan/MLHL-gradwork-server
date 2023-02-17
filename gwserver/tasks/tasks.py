import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from gwserver.core import config

rabbitmq_broker = RabbitmqBroker(host=config.RABBITMQ_HOST)
dramatiq.set_broker(rabbitmq_broker)


@dramatiq.actor
def predict(image_path: str) -> str:
    return "test"
