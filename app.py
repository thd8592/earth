from flask import Flask, render_template, request
import pyodbc
import random
import time



app = Flask(__name__)

# Define connection string and connect to the Azure SQL database
server = 'hxt74391.database.windows.net'
database = 'earthquakedb'
connection_string = 'Driver={ODBC Driver 17 for SQL Server};Server=tcp:hxt74391.database.windows.net,1433;Database=earthquakedb;Uid=hxt74391;Pwd={Aimbig2911@};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
cnxn = pyodbc.connect(connection_string)

# Define a function to execute random queries on the SQL table and measure performance


def random_queries(num_queries):
    cursor = cnxn.cursor()
    start_time = time.time()
    for i in range(num_queries):
        rand_id = random.randint(1, 30000)  # Select a random earthquake ID
        cursor.execute(f'SELECT * FROM all_month WHERE id = \'{rand_id}\'')
    end_time = time.time()
    query_time = end_time - start_time
    return query_time

# Define a function to execute restricted queries on the SQL table and measure performance


def restricted_queries(query_type, query_param):
    cursor = cnxn.cursor()
    start_time = time.time()
    if query_type == 'location':
        cursor.execute(
            f'SELECT * FROM all_month WHERE place LIKE \'%{query_param}%\'')
    elif query_type == 'time_range':
        cursor.execute(
            f'SELECT * FROM all_month WHERE time >= \'{query_param[0]}\' AND time <= \'{query_param[1]}\'')
    elif query_type == 'magnitude_range':
        cursor.execute(
            f'SELECT * FROM all_month WHERE mag >= {query_param[0]} AND mag <= {query_param[1]}')
    end_time = time.time()
    query_time = end_time - start_time
    return query_time

# Define the Flask routes for the web application

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/random_queries', methods=['POST'])
def random_queries_route():
    num_queries = int(request.form['num_queries'])
    query_time = random_queries(num_queries)
    return render_template('results.html', query_time=query_time)


@app.route('/restricted_queries', methods=['POST'])
def restricted_queries_route():
    query_type = request.form['query_type']
    if query_type == 'location':
        query_param = request.form['location']
        query_time = restricted_queries(query_type, query_param)
    elif query_type == 'time_range':
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        query_param = [start_time, end_time]
        query_time = restricted_queries(query_type, query_param)
    elif query_type == 'magnitude_range':
        min_mag = request.form['min_mag']
        max_mag = request.form['max_mag']
        query_param = [min_mag, max_mag]
        query_time = restricted_queries(query_type, query_param)
    return render_template('results.html', query_time=query_time)

if __name__ == '__main__':
    app.run()
