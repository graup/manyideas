from vignette import Vignette, Question
from collections import defaultdict

class GCOS(Vignette):
    name = 'gcos'
    scale = range(1, 8)

    def score_test(self, ratings):
        "ratings is a 2d list of integers: ratings[question_index][answer_index]: int(rating)"
        scores = defaultdict(int)
        for qidx, q in enumerate(self.questions):
            for aidx, a in enumerate(q['answers']):
                scores[a['scale']] += ratings[str(qidx)][str(aidx)]
        return scores

gcos_source = [
{
    "text": "(Attention check) You are taking a personality test. You are likely to:",
    "answers": [
        {
            "text": "Read all the items thoroughly",
            "name": "check_high"
        },
        {
            "text": "Pay attention and think about each answer before choosing a response",
            "name": "check_high"
        },
        {
            "text": "Rate answers randomly because you don't care",
            "name": "check_low"
        },
    ]
},
{
    "text": "You have been offered a new position in a company where you have worked for some time. The first question that is likely to come to mind is:",
    "answers": [
        {
            "text": "What if I can't live up to the new responsibility?",
            "name": "impersonal"
        },
        {
            "text": "Will I make more at this position?",
            "name": "control"
        },
        {
            "text": "I wonder if the new work will be interesting",
            "name": "autonomy"
        },
    ]
},
{
    "text": "You have a school-age daughter. On parents' night the teacher tells you that your daughter is doing poorly and doesn't seem involved in the work. You are likely to:",
    "answers": [
        {
            "text": "Talk it over with your daughter to understand further what the problem is.",
            "name": "autonomy"
        },
        {
            "text": "Scold her and hope she does better.",
            "name": "impersonal"
        },
        {
            "text": "Make sure she does the assignments, because she should be working harder. ",
            "name": "control"
        },
    ]
},
{
    "text": "You had a job interview several weeks ago. In the mail you received a form letter which states that the position has been filled. It is likely that you might think:",
    "answers": [
        {
            "text": "It's not what you know, but who you know.",
            "name": "control"
        },
        {
            "text": "I'm probably not good enough for the job.",
            "name": "impersonal"
        },
        {
            "text": "Somehow they didn't see my qualifications as matching their needs.",
            "name": "autonomy"
        },
    ]
},
{
    "text": "You are a plant supervisor and have been charged with the task of allotting coffee breaks to three workers who cannot all break at once. You would likely handle this by:",
    "answers": [
        {
            "text": "Telling the three workers the situation and having them work with you on the schedule.",
            "name": "autonomy"
        },
        {
            "text": "Simply assigning times that each can break to avoid any problems.",
            "name": "control"
        },
        {
            "text": "Find out from someone in authority what to do or do what was done in the past.",
            "name": "impersonal"
        },
    ]
},
{
    "text": "A close (same-sex) friend of yours has been moody lately, and a couple of times has become very angry with you over \"nothing.\" You might:",
    "answers": [
        {
            "text": "Share your observations with him/her and try to find out what is going on for him/her.",
            "name": "autonomy"
        },
        {
            "text": "Ignore it because there's not much you can do about it anyway.",
            "name": "impersonal"
        },
        {
            "text": "Tell him/her that you're willing to spend time together if and only if he/she makes more effort to control him/herself.",
            "name": "control"
        },
    ]
},
{
    "text": "You have just received the results of a test you took, and you discovered that you did very poorly. Your initial reaction is likely to be:",
    "answers": [
        {
            "text": "\"I can't do anything right,\" and feel sad.",
            "name": "impersonal"
        },
        {
            "text": "\"I wonder how it is I did so poorly,\" and feel disappointed.",
            "name": "autonomy"
        },
        {
            "text": "\"That stupid test doesn't show anything,\" and feel angry.",
            "name": "control"
        },
    ]
},
{
    "text": "You have been invited to a large party where you know very few people. As you look forward to the evening, you would likely expect that:",
    "answers": [
        {
            "text": "You'll try to fit in with whatever is happening in order to have a good time and not look bad.",
            "name": "control"
        },
        {
            "text": "You'll find some people with whom you can relate.",
            "name": "autonomy"
        },
        {
            "text": "You'll probably feel somewhat isolated and unnoticed.",
            "name": "impersonal"
        },
    ]
},
{
    "text": "You are asked to plan a picnic for yourself and your fellow employees. Your style for approaching this project could most likely be characterized as:",
    "answers": [
        {
            "text": "Take charge: that is, you would make most of the major decisions yourself.",
            "name": "control"
        },
        {
            "text": "Follow precedent: you're not really up to the task so you'd do it the way it's been done before.",
            "name": "impersonal"
        },
        {
            "text": "Seek participation: get inputs from others who want to make them before you make the final plans.",
            "name": "autonomy"
        },
    ]
},
{
    "text": "Recently a position opened up at your place of work that could have meant a promotion for you. However, a person you work with was offered the job rather than you. In evaluating the situation, you're likely to think:",
    "answers": [
        {
            "text": "You didn't really expect the job; you frequently get passed over.",
            "name": "impersonal"
        },
        {
            "text": "The other person probably \"did the right things\" politically to get the job.",
            "name": "control"
        },
        {
            "text": "You would probably take a look at factors in your own performance that led you to be passed over.",
            "name": "autonomy"
        },
    ]
},
{
    "text": "For an online study, you have to read and answer a set of questions. You are likely to:",
    "answers": [
        {
            "text": "Read every scenario and think about it thoroughly",
            "name": "check_high"
        },
        {
            "text": "Answer everything as quickly as possible without thinking much",
            "name": "check_low"
        },
        {
            "text": "Think about each answer and rate them honestly",
            "name": "check_high"
        },
    ]
},
{
    "text": "You are embarking on a new career. The most important consideration is likely to be:",
    "answers": [
        {
            "text": "Whether you can do the work without getting in over your head.",
            "name": "impersonal"
        },
        {
            "text": "How interested you are in that kind of work.",
            "name": "autonomy"
        },
        {
            "text": "Whether there are good possibilities for advancement.",
            "name": "control"
        },
    ]
},
{
    "text": "A woman who works for you has generally done an adequate job. However, for the past two weeks her work has not been up to par and she appears to be less actively interested in her work. Your reaction is likely to be:",
    "answers": [
        {
            "text": "Tell her that her work is below what is expected and that she should start working harder.",
            "name": "control"
        },
        {
            "text": "Ask her about the problem and let her know you are available to help work it out.",
            "name": "autonomy"
        },
        {
            "text": "It's hard to know what to do to get her straightened out.",
            "name": "impersonal"
        },
    ]
},
{
    "text": "Your company has promoted you to a position in a city far from your present location. As you think about the move you would probably:",
    "answers": [
        {
            "text": "Feel interested in the new challenge and a little nervous at the same time.",
            "name": "autonomy"
        },
        {
            "text": "Feel excited about the higher status and salary that is involved.",
            "name": "control"
        },
        {
            "text": "Feel stressed and anxious about the upcoming changes.",
            "name": "impersonal"
        },
    ]
}
]

gcos = GCOS()

for q in gcos_source:
    gcos.questions.append(Question(
        text=q['text'],
        answers=q['answers'],
        vignette=gcos,
        scale_labels=('very unlikely', 'moderately likely', 'very likely')
    ))
