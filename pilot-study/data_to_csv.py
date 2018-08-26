import json
import glob, os
import csv
from experiment import get_top_preference, get_preference_counts, orderings, conditions, get_ranking
from gcos import normalize_score, vignette as gcos_vignette
from mvs import vignette as mvs_vignette
from itertools import combinations
from operator import itemgetter
from collections import defaultdict

csvfile =  open('data/preferences.csv', 'w', newline='')
writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

csvfile2 =  open('data/data.csv', 'w', newline='')
writer2 = csv.writer(csvfile2, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)     

csvfile3 =  open('data/uncoded.csv', 'w', newline='')
writer3 = csv.writer(csvfile3, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL) 

csvfile4 =  open('data/raw_answers.csv', 'w', newline='')
writer4 = csv.writer(csvfile4, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)    
    
#header = ['subject', 'duration', 'test_A', 'test_C', 'test_I', 'item_1', 'item_2', 'result', 'order', 'pair_order']
pairs = list(combinations(conditions, 2))
pairs = ['_'.join(item) for item in sorted(pairs, key=lambda item: (conditions.index(item[1]), conditions.index(item[0])))]
# order should be (12) (13) (23) (14) (24) (34) (15) (25) 

test_keys = ('A','C','I',)
mvs_scales = ['intrinsic', 'integrated', 'identified', 'introjected', 'external', 'amotivation']

header = pairs + ['mvs_check', 'comp_check','gcos_check',] + mvs_scales + ['test', ] + ['test_A', 'test_C', 'test_I',] + ['duration', 'order', 'volunteering_freq']
print(header)
writer.writerow(header)

test_score_categories = []

interest_pairs = ('A_C', 'C_BL', 'A_BL',)

raw_score_header = pairs + ['mvs_check', 'comp_check']
raw_score_header += ['mvs_%d_%s' % (i, mvs_vignette[i]['scale']) for i in range(len(mvs_vignette))]
raw_score_header += ['gcos_%d_%s' % (q, gcos_vignette[q]['code'][a]) for a in range(3) for q in range(len(gcos_vignette)) if gcos_vignette[q]['code']!=None]
#raw_score_header += ['gcos_check_%d' % i for i in range(1, 7)] + ['gcos_check_all']
raw_score_header += ['gcos_check']
raw_score_header += ['test_A', 'test_C', 'test_I',] + mvs_scales + ['preferred', 'preferred_simple', ] + ['pref_%s' % p for p in interest_pairs]
writer4.writerow(raw_score_header)

data_header = ['duration', 'order', 'pair_order'] + \
    mvs_scales + \
    ['mvs_check', 'comp_check', 'gcos_check', 'preferred', 'test_max',] + \
    ['test_A', 'test_C', 'test_I',] + \
    ['testabs_A', 'testabs_C', 'testabs_I',] + \
    ['result_correct', 'result_reason', 'rationale_correct', 'open'] + \
    ['age', 'education', 'sex', 'volunteering_freq']
writer2.writerow(data_header)


def get_first_in(ranks, include):
    if len(ranks) == 0:
        return None
    first = ranks.pop(0)
    if first in include:
        return first
    return get_first_in(ranks, include)


for filename in glob.glob("data/*.json"):
    row = []
    row_raw = []
    with open(filename) as data_file:    
        data = json.load(data_file)
        if not 'comparisons' in data:
            continue
        
        # Comparisons
        comps = []
        for pair in pairs:
            result = data['comparisons'][pair]
            a, b = pair.split('_')
            numeric = 1 if result == a else -1
            comps.append(numeric)
        row += comps

        ranking = get_ranking(data['comparisons'])



        # Order effect
        order = 1 + data['user_counter']%len(orderings)
        pair_orders = [pair['pair_order'] for pair in data.get('comparison_pairs', [])]
        pair_order = 'o' + ''.join(map(str, pair_orders))

        # MVS response
        freq = data['volunteering']['frequency']
        mvs_scale_scores = defaultdict(int)
        for idx, item in enumerate(mvs_vignette):
            mvs_scale_scores[item['scale']] += int(data['volunteering']['mvs_%d' % idx])
        
        mvs_check = int(data['volunteering']['mvs_check']) >= 4
        row.append(int(mvs_check))

        # raw test responses
        for i in range(len(mvs_vignette)):
            row_raw.append(data['volunteering']['mvs_%d' % i])

        for q in range(len(gcos_vignette)):
            if gcos_vignette[q]['code'] is None:
                continue
            for a in range(3):    
                row_raw.append(data['gcos_raw'][str(q)][str(a)])


        # find attention check in comparisons
        check_comp = list(filter(lambda k: k.endswith('check'), data['comparisons'].keys()))[0]
        check_passed = data['comparisons'][check_comp] == data['comparisons'][check_comp.replace('_check', '')]
        row.append(int(check_passed))
        
        # GCOS attention checks
        gcos_checks = list(map(int, [
            data['gcos_raw']['0']['0'] >= 6,
            data['gcos_raw']['0']['1'] >= 6,
            data['gcos_raw']['0']['2'] <= 2,
            data['gcos_raw']['10']['0'] >= 6,
            data['gcos_raw']['10']['1'] <= 2,
            data['gcos_raw']['10']['2'] >= 6,
        ]))
        row.append(int(sum(gcos_checks) >= 5))

        

        row += [mvs_scale_scores[key] for key in mvs_scales]

        if 'finished' in data:
            duration = int(data['finished'] - data['started'])
        else:
            duration = 0
        #row.append(data['user_counter'])
        #row.append(duration)
        test_scores_sorted = sorted(data['test_scores'].items(), key=lambda item: item[1])[::-1]
        test_scores_order = '>'.join([item[0] for item in test_scores_sorted])
        if test_scores_order not in test_score_categories:
            test_score_categories.append(test_scores_order)
        row.append(1+test_score_categories.index(test_scores_order))

        test_scores_values = [data['test_scores'][key] for key in test_keys]
        test_scores_values_norm = [normalize_score(score) for score in test_scores_values]

        demographics = data.get('demographics', {})
        
        vol_freq = min(2, int(data['volunteering']['frequency']))+1
        row = row + test_scores_values + [duration, order, str(vol_freq)]
        print(filename[:16])
        print(row)
        writer.writerow(row)
        survey = data.get('survey', {})
        writer2.writerow([
            duration,
            order,
            pair_order] +
            [mvs_scale_scores[key] for key in mvs_scales] + [
            int(mvs_check), int(check_passed), int(sum(gcos_checks) >= 5),
            ranking[0]] #get_top_preference(data['comparisons'])]
            + [test_scores_sorted[0][0]] + test_scores_values + test_scores_values + [
            survey.get('result_correct'),
            survey.get('result_reason'),
            survey.get('rationale_correct'),
            survey.get('open'),
            demographics.get('age'),
            demographics.get('education'),
            demographics.get('gender'),
            vol_freq
        ])

        prefs = []
        for pair in interest_pairs:
            items = pair.split('_')
            prefs.append( ranking.index(items[0]) < ranking.index(items[1]) )

        #writer3.writerow([survey.get('result_reason'), survey.get('open')])
        writer3.writerow([survey.get('result_reason')])
        writer4.writerow(
            comps +
            [int(mvs_check), int(check_passed)] +
            row_raw + [int(sum(gcos_checks) >= 5)] + test_scores_values + [mvs_scale_scores[key] for key in mvs_scales] +
            
            [ranking[0],
            get_first_in(ranking, ['A', 'C', ]),
            
            ] + prefs)

print(raw_score_header)
print('Labels for test (category column)', test_score_categories)
print('Conditions: ', conditions)
print('Compairsons: ', pairs)