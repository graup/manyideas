from flask import Flask, make_response, render_template, session, url_for, request, redirect
from datetime import datetime
from collections import defaultdict
import os
import uuid
import json

from gcos import gcos
from mvs import mvs
#from experiment import get_ordered_pairs, get_ordering, shuffle_pair_random, get_top_preference, rationale_texts, num_combinations
from survey import onlineusage, appusage, attrakdiff

base_directory = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)

steps = [
    { 'name': 'start', 'count': 0 },
    { 'name': 'gcos', 'count': len(gcos) },
    { 'name': 'mvs', 'count': len(mvs) },
    { 'name': 'onlineusage', 'count': len(onlineusage) },
    { 'name': 'appusage', 'count': len(appusage) },
    { 'name': 'attrakdiff', 'count': len(attrakdiff) }
]
total_count = sum([s['count'] for s in steps])
def count_until(n):
    return sum([s['count'] for s in steps[:n]])

def save_session(session):
    filename = '%s/data/%s.json' % (base_directory, session['user_id'])
    data = dict(session)
    data['user_id'] = str(data['user_id'])
    with open(filename, 'w') as fp:
        json.dump(data, fp)

def survey_step(vignette, request, next_route, template, step=0, extra_context=None):
    context = {
        'total_count': total_count,
        'completed_count': count_until(step),
        'user_id': session['user_id'],
        'user_counter': session['user_counter'],
        'vignette': vignette
    }
    if extra_context:
        context.update(extra_context)

    if request.method == 'POST':
        if vignette:
            session[vignette.name] = request.form
        save_session(session)
        return redirect(url_for(next_route))
    
    return make_response(render_template(template, **context))

@app.before_request
def before_request():
    "Ensure user id and counter in session"
    if not session.get('user_id', None):
        user_id = uuid.uuid1()
        session['user_id'] = user_id
        session['started'] = datetime.now().timestamp()
    if session.get('user_counter', None) is None:
        session['user_counter'] = app.user_counter
        app.user_counter += 1

@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        session['email'] = request.form['email']
        save_session(session)
    return survey_step(vignette=None, request=request, next_route='survey1', step=0, template='start.html')

@app.route('/step-1', methods=['GET', 'POST'])
def survey1():
    return survey_step(vignette=gcos, request=request, next_route='survey2', step=1, template='gcos.html')

@app.route('/step-2', methods=['GET', 'POST'])
def survey2():
    return survey_step(vignette=mvs, request=request, next_route='survey4', step=2, template='mvs.html')

@app.route('/step-3', methods=['GET', 'POST'])
def survey3():
    return survey_step(vignette=onlineusage, request=request, next_route='survey4', step=3, template='onlineusage.html')

@app.route('/step-4', methods=['GET', 'POST'])
def survey4():
    return survey_step(vignette=appusage, request=request, next_route='survey5', step=4, template='appusage.html')

@app.route('/step-5', methods=['GET', 'POST'])
def survey5():
    if request.method == 'POST':
        session['finished'] = datetime.now().timestamp()
    return survey_step(vignette=attrakdiff, request=request, next_route='finish', step=5, template='attrakdiff.html')


@app.route('/finish')
def finish():
    "Finish "
    context = {'total_count': total_count, 'completed_count': total_count}
    context['code'] = str(session['user_id'])[:6].upper()
    return make_response(render_template('finish.html', **context))

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    "Add a cashbusting query param to static urls"
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

app.secret_key = 'sdy2f356rfvesfudnufd8'
app.user_counter = 0

if __name__ == '__main__':
    app.secret_key = 'sdy2f356rfvesfudnufd8'
    app.secret_key = os.urandom(32)  # random key resets sessions every time the app loads
    app.user_counter = 0  # user counter for balanced experiment
    app.config['DEBUG'] = True
    app.run(threaded=True) #, host='0.0.0.0'