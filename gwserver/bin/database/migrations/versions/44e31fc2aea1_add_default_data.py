"""Add default data

Revision ID: 44e31fc2aea1
Revises: c8f2b7fa3eff
Create Date: 2023-02-14 20:33:30.579450

"""
import pandas as pd
from alembic import op
from sqlalchemy import Integer, String
from sqlalchemy.sql import column, table

from gwserver.core.s3 import s3

# revision identifiers, used by Alembic.
revision = "44e31fc2aea1"
down_revision = "c8f2b7fa3eff"
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
)


def upgrade() -> None:
    initial = s3.reader("database.csv")
    database = pd.read_csv(initial)

    #                       path category
    # 0  data/test/Bean/0001.jpg     Bean
    # 1  data/test/Bean/0002.jpg     Bean
    # 2  data/test/Bean/0003.jpg     Bean
    # 3  data/test/Bean/0004.jpg     Bean
    # 4  data/test/Bean/0005.jpg     Bean

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
            }
            for idx, row in database.iterrows()
        ],
    )

    op.execute(f'ALTER SEQUENCE "CATEGORY_uid_seq" RESTART WITH {len(categories)}')
    op.execute(f'ALTER SEQUENCE "IMAGE_uid_seq" RESTART WITH {database.shape[0]}')


def downgrade() -> None:
    op.execute(f'DELETE FROM "{image_table.name}"')
    op.execute(f'DELETE FROM "{category_table.name}"')
