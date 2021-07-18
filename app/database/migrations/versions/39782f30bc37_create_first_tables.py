"""create_first_tables

Revision ID: 39782f30bc37
Revises:
Create Date: 2021-06-15 21:18:50.571188

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy.schema import ForeignKey


# revision identifiers, used by Alembic
revision = '39782f30bc37'
down_revision = None
branch_labels = None
depends_on = None


def create_account_table():
    op.create_table(
        "account",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("password", sa.Text, nullable=False),
        sa.Column("is_active", sa.Boolean, default=True, nullable=False),
        sa.Column("created_at",
                  sa.DateTime(timezone=True),
                  nullable=False,
                  server_default=func.now()),
        sa.Column("updated_at",
                  sa.DateTime(timezone=True),
                  nullable=False,
                  server_default=func.now(),
                  onupdate=func.now()),
    )


def create_collection_destination_table():
    op.create_table(
        "collection_destination",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("domain", sa.Text, nullable=False),
        sa.Column("contents_attr_name", sa.Text, nullable=False),
        sa.Column("title_attr_name", sa.Text, nullable=False),
        sa.Column("published_date_attr_name", sa.Text, nullable=False),
        sa.Column("is_getting_domain", sa.Boolean, nullable=False),
        sa.Column("domain_attr_name", sa.Text, nullable=False),
        sa.Column("content_url_attr_name", sa.Text, nullable=False),
        sa.Column("account_id",
                  sa.Integer,
                  ForeignKey("account.id",
                             name="fk_collection_destination_account_id")),
        sa.Column("created_at",
                  sa.DateTime(timezone=True),
                  nullable=False,
                  server_default=func.now()),
        sa.Column("updated_at",
                  sa.DateTime(timezone=True),
                  nullable=False,
                  server_default=func.now(),
                  onupdate=func.now()),
    )


def create_content_table():
    op.create_table(
        "content",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("title", sa.Text, nullable=False),
        sa.Column("content_url", sa.Text, nullable=False),
        sa.Column("published_at", sa.DateTime, nullable=False),
        sa.Column("domain", sa.Text, nullable=False),
        sa.Column("is_read_later", sa.Boolean, nullable=False),
        sa.Column("collection_destination_id",
                  sa.Integer,
                  ForeignKey("collection_destination.id",
                             name="fk_content_collection_destination_id")),
        sa.Column("account_id",
                  sa.Integer,
                  ForeignKey("account.id",
                             name="fk_content_account_id")),
        sa.Column("created_at",
                  sa.DateTime(timezone=True),
                  nullable=False,
                  server_default=func.now()),
        sa.Column("updated_at",
                  sa.DateTime(timezone=True),
                  nullable=False,
                  server_default=func.now(),
                  onupdate=func.now()),
    )


def upgrade():
    create_account_table()
    create_collection_destination_table()
    create_content_table()


def downgrade():
    pass
