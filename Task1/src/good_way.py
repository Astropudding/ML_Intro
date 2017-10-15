import pymorphy2
import collections

class Node():
    def __init__(self):
        self.childs = {}
        self.max_freq = 0
        self.best_match = ''

    
    def add_suffix(self, suffix):
        if not suffix:
            self.max_freq += 1
            return
        if suffix[0] not in self.childs:
            self.childs[suffix[0]] = Node()
        self.childs[suffix[0]].add_suffix(suffix[1:])

    
    def fill_matches(self, prefix):
        self.best_match = prefix
        for child in self.childs:
            self.childs[child].fill_matches(prefix + child)
            if self.max_freq < self.childs[child].max_freq:
                self.max_freq = self.childs[child].max_freq
                self.best_match = self.childs[child].best_match


    def find_answer(self, suffix):
        if not suffix:
            return self.best_match
        if suffix[0] not in self.childs:
            return ''
        return self.childs[suffix[0]].find_answer(suffix[1:])

    def find_answer_not_full(self, suffix):
        if not suffix:
            return self.best_match
        if suffix[0] not in self.childs:
            return self.best_match
        return self.childs[suffix[0]].find_answer(suffix[1:])


if __name__ == '__main__':
    PATH_TRAIN = '../input/train.csv'
    PATH_TEST = '../input/test.csv'
    PATH_PRED = 'pred.csv'

    morph = pymorphy2.MorphAnalyzer()

    PLAIN_DICT = {}

    CONNECT_DICT = {}

    TAG_DICT = {}

    DICTS = {
        'ALL' : Node(),
        'NOUN' : Node(),
        'ADJF' : Node(),
        'ADJS' : Node(),
        'COMP' : Node(),
        'VERB' : Node(),
        'INFN' : Node(),
        'PRTF' : Node(),
        'PRTS' : Node(),
        'GRND' : Node(),
        'NUMR' : Node(),
        'ADVB' : Node(),
        'NPRO' : Node(),
        'PRED' : Node(),
        'PREP' : Node(),
        'CONJ' : Node(),
        'PRCL' : Node(),
        'INTJ' : Node()
    }

    with open(PATH_TRAIN, 'r') as file:
        file.readline()
        for line in file:
            Id, Sample, Prediction = line.strip().split(',')
            PLAIN_DICT[Sample] = Prediction
            word1, word2 = Prediction.split(' ')
            if word1 not in CONNECT_DICT:
                CONNECT_DICT[word1] = {}
            if word2 not in CONNECT_DICT[word1]:
                CONNECT_DICT[word1][word2] = 0
            CONNECT_DICT[word1][word2] += 1

            parse1 = morph.parse(word1)[0]
            parse2 = morph.parse(word2)[0]

            key1 = str(parse1.tag)
            key2 = str(parse2.tag)

            '''if key1 not in TAG_DICT:
                TAG_DICT[key1] = {}
            if key2 not in TAG_DICT[key1]:
                TAG_DICT[key1][key2] = 0
            TAG_DICT[key1][key2] += 1

            if parse1.tag.POS:
                DICTS[parse1.tag.POS].add_suffix(parse1.normal_form)
            if parse2.tag.POS:
                DICTS[parse2.tag.POS].add_suffix(parse2.normal_form)'''
            
            DICTS['ALL'].add_suffix(word1)
            DICTS['ALL'].add_suffix(word2)

    for key in DICTS:
        DICTS[key].fill_matches('')

    for key in TAG_DICT:
        TAG_DICT[key] = collections.OrderedDict(sorted(TAG_DICT[key].items(), key=lambda t: t[1]))

    with open(PATH_PRED, 'w') as pred:
        pred.write('Id,Prediction\n')
        with open(PATH_TEST, 'r') as test:
            test.readline()
            for line in test:
                Id, Sample = line.strip().split(',')
                word1, word2 = Sample.split(' ')

                if Sample in PLAIN_DICT:
                    pred.write('%s,%s\n' % (Id, PLAIN_DICT[Sample]))
                    print(word1, word2, 'plain_connect')
                    continue
                
                if word1 in CONNECT_DICT:
                    some_words = {k : CONNECT_DICT[word1][k] for k in CONNECT_DICT[word1] if word2 in k}
                    if some_words:
                        pred.write('%s,%s %s\n' % (Id, word1, max(some_words, key=some_words.get)))
                        print(word1, word2, 'connect')
                        continue
                '''tag = str(morph.parse(word1)[0].tag) 
                if tag in TAG_DICT:
                    value_tag = list(TAG_DICT[tag].keys())[0]
                    answer = DICTS[value_tag[:4]].find_answer(word2)
                    if answer:
                        print(word1, word2, 'bor', answer)
                        tags = value_tag.split(',')
                        for ind, tag in enumerate(tags):
                            if ' ' in tag:
                                tags[ind] = tag.split(' ')[1]
                        form = morph.parse(answer)[0].inflect(set(tags))
                        if form:
                            pred.write('%s,%s %s\n' % (Id, word1, form.word))
                        else:
                            pred.write('%s,%s %s\n' % (Id, word1, answer))
                        continue'''
                answer = DICTS['ALL'].find_answer(word2)
                if answer:
                    pred.write('%s,%s %s\n' % (Id, word1, answer))
                    print(word1, word2, 'all', answer)
                    continue
                pred.write('%s,%s %s\n' % (Id, word1, DICTS['ALL'].find_answer_not_full(word2)))
                print (word1, word2, 'not')

                    
        









