import json
import glob, os, sys
import csv
from operator import itemgetter
from collections import defaultdict

gcos_scales = ['autonomy', 'control', 'impersonal']
mvs_scales = ['intrinsic', 'integrated', 'introjected', 'identified', 'external', 'amotivation', ]
attrakdiff_scales = ['pq', 'hq', 'beauty', 'goodness']
appusage_items = ["freq_use_4_0", "plan_continue_3_", "plan_revisit_2_", "reason_dropout_5_0_interesting", "reason_dropout_5_1_unclear", "reason_dropout_5_2_reward", "reason_dropout_5_3_impact", "reason_dropout_5_4_time", "reason_dropout_5_5_enough", "reason_join_0_0_interesting", "reason_join_0_1_fun", "reason_join_0_2_important", "reason_join_0_3_relatedness", "reason_join_0_4_sharing", "reason_join_0_5_help", "reason_join_0_6_reward", "reason_join_0_7_amotivation", "reason_join_free_", "reward_free_", 'motivation_free_']
header = ['email', 'duration', ] + gcos_scales + mvs_scales + attrakdiff_scales + appusage_items

csvfile = open('data/responses.csv', 'w', newline='')
writer = csv.writer(sys.stdout, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
writer.writerow(header)


def calculate_scales(answers):
    scales = defaultdict(int)
    for key, value in answers.items():
        scale = key.split('_')[-1]
        try:
            scales[scale] += int(value)
        except ValueError:
            pass
    return scales

for filename in glob.glob("data/*.json"):
    with open(filename) as data_file:    
        data = json.load(data_file)
        if len(data.keys()) <= 4:
            # hasn't finished
            #print(data['email'])
            continue
        if data['user_id'] == '4d382294-3fcc-11e8-b1c3-0a507b979d1e':
            continue # fixed this one manually, merged with another one TODO check this gain..
        if data['email'] == 'rkdtjddnd96@kaist.ac.kr':
            data['email'] = 'rkdtjddnd96@naver.com'
        if data['email'] == 'sidlilac@kaist.ac.kr':
            data['email'] = '98krsu98@naver.com'
        if data['email'] == 'natalie.vvvv@gmail.com':
            data['email'] = 'sk8ergirlv@kaist.ac.kr'

        #print(data.get('email', 'MISSING'))
        #print(filename)
        #continue
        
        if 'gcos' in data:
            gcos = calculate_scales(data['gcos'])
        else:
            gcos = {}
        if 'mvs' in data:
            mvs = calculate_scales(data['mvs'])
        else:
            mvs = {}
        if 'attrakdiff' in data:
            attrakdiff = calculate_scales(data['attrakdiff'])
            attrakdiff['pq'] = attrakdiff['pq']/4
            attrakdiff['hq'] = attrakdiff['hq']/4
        else:
            attrakdiff = {}
                
        if 'finished' in data:
            duration = int(data['finished'] - data['started'])
        else:
            duration = None

        writer.writerow([
                data.get('email', 'MISSING'),
                duration,
            ]
            + [gcos.get(scale, None) for scale in gcos_scales]
            + [mvs.get(scale, None) for scale in mvs_scales]
            + [attrakdiff.get(scale, None) for scale in attrakdiff_scales]
            + [data.get('appusage', {}).get(key, '') for key in appusage_items]
        )

