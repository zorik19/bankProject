from sqlalchemy import BigInteger, Boolean, Column, DateTime, Float, ForeignKey, func, VARCHAR

from fwork.common.db.postgres.conn_async import db


# TODO: rm __table_args__ = {'extend_existing': True} why meta called twice?

class Lead(db.Model):
    __tablename__ = 'leads'

    id = Column(BigInteger, primary_key=True)
    external_id = Column(BigInteger, nullable=True, index=True, comment='ID пользователя из сервиса авторизации')
    status_id = Column(BigInteger, ForeignKey('lead_statuses.id'), nullable=True, index=True, comment='Статус')
    source_id = Column(BigInteger, ForeignKey('lead_sources.id'), nullable=False, comment='Источник создания')
    name = Column(VARCHAR(150), index=True, nullable=False, comment='Имя или ФИО')
    phone_number = Column(VARCHAR(length=20), index=True, comment='Телефон')
    email = Column(VARCHAR(length=200), index=True, comment='email')
    in_progress = Column(Boolean, server_default="0", index=True, nullable=False,
                         comment="Флаг забаненного пользователя")
    feedback_type = Column(VARCHAR(length=100), comment='email')  # TODO: enum or ForeignKey in future
    description = Column(VARCHAR(), nullable=True, comment='Описание заказа')
    amount = Column(Float, nullable=True, comment='Сумма сделки')
    created_at = Column(DateTime(timezone=True), server_default=func.current_timestamp())
    modified_at = Column(DateTime(timezone=True), onupdate=func.current_timestamp())
    finish_at = Column(DateTime(timezone=True), nullable=True, comment='Время завершения')

    __table_args__ = {'extend_existing': True}

    def __repr__(self):
        return f'<Lead(' \
               f'id={self.id}, ' \
               f'external_id={self.external_id}, ' \
               f'status_id={self.status_id}, ' \
               f'source_id={self.source_id}, ' \
               f'name={self.name}, ' \
               f'phone_number={self.phone_number}, ' \
               f'email={self.email}, ' \
               f'in_progress={self.in_progress}, ' \
               f'feedback_type={self.feedback_type}, ' \
               f'description={self.description}, ' \
               f'amount={self.amount}, ' \
               f'created_at={self.created_at}, ' \
               f'modified_at={self.modified_at}, ' \
               f'finish_at={self.finish_at} ' \
               f')>'


class LeadStatus(db.Model):
    __tablename__ = 'lead_statuses'

    id = Column(BigInteger, primary_key=True)
    name = Column(VARCHAR(length=200), nullable=False, comment='Название статуса')
    description = Column(VARCHAR(length=1000), nullable=True, comment='Краткое описание')
    created_at = Column(DateTime(timezone=True), server_default=func.current_timestamp())
    modified_at = Column(DateTime(timezone=True), onupdate=func.current_timestamp())

    __table_args__ = {'extend_existing': True}

    def __repr__(self):
        return f'<LeadStatus(' \
               f'id={self.id}, ' \
               f'name={self.name}, ' \
               f'description={self.description}, ' \
               f'created_at={self.created_at}, ' \
               f'modified_at={self.modified_at}' \
               f')>'


class LeadSource(db.Model):
    __tablename__ = 'lead_sources'

    id = Column(BigInteger, primary_key=True)
    name = Column(VARCHAR(length=200), nullable=False, comment='Название статуса')
    description = Column(VARCHAR(length=1000), nullable=True, comment='Краткое описание')
    created_at = Column(DateTime(timezone=True), server_default=func.current_timestamp())
    modified_at = Column(DateTime(timezone=True), onupdate=func.current_timestamp())

    __table_args__ = {'extend_existing': True}


def __repr__(self):
    return f'<LeadSource(' \
           f'id={self.id}, ' \
           f'name={self.name}, ' \
           f'description={self.description}, ' \
           f'created_at={self.created_at}, ' \
           f'modified_at={self.modified_at}' \
           f')>'


class LeadHistory:
    """
    comment and corresponding status on lead
    """
    ...
