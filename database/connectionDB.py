import mysql.connector as SQLC

def DatabaseConnection():
    try:
        db_config=SQLC.connect(
            host="localhost",
            user="root",
            password="Tejaa@0987",
            database="subscription_hub"
        )
        print("Database connected successfully")
        return db_config
    except Exception as e:
        print("Database connection failed:", e)