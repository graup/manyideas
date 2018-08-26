"""
Motivation to Volunteer Scale

References for the scale: 

Grano, C., & Lucidi, F. (2005). Motivazioni e determinanti alla base del volontariato nelle persone anziane. Relazioni Solidali, 2, 109-130.
Grano, C., Lucidi, F., Zelli, A., Violani, C. (2008).  Motives and Determinants of Volunteering in Older Adults: An Integrated Model, The International Journal of Aging and Human Development 67 (4) pp. 305-236.
"""

from vignette import Vignette, Question
from collections import defaultdict

class MVS(Vignette):
    name = 'mvs'
    scale = range(1, 6)


# Prompt: To what extent correspond each of the following item to your personal motives for engaging in volunteering? "I volunteer""
mvs_source = [
# Intrinsic motivation
{
    'text': "for the pleasure I feel in finding new ways of help",
    'name': "intrinsic"
},
{
    'text': "for the pleasure and interest I feel in doing this activity",
    'name': "intrinsic"
},
{
    'text': "for the pleasure I feel in doing something new",
    'name': "intrinsic"
},
{
    'text': "for the pleasure I feel when I master the situations I’m dealing with",
    'name': "intrinsic"
},
# Integrated regulation
{
    'text': "because this activity has become an integral part of my life",
    'name': 'integrated'
},
{
    'text': "because volunteering has become a part of who I am",
    'name': 'integrated'
},
{
    'text': "because it is one of the ways I live my life",
    'name': 'integrated'
},
{
    'text': "because volunteering is a suitable activity for me",
    'name': 'integrated'
},
# Identified regulation
{
    'text': "because it’s something that is fulfilling  for me as a person",
    'name': 'identified'
},
{
    'text': "because it’s something that contributes to my personal growth",
    'name': 'identified'
},
{
    'text': "because it is a wise thing to do",
    'name': 'identified'
},
{
    'text': "because it’s a good way to contribute",
    'name': 'identified'
},
# Introjected regulation
{
    'text': "because I would feel very bad if I did not help others",
    'name': 'introjected'
},
{
    'text': "because I would feel guilty if  I did not volunteer",
    'name': 'introjected'
},
{
    'text': "because I would regret not doing volunteering",
    'name': 'introjected'
},
{
    'text': "because I would be ashamed if I  did not volunteer",
    'name': 'introjected'
},
# External regulation

{
    'text': "because other people will be sorry if I didn’t do it",
    'name': 'external'
},
{
    'text': "for the recognition I get from others",
    'name': 'external'
},
{
    'text': "to avoid being criticized",
    'name': 'external'
},
{
    'text': "because I know others are pleased that I volunteer",
    'name': 'external'
},
# Amotivation
{
    'text': "I don’t know; Sometimes I have the impression I’m wasting time when I volunteer",
    'name': 'amotivation'
},
{
    'text': "I don’t know; I can’t see how my efforts are helping others when I volunteer",
    'name': 'amotivation'
},
{
    'text': "I don’t know; I can’t see how all this helps",
    'name': 'amotivation'
},
{
    'text': "I don’t know; I can’t see what I’m getting out of it",
    'name': 'amotivation'
},
# Check
{
    'text': 'To show that you are concentrated, please answer this question with 5.',
    'name': 'check'
}
]

mvs = MVS(randomize=True)

mvs.questions = [
    Question(
        text="Please indicate to what extent each of the following items correspond to your personal motives for engaging in volunteering. I volunteer...",
        answers=mvs_source,
        vignette=mvs
    )
]


