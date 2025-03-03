"""empty message

Revision ID: 61d124654655
Revises: 0763d677d453
Create Date: 2025-03-03 17:53:26.707605

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '61d124654655'
down_revision = '0763d677d453'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Agrega la columna `name` como nullable
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('name', sa.String(length=120), nullable=True))

    # 2. Actualiza las filas existentes para que tengan un valor en la columna `name`
    op.execute("UPDATE \"user\" SET name = 'default_name' WHERE name IS NULL")

    # 3. Cambia la columna `name` a NOT NULL
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('name', nullable=False)


def downgrade():
    # Elimina la columna `name`
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('name')
