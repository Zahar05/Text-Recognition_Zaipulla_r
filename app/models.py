from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime


class GeneralBase(DeclarativeBase):
    id = Column(Integer, primary_key=True)


class Document(GeneralBase):
    __tablename__ = 'documents'

    pasth = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    doc_text = relationship(
        'Document_text',
        backref='Document',
        uselist=False,
        cascade="all, delete-orphan"
    )


class Document_text(GeneralBase):
    __tablename__ = 'documents_text'

    id_doc = Column(Integer, ForeignKey('documents.id'), unique=True)
    text = Column(String, nullable=False)
