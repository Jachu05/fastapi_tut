"""add create_time to post table

Revision ID: 1df5625eb3be
Revises: 95b008eae8c9
Create Date: 2022-06-08 00:44:49.567465

"""
from alembic import op

# revision identifiers, used by Alembic.
from sqlalchemy import Column, TIMESTAMP, text

revision = '1df5625eb3be'
down_revision = '95b008eae8c9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'posts',
        Column('created_at', TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')),
    )


def downgrade() -> None:
    op.drop_column('posts', 'created_at')
