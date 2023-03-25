![CI](https://github.com/DramatikMan/MLHL-gradwork-server/actions/workflows/ci.yml/badge.svg)

---

## Смежные проекты

- [web UI](https://github.com/DramatikMan/MLHL-gradwork-web-UI)

---

## CLI

```
gwserver --help
```

---

## Переменные окружения

```python
# API
GWSERVER_API_ROOT_PATH: str = ""
GWSERVER_API_WORKERS: int = 4
GWSERVER_API_PORT: int = 8000

# database
GWSERVER_DB_HOST: str = "postgres"
GWSERVER_DB_USER: str = "postgres"
GWSERVER_DB_PWD: str = "postgres"
GWSERVER_DB_PORT: int = 5432
GWSERVER_DB_NAME: str = "postgres"

# S3
GWSERVER_S3_URL: str = "https://storage.yandexcloud.net"
GWSERVER_S3_ID: str
GWSERVER_S3_SECRET: str
GWSERVER_S3_BUCKET: str = "gwserver"
GWSERVER_S3_USER_DATA_SUBPATH: str = "userdata"

# RabbitMQ
GWSERVER_RABBITMQ_HOST: str = "broker"

# model
GWSERVER_MODEL_KEY: str = "model.onnx"
GWSERVER_MODEL_VOLUME: str = "/app/model"
```
