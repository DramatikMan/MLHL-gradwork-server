import base64
import io
import logging
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np
import onnxruntime as ort
import sqlalchemy as sa
from PIL import Image

from gwserver.core import config
from gwserver.core.database import DB
from gwserver.model import Image as Mapper
from gwserver.model.constant import RGB, RYB


def get_distance(p1: tuple[int, int, int], p2: tuple[int, int, int]) -> float:
    return float(((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2) ** 0.5)


def get_dominant_color(mapping: dict[str, tuple[int, int, int]], px: Any) -> str:
    colors: list[str] = []

    for x in range(299):
        for y in range(299):
            dominant_color, min_distance = "#FFFFFF", float("+inf")

            for key, color in mapping.items():
                if (distance := get_distance(color, px[x, y])) < min_distance:
                    min_distance = distance
                    dominant_color = key

            colors.append(dominant_color)

    return Counter(colors).most_common()[0][0]


def predict(uid: int, content: str) -> None:
    path = Path(config.MODEL_VOLUME).joinpath(config._MODEL_FNAME)
    inference = ort.InferenceSession(str(path), providers=["CPUExecutionProvider"])

    binary = base64.b64decode(content.encode("utf-8"))
    image = Image.open(io.BytesIO(binary), formats=("JPEG",)).resize((299, 299))
    array = np.expand_dims(np.moveaxis(np.asarray(image).astype(np.float32), -1, 0), axis=0)
    array /= 255.0

    outputs = inference.run(None, {"input": array})
    prediction = int(outputs[0][0].argmax(0)) + 1

    db, pixel_access = DB.make_session(), image.load()

    try:
        stmt = (
            sa.update(Mapper)
            .where(Mapper.uid == uid)
            .values(
                category_uid=prediction,
                color_rgb=get_dominant_color(RGB, pixel_access),
                color_ryb=get_dominant_color(RYB, pixel_access),
            )
        )

        db.execute(stmt)
        db.commit()
    except Exception as e:
        logging.exception(f"Failed to classify image [uid = {uid}]:\n{e}")
        raise
    finally:
        db.close()
