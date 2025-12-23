from auth import creat_access_token , secret_key , algo
from jose import jwt


token=creat_access_token({"user_id":5})
decode=jwt.decode(token,secret_key,algorithms=algo)
print(decode)
 