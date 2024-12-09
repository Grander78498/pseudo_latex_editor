"""create formula and expression table

Revision ID: cc102e8f3f75
Revises: 
Create Date: 2024-12-09 18:21:56.865549

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc102e8f3f75'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    formula_table = op.create_table(
        'formula',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), index=True),
        sa.Column('formula', sa.String(), index=True)
    )
    expr_table = op.create_table(
        'expression',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('expr', sa.String())
    )
    expressions = [
        "\\frac{}{}",
        "{}^{}",
        "\\sqrt{}"
    ]
    op.bulk_insert(expr_table, 
                   [{"expr": expr} for expr in expressions])


def downgrade() -> None:
    op.drop_table('expression')
    op.drop_table('formula')
