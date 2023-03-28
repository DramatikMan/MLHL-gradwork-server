"""Add default data

Revision ID: 000000000002
Revises: 000000000001
Create Date: 2023-02-14 20:33:30.579450

"""
import pandas as pd
from alembic import op
from sqlalchemy import Integer, String
from sqlalchemy.sql import column, table

from gwserver.core.s3 import s3

# revision identifiers, used by Alembic.
revision = "000000000002"
down_revision = "000000000001"
branch_labels = None
depends_on = None


category_table = table(
    "CATEGORY",
    column("uid", Integer),
    column("title", String),
)

image_table = table(
    "IMAGE",
    column("uid", Integer),
    column("path", String),
    column("category_uid", Integer),
    column("color_rgb", String),
    column("color_ryb", String),
)


def upgrade() -> None:
    initial = s3.reader("database.csv")
    database = pd.read_csv(initial)

    #                       path category color_RGB color_RYB
    # 0  data/test/Bean/0001.jpg     Bean   #80FF00   #66B032
    # 1  data/test/Bean/0002.jpg     Bean   #80FF00   #66B032
    # 2  data/test/Bean/0003.jpg     Bean   #FF8000   #347C98
    # 3  data/test/Bean/0004.jpg     Bean   #0080FF   #347C98
    # 4  data/test/Bean/0005.jpg     Bean   #80FF00   #66B032

    categories: list[str] = database["category"].unique().tolist()
    category_map = {category: i for i, category in enumerate(categories, 1)}

    op.bulk_insert(
        category_table,
        [
            {
                "uid": category_map[category],
                "title": category,
            }
            for category in categories
        ],
    )

    op.bulk_insert(
        image_table,
        [
            {
                "uid": idx + 1,
                "path": row["path"],
                "category_uid": category_map[row["category"]],
                "color_rgb": row["color_RGB"],
                "color_ryb": row["color_RYB"],
            }
            for idx, row in database.iterrows()
        ],
    )

    op.execute(f'ALTER SEQUENCE "CATEGORY_uid_seq" RESTART WITH {len(categories) + 1}')
    op.execute(f'ALTER SEQUENCE "IMAGE_uid_seq" RESTART WITH {database.shape[0] + 1}')


def downgrade() -> None:
    op.execute(f'DELETE FROM "{image_table.name}"')
    op.execute(f'DELETE FROM "{category_table.name}"')
