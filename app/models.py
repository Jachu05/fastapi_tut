from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text

from app.database import Base


class Post(Base):
    __tablename__ = 'Posts'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
