
from database.connectionDB import DatabaseConnection

from datetime import date, timedelta




#check if email exists or not 
def checkEmailExists(email:str,data:bool=False):
    db_config = None
    cursor = None
    try:
        db_config=DatabaseConnection()
        cursor=db_config.cursor(dictionary=True)
        get_userby_email="""select * from customers where email=%s"""
        cursor.execute(get_userby_email,(email,))
        user=cursor.fetchone()

        


        if data:
            if user:
                return True,user
            else:
                return False,"Invalid Details"
        if not user:
            return True,"Email Available"
        else:
            return False,"Email Already Exists"
    except Exception as e:
        return False,f"Something went wrong in utilityDB/checkEmailExists: {e}"
    finally:
        if cursor:
            cursor.close()
        if db_config:
            db_config.close()


#Insert user into table
def insertCustomer(username:str,email:str,password:str):
    db_config = None
    cursor = None
    try:
        db_config=DatabaseConnection()
        cursor=db_config.cursor()
        # Assign role based on email
        if email.strip().lower() == "admin123@gmail.com":
            role = "admin"
        else:
            role = "customer"
        insert_customer_query="""insert into customers(name,email,password,role) values(%s,%s,%s,%s)"""
        cursor.execute(insert_customer_query,(username,email,password,role))
        db_config.commit()

        return True ,"You have Registered Successfully"
    except Exception as e:
        return False,f"Something went wrong in utilityDB/insertCustomer: {e}"
    finally:
        if cursor:
            cursor.close()
        if db_config:
            db_config.close()
    

#Insert plan into table
def insertPlan(plan_name:str,price:float,duration:int):
    db_config = None
    cursor = None
    try:
        db_config=DatabaseConnection()
        cursor=db_config.cursor()
        
        insert_plan_query="""insert into plans(plan_name,price,duration) values(%s,%s,%s)"""
        cursor.execute(insert_plan_query,(plan_name,price,duration))
        db_config.commit()

        return True ,"Plan Successfully Added"
    except Exception as e:
        return False,f"Something went wrong in utilityDB/insertPlan: {e}"
    finally:
        if cursor:
            cursor.close()
        if db_config:
            db_config.close()
    

def getAllPlans():
    db_config = None
    cursor = None
    try:
        db_config = DatabaseConnection()
        cursor = db_config.cursor(dictionary=True)

        query = """
            SELECT plan_id, plan_name, price, duration,is_active
            FROM plans
            ORDER BY plan_id 
        """

        cursor.execute(query)
        plans = cursor.fetchall()

        

        return True, plans

    except Exception as e:
        print(f"Error in getAllPlans: {e}")
        return False, "Unable to retrieve subscription plans."

    finally:
        if cursor:
            cursor.close()
        if db_config:
            db_config.close()


#update plan

def updatePlans(plan_id: int, plan_name: str, price: float, duration: int):
    db_config = None
    cursor = None

    try:
        db_config = DatabaseConnection()
        cursor = db_config.cursor()

        # Check whether the plan exists
        cursor.execute(
            "SELECT plan_id FROM plans WHERE plan_id = %s",
            (plan_id,)
        )

        if cursor.fetchone() is None:
            return False, "Subscription plan not found."

        # Update the plan details
        query = """
            UPDATE plans
            SET plan_name = %s,
                price = %s,
                duration = %s
            WHERE plan_id = %s
        """

        cursor.execute(
            query,
            (plan_name, price, duration, plan_id)
        )

        db_config.commit()

        return True, "Subscription plan updated successfully."

    except Exception as e:
        if db_config:
            db_config.rollback()

        print(f"Error in updatePlan: {e}")
        return False, "Unable to update subscription plan."

    finally:
        if cursor:
            cursor.close()
        if db_config:
            db_config.close()





#deactivate plan
def deactivatePlan(plan_id: int):
    db_config = None
    cursor = None

    try:
        db_config = DatabaseConnection()
        cursor = db_config.cursor()

        query = """
            UPDATE plans
            SET is_active = FALSE
            WHERE plan_id = %s AND is_active = TRUE
        """

        cursor.execute(query, (plan_id,))

        if cursor.rowcount == 0:
            cursor.execute(
                "SELECT is_active FROM plans WHERE plan_id = %s",
                (plan_id,)
            )
            plan = cursor.fetchone()

            if not plan:
                db_config.rollback()
                return False, "Subscription plan not found."

            db_config.commit()
            return True, "Plan is already deactivated."

        db_config.commit()
        return True, "Subscription plan deactivated successfully."

    except Exception as e:
        

       
        return False, f"Something went wrong in utilityDB/updatePlans:{e}"

    finally:
        if cursor:
            cursor.close()
        if db_config:
            db_config.close()

#reactivate plan

def reactivatePlan(plan_id: int):
    db_config = None
    cursor = None

    try:
        db_config = DatabaseConnection()
        cursor = db_config.cursor()

        query = """
            UPDATE plans
            SET is_active = TRUE
            WHERE plan_id = %s
        """

        cursor.execute(query, (plan_id,))

        if cursor.rowcount == 0:
            cursor.execute(
                "SELECT plan_id FROM plans WHERE plan_id = %s",
                (plan_id,)
            )

            if cursor.fetchone() is None:
                db_config.rollback()
                return False, "Subscription plan not found."

        db_config.commit()
        return True, "Subscription plan activated successfully."

    except Exception as e:
        if db_config:
            db_config.rollback()

        print(f"Error in reactivatePlan: {e}")
        return False, "Unable to reactivate subscription plan."

    finally:
        if cursor:
            cursor.close()
        if db_config:
            db_config.close()



#get all customers

def getAllCustomers():
    db_config = None
    cursor = None

    try:
        db_config = DatabaseConnection()
        cursor = db_config.cursor(dictionary=True)

        query = """
            SELECT customer_id, name, email, role
            FROM customers
            ORDER BY customer_id DESC
        """

        cursor.execute(query)
        customers = cursor.fetchall()

        return True, customers

    except Exception as e:
        print(f"Error in getAllCustomers: {e}")
        return False, "Unable to retrieve customers."

    finally:
        if cursor:
            cursor.close()
        if db_config:
            db_config.close()


#search customers


def searchCustomers(search_term: str):
    db_config = None
    cursor = None

    try:
        db_config = DatabaseConnection()
        cursor = db_config.cursor(dictionary=True)

        query = """
            SELECT customer_id, name, email, role
            FROM customers
            WHERE name LIKE %s OR email LIKE %s
            ORDER BY customer_id 
        """

        search_value = f"%{search_term}%"

        cursor.execute(query, (search_value, search_value))
        customers = cursor.fetchall()

        return True, customers

    except Exception as e:
        print(f"Error in searchCustomers: {e}")
        return False, "Unable to search customers."

    finally:
        if cursor:
            cursor.close()
        if db_config:
            db_config.close()



#getallsubscriptions

def getAllSubscriptions():
    db_config = None
    cursor = None

    try:
        db_config = DatabaseConnection()
        cursor = db_config.cursor(dictionary=True)

        query = """
            SELECT
                s.subscription_id,
                s.customer_id,
                c.name AS customer_name,
                c.email AS customer_email,
                s.plan_id,
                p.plan_name,
                p.price,
                s.start_date,
                s.expiry_date,
                s.status
            FROM subscriptions s
            JOIN customers c
                ON s.customer_id = c.customer_id
            JOIN plans p
                ON s.plan_id = p.plan_id
            ORDER BY s.subscription_id 
        """

        cursor.execute(query)
        subscriptions = cursor.fetchall()

        return True, subscriptions

    except Exception as e:
        print(f"Error in getAllSubscriptions: {e}")
        return False, "Unable to retrieve subscriptions."

    finally:
        if cursor:
            cursor.close()
        if db_config:
            db_config.close()

#create subscription

def createSubscription(customer_id: int, plan_id: int):
    db_config = None
    cursor = None

    try:
        db_config = DatabaseConnection()
        cursor = db_config.cursor(dictionary=True)

        # Check whether the selected plan is active
        query = """
            SELECT duration
            FROM plans
            WHERE plan_id = %s AND is_active = TRUE
        """
        cursor.execute(query, (plan_id,))
        plan = cursor.fetchone()

        if not plan:
            return False, "This plan is unavailable or inactive."

        # Calculate subscription dates
        start_date = date.today()
        expiry_date = start_date + timedelta(days=plan['duration'])

        # Insert the subscription
        query = """
            INSERT INTO subscriptions
                (customer_id, plan_id, start_date, expiry_date, status)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (customer_id, plan_id, start_date, expiry_date, 'active')
        )

        db_config.commit()
        return True, "Subscription created successfully!"

    except Exception as e:
        if db_config:
            db_config.rollback()

        print(f"Error in createSubscription: {e}")
        return False, "Unable to create your subscription."

    finally:
        if cursor:
            cursor.close()
        if db_config:
            db_config.close()


#getcustomer subscription

def getCustomerSubscriptions(customer_id: int):
    db_config = None
    cursor = None

    try:
        db_config = DatabaseConnection()
        cursor = db_config.cursor(dictionary=True)

        query = """
            SELECT
                s.subscription_id,
                s.customer_id,
                s.plan_id,
                p.plan_name,
                p.price,
                p.duration,
                s.start_date,
                s.expiry_date,
                s.status
            FROM subscriptions s
            JOIN plans p
                ON s.plan_id = p.plan_id
            WHERE s.customer_id = %s
            ORDER BY s.subscription_id 
        """

        cursor.execute(query, (customer_id,))
        subscriptions = cursor.fetchall()

        return True, subscriptions

    except Exception as e:
        print(f"Error in getCustomerSubscriptions: {e}")
        return False, "Unable to retrieve your subscriptions."

    finally:
        if cursor:
            cursor.close()
        if db_config:
            db_config.close()



#generate subscriptionnotification
@staticmethod
def generateSubscriptionNotifications(customer_id: int):
    db_config = None
    cursor = None

    try:
        db_config = DatabaseConnection()
        cursor = db_config.cursor(dictionary=True)

        today = date.today()
        reminder_limit = today + timedelta(days=3)

        # Get this customer's subscriptions
        query = """
            SELECT subscription_id, expiry_date
            FROM subscriptions
            WHERE customer_id = %s
        """
        cursor.execute(query, (customer_id,))
        subscriptions = cursor.fetchall()

        for subscription in subscriptions:
            subscription_id = subscription['subscription_id']
            expiry_date = subscription['expiry_date']

            # Decide which notification is required
            if expiry_date < today:
                notification_type = "Subscription Expired"
                message = (
                    f"Your subscription S{subscription_id} expired on "
                    f"{expiry_date:%Y-%m-%d}. Please renew to enjoy "
                    "uninterrupted services."
                )

            elif expiry_date <= reminder_limit:
                days_left = (expiry_date - today).days
                notification_type = "Expiry Reminder"
                message = (
                    f"Your subscription S{subscription_id} expires on "
                    f"{expiry_date:%Y-%m-%d}. You have {days_left} "
                    "day(s) remaining. Please renew to enjoy "
                    "uninterrupted services."
                )

            else:
                continue

            # Prevent duplicate notifications on repeated logins
            check_query = """
                SELECT notification_id
                FROM notifications
                WHERE subscription_id = %s
                  AND customer_id = %s
                  AND notification_type = %s
                LIMIT 1
            """
            cursor.execute(
                check_query,
                (subscription_id, customer_id, notification_type)
            )

            if cursor.fetchone():
                continue

            # Create the notification
            insert_query = """
                INSERT INTO notifications
                (
                    subscription_id,
                    customer_id,
                    notification_type,
                    message,
                    notification_date,
                    status
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                insert_query,
                (
                    subscription_id,
                    customer_id,
                    notification_type,
                    message,
                    today,
                    "Unread"
                )
            )

        db_config.commit()
        return True, "Notifications checked successfully."

    except Exception as e:
        if db_config:
            db_config.rollback()

        print(f"Error generating notifications: {e}")
        return False, "Unable to generate notifications."

    finally:
        if cursor:
            cursor.close()
        if db_config:
            db_config.close()


#getcustomer notification

@staticmethod
def getCustomerNotifications(customer_id: int):
    db_config = None
    cursor = None

    try:
        db_config = DatabaseConnection()
        cursor = db_config.cursor(dictionary=True)

        query = """
            SELECT
                notification_id,
                subscription_id,
                notification_type,
                message,
                notification_date,
                status
            FROM notifications
            WHERE customer_id = %s
            ORDER BY notification_date DESC, notification_id DESC
        """

        cursor.execute(query, (customer_id,))
        notifications = cursor.fetchall()

        return True, notifications

    except Exception as e:
        print(f"Error retrieving notifications: {e}")
        return False, "Unable to retrieve notifications."

    finally:
        if cursor:
            cursor.close()
        if db_config:
            db_config.close()




#getallnotiifcations

@staticmethod
def getAllNotifications():
    db_config = None
    cursor = None

    try:
        db_config = DatabaseConnection()
        cursor = db_config.cursor(dictionary=True)

        query = """
            SELECT
                n.notification_id,
                n.subscription_id,
                n.customer_id,
                c.name AS customer_name,
                c.email AS customer_email,
                n.notification_type,
                n.message,
                n.notification_date,
                n.status
            FROM notifications n
            JOIN customers c
                ON n.customer_id = c.customer_id
            ORDER BY n.notification_date DESC,
                     n.notification_id DESC
        """

        cursor.execute(query)
        notifications = cursor.fetchall()

        return True, notifications

    except Exception as e:
        print(f"Error retrieving all notifications: {e}")
        return False, "Unable to retrieve notifications."

    finally:
        if cursor:
            cursor.close()
        if db_config:
            db_config.close()



#marknotifications as read

@staticmethod
def markNotificationAsRead(notification_id: int, customer_id: int):
    db_config = None
    cursor = None

    try:
        db_config = DatabaseConnection()
        cursor = db_config.cursor()

        query = """
            UPDATE notifications
            SET status = 'Read'
            WHERE notification_id = %s
              AND customer_id = %s
              AND status = 'Unread'
        """

        cursor.execute(query, (notification_id, customer_id))
        db_config.commit()

        if cursor.rowcount > 0:
            return True, "Notification marked as read."

        return False, "Notification not found or already read."

    except Exception as e:
        if db_config:
            db_config.rollback()

        print(f"Error marking notification as read: {e}")
        return False, "Unable to mark notification as read."

    finally:
        if cursor:
            cursor.close()
        if db_config:
            db_config.close()
