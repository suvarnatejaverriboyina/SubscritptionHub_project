from flask import Flask,render_template,session,flash,request,redirect,url_for
import bcrypt
from utils import generateHashpassword,verifyHashpassword

from database import checkEmailExists,insertCustomer,insertPlan,getAllPlans,updatePlans,deactivatePlan,reactivatePlan,getAllCustomers,searchCustomers,getAllSubscriptions,createSubscription,getCustomerSubscriptions,getCustomerNotifications,generateSubscriptionNotifications,getAllNotifications,markNotificationAsRead


app=Flask(__name__)
app.secret_key = "Suvarnateja1234"

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    if request.method=='POST':
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        confirmpassword=request.form.get('confirmpassword')
        # check password and confirmpassword are same or not
        if password!=confirmpassword:
            flash("Password Mismatch",'err')
            return redirect(url_for('register'))
        #check if email exists or not
        status,msg=checkEmailExists(email)
        if status==False:
            flash(msg,"err")
            return redirect(url_for('register'))
        else:
            
            #generate hashpassword
            hash_password=generateHashpassword(password)
            status,msg=insertCustomer(username,email,hash_password)
            if status==True:
                flash(msg,'msg')
                return redirect(url_for('login'))
            else:
                flash(msg,'err')
                return redirect(url_for('register'))

            
            



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check whether the email exists
        status, data = checkEmailExists(email=email, data=True)

        if status == False:
            flash(data, 'err')
            return redirect(url_for('login'))

        # Verify password
        hash_password = data['password']

        if verifyHashpassword(
            user_password=password,
            hash_password=hash_password
        ):
            # Store customer details in session
            session.clear()
            session['customer_id'] = data['customer_id']
            session['username'] = data['name']
            session['email'] = data['email']
            session['role'] = data['role']

            # Generate notifications for customers only
            if data['role'] == 'customer':
                print("DEBUG: Customer login successful")
                print("DEBUG: Customer ID:", data['customer_id'])
                print("DEBUG: Customer role:", data['role'])

                success, message = generateSubscriptionNotifications(
                    customer_id=data['customer_id']
                )

                

            # Welcome message
            flash(
                f"Hello {data['name']}. Welcome to SMS - Hub. "
                "Enjoy our services by purchasing them.",
                'msg'
            )

            return redirect(url_for('dashboard'))

        flash("Check your password", 'err')
        return redirect(url_for('login'))



@app.route('/customer/dashboard')
def customer_dashboard():
    return render_template('admin_dashboard.html')


#common dashboard

@app.route('/dashboard')
def dashboard():

    if 'customer_id' not in session:
        flash("Please login first.", "err")
        return redirect(url_for('login'))

    if session.get('role') == 'admin':
        return render_template('admin_dashboard.html')

    return render_template('customer_dashboard.html')


@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('customer_dashboard.html')

@app.route('/admin/manage_plans',methods=['GET','POST'])
def manage_plans():
    # #check if customer is in session
    # if 'customer_id' not in session:
    #     flash('Please login first','err')
    #     return redirect(url_for('login'))
    # #check if the role is admin to access manage_plans
    # if session.get('role')!='admin':
    #     flash('Access is denied for Customers','err')
    #     return redirect(url_for('dashboard'))

    if request.method=='GET':
        success, result = getAllPlans()
        if success:
            plans = result
        else:
            plans = []
            flash(result, "err")
        return render_template("manage_plans.html", plans=plans)

       
    if request.method=='POST':
        plan_name=request.form.get('plan_name')
        price=request.form.get('price')
        duration=request.form.get('duration')

        if not plan_name or not price or not duration:
            flash('Please fill all the details','err')
        status,msg= insertPlan(plan_name=plan_name,price=price,duration=duration)
        if status==False:
            flash(msg,'err')
            return redirect(url_for('dashboard'))
        else:
            flash(msg,'msg')
            return redirect(url_for('manage_plans'))
        

@app.route('/admin/plans/edit/<int:plan_id>', methods=['GET', 'POST'])
def edit_plan(plan_id):

    if 'customer_id' not in session:
        flash("Please login first.", "err")
        return redirect(url_for('login'))

    if session.get('role') != 'admin':
        flash("Access denied. Admins only.", "err")
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        plan_name = request.form.get('plan_name', '').strip()
        price = request.form.get('price', '').strip()
        duration = request.form.get('duration', '').strip()

        if not plan_name or not price or not duration:
            flash("Please fill in all fields.", "err")
            return redirect(url_for('edit_plan', plan_id=plan_id))

        try:
            price = float(price)
            duration = int(duration)

            if price <= 0 or duration <= 0:
                flash("Price and duration must be positive.", "err")
            else:
                success, message = updatePlans(
                    plan_id, plan_name, price, duration
                )
                flash(message, "msg" if success else "err")

        except ValueError:
            flash("Enter a valid price and duration.", "err")

        return redirect(url_for('manage_plans'))

    success, result = getAllPlans()

    if not success:
        flash(result, "err")
        return redirect(url_for('manage_plans'))

    plan = next(
        (item for item in result if item['plan_id'] == plan_id),
        None
    )

    if not plan:
        flash("Subscription plan not found.", "err")
        return redirect(url_for('manage_plans'))

    return render_template('edit_plan.html', plan=plan)


@app.route('/admin/plans/deactivate/<int:plan_id>', methods=['POST'])
def deactivate_plan(plan_id):

    if 'customer_id' not in session:
        flash("Please login first.", "err")
        return redirect(url_for('login'))

    if session.get('role') != 'admin':
        flash("Access denied. Admins only.", "err")
        return redirect(url_for('dashboard'))

    success, message = deactivatePlan(plan_id)
    flash(message, "msg" if success else "err")

    return redirect(url_for('manage_plans'))



@app.route('/admin/plans/reactivate/<int:plan_id>', methods=['POST'])
def reactivate_plan(plan_id):

    if 'customer_id' not in session:
        flash("Please login first.", "err")
        return redirect(url_for('login'))

    if session.get('role') != 'admin':
        flash("Access denied. Admins only.", "err")
        return redirect(url_for('dashboard'))

    success, message = reactivatePlan(plan_id)

    flash(message, "msg" if success else "err")

    return redirect(url_for('manage_plans'))


#managing customers


@app.route('/admin/customers')
def manage_customers():
    if 'customer_id' not in session:
        flash("Please login first.", "err")
        return redirect(url_for('login'))

    if session.get('role') != 'admin':
        flash("Access denied. Admins only.", "err")
        return redirect(url_for('dashboard'))

    search_term = request.args.get('search', '').strip()

    if search_term:
        success, result = searchCustomers(search_term)
    else:
        success, result = getAllCustomers()

    if not success:
        flash(result, "err")
        return redirect(url_for('dashboard'))

    return render_template(
        'manage_customers.html',
        customers=result,
        search_term=search_term
    )


#managesubscriptions

@app.route('/admin/subscriptions')
def manage_subscriptions():
    if 'customer_id' not in session:
        flash("Please login first.", "err")
        return redirect(url_for('login'))

    if session.get('role') != 'admin':
        flash("Access denied. Admins only.", "err")
        return redirect(url_for('dashboard'))

    success, result = getAllSubscriptions()

    if not success:
        flash(result, "err")
        return redirect(url_for('dashboard'))

    return render_template(
        'manage_subscriptions.html',
        subscriptions=result
    )


@app.route('/customer/plans')
def available_plans():
    # Check whether the customer is logged in
    if 'customer_id' not in session:
        flash('Please login first.', 'err')
        return redirect(url_for('login'))

    # Only customers should access this page
    if session.get('role') != 'customer':
        flash('This page is for customers only.', 'err')
        return redirect(url_for('dashboard'))

    success, result = getAllPlans()

    if not success:
        flash(result, 'err')
        plans = []
    else:
        # Display only active plans
        plans = [
            plan for plan in result
            if plan['is_active']
        ]

    return render_template(
        'available_plans.html',
        plans=plans
    )

#subscriber route

@app.route('/customer/subscribe', methods=['POST'])
def subscribe_plan():
    # Check login
    if 'customer_id' not in session:
        flash('Please login first.', 'err')
        return redirect(url_for('login'))

    # Allow customers only
    if session.get('role') != 'customer':
        flash('Only customers can subscribe to plans.', 'err')
        return redirect(url_for('dashboard'))

    # Get the selected plan ID
    plan_id = request.form.get('plan_id', type=int)

    if not plan_id:
        flash('Please select a valid plan.', 'err')
        return redirect(url_for('available_plans'))

    # Create subscription for the logged-in customer
    success, message = createSubscription(
        customer_id=session['customer_id'],
        plan_id=plan_id
    )

    if success:
        flash(message, 'msg')
        return redirect(url_for('my_subscriptions'))

    flash(message, 'err')
    return redirect(url_for('available_plans'))



#mysubscriptions

@app.route('/customer/my-subscriptions')
def my_subscriptions():
    if 'customer_id' not in session:
        flash('Please login first.', 'err')
        return redirect(url_for('login'))

    if session.get('role') != 'customer':
        flash('Access denied. Customers only.', 'err')
        return redirect(url_for('dashboard'))

    success, result = getCustomerSubscriptions(
        session['customer_id']
    )

    if not success:
        flash(result, 'err')
        subscriptions = []
    else:
        subscriptions = result

    return render_template(
        'my_subscriptions.html',
        subscriptions=subscriptions
    )


#notifications route

@app.route('/customer/notifications')
def customer_notifications():

    # Check whether the customer is logged in
    if 'customer_id' not in session:
        flash("Please login first.", "err")
        return redirect(url_for('login'))

    # Allow customers only
    if session.get('role') != 'customer':
        flash("Access denied. Customers only.", "err")
        return redirect(url_for('dashboard'))

    # Retrieve notifications for the logged-in customer
    success, result = getCustomerNotifications(
        customer_id=session['customer_id']
    )

    if not success:
        flash(result, "err")
        result = []

    return render_template(
        'notifications.html',
        notifications=result
    )



@app.route('/admin/manage_notifications')
def manage_notifications():

    if 'customer_id' not in session:
        flash("Please login first.", "err")
        return redirect(url_for('login'))

    if session.get('role') != 'admin':
        flash("Access denied. Admins only.", "err")
        return redirect(url_for('dashboard'))

    success, result = getAllNotifications()

    if not success:
        flash(result, "err")
        result = []

    return render_template(
        'manage_notifications.html',
        notifications=result
    )

#marknotifications as read

@app.route('/customer/notifications/read/<int:notification_id>', methods=['POST'])
def mark_notification_read(notification_id):

    if 'customer_id' not in session:
        flash("Please login first.", "err")
        return redirect(url_for('login'))

    if session.get('role') != 'customer':
        flash("Access denied. Customers only.", "err")
        return redirect(url_for('dashboard'))

    success, message = markNotificationAsRead(
        notification_id=notification_id,
        customer_id=session['customer_id']
    )

    if success:
        flash(message, "msg")
    else:
        flash(message, "err")

    return redirect(url_for('customer_notifications'))



@app.route('/logout')
def logout():
    session.clear()
    flash("You have successfully logged out",'msg')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)


