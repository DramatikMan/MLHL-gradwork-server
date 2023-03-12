"""Add initial state

Revision ID: c8f2b7fa3eff
Revises:
Create Date: 2023-02-08 16:43:16.994527

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.schema import CreateSequence, DropSequence, Sequence

from gwserver.core.database import Base

# revision identifiers, used by Alembic.
revision = "c8f2b7fa3eff"
down_revision = None
branch_labels = None
depends_on = None


CategorySequence = Sequence("CATEGORY_uid_seq", start=1, metadata=Base.metadata)
ImageSequence = Sequence("IMAGE_uid_seq", start=1, metadata=Base.metadata)


def upgrade() -> None:
    op.execute(CreateSequence(CategorySequence))
    op.execute(CreateSequence(ImageSequence))

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "CATEGORY",
        sa.Column("uid", sa.Integer(), server_default=sa.text("nextval('\"CATEGORY_uid_seq\"')"), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("uid"),
        sa.UniqueConstraint("title"),
    )

    op.create_table(
        "IMAGE",
        sa.Column("uid", sa.Integer(), server_default=sa.text("nextval('\"IMAGE_uid_seq\"')"), nullable=False),
        sa.Column("path", sa.String(), nullable=False),
        sa.Column("category_uid", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["category_uid"], ["CATEGORY.uid"]),
        sa.PrimaryKeyConstraint("uid"),
        sa.UniqueConstraint("path"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("IMAGE")
    op.drop_table("CATEGORY")
    # ### end Alembic commands ###
    op.execute(DropSequence(ImageSequence))
    op.execute(DropSequence(CategorySequence))