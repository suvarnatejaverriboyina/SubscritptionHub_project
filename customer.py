from datetime import date, timedelta

from file_manager import (
    load_plans,
    generate_subscription_id,
    save_subscription,
    load_subscriptions,
    update_subscriptions

)


def purchase_subscription(current_user):
    plans = load_plans()

    if not plans:
        print("\nNo subscription plans are available.")
        return

    print("\n===== AVAILABLE PLANS =====")

    for plan in plans:
        print(
            f"{plan['plan_id']} | "
            f"{plan['plan_name']} | "
            f"${plan['price']} | "
            f"{plan['duration']} days"
        )

    plan_id = input("\nEnter Plan ID to purchase: ")

    selected_plan = None

    for plan in plans:
        if plan["plan_id"] == plan_id:
            selected_plan = plan
            break

    if selected_plan is None:
        print("Invalid Plan ID.")
        return

    subscriptions = load_subscriptions()

    for subscription in subscriptions:
        if (
            subscription["customer_id"]
            == current_user["customer_id"]
            and subscription["status"] == "Active"
        ):
            print("You already have an active subscription.")
            return

    start_date = date.today()

    expiry_date = (
        start_date
        + timedelta(days=selected_plan["duration"])
    )

    subscription = {
        "sub_id": generate_subscription_id(),
        "customer_id": current_user["customer_id"],
        "plan_id": selected_plan["plan_id"],
        "start_date": str(start_date),
        "expiry_date": str(expiry_date),
        "status": "Active"
    }

    save_subscription(subscription)

    print("\nSubscription Purchased Successfully!")
    print(f"Subscription ID: {subscription['sub_id']}")
    print(f"Plan: {selected_plan['plan_name']}")
    print(f"Start Date: {start_date}")
    print(f"Expiry Date: {expiry_date}")


def view_my_subscription(current_user):
    subscriptions = load_subscriptions()

    customer_id = current_user["customer_id"]

    found = False

    for subscription in subscriptions:

        if subscription["customer_id"] == customer_id:
            found = True

            print("\n" + "=" * 40)
            print("       MY SUBSCRIPTION")
            print("=" * 40)

            print(f"Subscription ID : {subscription['sub_id']}")
            print(f"Customer ID     : {subscription['customer_id']}")
            print(f"Plan ID         : {subscription['plan_id']}")
            print(f"Start Date      : {subscription['start_date']}")
            print(f"Expiry Date     : {subscription['expiry_date']}")
            print(f"Status          : {subscription['status']}")

            print("=" * 40)

    if not found:
        print("\nYou do not have any subscription.")

def renew_subscription(current_user):
    subscriptions = load_subscriptions()
    plans = load_plans()

    customer_id = current_user["customer_id"]

    for subscription in subscriptions:

        if (
            subscription["customer_id"] == customer_id
            and subscription["status"] == "Active"
        ):

            plan = None

            for p in plans:
                if p["plan_id"] == subscription["plan_id"]:
                    plan = p
                    break

            if plan is None:
                print("Plan not found.")
                return

            expiry_date = date.fromisoformat(
                subscription["expiry_date"]
            )

            new_expiry_date = (
                expiry_date
                + timedelta(days=plan["duration"])
            )

            subscription["expiry_date"] = str(new_expiry_date)

            update_subscriptions(subscriptions)

            print("\nSubscription Renewed Successfully!")
            print(f"New Expiry Date: {new_expiry_date}")

            return

    print("\nYou do not have an active subscription.")

def cancel_subscription(current_user):
    subscriptions = load_subscriptions()

    customer_id = current_user["customer_id"]

    for subscription in subscriptions:

        if (
            subscription["customer_id"] == customer_id
            and subscription["status"] == "Active"
        ):

            print("\nYour Active Subscription")
            print(f"Subscription ID: {subscription['sub_id']}")
            print(f"Plan ID: {subscription['plan_id']}")
            print(f"Expiry Date: {subscription['expiry_date']}")

            confirm = input(
                "\nAre you sure you want to cancel? (yes/no): "
            ).lower()

            if confirm == "yes":

                subscription["status"] = "Cancelled"

                update_subscriptions(subscriptions)

                print("\nSubscription Cancelled Successfully!")

            else:
                print("\nCancellation Cancelled.")

            return

    print("\nYou do not have an active subscription.")


def view_available_plans():
    plans = load_plans()

    if not plans:
        print("\nNo subscription plans are available.")
        return

    print("\n" + "=" * 45)
    print("          AVAILABLE SUBSCRIPTION PLANS")
    print("=" * 45)

    for plan in plans:
        print(f"Plan ID  : {plan['plan_id']}")
        print(f"Name     : {plan['plan_name']}")
        print(f"Price    : ${plan['price']}")
        print(f"Duration : {plan['duration']} days")
        print("-" * 45)

def customer_menu(current_user):
    while True:
        print("\n" + "=" * 40)
        print("          CUSTOMER MENU")
        print("=" * 40)

        print("1. View Available Plans")
        print("2. Purchase Subscription")
        print("3. View My Subscription")
        print("4. Renew Subscription")
        print("5. Cancel Subscription")
        print("6. Logout")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if choice == 1:
            view_available_plans()

        elif choice == 2:
            purchase_subscription(current_user)

        elif choice == 3:
            view_my_subscription(current_user)

        elif choice == 4:
            renew_subscription(current_user)

        elif choice == 5:
            cancel_subscription(current_user)

        elif choice == 6:
            print("Logged out successfully.")
            break

        else:
            print("Invalid choice.")