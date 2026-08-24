
from auth import register,login,admin_login,logout
from admin import manage_plans,manage_customers,manage_subscriptions,manage_notifications,create_expiry_reminders
from customer import purchase_subscription,view_my_subscription,renew_subscription,cancel_subscription,view_available_plans


def welcome():
    print("-"*50)
    print("            WELCOME")
    print("       Subscription Management System")
    print("-"*50)
def main_menu():
    print(("="*10)+"MAIN MENU"+("="*10))
    print("1. Admin Login")
    print("2. Customer Login")
    print("3. Customer Registration")
    print("4. Exit")
    try:
        choice=int(input("Enter your choice:"))
    except ValueError:
        print("Please Enter a Valid Number.")
        return 0
    return choice
def admin_menu():
    print(("="*10)+"ADMIN MENU"+("="*10))
    print("1. Manage Subscription Plans")
    print("2. Manage Customers")
    print("3. Manage Subscriptions")
    print("4. Notifications and Remainders")
    print("5. Logout")
    try:
        choice=int(input("Enter your choice:"))
    except ValueError:
        print("Please Enter a Valid Number.")
        return 0
    return choice
def customer_menu():
    print(("="*10)+"CUSTOMER MENU"+("-"*10))
    print("1. View Available Plans")
    print("2. Purchase Subscription")
    print("3. View My Subscription")
    print("4. Renew Subscription")
    print("5. Cancel Subscription")
    print("6. Logout")
    try:
        choice=int(input("Enter your choice:"))
    except ValueError:
        print("Please Enter a Valid Number.")
        return 0
    return choice
while True:
    welcome()
    choice = main_menu()
    if choice == 1:
        success=admin_login()
        if success:
            create_expiry_reminders()
            while True:
                admin_choice=admin_menu()
                if admin_choice==1:
                    manage_plans()
                elif admin_choice==2:
                    manage_customers()
                elif admin_choice==3:
                    manage_subscriptions()
                elif admin_choice==4:
                    manage_notifications()

                elif admin_choice==5:
                    logout()
                    break
    elif choice == 2:
        current_user = login()
        if current_user:
            while True:
                customer_choice = customer_menu()
                if customer_choice == 1:
                    view_available_plans()

                elif customer_choice == 2:
                    purchase_subscription(current_user)

                elif customer_choice == 3:
                    view_my_subscription(current_user)

                elif customer_choice == 4:
                    renew_subscription(current_user)

                elif customer_choice == 5:
                    cancel_subscription(current_user)


                elif customer_choice == 6:
                    logout()
                    break
    elif choice == 3:
        register()

    elif choice==4:
        print("---------Thank you for using Subscription Hub---------")
        break
    else:
        print("Invalid Choice")
    


                            
