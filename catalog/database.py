import sys
import os
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine


# to create database
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False)
    picture = Column(String(200))


class SeriesName(Base):
    __tablename__ = 'seriesname'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="seriesname")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'name': self.name,
            'id': self.id
        }


class SerType(Base):
    __tablename__ = 'sertype'
    name = Column(String(200), nullable=False)
    id = Column(Integer, primary_key=True)
    color = Column(String(150))
    ram = Column(String(150))
    memory = Column(Integer)
    frontcamera = Column(String(50))
    rearcamera = Column(String(50))
    price = Column(Integer)
    screen = Column(Integer)
    slink = Column(String(300))
    date = Column(DateTime, nullable=False)
    sernameid = Column(Integer, ForeignKey('seriesname.id'))
    sername = relationship(
        SeriesName, backref=backref('sertype', cascade='all, delete'))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="sertype")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'name': self.name,
            'color': self.color,
            'ram': self.ram,
            'memory': self.memory,
            'frontcamera': self.frontcamera,
            'rearcamera': self.rearcamera,
            'price': self.price,
            'screen': self.screen,
            'slink': self.slink,
            'date': self.date,
            'id': self. id
        }

engin = create_engine('sqlite:///samsung.db')
Base.metadata.create_all(engin)
