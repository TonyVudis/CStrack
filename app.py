from flask import Flask, render_template, redirect, url_for, flash, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from sync import pull_leetify_prof
import os
from dotenv import load_dotenv
import psycopg2

app = Flask(__name__)

load_dotenv()
Db_password = os.getenv('DB_PASSWORD')
Db_user = os.getenv('DB_USER')
Localhost = os.getenv('DB_HOST')
Port = os.getenv('PORT')
Db_name = os.getenv('DB_NAME')
secret_key = os.getenv('Flash_key')
leetify_api_key = os.getenv('Leetify_API_key')

limiter = Limiter(get_remote_address, app=app, default_limits=["200 per hour"])#Limit per hour for API requests

#Connects to DB 
def get_db_connection(Db_password, Db_user, Localhost, Db_name, Port):
    return psycopg2.connect(
        host = Localhost,
        dbname = Db_name,
        user = Db_user,
        password = Db_password,
        port = Port
    )


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/Lineups')
def Lineups():
    return render_template('Lineups.html')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

@app.route('/go')
def go():
    steam_id = request.args.get('steam_id')
    return redirect(url_for('lookup', steam_id=steam_id))

@app.route('/lookup/<steam_id>')#Route for lookup
@limiter.limit("1 per 5 seconds")#Limit per second


#Leetify API - Connection with database
def lookup(steam_id):
    result = pull_leetify_prof(steam_id, leetify_api_key)
    success = result is not None

    conn = get_db_connection(Db_password, Db_user, Localhost, Db_name, Port)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO lookup_log (steam_id, success) VALUES (%s, %s)",
        (steam_id, success)
    )
    conn.commit()
    cur.close()
    conn.close()

    if result is None:
        flash("Couldnt find that Player - check Steam ID and try again")
        return redirect(url_for('home'))

    return render_template('analysis.html', data=result)


if __name__ == '__main__':
    app.run(debug = True)
