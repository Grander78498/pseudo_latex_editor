"""Add name column to expression table

Revision ID: 2d536e502eea
Revises: cc102e8f3f75
Create Date: 2024-12-10 20:08:14.976540

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d536e502eea'
down_revision: Union[str, None] = 'cc102e8f3f75'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('expression',
                  sa.Column('name', sa.String(), nullable=True))
    expr_table = sa.Table(
        'expression',
        sa.MetaData(),
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('expr', sa.String()),
        sa.Column('name', sa.String(), nullable=True)
    )
    connection = op.get_bind()
    names = ['Дробь', 'Степень', 'Квадратный корень']
    expressions = connection.execute(sa.select(
        expr_table.c.id,
        expr_table.c.expr
    )).fetchall()
    assert len(names) == len(expressions)

    for i, (id_, _) in enumerate(expressions):
        connection.execute(expr_table.update().where(expr_table.c.id == id_).values(
            name=names[i]
        ))



def downgrade() -> None:
    op.drop_column('expression', 'name')
