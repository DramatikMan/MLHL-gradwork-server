import base64
import io
from pathlib import Path

import numpy as np
import onnxruntime as ort
import sqlalchemy as sa
from color_utils import RGB, RYB
from PIL import Image

from gwserver.core import config
from gwserver.core.database import DB
from gwserver.model import Image as Mapper


def predict(uid: int, content: str) -> None:
    path = Path(config.MODEL_VOLUME).joinpath(config._MODEL_FNAME)
    inference = ort.InferenceSession(str(path), providers=["CPUExecutionProvider"])

    binary = base64.b64decode(content.encode("utf-8"))
    image = Image.open(io.BytesIO(binary), formats=("JPEG",))
    array = np.asanyarray(image)

    inp = np.expand_dims(
        np.moveaxis(np.asarray(image.resize((299, 299))).astype(np.float32), -1, 0),
        axis=0,
    )

    outputs = inference.run(None, {"input": inp / 255.0})
    prediction = int(outputs[0][0].argmax(0)) + 1

    try:
        db = DB.make_session()

        stmt = (
            sa.update(Mapper)
            .where(Mapper.uid == uid)
            .values(
                category_uid=prediction,
                color_rgb=RGB.get_dominant_color(array),
                color_ryb=RYB.get_dominant_color(array),
            )
        )

        db.execute(stmt)
        db.commit()
    finally:
        db.close()
