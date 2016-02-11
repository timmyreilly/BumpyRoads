"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from FlaskWebProject import app

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )
    
@app.route('/t')
def trial():
    return render_template('trial.html')

@app.route('/b')
def bingtrial():
    return render_template('bingtrial.html')
    
'''

return list of 
lat long that and severity number 

From 1 - 10 how bumpy was the road? 
On this section? 

return 

'''

