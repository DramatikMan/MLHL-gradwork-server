import base64
import io
import logging
from pathlib import Path

import dramatiq
import numpy as np
import onnxruntime as ort
import sqlalchemy as sa
from PIL import Image

from gwserver.core import config
from gwserver.core.database import DB
from gwserver.model import Image as Mapper


@dramatiq.actor
def predict(uid: int, content: str) -> None:
    path = Path(config.MODEL_VOLUME).joinpath(config._MODEL_FNAME)
    inference = ort.InferenceSession(str(path), providers=["CPUExecutionProvider"])

    binary = base64.b64decode(content.encode("utf-8"))
    image = Image.open(io.BytesIO(binary), formats=("JPEG",)).resize((299, 299))
    array = np.expand_dims(np.moveaxis(np.asarray(image).astype(np.float32), -1, 0), axis=0)
    array /= 255.0

    outputs = inference.run(None, {"input": array})
    prediction = int(outputs[0][0].argmax(0)) + 1

    db = DB.make_session()

    try:
        stmt = sa.update(Mapper).where(Mapper.uid == uid).values(category_uid=prediction)
        db.execute(stmt)
        db.commit()
    except Exception as e:
        logging.exception(f"Failed to classify image [uid = {uid}]:\n{e}")
        raise
    finally:
        db.close()
