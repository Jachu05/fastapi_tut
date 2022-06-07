"""add user table

Revision ID: 98a31cca4c32
Revises: 1df5625eb3be
Create Date: 2022-06-08 00:53:17.460101

"""
from alembic import op
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, text

# revision identifiers, used by Alembic.
revision = '98a31cca4c32'
down_revision = '1df5625eb3be'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        Column('id', Integer, primary_key=True, autoincrement=True, nullable=False),
        Column('email', String, nullable=False, unique=True),
        Column('password', String, nullable=False),
        Column('created_at', TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')),
    )


def downgrade() -> None:
    op.drop_table('users')
