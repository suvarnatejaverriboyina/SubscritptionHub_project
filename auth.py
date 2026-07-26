from models import Customer
from file_manager import save_user,load_users,generate_customer_id


def register():
    name = input("Enter Name: ")
    email = input("Enter Email: ")
    password = input("Enter Password: ")
    customer_id=generate_customer_id()

    customer = Customer(customer_id,name, email, password)
    save_user(customer)
    print("Customer successfully Registered")
    print(f"Your Customer ID is: {customer_id}")


def login():
    email=input("Enter Email:")
    password=input("Enter Password:")
    customer_id=input("Enter CustomerID:")
    users=load_users()
    for user in users:
        if user["customer_id"]==customer_id and user["email"]==email and user["password"]==password:
            print("Login Successful.")
            return user
    print("Invalid Email or Password.")
    return None
def admin_login():
    email = input("Enter Admin Email: ")
    password = input("Enter Admin Password: ")
    # Compare with admin credentials
    if email == "admin@subscriptionhub.com" and password == "admin123":
        print("Admin Login Successful.")
        return True

    print("Invalid Admin Email or Password.")
    return False

def logout():
    print("Successfully Logged out")
    

    

    