import hashlib
from jose import jwt
from datetime import datetime , timedelta , timezone


secret_key="123_secret-token"
algo="HS256"
expire_minutes= 30


def hash_password(password:str):
    hashed_password=hashlib.sha256(password.encode("utf-8")).hexdigest()
    return hashed_password


def verfy_password(plain_password:str,hashed_password:str):
    hashing_plain_pass=hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
    if hashing_plain_pass == hashed_password:
        return True
    else :
       return False

def creat_access_token(user_id: dict):
    to_encode=user_id.copy()
    expire_time=datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)

    to_encode.update({"exp":expire_time})
    encoded_jwt=jwt.encode(to_encode,secret_key,algorithm=algo)
    return encoded_jwt








# ss=hash_password("ain123")
# print("the first password :", ss)

# res=verfy_password("ain123",ss)
# print("the result is ",res)






















# import hashlib
# from jose import jwt
# from datetime import datetime, timedelta, timezone

# SECRET_KEY = "your-secret-key-here"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# def hash_password(password: str):
#      return hashlib.sha256(password.encode()).hexdigest()

# def verify_password(plain_password: str, hashed_password: str):
#      return hash_password(plain_password) == hashed_password

# def create_access_token(data: dict):
     
#     to_encode = data.copy()
#     expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt