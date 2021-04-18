from flask import Flask, request, render_template, url_for, redirect, session
import sqlite3

conn = sqlite3.connect('database.db')
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route("/")
@app.route("/login", methods=['POST','GET'])
def login():
    if request.method == "POST":
        # Grab "users" and "passwords" from database
        conn = sqlite3.connect('database.db')
        conn.row_factory = dict_factory
        c = conn.cursor()
        c.execute("SELECT landlordID, firstName FROM Landlord")
        user_storage = c.fetchall()

        # Store user-password combinations in python dictionary
        users = {}
        for user in user_storage:
            users[user['firstName']] = str(user['landlordID'])
        print(users) # for debugging

        # Grab form data from login page
        username = request.form['username']
        pwd = request.form['pwd']

        # Check form data for a user-password combination match
        if username in users:
            if users[username] == pwd:
                session['user'] = username
                session['id'] = users[username]
                return home()
            else:
                return render_template('log-in.html', info='invalid password')
        else:
            return render_template('log-in.html', info='invalid user')
    else:
        return render_template('log-in.html')

@app.route("/logout")
def logout():
    session.pop('user', None)
    session.pop('id', None)
    return redirect(url_for('login'))

@app.route("/home")
def home():

    if 'user' in session:
        conn = sqlite3.connect('database.db')
        conn.row_factory = dict_factory
        c = conn.cursor()
        # Get user, currently set to default id: 1
        userID = session['id']

        c.execute("SELECT * FROM Landlord WHERE landlordID = ?", (userID,))
        landlord = c.fetchone();

        # Get monthly income for user
        c.execute("SELECT SUM(monthlyRent) as rentSum FROM Rents JOIN TenantTemp ON (Rents.tenantID == TenantTemp.tenantID) WHERE propertyID IN (SELECT propertyID FROM Property WHERE landlordID = ?)", (userID,))
        totalIncome = c.fetchone()

        # Get monthly expenses for user
        c.execute("SELECT SUM(utilityBill)+SUM(MaintNRepairs)+SUM(propertyTax) as totalExpenses FROM MonthlyExpenses WHERE propertyID IN (SELECT propertyID FROM Property WHERE landlordID = ?)", (userID,))
        totalExpenses = c.fetchone()

        # Get incomes of each property

        c.execute("SELECT propertyID, totalIncome FROM PropertyIncome WHERE propertyID IN (SELECT propertyID FROM Property WHERE landlordID = ?)", (userID, ))
        totalPropertyIncomes = c.fetchall();
        # Get properties
        c.execute("SELECT * FROM Property WHERE landlordID=?", (userID,))
        propertyList = c.fetchall();

        # Get rental agreements for properties owned by user
        c.execute("SELECT * FROM Rents WHERE propertyID IN (SELECT propertyID FROM Property WHERE landlordID = ?)", (userID,))
        renters = c.fetchall();

        # Get tenants of property with propertyID
        # c.execute("SELECT tenantID, name, monthlyRent FROM (SELECT tenantID, companyName as name, monthlyRent FROM Company WHERE tenantID IN (SELECT tenantID FROM Rents WHERE propertyID =?) UNION SELECT tenantID, (firstName||' '||lastName) as name, monthlyRent FROM Individual WHERE tenantID IN ( SELECT tenantID FROM Rents WHERE propertyID =?))", (propertyID,propertyID, ))
        # tenantList = c.fetchall();

        ##### THIS QUERY SATISFIES THE JOIN REQUIREMENT #####
        c.execute("SELECT propertyID, name, monthlyRent FROM Rents JOIN TenantTemp ON (Rents.tenantID == TenantTemp.tenantID) WHERE propertyID IN (SELECT propertyID FROM Property WHERE landlordID = ?)", (userID, ))
        tenantList = c.fetchall();


        return render_template('home.html',
            user = landlord,
            income = totalIncome,
            expenses = totalExpenses,
            propertyIncomes = totalPropertyIncomes,
            properties = propertyList,
            rentalList = renters,
            tenants = tenantList
        )
    else:
        return redirect(url_for('login'))



@app.route("/landlords")
def landlords():
    conn = sqlite3.connect('database.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("SELECT * FROM Landlord")
    landlords = c.fetchall()

    return render_template('landlords.html', data=landlords)


@app.route("/info")
def info():
    if 'user' in session:
        username = session['user']
        conn = sqlite3.connect('database.db')
        conn.row_factory = dict_factory
        c = conn.cursor()
        c.execute("SELECT * FROM Landlord WHERE firstName=='"+ username +"'")
        landlords = c.fetchall()
        return render_template('info.html', data=landlords)
    else:
        return redirect(url_for('login'))

@app.route("/properties", methods=['POST','GET'])
def properties():
    if 'user' in session:
        username = session['user']
        id = session['id']
        conn = sqlite3.connect('database.db')
        conn.row_factory = dict_factory
        c = conn.cursor()

        if request.method == "POST":
            p1 = request.form['province']
            p2 = request.form['street']
            p3 = request.form['postcode']
            p4 = request.form['price']
            p5 = request.form['monthlyIncome']
            p6 = request.form['lotSize']
            p7 = request.form['buildDate']
            p8 = id
            query = 'INSERT INTO Property (province, street, postcode, price, monthlyIncome, lotSize, buildDate, landlordID) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
            c.execute(query, (p1, p2, p3, p4, p5, p6, p7, p8))
            conn.commit()
            # test = {'province': p1, 'street': p2, 'postcode': p3, 'price': p4, 'monthlyIncome': p5, 'lotSize': p6, 'buildDate': p7}

        c.execute("SELECT * FROM Landlord L, Property P WHERE L.landlordID==P.landlordID AND L.landlordID=="+str(id))
        properties = c.fetchall()
        return render_template('properties.html', data=properties)
    else:
        return redirect(url_for('login'))



# @app.route("/register", methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm()

#     if form.validate_on_submit():
#         conn = sqlite3.connect('database.db')
#         c = conn.cursor()

#         #Add the new blog into the 'blogs' table
#         query = 'insert into users VALUES (?, ?, ?)'
#         c.execute(query, (form.username.data, form.email.data, form.password.data)) #Execute the query
#         conn.commit() #Commit the changes

#         flash(f'Account created for {form.username.data}!', 'success')
#         return redirect(url_for('home'))
#     return render_template('register.html', title='Register', form=form)


# @app.route("/blog", methods=['GET', 'POST'])
# def blog():
#     conn = sqlite3.connect('blog.db')

#     #Display all usernames stored in 'users' in the Username field
#     conn.row_factory = lambda cursor, row: row[0]
#     c = conn.cursor()
#     c.execute("SELECT username FROM users")
#     results = c.fetchall()
#     users = [(results.index(item), item) for item in results]

#     form = BlogForm()
#     form.username.choices = users

#     if form.validate_on_submit():
#         choices = form.username.choices
#         user =  (choices[form.username.data][1])
#         title = form.title.data
#         content = form.content.data

#         #Add the new blog into the 'blogs' table in the database
#         query = 'insert into blogs (username, title, content) VALUES (?, ?, ?)' #Build the query
#         c.execute(query, (user, title, content)) #Execute the query
#         conn.commit() #Commit the changes

#         flash(f'Blog created for {user}!', 'success')
#         return redirect(url_for('home'))
#     return render_template('blog.html', title='Blog', form=form)

if __name__ == '__main__':
    app.run(debug=True)
