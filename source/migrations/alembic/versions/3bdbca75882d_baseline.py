"""baseline

Revision ID: 3bdbca75882d
Revises: 
Create Date: 2020-05-04 00:03:47.352185

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3bdbca75882d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lead_sources',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=200), nullable=False, comment='Название статуса'),
    sa.Column('description', sa.VARCHAR(length=1000), nullable=True, comment='Краткое описание'),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('modified_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('lead_statuses',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=200), nullable=False, comment='Название статуса'),
    sa.Column('description', sa.VARCHAR(length=1000), nullable=True, comment='Краткое описание'),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('modified_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('leads',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('external_id', sa.BigInteger(), nullable=True, comment='ID пользователя из сервиса авторизации'),
    sa.Column('status_id', sa.BigInteger(), nullable=True, comment='Статус'),
    sa.Column('source_id', sa.BigInteger(), nullable=False, comment='Источник создания'),
    sa.Column('name', sa.VARCHAR(length=150), nullable=False, comment='Имя или ФИО'),
    sa.Column('phone_number', sa.VARCHAR(length=20), nullable=True, comment='Телефон'),
    sa.Column('description', sa.VARCHAR(), nullable=True, comment='Описание заказа'),
    sa.Column('amount', sa.Float(), nullable=True, comment='Сумма сделки'),
    sa.Column('contacts', postgresql.JSONB(astext_type=sa.Text()), nullable=True, comment='Контакты пользователя'),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('modified_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('finish_at', sa.DateTime(timezone=True), nullable=True, comment='Время завершения'),
    sa.ForeignKeyConstraint(['source_id'], ['lead_sources.id'], ),
    sa.ForeignKeyConstraint(['status_id'], ['lead_statuses.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_leads_external_id'), 'leads', ['external_id'], unique=False)
    op.create_index(op.f('ix_leads_name'), 'leads', ['name'], unique=False)
    op.create_index(op.f('ix_leads_phone_number'), 'leads', ['phone_number'], unique=False)
    op.create_index(op.f('ix_leads_status_id'), 'leads', ['status_id'], unique=False)
    op.create_table('comments',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('lead_id', sa.BigInteger(), nullable=True, comment='ID Задачи'),
    sa.Column('external_id', sa.BigInteger(), nullable=True, comment='ID пользователя из сервиса авторизации'),
    sa.Column('comment', sa.VARCHAR(), nullable=True, comment='Комментарий'),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('modified_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('comments_lead_created_at_idx', 'comments', ['lead_id', sa.text('created_at DESC')], unique=False)
    op.create_index(op.f('ix_comments_lead_id'), 'comments', ['lead_id'], unique=False)
    # ### end Alembic commands ###
    fill_static_data()

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_comments_lead_id'), table_name='comments')
    op.drop_index('comments_lead_created_at_idx', table_name='comments')
    op.drop_table('comments')
    op.drop_index(op.f('ix_leads_status_id'), table_name='leads')
    op.drop_index(op.f('ix_leads_phone_number'), table_name='leads')
    op.drop_index(op.f('ix_leads_name'), table_name='leads')
    op.drop_index(op.f('ix_leads_external_id'), table_name='leads')
    op.drop_table('leads')
    op.drop_table('lead_statuses')
    op.drop_table('lead_sources')
    # ### end Alembic commands ###


def fill_static_data():
    from source.models.lead import LeadStatus, LeadSource
    lead_status = LeadStatus.t
    lead_source = LeadSource.t

    op.bulk_insert(lead_status,
                   [
                       {
                           'name': 'not_phoned',
                           'description': 'Не удалось дозвониться'
                           },
                       {
                           'name': 'wait_for_pay',
                           'description': 'Ожидание оплаты'
                           },
                       {
                           'name': 'change_time',
                           'description': 'Перенести'
                           },
                       {
                           'name': 'denial',
                           'description': 'Отказ'
                           },
                       ]
                   )

    op.bulk_insert(lead_source,
                   [
                       {
                           'name': 'manual',
                           'description': 'Вручную'
                           },
                       {
                           'name': 'xlsx',
                           'description': 'Данные внесены через xlsx'
                           },
                       {
                           'name': 'outer',
                           'description': 'По внешней ссылке'
                           },
                       {
                           'name': 'form',
                           'description': 'Клиент заполнил форму'
                           },
                       ]
                   )
