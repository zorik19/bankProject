from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, func, Index, VARCHAR

from fwork.common.db.postgres.conn_async import db


class Comment(db.Model):
    __tablename__ = 'comments'

    id = Column(BigInteger, primary_key=True)
    lead_id = Column(BigInteger, ForeignKey('leads.id'), index=True, comment='ID Задачи')
    external_id = Column(BigInteger, nullable=True, comment='ID пользователя из сервиса авторизации')
    comment = Column(VARCHAR(), comment='Комментарий')
    created_at = Column(DateTime(timezone=True), server_default=func.current_timestamp())
    modified_at = Column(DateTime(timezone=True), onupdate=func.current_timestamp())

    def __repr__(self):
        return f'<Comment(' \
               f'id={self.id}, ' \
               f'lead_id={self.lead_id}, ' \
               f'comment={self.comment}, ' \
               f'created_at={self.created_at},' \
               f'modified_at={self.modified_at},' \
               f')>'


Index('comments_lead_created_at_idx', Comment.lead_id, Comment.created_at.desc())
