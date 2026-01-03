"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    """
    Apply the migration (upgrade database schema).
    
    This function contains the changes to apply to the database.
    """
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    """
    Revert the migration (downgrade database schema).
    
    This function contains the changes to undo the migration.
    Always write downgrade functions so you can rollback if needed!
    """
    ${downgrades if downgrades else "pass"}
