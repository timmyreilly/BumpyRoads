"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, Response, session, redirect, url_for  
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from FlaskWebProject import app
from helper import *  
import os

token = os.getenv('BING_MAP_TOKEN')

if token == None:
    from tokens import *  
    token = BING_API_KEY
    
class RouteForm(Form):
    route_name = StringField('What route?', validators=[Required()])
    submit = SubmitField('Submit')

@app.route('/f', methods=['GET', 'POST'])
def bingerrino():
    data = get_data_from_table(session['route_name'])
    jdata = json.dumps(data)
    form = RouteForm()
    if form.validate_on_submit():
        route = session.get('route')
        session['route_name'] = form.route_name.data
        return redirect(url_for('bingerrino'))
    return render_template(
        'bingerino.html',
        data = jdata,
        key=token,
        form=form,
        route=session.get('route_name')
    )
    

@app.route('/e')
def bingerr():
    data = get_data_from_table(session['route_name'])
    jdata = json.dumps(data)
    return render_template(
        'binged.html',
        data = jdata,
        key=token
    )   
    
@app.route('/d')
def binged():   
    data = get_json_list()
    jdata = json.dumps(data)
    return render_template(
        'binged.html',
        data=jdata,
        key=token 
    )

@app.route('/e')
def bingerine():
    data = get_lat_long_dict(6)
    # print data 
    return render_template(
        'bingerino.html',
        data=data,
        key=token)

@app.route('/c')
def bingerino():
    data = get_data()
    print data 
    return render_template(
        'bingerino.html',
        data=data,
        key=token)
        

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
        key=token)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = RouteForm()
    if form.validate_on_submit():
        route = session.get('route')
        session['route_name'] = form.route_name.data
        return redirect(url_for('bingerrino'))
    return render_template('index.html', form=form, route=session.get('route_name'))

    
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

