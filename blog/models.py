from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship
import uuid

class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    creator = relationship('User',back_populates='blogs')

class Node(Base):
    __tablename__ = 'nodes'

    id = Column(Integer,primary_key=True,index=True)
    uid = Column(String, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    pwm = Column(String)
    volt = Column(String)
    ampe = Column(String)
    health = Column(String)
    log = Column(String)
    

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True,index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    blogs = relationship('Blog', back_populates='creator')