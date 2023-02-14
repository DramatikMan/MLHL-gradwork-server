"""Add default data

Revision ID: 44e31fc2aea1
Revises: c8f2b7fa3eff
Create Date: 2023-02-14 20:33:30.579450

"""
import pandas as pd

from gwserver.core.s3 import s3

# revision identifiers, used by Alembic.
revision = "44e31fc2aea1"
down_revision = "c8f2b7fa3eff"
branch_labels = None
depends_on = None


def upgrade() -> None:
    initial = s3.reader("database.csv")
    database = pd.read_csv(initial)


def downgrade() -> None:
    pass
