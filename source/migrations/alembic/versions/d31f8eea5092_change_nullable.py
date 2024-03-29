"""change_nullable

Revision ID: d31f8eea5092
Revises: 14ba29293ee5
Create Date: 2020-05-22 22:32:57.599769

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd31f8eea5092'
down_revision = '14ba29293ee5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('leads', 'name',
               existing_type=sa.VARCHAR(length=150),
               nullable=True,
               existing_comment='ФИО или название компании')
    # ### end Alembic commands ###

    op.execute("""
       ALTER TABLE leads ALTER COLUMN incoming_date SET DEFAULT current_date;
    """)

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('leads', 'name',
               existing_type=sa.VARCHAR(length=150),
               nullable=False,
               existing_comment='ФИО или название компании')
    # ### end Alembic commands ###
