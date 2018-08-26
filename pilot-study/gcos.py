vignette = [
{
    "prompt": "You are taking a personality test. You are likely to:",
    "answers": [
        "Read all the items thoroughly",
        "Pay attention and think about each answer before choosing a response",
        "Rate answers randomly because you don't care",
    ],
    "code": None
},
{
    "prompt": "You have been offered a new position in a company where you have worked for some time. The first question that is likely to come to mind is:",
    "answers": [
        "What if I can't live up to the new responsibility?",
        "Will I make more at this position?",
        "I wonder if the new work will be interesting",
    ],
    "code": "ICA"
},
{
    "prompt": "You have a school-age daughter. On parents' night the teacher tells you that your daughter is doing poorly and doesn't seem involved in the work. You are likely to:",
    "answers": [
        "Talk it over with your daughter to understand further what the problem is.",
        "Scold her and hope she does better.",
        "Make sure she does the assignments, because she should be working harder. ",
    ],
    "code": "AIC"
},
{
    "prompt": "You had a job interview several weeks ago. In the mail you received a form letter which states that the position has been filled. It is likely that you might think:",
    "answers": [
        "It's not what you know, but who you know.",
        "I'm probably not good enough for the job.",
        "Somehow they didn't see my qualifications as matching their needs.",
    ],
    "code": "CIA"
},
{
    "prompt": "You are a plant supervisor and have been charged with the task of allotting coffee breaks to three workers who cannot all break at once. You would likely handle this by:",
    "answers": [
        "Telling the three workers the situation and having them work with you on the schedule.",
        "Simply assigning times that each can break to avoid any problems.",
        "Find out from someone in authority what to do or do what was done in the past.",
    ],
    "code": "ACI"
},
{
    "prompt": "A close (same-sex) friend of yours has been moody lately, and a couple of times has become very angry with you over \"nothing.\" You might:",
    "answers": [
        "Share your observations with him/her and try to find out what is going on for him/her.",
        "Ignore it because there's not much you can do about it anyway.",
        "Tell him/her that you're willing to spend time together if and only if he/she makes more effort to control him/herself.",
    ],
    "code": "AIC"
},
{
    "prompt": "You have just received the results of a test you took, and you discovered that you did very poorly. Your initial reaction is likely to be:",
    "answers": [
        "\"I can't do anything right,\" and feel sad.",
        "\"I wonder how it is I did so poorly,\" and feel disappointed.",
        "\"That stupid test doesn't show anything,\" and feel angry.",
    ],
    "code": "IAC"
},
{
    "prompt": "You have been invited to a large party where you know very few people. As you look forward to the evening, you would likely expect that:",
    "answers": [
        "You'll try to fit in with whatever is happening in order to have a good time and not look bad.",
        "You'll find some people with whom you can relate.",
        "You'll probably feel somewhat isolated and unnoticed.",
    ],
    "code": "CAI"
},
{
    "prompt": "You are asked to plan a picnic for yourself and your fellow employees. Your style for approaching this project could most likely be characterized as:",
    "answers": [
        "Take charge: that is, you would make most of the major decisions yourself.",
        "Follow precedent: you're not really up to the task so you'd do it the way it's been done before.",
        "Seek participation: get inputs from others who want to make them before you make the final plans.",
    ],
    "code": "CIA"
},
{
    "prompt": "Recently a position opened up at your place of work that could have meant a promotion for you. However, a person you work with was offered the job rather than you. In evaluating the situation, you're likely to think:",
    "answers": [
        "You didn't really expect the job; you frequently get passed over.",
        "The other person probably \"did the right things\" politically to get the job.",
        "You would probably take a look at factors in your own performance that led you to be passed over.",
    ],
    "code": "ICA"
},
{
    "prompt": "For an online study, you have to read and answer a set of questions. You are likely to:",
    "answers": [
        "Read every scenario and think about it thoroughly",
        "Answer everything as quickly as possible without thinking much",
        "Think about each answer and rate them honestly",
    ],
    "code": None
},
{
    "prompt": "You are embarking on a new career. The most important consideration is likely to be:",
    "answers": [
        "Whether you can do the work without getting in over your head.",
        "How interested you are in that kind of work.",
        "Whether there are good possibilities for advancement.",
    ],
    "code": "IAC"
},
{
    "prompt": "A woman who works for you has generally done an adequate job. However, for the past two weeks her work has not been up to par and she appears to be less actively interested in her work. Your reaction is likely to be:",
    "answers": [
        "Tell her that her work is below what is expected and that she should start working harder.",
        "Ask her about the problem and let her know you are available to help work it out.",
        "It's hard to know what to do to get her straightened out.",
    ],
    "code": "CAI"
},
{
    "prompt": "Your company has promoted you to a position in a city far from your present location. As you think about the move you would probably:",
    "answers": [
        "Feel interested in the new challenge and a little nervous at the same time.",
        "Feel excited about the higher status and salary that is involved.",
        "Feel stressed and anxious about the upcoming changes.",
    ],
    "code": "ACI"
}
]

def normalize_score(score):
    return (score - 12)/(12*7)

def score_test(ratings):
    "ratings is a 2d list of integers: ratings[question_index][answer_index]: int(rating)"
    scores = {
        "A": 0,
        "C": 0,
        "I": 0
    }
    for qidx, q in enumerate(vignette):
        if not q['code']:
            continue
        code = list(q['code'])
        for aidx, a in enumerate(q['answers']):
            scores[code[aidx]] += ratings[str(qidx)][str(aidx)]
    return scores