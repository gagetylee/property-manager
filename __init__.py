from flask import Flask, request, render_template, url_for, flash, redirect
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
@app.route("/home")
def home():
    conn = sqlite3.connect('database.db')
    conn.row_factory = dict_factory
    c = conn.cursor()

    # Get user, currently set to default id: 1
    userID = 1

    c.execute("SELECT * FROM Landlord WHERE landlordID = ?", (userID, ))
    landlord = c.fetchone();
    # Get monthly income for user

    c.execute("SELECT SUM(monthlyIncome) as total FROM Property WHERE landlordID = ?", (userID,))
    totalIncome = c.fetchone()

    # Get monthly outcome for user
    c.execute("SELECT * FROM MonthlyExpenses")
    totalOutcome = c.fetchone()
    return render_template('home.html', user = landlord, income = totalIncome, outcome = totalOutcome)
    
@app.route("/landlords")
def landlords():
    conn = sqlite3.connect('database.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("SELECT * FROM Landlord")
    landlords = c.fetchall()

    return render_template('landlords.html', data=landlords)
    
@app.route("/properties")
def properties():
    conn = sqlite3.connect('database.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("SELECT * FROM Property")
    properties = c.fetchall()

    return render_template('properties.html', data=properties)


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

