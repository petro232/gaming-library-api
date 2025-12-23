from fastapi import FastAPI , HTTPException , status
from sqlalchemy.orm import sessionmaker
from database import open_session
from modules import GameTable
from database import engine , base
from modules import User , Review , UserLibrery
from schemas import LibraryCreate , CreatingUser , ReviewCreating , LibraryUpdate   ,ReviewUpdate
from auth import  hash_password , verfy_password , creat_access_token , secret_key , algo

from jose import jwt , JWTError
 


app=FastAPI()


# endpint that create new user and stores a hashed password instead of plain password ^^
@app.post("/user/")
def creating_user(creating:CreatingUser) :
    
    session=open_session()
    add_user=User(username=creating.username,email=creating.email,password_hash=hash_password(creating.password))
     
    session.add(add_user)
    session.commit()
    session.refresh(add_user)
    session.close()
    return {"user was created" :f"{add_user.username}",
            "user_id":f"{add_user.id}"}

#endpoint tha creates new user and provides the login token  ^^^
@app.post("/login/")
def login(username: str, password:str):

    session=open_session()

    user=session.query(User).filter(User.username==username).first()
    if  not user :
        session.close()
        return {"error" : "invalid username"}
    
    if not verfy_password(password, user.password_hash) :
        session.close()
        return {"error": "invalid   password"}
    
    token=creat_access_token({"user_id":user.id})
    
    session.close()
    return {"access_token":token}

#endpoint that list 20 games  ^^^^^
@app.get("/games/")
def reading_list_games(limit:int=20):
    
    session=open_session()

    reading=session.query(GameTable).limit(limit).all()
    if not reading :
        session.close()
        return HTTPException (status_code=404,detail="reading failed")
    
    result=[]
    for items in reading:
        result.append({"title":items.title,
                       "year":items.year,
                       "genres":items.genres,
                       "rating":items.genres})
    session.close()   
    return result

#getting game full detaill ^^^
@app.get("/games/single/{title}")
def read_one_game(title:str):

    session=open_session()
    reading=session.query(GameTable).filter(GameTable.title==title).first()

    if not reading :
        session.close()
        return HTTPException(status_code=404,detail="error game not found")
    
    return {"title":reading.title,
            "year":reading.year,
            "rating":reading.rating,
            "played":reading.played,
            "playing":reading.playing,
            "backlog":reading.backlog,
            "wishlist":reading.wishlist,
            "likes":reading.likes,
            "released":reading.released,
            "studio":reading.studio,
            "genre":reading.genres,
            "story":reading.story}

#endpoint that search games by title ^^^
@app.get("/search/{title_name}/")
def search_title(title_name:str):

    session=open_session()
    game_search=session.query(GameTable).filter(GameTable.title.ilike(f"%{title_name}%")).all()
    if not game_search :
        session.close()
        return {"game was not found"}
    result=[]
    for game in game_search:

        result.append( {"title":game.title,
            "year":game.year,
            "rating":game.rating,
            "genres":game.genres,
            "story":game.story})
        
    return result


#reading top rated games ^^
@app.get("/games/top_rated/")

def top_rated(limit:int):

    session=open_session()
    reading=session.query(GameTable).order_by(GameTable.rating.desc()).limit(limit).all()
    session.close()
    result=[]
    for x in reading:
        result.append({"title":x.title,
                   "year":x.year,
                   "rating":x.rating,
                   "played":x.played,
                   "playing":x.playing,
                   "wishlist":x.wishlist,
                   "backlog":x.backlog,
                   "released":x.released,
                   "studio":x.studio,
                   "story":x.story})
        
    return result

#endpint that gets most played games
@app.get("/games/most_played/")
def reading_most_played(limit:int):

    session=open_session()
    reading=session.query(GameTable).order_by(GameTable.played.desc()).limit(limit).all()
    if not reading :
        session.close()
        return {"error":"could not access your requist "}
    
    result=[]
    for x in reading:
        result.append({"title":x.title,
                   "year":x.year,
                   "rating":x.rating,
                   "played":x.played,
                   "playing":x.playing,
                   "wishlist":x.wishlist,
                   "backlog":x.backlog,
                   "released":x.released,
                   "studio":x.studio,
                   "story":x.story})
    return result

#enpoint that reads based on genres 
@app.get("/games/genres/")
def reading_genres(limit=int,genre=str):
    
    session=open_session()
    reading=session.query(GameTable).filter(GameTable.genres.contains(genre)).limit(limit).all()
    if not reading:
        session.close()
        return {"error": "could not access your requist"}
    
    result=[]
    for x in reading:
        result.append({"title":x.title,
                   "year":x.year,
                   "rating":x.rating,
                   "played":x.played,
                   "playing":x.playing,
                   "wishlist":x.wishlist,
                   "backlog":x.backlog,
                   "released":x.released,
                   "studio":x.studio,
                   "story":x.story,
                   "genre":x.genres})
    return result
# endpint that adds games to users librery  ^^^
@app.post("/library/")
def add_to_library(token:str  ,data : LibraryCreate) :

    session=open_session()
    try:
        playload=jwt.decode(token,secret_key,algorithms=[algo])
        user_id=playload.get("user_id")
    except JWTError:
        session.close()
        return {"error":"invalid token"}
        
    #checking if the user exsist in db
    check_user=session.query(User).filter(User.id==user_id).first()
    if  not check_user :
        session.close()
        return {"error": "user was not found "}
    #check if the game_title exsist in db 
    check_game=session.query(GameTable).filter(GameTable.title==data.game_title).first()
    if not check_game :
        session.close()
        return {"error":"game was not found"}

    creating=UserLibrery(user_id=user_id,game_title=data.game_title,status=data.status,hours_played=data.hours_played)
    session.add(creating)
    session.commit()
    session.refresh(creating)
    session.close()

    return {"Library was created" : f"user id : {user_id} || game :{data.game_title} || status {data.status} || played for {data.hours_played}"}


#enpoint to get all games in logged in librery  ^^^
@app.get("/library/")
def read_games(token:str):

    sesssion=open_session()
    try:
        payload_token=jwt.decode(token,secret_key,algorithms=[algo])
        user_id=payload_token.get("user_id")
    except JWTError:
        sesssion.close()
        return {"error":"invalid token "}
    read=sesssion.query(UserLibrery).filter(UserLibrery.user_id==user_id).all()

    if not read :
        sesssion.close()
        return {"error":"we could not return your query"}
    result=[]
    for x in read:
        result.append({"title":x.game_title,
                       "status":x.status,
                       "hours_played":x.hours_played})
        
    return result



# updating game status 
@app.patch("/library/{game_title}")
def updating_stutas(game_title:str,data:LibraryUpdate,token:str):

    session=open_session()
    try:
        payload=jwt.decode(token,secret_key,algorithms=[algo])
        user_id=payload.get("user_id")
    except JWTError:
        session.close()
        return {"error":"in token validation"}
    game_entry=session.query(UserLibrery).filter(UserLibrery.user_id==user_id,UserLibrery.game_title==game_title).first()
    if not game_entry:
        session.close()
        return {"error":"method not allowed"}
    
    game_entry.status= data.status
    session.commit()
    return {"status":f"was updated to {game_entry.status}"}
    
     
       




#this endpoint deletes librery row by its game tile   
@app.delete("/library/{game_title}")
def removing(game_title:str ,token:str):

    session=open_session()
    try:
        payload_token=jwt.decode(token,secret_key,algorithms=[algo])
        user_id=payload_token.get("user_id")
    except JWTError:
        session.close()
        return {"error":"invalid token"}
    
    deleting=session.query(UserLibrery).filter(UserLibrery.user_id==user_id,UserLibrery.game_title==game_title).first()
    

    if not deleting:
        session.close()
        return {"error":"the prosses of deleting failed"}
    
    session.delete(deleting)
    session.commit()
     
    session.close()
    return {"delete":"succeded"}
     

# endpoint that allows users to create reviews  ^^^^
@app.post("/review/")
def adding_review(data :ReviewCreating,token:str):

    session=open_session()
    try:
        payload_token=jwt.decode(token,secret_key,algorithms=[algo])
        user_id=payload_token.get("user_id")
    except JWTError:
        session.close()
        return {"error":"token isn't valid  "}

    creating_review=Review(user_id=user_id,game_title=data.game_title,rating=data.rating,Review_text=data.Review_text)
    checking_game=session.query(GameTable).filter(GameTable.title==creating_review.game_title).first()
    if not checking_game :
        session.close()
        return {"error":"game dose not exsist "}
    
    session.add(creating_review)
    session.commit()
    session.refresh(creating_review)
    session.close()
    return {"review was created by:":f"user_id:{creating_review.user_id} text:{creating_review.Review_text}"}


# endpoint that reads game revwies and checks if the review exsist 
@app.get("/reading_rev/{title}")
def reading_rev(title:str):
    session=open_session()
    read=session.query(Review).filter(Review.game_title==title).first()
    if not read :
        return {"game was not reviewed"}

    result={"title":read.game_title,
            "rating":read.rating,
            "Review_text":read.Review_text,
            "created_at":read.created_at}
    
    session.close() 
    return result

@app.patch("/review/{game_title}")
def updating_rev(game_title:str,data:ReviewUpdate,token:str):

    session=open_session()
    try:
        payload_token=jwt.decode(token,secret_key,algorithms=[algo])
        user_id=payload_token.get("user_id")
    except JWTError:
        session.close()
        return {"error":"token validation"}

    rev_entry=session.query(Review).filter(Review.user_id==user_id,Review.game_title==game_title)
    if not rev_entry:
        session.close()
        return {"error":"can't validat"}
    rev_entry.Review_text=data.Review_text
    session.commit()

    return {"review":f"updated to : {rev_entry.Review_text}"}



@app.delete("/review_del/{game_title}")
def delete_rev(game_title:str,token:str):
    
    session=open_session()
    try:

        payload_token=jwt.decode(token,secret_key,algorithms=[algo])
        user_id=payload_token.get("user_id")
    except JWTError:
        session.close()
        return {"error":"token validation"}
    

    delete=session.query(Review).filter(Review.user_id==user_id,Review.game_title==game_title).first()
    if not delete:
        session.close()
        return {"error": "game title can not be found"}
     
    
    session.delete(delete)
    session.commit()

    return{"the game" : " review was deleted "}
    



base.metadata.create_all(bind=engine)








    #   "username": "nasr" ,
    # "email" : "nasr8272@yahoo.com",
    # # "password" : "entering1234!"
    # token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo2LCJleHAiOjE3NjY0MjUzNTR9.
    


#     {

#     "username":"mario_j",
#     "email": "mario_j343@gmail.com",
#     "password":"mario_j432"
# }  "access_token": " eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo3LCJleHAiOjE3NjY0OTY2ODZ9.iZJd2z_ddugqqsuE03FYE7ipnrao-zrYUQUODzppiL