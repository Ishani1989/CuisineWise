from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
    
    
class Cuisine(Base):
    __tablename__ = 'cuisine'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.id,
       } 
       
class Dish(Base):
    __tablename__ = 'dish'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    description = Column(String(300), nullable=False)
    picurl = Column(String(300), nullable=False)
    recipe = Column(String(2000), nullable=False) 
    cuisine_id = Column(Integer,ForeignKey('cuisine.id'))
    cuisine = relationship(Cuisine)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    created_on = Column(String(50), nullable=False)
    modified_on = Column(String(50), nullable=False)
    
    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id'           : self.id,
           'name'         : self.name,
           'description'  : self.description,
           'picurl'       : self.picurl,
           'recipe'       : self.recipe,
           'cuisine_id'   : self.cuisine_id,
           'user_id'      : self.user_id,
           'created_on'   : self.created_on,
           'modified_on'  : self.modified_on,
       }

engine = create_engine('sqlite:///new-cuisinewise.db')
 

Base.metadata.create_all(engine)