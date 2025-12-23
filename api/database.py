from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker
import os

base_dir=os.path.dirname(os.path.dirname(__file__))
db_path=os.path.join(base_dir,"backloged","spiders","backlooged.db")
engine=create_engine(f"sqlite:///{db_path}")

base =declarative_base() # what is this 

open_session=sessionmaker(bind=engine) # and what is this 


 
