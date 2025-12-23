from sqlalchemy import Column, String, Integer, Float, Text , DateTime ,ForeignKey
from database import base
from datetime import datetime  , timezone


class GameTable(base):
    __tablename__= "game"

    title= Column(String,primary_key=True)
    year = Column(String)
    rating = Column(Float)
    played = Column(Integer)
    playing = Column(Integer)
    backlog = Column(Integer)
    wishlist = Column(Integer)
    likes = Column(Integer)
    released = Column(String)
    url = Column(String)
    post_image = Column(String)
    studio = Column(String)
    genres = Column(String)
    story = Column(Text)



class User(base):
    __tablename__= "user_table"

    id = Column(Integer,primary_key=True,autoincrement=True)
    username= Column(String,unique=True)
    email= Column(String,unique=True)
    password_hash= Column(String)
    created_at = Column(DateTime,default=lambda : datetime.now(timezone.utc))


class Review (base):
    __tablename__= "review"

    id= Column(Integer,primary_key=True,autoincrement=True)
    user_id= Column(Integer,ForeignKey("user_table.id"))
    game_title= Column(String,ForeignKey("game.title"))
    rating= Column (Float)
    Review_text = Column (Text)
    created_at = Column (DateTime,default=lambda:datetime.now(timezone.utc))



class UserLibrery(base):

    __tablename__= "librery"

    id=Column(Integer,primary_key=True,autoincrement=True)
    user_id= Column (Integer,ForeignKey("user_table.id"))
    game_title= Column (String,ForeignKey("game.title"))
    status = Column(String)
    hours_played = Column (Integer)
    added_at = Column(DateTime,default=lambda:datetime.now(timezone.utc))



class Genre (base):
    __tablename__="genre"

    id = Column(Integer,primary_key=True,autoincrement=True)
    name= Column(String,unique=True)


class Platform (base):

    __tablename__= "platform"

    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column (String,unique=True)



class GameGenre(base):

    __tablename__= "game_genre"

    game_title=Column(String,ForeignKey("game.title"),primary_key=True)
    genre_id= Column(Integer,ForeignKey("genre.id"),primary_key=True)