from flask import Flask, make_response, render_template, session, url_for, request, redirect
from datetime import datetime
from collections import defaultdict
import os
import uuid
import json

from gcos import vignette, score_test
from mvs import get_shuffled_vignette, vignette as mvs_vignette
from experiment import get_ordered_pairs, get_ordering, shuffle_pair_random, get_top_preference, rationale_texts, num_combinations

base_directory = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)

steps = [
    { 'name': 'start', 'count': 3 },
    { 'name': 'gcos', 'count': len(vignette)*3 },
    { 'name': 'mvs', 'count': len(mvs_vignette)+1 },
    { 'name': 'comparison', 'count': num_combinations },
    { 'name': 'post', 'count': 2 },
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
    "Welcome page"
    context = {'total_count': total_count, 'completed_count': 0}

    if request.method == 'POST':
        session['demographics'] = request.form
        save_session(session)
        return redirect(url_for('gcos'))

    context['user_id'] = session['user_id']
    context['user_counter'] = session['user_counter']
    return make_response(render_template('start.html', **context))

@app.route('/pre-test', methods=['GET', 'POST'])
def gcos():
    "GCOS survey"
    if request.method == 'POST':
        ratings = defaultdict(lambda: defaultdict(dict))
        for key in request.form:
            _, question, answer = key.split('_')
            ratings[question][answer] = int(request.form[key])
        session['test_scores'] = score_test(ratings)
        session['gcos_raw'] = ratings
        save_session(session)
        return redirect(url_for('mvs'))

    context = {'total_count': total_count, 'completed_count': count_until(1)}
    context['vignette'] = vignette
    return make_response(render_template('gcos.html', **context))

@app.route('/pre-test-2', methods=['GET', 'POST'])
def mvs():
    "Volunteering survey"
    if request.method == 'POST':
        session['volunteering'] = request.form
        save_session(session)
        return redirect(url_for('comparison'))

    context = {'total_count': total_count, 'completed_count': count_until(2)}
    context['vignette'] = get_shuffled_vignette(session['user_counter'])
    return make_response(render_template('mvs.html', **context))

@app.route('/comparison', methods=['GET', 'POST'])
def comparison():
    "Comparison"
    context = {'total_count': total_count, 'completed_count': count_until(3)}
    if request.method == 'POST':
        session['comparisons'] = request.form
        save_session(session)
        return redirect(url_for('survey'))

    comparison_pair_items = get_ordered_pairs(get_ordering(session['user_counter']))

    comparison_pairs = []
    for idx, pair_items in enumerate(comparison_pair_items):
        pair = {'key': '_'.join(pair_items), 'order': idx}
        pair['items'], pair['pair_order'] = shuffle_pair_random(pair_items)
        comparison_pairs.append(pair)

    # repeat one pair for checking consistency/attention
    bogus_item = dict(comparison_pairs[len(comparison_pairs)//2])  # take one from the middle
    bogus_item['key'] += '_check'
    bogus_item['items'] = bogus_item['items'][::-1]  # reverse to catch people who always select the first item
    comparison_pairs.append(bogus_item)
    
    context['comparison_pairs'] = comparison_pairs
    session['comparison_pairs'] = comparison_pairs

    return make_response(render_template('comparison.html', **context))


@app.route('/survey', methods=['GET', 'POST'])
def survey():
    "Post-test survey"
    context = {'total_count': total_count, 'completed_count': count_until(4)}

    if request.method == 'POST':
        session['survey'] = request.form
        session['finished'] = datetime.now().timestamp()
        save_session(session)
        return redirect(url_for('finish'))

    if 'comparisons' in session:
        context['winner'] = get_top_preference(session['comparisons'])
        #if context['winner']:
        #    context['rationale_text'] = rationale_texts[context['winner']]

    return make_response(render_template('survey.html', **context))


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

app.secret_key = os.urandom(32)
app.user_counter = 0

if __name__ == '__main__':
    app.secret_key = 'sdy2f356rfvesfudnufd8'
    #app.secret_key = os.urandom(32)  # random key resets sessions every time the app loads
    app.user_counter = 0  # user counter for balanced experiment
    app.config['DEBUG'] = True
    app.run(threaded=True) #, host='0.0.0.0'