from numpy import random
import random as pyrandom

def _shuffle(items):
    return list(random.permutation(items))
    
class Vignette(object):
    name = ''
    scale = None
    randomize = False

    def __init__(self, name=None, scale=None, questions=None, randomize=False, flip_answers=False):
        self.questions = questions
        if questions is None:
            self.questions = []
        if scale is not None:
            self.scale = scale
        if self.scale is None:
            self.scale = range(1, 8)
        if name is not None:
            self.name = name
        self.randomize = randomize
        self.flip_answers = flip_answers

    def __len__(self):
        return sum([len(question.answers) for question in self.questions])
    
    def get_items(self, randomize=False, seed=None):
        if randomize:
            if seed is not None:
                random.seed(seed)
            return _shuffle(self.questions)
        return self.questions

class Question(object):
    def __init__(self, text, vignette, name=None, answers=[], scale_labels=None, free_form=False):
        self.free_form = free_form
        self.text = text
        self.answers = answers
        self.vignette = vignette
        self.name = name
        if name is None:
            self.name = vignette.name
        self.scale_labels = scale_labels
        if scale_labels is None:
            self.scale_labels = ('not at all', 'to a great extent')
        
        for idx, answer in enumerate(self.answers):
            if 'name' in answer:
                answer['key'] = '%d_%s' % (idx, answer['name'])
            else:
                answer['key'] = idx
    
    def get_items(self, randomize=False, flip_answers=False, seed=None):
        if not len(self.answers):
            return [{
                'text': '',
                'name': self.name,
                'key': ''
            }]
        items = self.answers
        if seed is not None:
            random.seed(seed)
            pyrandom.seed(seed)
        if randomize:
            items = _shuffle(self.answers)     
        if flip_answers:
            for item in items:
                item['flip'] = pyrandom.random() > 0.5
        return items

