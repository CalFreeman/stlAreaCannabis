"""create main tables
Revision ID: 29179440750b
Revises:
Create Date: 2020-05-05 10:41:35.468471
"""
from typing import Tuple
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = "29179440750b"
down_revision = None
branch_labels = None
depends_on = None
def create_updated_at_trigger() -> None:
    op.execute(
        """
        CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS
        $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        """
    )

def timestamps(indexed: bool = False) -> Tuple[sa.Column, sa.Column]:
    return (
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed,
        ),
    )

def create_companies_table() -> None:
    op.create_table(
        "companies",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Text, nullable=False, index=True),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_companies_modtime
            BEFORE UPDATE
            ON companies
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )

def create_dispensaries_table() -> None:
    op.create_table(
        "dispensaries",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("company_id", sa.Integer, sa.ForeignKey("companies.id")),        
        sa.Column("flower_url", sa.Text, unique=False, nullable=True, index=True),
        sa.Column("pre_rolls_url", sa.Text, unique=False, nullable=True, index=True),
        sa.Column("vaporizers_url", sa.Text, unique=False, nullable=True, index=True),
        sa.Column("concentrates_url", sa.Text, unique=False, nullable=True, index=True),
        sa.Column("edibles_url", sa.Text, unique=False, nullable=True, index=True),
        sa.Column("tinctures_url", sa.Text, unique=False, nullable=True, index=True),
		sa.Column("topicals_url", sa.Text, unique=False, nullable=True, index=True),
        sa.Column("cbd_url", sa.Text, unique=False, nullable=True, index=True),
        sa.Column("address", sa.Text, unique=True, nullable=True, index=True),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_dispensaries_modtime
            BEFORE UPDATE
            ON dispensaries
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )

def create_raw_json_table() -> None:
    op.create_table(
        "raw_json",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("json_doc", sa.JSON(), nullable=True),
        *timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_raw_json_modtime
            BEFORE UPDATE
            ON raw_json
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )

def upgrade() -> None:
    create_updated_at_trigger()
    create_companies_table()
    create_dispensaries_table()
    create_raw_json_table()
def downgrade() -> None: 
    op.drop_table("dispensaries")
    op.drop_table("companies")
    op.drop_table("raw_json")
    op.execute("DROP FUNCTION update_updated_at_column")
