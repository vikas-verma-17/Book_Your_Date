from flask import Flask, request, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection details
db_config = {
    'host': 'localhost',
    'user': 'root',  # Update this with your MySQL username
    'password': 'verma08',  # Update with your MySQL password
    'database': 'reservations'
}

# Connect to the MySQL database
def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    # Retrieve the success message (if any) from the URL parameters
    success_message = request.args.get('success', None)
    return render_template('index.html', success_message=success_message)  # Pass message to the template

@app.route('/submit', methods=['POST'])
def submit():
    # Get data from the form
    name = request.form['name']
    phone = request.form['phone']
    reservation_from = request.form['reservation-date']
    reservation_to = request.form['reservation-to-date']
    shoot_option = request.form['shoot-options']
    message = request.form['message']
    
    # Save data to the database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """INSERT INTO reservations (name, phone, reservation_from, reservation_to, shoot_option, message) 
               VALUES (%s, %s, %s, %s, %s, %s)"""
    
    cursor.execute(query, (name, phone, reservation_from, reservation_to, shoot_option, message))
    conn.commit()
    cursor.close()
    conn.close()
    
    # Redirect to the index page with a success message
    return redirect(url_for('index', success='Reservation successfully booked!'))

if __name__ == '__main__':
    app.run(debug=True)
