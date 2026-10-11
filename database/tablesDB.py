from database.connectionDB import DatabaseConnection

def CreateTables():
    #db connection
    try:
        db_config=DatabaseConnection()
        #create cursor object
        cursor=db_config.cursor()
        #tables Queries
        #Customer table
        customers_table="""CREATE TABLE if not exists customers (
                        customer_id INT PRIMARY KEY AUTO_INCREMENT,
                        name VARCHAR(100) NOT NULL,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        password VARCHAR(255) NOT NULL
                        
                        );"""
        


        #plans table
        plans_table="""CREATE TABLE IF NOT EXISTS plans  (
                    plan_id INT PRIMARY KEY AUTO_INCREMENT,
                    plan_name VARCHAR(100) NOT NULL,
                    price DECIMAL(10,2) NOT NULL,
                    duration INT NOT NULL
                    );"""


        #subscriptions table
        subscriptions_table="""CREATE TABLE IF NOT EXISTS subscriptions (
                    subscription_id INT PRIMARY KEY AUTO_INCREMENT,
                    customer_id INT NOT NULL,
                    plan_id INT NOT NULL,
                    start_date DATE NOT NULL,
                    expiry_date DATE NOT NULL,
                    status VARCHAR(30) NOT NULL,

                    FOREIGN KEY (customer_id)
                        REFERENCES customers(customer_id),

                    FOREIGN KEY (plan_id)
                        REFERENCES plans(plan_id)
                    );"""

        #notifications table
        notifications_table="""CREATE TABLE IF NOT EXISTS notifications (
                    notification_id INT PRIMARY KEY AUTO_INCREMENT,
                    customer_id INT NOT NULL,
                    notification_type VARCHAR(100),
                    message VARCHAR(500),
                    notification_date DATE,
                    status VARCHAR(30),

                    FOREIGN KEY (customer_id)
                        REFERENCES customers(customer_id)
                    );"""

        #payments table
        payments_table="""CREATE TABLE IF NOT EXISTS payments (
                    payment_id INT PRIMARY KEY AUTO_INCREMENT,
                    subscription_id INT NOT NULL,
                    amount DECIMAL(10,2) NOT NULL,
                    payment_date DATE,
                    payment_status VARCHAR(30),

                    FOREIGN KEY (subscription_id)
                        REFERENCES subscriptions(subscription_id)
                    );"""
        # drop_table="""DROP TABLE payments_table;"""
        cursor.execute(customers_table)
        cursor.execute(plans_table)
        cursor.execute(subscriptions_table)
        cursor.execute(notifications_table)
        cursor.execute(payments_table)
        # cursor.execute(drop_table)
        return "Tables Created"



        





    except Exception as e:
        return f"Something wrong in database/tablesDB.py - CreateTables() :{e}"
    finally:
        if db_config:
            db_config.close()
            cursor.close()