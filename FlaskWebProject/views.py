"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from FlaskWebProject import app
from tokens import *
from helper import *  





@app.route('/c')
def bingerino():
    data = get_data()
    return render_template(
        'bingtrial.html',
        data=data,
        key=BING_API_KEY)
        



@app.route('/b')
def bingtrial():
    data = [
        {
            "list_a": [37.767111,-122.445811],
            "list_b": [37.792111, -122.403611],
            "color": [200, 200, 0, 100]
        }
    ]
    return render_template(
        'bingtrial.html',
        data=data,
        key=BING_API_KEY)


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

# python_data = {
#     'list_a': [37.767111,-122.445811]
#     'list_b': [37.792111, -122.403611]
# }
 


        
'''

return list of 
lat long that and severity number 

From 1 - 10 how bumpy was the road? 
On this section? 

return 

'''

