
class User:
    def __init__(self,name,email,password):
        self.name=name
        self.email=email
        self.password=password
    def display_details(self):
        print(f"Name:{self.name}\nEmail:{self.email}\nPassword:{self.password}")
    def __str__(self):
        return f"{self.name} - {self.email}"
class Admin(User):
    def __init__(self,email,password):
        self.email=email
        self.password=password
class Customer(User):
    def __init__(self,customer_id,name,email,password):
        super().__init__(name,email,password)
        self.customer_id=customer_id

#admin=Admin("teja","sverr@gmail.com","Teja@0987")
#admin.display_details()


#Subscription Plan
class SubscriptionPlan:
    def __init__(self,plan_id,plan_name,price,duration):
        self.plan_id=plan_id
        self.plan_name=plan_name
        self.price=price
        self.duration=duration
    def display_plan(self):
        print(f"Plan ID:{self.plan_id}\nPlan Name:{self.plan_name}\nPlan Price:{self.price}\nDuration:{self.duration}")
    def __str__(self):
        return f"{self.plan_name} - {self.price}rs"
#basic = SubscriptionPlan("P001", "Basic", 299, 30)
#basic.display_plan()

#Connecting Customers-------->subscribes to------>Subscription Plan
class Subscription:
    def __init__(self,sub_id,customer,plan,start_date,expiry_date,status):
        self.sub_id=sub_id
        self.customer=customer    #Can be customer Object
        self.plan=plan            #Can be subscription Plan Object
        self.start_date=start_date
        self.expiry_date=expiry_date
        self.status=status
    def display_subscription(self):
        print(f"Subscription ID:{self.sub_id}\nCustomer:{self.customer}\nPlan:{self.plan}\nStart Date:{self.start_date}\nExpliry Date:{self.expiry_date}\nStatus:{self.status}")
    def __str__(self):
        return f"{self.sub_id} - {self.plan}"

#customer=Customer("teja","sverr@gmail.com","Teja@0987")
#premium=SubscriptionPlan("P001", "Basic", 299, 30)
#sub_obj=Subscription("S001",customer,premium,"23-07-2026","23-10-2026","Active")
#sub_obj.display_subscription()


class Notifications:
    def __init__(self,noti_id,customer,noti_type,message,date,status):
        self.noti_id=noti_id
        self.customer=customer
        self.noti_type=noti_type
        self.message=message
        self.date=date
        self.status=status
    def display_notification(self):
        print(f"Notification Id:{self.noti_id}\nCustomer:{self.customer}\nType:{self.noti_type}\nMessage:{self.message}\nDate:{self.date}\nStatus:{self.status}")
    def __str__(self):
        return f"{self.noti_id} - {self.noti_type}"
#n=Notifications("s012","teja","Expiry Remainder","Your plan will be expired soon","25-07-2026","Active")
#n.display_notification()



class ActivityLog:
    def __init__(self,activity_id,customer,action,description,date):
        self.activity_id=activity_id
        self.customer=customer
        self.action=action
        self.description=description
        self.date=date
    def display_activity(self):
        print(f"Activity ID:{self.activity_id}\nCustomer:{self.customer}\nAction:{self.action}\nDescription:{self.description}\nDate:{self.date}")
#a=ActivityLog("A001","teja","Subscription Purchased","Premium plan purchased successfully","25-07-2026")
#a.display_activity()