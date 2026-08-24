from models import Customer

def save_user(user):
    with open("data/users.txt", "a") as file:
        file.write(
            f"{user.customer_id}|"
            f"{user.name}|"
            f"{user.email}|"
            f"{user.password}\n"
        )
def load_users():
    users = []

    try:
        with open("data/users.txt", "r") as file:

            for line in file:
                line = line.strip()

                # Skip empty lines
                if not line:
                    continue

                data = line.split("|")

                # Skip invalid records
                if len(data) != 4:
                    continue

                user = {
                    "customer_id": data[0],
                    "name": data[1],
                    "email": data[2],
                    "password": data[3]
                }

                users.append(user)

    except FileNotFoundError:
        print("Users file not found.")

    return users
def generate_customer_id():
    try:
        with open("data/users.txt", "r") as file:
            lines = file.readlines()

        next_number = len(lines) + 1

    except FileNotFoundError:
        next_number = 1

    return f"C{next_number:03d}"
def generate_plan_id():
    try:
        with open("data/plans.txt", "r") as file:
            lines = file.readlines()

        next_number = len(lines) + 1

    except FileNotFoundError:
        next_number = 1

    return f"P{next_number:03d}"


def load_plans():
    plans = []

    try:
        with open("data/plans.txt", "r") as file:
            for line in file:

                if not line.strip():
                    continue

                data = line.strip().split("|")

                if len(data) != 4:
                    print(f"Invalid plan data: {line.strip()}")
                    continue

                plan = {
                    "plan_id": data[0],
                    "plan_name": data[1],
                    "price": float(data[2]),
                    "duration": int(data[3])
                }

                plans.append(plan)

    except FileNotFoundError:
        print("Plans file not found.")

    return plans

def delete_user(customer_id):
    users = load_users()

    new_users = []
    found = False

    for user in users:
        if user["customer_id"] == customer_id:
            found = True
        else:
            new_users.append(user)

    if not found:
        return False

    with open("data/users.txt", "w") as file:
        for user in new_users:
            file.write(
                f"{user['customer_id']}|"
                f"{user['name']}|"
                f"{user['email']}|"
                f"{user['password']}\n"
            )

    return True

def generate_subscription_id():
    try:
        with open("data/subscriptions.txt", "r") as file:
            lines = file.readlines()

        numbers = []

        for line in lines:
            line = line.strip()

            # Skip blank lines
            if not line:
                continue

            data = line.split("|")

            # Skip invalid records
            if len(data) < 1:
                continue

            sub_id = data[0]

            # Skip if Subscription ID is invalid
            if not sub_id.startswith("S"):
                continue

            try:
                number = int(sub_id[1:])
                numbers.append(number)
            except ValueError:
                continue

        # If no valid subscriptions exist
        if not numbers:
            return "S001"

        next_number = max(numbers) + 1
        return f"S{next_number:03d}"

    except FileNotFoundError:
        return "S001"

def save_subscription(subscription):
    with open("data/subscriptions.txt", "a") as file:
        file.write(
            f"{subscription['sub_id']}|"
            f"{subscription['customer_id']}|"
            f"{subscription['plan_id']}|"
            f"{subscription['start_date']}|"
            f"{subscription['expiry_date']}|"
            f"{subscription['status']}\n"
        )

def load_subscriptions():
    subscriptions = []

    try:
        with open("data/subscriptions.txt", "r") as file:
            for line in file:

                if not line.strip():
                    continue

                data = line.strip().split("|")

                if len(data) != 6:
                    continue

                subscription = {
                    "sub_id": data[0],
                    "customer_id": data[1],
                    "plan_id": data[2],
                    "start_date": data[3],
                    "expiry_date": data[4],
                    "status": data[5]
                }

                subscriptions.append(subscription)

    except FileNotFoundError:
        return []

    return subscriptions

def update_subscriptions(subscriptions):
    with open("data/subscriptions.txt", "w") as file:
        for subscription in subscriptions:
            file.write(
                f"{subscription['sub_id']}|"
                f"{subscription['customer_id']}|"
                f"{subscription['plan_id']}|"
                f"{subscription['start_date']}|"
                f"{subscription['expiry_date']}|"
                f"{subscription['status']}\n"
            )




def generate_notification_id():
    try:
        with open("data/notifications.txt", "r") as file:
            lines = file.readlines()

        if not lines:
            return "N001"

        numbers = []

        for line in lines:
            notification_id = line.strip().split("|")[0]
            number = int(notification_id[1:])
            numbers.append(number)

        next_number = max(numbers) + 1

    except FileNotFoundError:
        next_number = 1

    return f"N{next_number:03d}"


def save_notification(notification):
    with open("data/notifications.txt", "a") as file:
        file.write(
            f"{notification['notification_id']}|"
            f"{notification['customer_id']}|"
            f"{notification['notification_type']}|"
            f"{notification['message']}|"
            f"{notification['date']}|"
            f"{notification['status']}\n"
        )

def load_notifications():
    notifications = []

    try:
        with open("data/notifications.txt", "r") as file:
            for line in file:

                if not line.strip():
                    continue

                data = line.strip().split("|")

                if len(data) != 6:
                    continue

                notification = {
                    "notification_id": data[0],
                    "customer_id": data[1],
                    "notification_type": data[2],
                    "message": data[3],
                    "date": data[4],
                    "status": data[5]
                }

                notifications.append(notification)

    except FileNotFoundError:
        print("Notifications file not found.")

    return notifications