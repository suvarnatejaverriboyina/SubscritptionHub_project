from file_manager import (
    generate_plan_id,load_plans,load_users,delete_user,load_subscriptions,
    update_subscriptions,generate_notification_id,
    save_notification,
    load_notifications)
from models import SubscriptionPlan

from datetime import date,timedelta


#Add a Plan
def add_plan():
    plan_id=generate_plan_id()
    plan_name=input("Enter Plan Name:")
    try:
        price=float(input("Enter Plan Price: "))
        duration = int(input("Enter Duration in Days: "))
    except ValueError:
        print("Please enter a valid numeric value.")
        return
    with open("data/plans.txt","a") as file:
        file.write(
            f"{plan_id}|"
            f"{plan_name}|"
            f"{price}|"
            f"{duration}\n"
        )
    print("\nPlan Added Successfully!")
    print(f"Plan ID: {plan_id}")






#View Plans
def view_plans():
    plans = load_plans()

    if not plans:
        print("\nNo subscription plans available.")
        return

    print("\n" + "-" * 40)
    print("       ALL SUBSCRIPTION PLANS")
    print("-" * 40)

    for plan in plans:
        plan_object = SubscriptionPlan(
            plan["plan_id"],
            plan["plan_name"],
            plan["price"],
            plan["duration"]
        )
        plan_object.display_plan()
        print("-" * 40)



#Update plan
def update_plan():
    plans = load_plans()

    if not plans:
        print("\nNo plans available to update.")
        return

    plan_id = input("Enter Plan ID to update: ")

    found = False

    for plan in plans:
        if plan["plan_id"] == plan_id:
            found = True

            print("\nCurrent Plan Details:")
            print(f"Name: {plan['plan_name']}")
            print(f"Price: {plan['price']}")
            print(f"Duration: {plan['duration']} days")

            new_name = input("Enter New Plan Name: ")

            try:
                new_price = float(input("Enter New Price: "))
                new_duration = int(input("Enter New Duration in Days: "))
            except ValueError:
                print("Please enter valid numeric values.")
                return

            plan["plan_name"] = new_name
            plan["price"] = new_price
            plan["duration"] = new_duration

            break

    if not found:
        print("Plan not found.")
        return
    with open("data/plans.txt", "w") as file:
        for plan in plans:
            file.write(
                f"{plan['plan_id']}|"
                f"{plan['plan_name']}|"
                f"{plan['price']}|"
                f"{plan['duration']}\n"
            )

    print("Plan updated successfully.")



#Delete plan

def delete_plan():
    plans = load_plans()

    if not plans:
        print("\nNo plans available to delete.")
        return

    plan_id = input("Enter Plan ID to delete: ")

    new_plans = []
    found = False

    for plan in plans:
        if plan["plan_id"] == plan_id:
            found = True
        else:
            new_plans.append(plan)

    if not found:
        print("Plan not found.")
        return

    with open("data/plans.txt", "w") as file:
        for plan in new_plans:
            file.write(
                f"{plan['plan_id']}|"
                f"{plan['plan_name']}|"
                f"{plan['price']}|"
                f"{plan['duration']}\n"
            )

    print("Plan deleted successfully.")


def manage_plans():
    while True:
        print("\n" + "-" * 30)
        print("   MANAGE SUBSCRIPTION PLANS")
        print("=" * 30)

        print("1. Add Plan")
        print("2. View All Plans")
        print("3. Update Plan")
        print("4. Delete Plan")
        print("5. Back")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Please Enter a Valid Number.")
            continue

        if choice == 1:
            add_plan()

        elif choice == 2:
            view_plans()

        elif choice == 3:
            update_plan()

        elif choice == 4:
            delete_plan()

        elif choice == 5:
            break

        else:
            print("Invalid Choice.")



#View All Customers
def view_customers():
    users = load_users()

    if not users:
        print("\nNo customers found.")
        return

    print("\n" + "-" * 40)
    print("          ALL CUSTOMERS")
    print("-" * 40)

    for user in users:
        print(f"Customer ID: {user['customer_id']}")
        print(f"Name       : {user['name']}")
        print(f"Email      : {user['email']}")
        print("-" * 40)


#Search a customer
def search_customer():
    customer_id = input("Enter Customer ID: ")

    users = load_users()

    for user in users:
        if user["customer_id"] == customer_id:
            print("\nCustomer Found!")
            print(f"Customer ID: {user['customer_id']}")
            print(f"Name       : {user['name']}")
            print(f"Email      : {user['email']}")
            return

    print("Customer not found.")

#Remove the customer
def remove_customer():
    customer_id = input("Enter Customer ID to delete: ")

    confirm = input(
        "Are you sure you want to delete this customer? (yes/no): "
    ).lower()

    if confirm == "yes":
        success = delete_user(customer_id)

        if success:
            print("Customer deleted successfully.")
        else:
            print("Customer not found.")
    else:
        print("Deletion cancelled.")

def manage_customers():
    while True:
        print("\n" + "-" * 30)
        print("      MANAGE CUSTOMERS")
        print("-" * 30)

        print("1. View All Customers")
        print("2. Search Customer")
        print("3. Delete Customer")
        print("4. Back")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Please Enter a Valid Number.")
            continue

        if choice == 1:
            view_customers()

        elif choice == 2:
            search_customer()

        elif choice == 3:
            remove_customer()

        elif choice == 4:
            break

        else:
            print("Invalid Choice.")


def view_all_subscriptions():
    subscriptions = load_subscriptions()

    if not subscriptions:
        print("\nNo subscriptions found.")
        return

    print("\n" + "=" * 50)
    print("          ALL SUBSCRIPTIONS")
    print("=" * 50)

    for subscription in subscriptions:
        print(f"Subscription ID : {subscription['sub_id']}")
        print(f"Customer ID     : {subscription['customer_id']}")
        print(f"Plan ID         : {subscription['plan_id']}")
        print(f"Start Date      : {subscription['start_date']}")
        print(f"Expiry Date     : {subscription['expiry_date']}")
        print(f"Status          : {subscription['status']}")
        print("-" * 50)


def view_active_subscriptions():
    subscriptions = load_subscriptions()

    found = False

    for subscription in subscriptions:
        if subscription["status"] == "Active":
            found = True

            print(f"\nSubscription ID : {subscription['sub_id']}")
            print(f"Customer ID     : {subscription['customer_id']}")
            print(f"Plan ID         : {subscription['plan_id']}")
            print(f"Expiry Date     : {subscription['expiry_date']}")
            print(f"Status          : {subscription['status']}")
            print("-" * 40)

    if not found:
        print("\nNo active subscriptions found.")


def view_expired_subscriptions():
    subscriptions = load_subscriptions()

    found = False

    for subscription in subscriptions:
        if subscription["status"] == "Expired":
            found = True

            print(f"\nSubscription ID : {subscription['sub_id']}")
            print(f"Customer ID     : {subscription['customer_id']}")
            print(f"Plan ID         : {subscription['plan_id']}")
            print(f"Expiry Date     : {subscription['expiry_date']}")
            print(f"Status          : {subscription['status']}")
            print("-" * 40)

    if not found:
        print("\nNo expired subscriptions found.")


def cancel_subscription():
    subscriptions = load_subscriptions()

    sub_id = input("Enter Subscription ID to cancel: ")

    found = False

    for subscription in subscriptions:

        if subscription["sub_id"] == sub_id:

            found = True

            if subscription["status"] == "Cancelled":
                print("Subscription is already cancelled.")
                return

            subscription["status"] = "Cancelled"

            update_subscriptions(subscriptions)

            print("Subscription cancelled successfully.")
            return

    if not found:
        print("Subscription not found.")


def manage_subscriptions():
    while True:

        print("\n" + "=" * 35)
        print("      MANAGE SUBSCRIPTIONS")
        print("=" * 35)

        print("1. View All Subscriptions")
        print("2. View Active Subscriptions")
        print("3. View Expired Subscriptions")
        print("4. Cancel Subscription")
        print("5. Back")

        try:
            choice = int(input("Enter your choice: "))

        except ValueError:
            print("Please enter a valid number.")
            continue

        if choice == 1:
            view_all_subscriptions()

        elif choice == 2:
            view_active_subscriptions()

        elif choice == 3:
            view_expired_subscriptions()

        elif choice == 4:
            cancel_subscription()

        elif choice == 5:
            break

        else:
            print("Invalid Choice.")

            
def view_all_notifications():
    notifications = load_notifications()

    if not notifications:
        print("\nNo notifications found.")
        return

    print("\n" + "=" * 50)
    print("          ALL NOTIFICATIONS")
    print("=" * 50)

    for notification in notifications:
        print(f"Notification ID : {notification['notification_id']}")
        print(f"Customer ID     : {notification['customer_id']}")
        print(f"Type            : {notification['notification_type']}")
        print(f"Message         : {notification['message']}")
        print(f"Date            : {notification['date']}")
        print(f"Status          : {notification['status']}")
        print("-" * 50)


def send_notification():
    customer_id = input("Enter Customer ID: ")

    notification_type = input("Enter Notification Type: ")

    message = input("Enter Message: ")

    notification = {
        "notification_id": generate_notification_id(),
        "customer_id": customer_id,
        "notification_type": notification_type,
        "message": message,
        "date": str(date.today()),
        "status": "Unread"
    }

    save_notification(notification)

    print("Notification sent successfully.")


def create_expiry_reminders():
    subscriptions = load_subscriptions()
    notifications = load_notifications()

    today = date.today()
    reminder_date = today + timedelta(days=3)

    for subscription in subscriptions:

        if subscription["status"] != "Active":
            continue

        expiry_date = date.fromisoformat(
            subscription["expiry_date"]
        )

        if today <= expiry_date <= reminder_date:

            already_exists = False

            for notification in notifications:
                if (
                    notification["customer_id"]
                    == subscription["customer_id"]
                    and notification["notification_type"]
                    == "Expiry Reminder"
                    and notification["message"]
                    == f"Your subscription {subscription['sub_id']} expires on {subscription['expiry_date']}"
                ):
                    already_exists = True
                    break

            if not already_exists:

                notification = {
                    "notification_id": generate_notification_id(),
                    "customer_id": subscription["customer_id"],
                    "notification_type": "Expiry Reminder",
                    "message": (
                        f"Your subscription "
                        f"{subscription['sub_id']} expires on "
                        f"{subscription['expiry_date']}"
                    ),
                    "date": str(today),
                    "status": "Unread"
                }

                save_notification(notification)

                print(
                    f"Expiry reminder created for "
                    f"{subscription['customer_id']}"
                )

    print("Expiry reminder process completed.")



def manage_notifications():
    while True:

        print("\n" + "=" * 40)
        print("      NOTIFICATIONS AND REMINDERS")
        print("=" * 40)

        print("1. View All Notifications")
        print("2. Send Notification")
        print("3. Create Expiry Reminders")
        print("4. Back")

        try:
            choice = int(input("Enter your choice: "))

        except ValueError:
            print("Please enter a valid number.")
            continue

        if choice == 1:
            view_all_notifications()

        elif choice == 2:
            send_notification()

        elif choice == 3:
            create_expiry_reminders()

        elif choice == 4:
            break

        else:
            print("Invalid Choice.")