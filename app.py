from flask import Flask, render_template, redirect, url_for, flash, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from sync import pull_leetify_prof
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
app.secret_key = os.getenv('Flash_key')

load_dotenv()
leetify_api_key = os.getenv('Leetify_API_key')

limiter = Limiter(get_remote_address, app=app, default_limits=["200 per hour"])

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

@app.route('/go')
def go():
    steam_id = request.args.get('steam_id')
    return redirect(url_for('lookup', steam_id=steam_id))

@app.route('/lookup/<steam_id>')
@limiter.limit("1 per 5 seconds")
def lookup(steam_id):
    result = pull_leetify_prof(steam_id, leetify_api_key)

    if result is None:
        flash("Couldnt find that Player - check Steam ID and try again")
        return redirect(url_for('home'))
    
    return render_template('analysis.html', data = result)


if __name__ == '__main__':
    app.run(debug = True)
