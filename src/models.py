from .database import Base
from sqlalchemy import(
    Column,
    ForeignKey, 
    Integer, 
    String, 
    Boolean, 
    Text
)
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key = True)
    title = Column(String, nullable = False)
    content = Column(Text, nullable = False)
    published = Column(Boolean, server_default="TRUE")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,server_default=text('NOW()'))
    author_id = Column(Integer, ForeignKey("users.id" , ondelete="CASCADE"), nullable=False)

    author = relationship("User")
    with_like = relationship("Like")

    @property
    def total_like(self):
        return len(self.with_like) 
           
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,server_default=text('NOW()'))


class Like(Base):
    __tablename__ = "likes"
    user_id = Column(Integer, ForeignKey("users.id" , ondelete="CASCADE") , primary_key = True)
    post_id = Column(Integer, ForeignKey("posts.id" , ondelete="CASCADE") , primary_key = True)