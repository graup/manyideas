"""
Motivation to Volunteer Scale

References for the scale: 

Grano, C., & Lucidi, F. (2005). Motivazioni e determinanti alla base del volontariato nelle persone anziane. Relazioni Solidali, 2, 109-130.
Grano, C., Lucidi, F., Zelli, A., Violani, C. (2008).  Motives and Determinants of Volunteering in Older Adults: An Integrated Model, The International Journal of Aging and Human Development 67 (4) pp. 305-236.
"""

from numpy import random

# Prompt: To what extent correspond each of the following item to your personal motives for engaging in volunteering? "I volunteer""
vignette = [
# Intrinsic motivation
{
    'text': "for the pleasure I feel in finding new ways of help",
    'scale': "intrinsic"
},
{
    'text': "for the pleasure and interest I feel in doing this activity",
    'scale': "intrinsic"
},
{
    'text': "for the pleasure I feel in doing something new",
    'scale': "intrinsic"
},
{
    'text': "for the pleasure I feel when I master the situations I’m dealing with",
    'scale': "intrinsic"
},
# Integrated regulation
{
    'text': "because this activity has become an integral part of my life",
    'scale': 'integrated'
},
{
    'text': "because volunteering has become a part of who I am",
    'scale': 'integrated'
},
{
    'text': "because it is one of the ways I live my life",
    'scale': 'integrated'
},
{
    'text': "because volunteering is a suitable activity for me",
    'scale': 'integrated'
},
# Identified regulation
{
    'text': "because it’s something that is fulfilling  for me as a person",
    'scale': 'identified'
},
{
    'text': "because it’s something that contributes to my personal growth",
    'scale': 'identified'
},
{
    'text': "because it is a wise thing to do",
    'scale': 'identified'
},
{
    'text': "because it’s a good way to contribute",
    'scale': 'identified'
},
# Introjected regulation
{
    'text': "because I would feel very bad if I did not help others",
    'scale': 'introjected'
},
{
    'text': "because I would feel guilty if  I did not volunteer",
    'scale': 'introjected'
},
{
    'text': "because I would regret not doing volunteering",
    'scale': 'introjected'
},
{
    'text': "because I would be ashamed if I  did not volunteer",
    'scale': 'introjected'
},
# External regulation

{
    'text': "because other people will be sorry if I didn’t do it",
    'scale': 'external'
},
{
    'text': "for the recognition I get from others",
    'scale': 'external'
},
{
    'text': "to avoid being criticized",
    'scale': 'external'
},
{
    'text': "because I know others are pleased that I volunteer",
    'scale': 'external'
},
# Amotivation
{
    'text': "I don’t know; Sometimes I have the impression I’m wasting time when I volunteer",
    'scale': 'amotivation'
},
{
    'text': "I don’t know; I can’t see how my efforts are helping others when I volunteer",
    'scale': 'amotivation'
},
{
    'text': "I don’t know; I can’t see how all this helps",
    'scale': 'amotivation'
},
{
    'text': "I don’t know; I can’t see what I’m getting out of it",
    'scale': 'amotivation'
},
# Check
]

attention_check = {
    'text': 'To show that you are concentrated, please answer this question with 5.',
    'scale': '',
    'key': 'check'
}

def get_shuffled_vignette(seed):
    for idx, item in enumerate(vignette):
        item.update(key=idx)
    random.seed(seed)
    return list(random.permutation(vignette)) + [attention_check]
