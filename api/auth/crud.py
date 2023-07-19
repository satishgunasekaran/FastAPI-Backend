from api.utils.dbUtil import database
from api.auth import schema

def get_user(email: str):
    query = "SELECT * FROM py_users WHERE status = '1' AND email = :email"
    return database.fetch_one(query, values={"email": email})

def create_user(user: schema.UserCreate):
    query = "INSERT INTO py_users VALUES (nextval('user_id_seq'), :email, :password, :fullname,now() at time zone 'utc', '1')"
    
    return database.execute(query, values={"email": user.email, "password": user.password, "fullname": user.fullname})
    
def create_reset_code(email: str, reset_code: str):
    query = """INSERT INTO py_codes VALUES (nextval('code_id_seq'), 
             :email, :reset_code, '1', now() at time zone 'UTC'
              )"""
    
    return database.execute(query, values={'email': email, 'reset_code':reset_code})
    