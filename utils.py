import bcrypt
def generateHashpassword(password:str):
    hash_password=bcrypt.hashpw(password=password.encode('utf-8'),salt=bcrypt.gensalt(4))
    return hash_password

def verifyHashpassword(user_password:str,hash_password:str):
    status=bcrypt.checkpw(user_password.encode('utf-8'),hash_password.encode('utf-8'))
    return status