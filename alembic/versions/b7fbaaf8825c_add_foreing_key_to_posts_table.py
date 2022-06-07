"""add foreing key to posts table

Revision ID: b7fbaaf8825c
Revises: 98a31cca4c32
Create Date: 2022-06-08 01:05:58.194621

"""
from alembic import op

# revision identifiers, used by Alembic.
from sqlalchemy import Column, Integer, ForeignKey

revision = 'b7fbaaf8825c'
down_revision = '98a31cca4c32'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', Column('owner_id', Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False))


def downgrade() -> None:
    op.drop_constraint('posts_owner_id_fkey', table_name='posts')
    op.drop_column('posts', 'owner_idx')
