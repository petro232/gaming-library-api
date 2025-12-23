from pydantic import BaseModel



class CreatingUser(BaseModel):
    username: str
    email : str 
    password : str





class LibraryCreate(BaseModel):
     
    game_title : str
    status : str
    hours_played : int


class ReviewCreating(BaseModel):

    game_title : str
    rating : float 
    Review_text : str
 
class LibraryUpdate(BaseModel):
    status: str


class ReviewUpdate(BaseModel):
    Review_text : str