from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

#PLACE YOUR TABLE SETUP INFORMATION HERE

class Commenter(Base):
    __tablename__ = 'commenter'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    nationality = Column(String)
    gender = Column(String)
    comments = relationship('Comment')

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    lat = Column(Float)
    lon = Column(Float)
    text = Column(String)
    commenter_id = Column(Integer, ForeignKey('commenter.id'))
    commenter = relationship('Commenter', back_populates='comments')

class Vote(Base):
    __tablename__ = 'votes'
    id = Column(Integer, primary_key=True)
    voter_id = Column(Integer, ForeignKey('commenter.id'))
    voter = relationship('Commenter')
    comment_id = Column(Integer, ForeignKey('comment.id'))
    comment = relationship('Comment')
    sentiment = Column(Boolean)

