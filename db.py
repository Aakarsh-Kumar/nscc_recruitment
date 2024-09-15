from datetime import datetime
from user import User
from pymongo import MongoClient
import bcrypt

client = MongoClient("mongodb+srv://main:test@cluster0.yzd5f.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

_db = client.get_database("credentials")
collection = _db.get_collection("credentials") 

#---generate hash---------
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()

#-----check hash-----------------
def check_password(password: str, hashed_password: str) -> bool:
    hashed_password_bytes = hashed_password.encode()
    return bcrypt.checkpw(password.encode(), hashed_password_bytes)

def save_user(email,name,password):
    collection.insert_one({'email':email,'name':name,'password':hash_password(password)})

def get_user(email,password):
    user_data = collection.find_one({'email':email})
    try:
        if check_password(password,user_data['password']):
            return User(user_data['email'],user_data['name']) if user_data else None
        else:
            return None
    except:
        return None

