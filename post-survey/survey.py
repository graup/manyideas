from vignette import Vignette, Question

onlineusage_vignette = [
{
    'text': "How frequently do you use apps on your phone?",
    'name': "freq_app",
    'scale_labels': False,
    'answers': [{
        'text': '',
        'high_low': ('multiple times a day', 'rarely')
    }]
},
{
    'text': "How frequently do you use civic technology apps before? (Examples include: Reporting, public deliberation, petitions, …)",
    'name': "freq_civictech",
    'scale_labels': False,
    'answers': [{
        'text': '',
        'high_low': ('multiple times a day', 'rarely')
    }]
},
{
    'text': "How interested are you in civic participation?",
    'name': "interest_civictech",
    'scale_labels': False,
    'answers': [{
        'text': '',
        'high_low': ('not at all', 'a lot')
    }]
},
{
    'text': "How likely are you to engage personally and voluntarily with a civic application?",
    'name': "likely_engage",
    'scale_labels': False,
    'answers': [{
        'text': '',
        'high_low': ('not at all', 'very likely')
    }]
},

]

onlineusage = Vignette(name='onlineusage', scale=range(1, 8))
onlineusage.questions = [Question(vignette=onlineusage, **q) for q in onlineusage_vignette]


appusage_vignette = [
{
    'text': "What motivated you to join this app?",
    'name': 'reason_join',
    'answers': [
        {'text': "I thought the app’s goal sounded interesting.", 'name': 'interesting'},
        {'text': "I thought using the app could be fun.", 'name': 'fun'},
        {'text': "I thought the app’s goal is important.", 'name': 'important'},
        {'text': "I wanted to see what other people posted.", 'name': 'relatedness'},
        {'text': "I wanted to share my own idea.", 'name': 'sharing'},
        {'text': "I wanted to help this research project.", 'name': 'help'},
        {'text': "I was interested in the offered rewards.", 'name': 'reward'},
        {'text': "I don’t really know why I joined.", 'name': 'amotivation'},
    ]
},
{
    'text': '(한국어 답변 가능) Any other reason?',
    'name': 'reason_join_free',
    'free_form': True
},
{
    'text': "After your first session, did you plan on revisiting the app?",
    'name': "plan_revisit"
},
{
    'text': "The incentive period has finished, but would you be interested in continuing to use this application?",
    'name': "plan_continue"
},
{
    'text': "Without any special events, how often would you check the app?",
    'name': "freq_use",
    'scale_labels': False,
    'answers': [{
        'text': '',
        'high_low': ('never', 'daily')
    }]
},
{
    'text': "If you stopped using the app, why?",
    'name': 'reason_dropout',
    'answers': [
        {'text': "The content wasn’t interesting enough.", 'name': 'interesting'},
        {'text': "I didn’t know what to do.", 'name': 'unclear'},
        {'text': "The rewards offered were too little.", 'name': 'reward'},
        {'text': "It was hard to imagine what my contributions will be useful for.", 'name': 'impact'},
        {'text': "I didn’t have more time.", 'name': 'time'},
        {'text': "I thought I had contributed enough.", 'name': 'enough'},
    ]
},
{
    'text': '(한국어 답변 가능) If you could choose your own reward, what would that be?',
    'name': 'reward_free',
    'free_form': True
},
{
    'text': '(한국어 답변 가능) Apart from a reward, what else would motivate you to continue using this app?',
    'name': 'motivation_free',
    'free_form': True
}
]

appusage = Vignette(name='appusage', scale=range(1, 8))
appusage.questions = [Question(vignette=appusage, **q) for q in appusage_vignette]

attrakdiff_source = [
{
    'text': 'With the help of these word pairs, please enter what you consider the most appropriate description for Many Ideas.',
    'scale_labels': ('very', 'neither', 'very'),
     # Order: p PQ4, B1, p PQ2, p HQ2, p PQ3, HQ3, HQ4, p G1, PQ1, HQ1
    'answers': [
        {
            'text': '',
            'high_low': ('complicated', 'simple'),
            'name': 'pq'
        },
        {
            'text': '',
            'high_low': ('ugly', 'attractive'),
            'name': 'beauty'
        },
        {
            'text': '',
            'high_low': ('impractical', 'practical'),
            'name': 'pq'
        },
        {
            'text': '',
            'high_low': ('tacky', 'stylish'),
            'name': 'hq'
        },
        {
            'text': '',
            'high_low': ('unpredictable', 'predictable'),
            'name': 'pq'
        },
        {
            'text': '',
            'high_low': ('cheap', 'premium'),
            'name': 'hq'
        },
        {
            'text': '',
            'high_low': ('unimaginative', 'creative'),
            'name': 'hq'
        },
        {
            'text': '',
            'high_low': ('bad', 'good'),
            'name': 'goodness'
        },
        {
            'text': '',
            'high_low': ('confusing &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;', 'clearly structured'),
            'name': 'pq'
        },
        {
            'text': '',
            'high_low': ('dull', 'captivating'),
            'name': 'hq'
        },
    ]
},
{
    'text': '(한국어 답변 가능) Do you have any suggestions how we could make this app better?',
    'name': 'suggestion_free',
    'free_form': True
}
]
attrakdiff = Vignette(name='attrakdiff', scale=range(1, 8), randomize=False, flip_answers=True)
attrakdiff.questions = [Question(vignette=attrakdiff, **q) for q in attrakdiff_source]
