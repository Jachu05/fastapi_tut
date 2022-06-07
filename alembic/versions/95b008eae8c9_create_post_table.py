"""create post table

Revision ID: 95b008eae8c9
Revises: 
Create Date: 2022-06-08 00:23:28.701351

"""
from alembic import op

# revision identifiers, used by Alembic.
from sqlalchemy import Column, Integer, String, Boolean

revision = '95b008eae8c9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'posts',
        Column('id', Integer, primary_key=True, autoincrement=True, nullable=False),
        Column('title', String, nullable=False),
        Column('content', String, nullable=False),
        Column('published', Boolean, server_default='TRUE', nullable=False)
    )


def downgrade() -> None:
    op.drop_table('posts')
