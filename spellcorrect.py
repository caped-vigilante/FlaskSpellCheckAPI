import re
from collections import Counter


def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('big.txt').read()))

def P(word, N=sum(WORDS.values())): 
    "Probability of 'word' in the big.txt file."
    return WORDS[word] / N

def correction(word): 
    "Most probable spelling correction for word."
    #return max(candidates(word), key=P)
    word_list = candidates(word)
    to_be_sent = []
    for w in word_list:
        to_be_sent.append((w,P(w)))
    to_be_sent.sort(key = lambda x: x[1], reverse=True) 
    return to_be_sent

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of 'words' that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from 'word'."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from 'word'"
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def fixlistwordandprob(listofwords):
    """
    Given a list of words and their probability of occuring in the big.txt file, compute the final probability
    for the correctness of the word
    """
    final_dict = {}
    for line in listofwords:
        #temp_dict = []
        for key in line:
            total_prob = 0
            temp_list = []
            for suggestion in line[key]:
                total_prob = total_prob + suggestion[1]
            for suggestion in line[key]:
                print(suggestion[0],suggestion[1],total_prob)
                if (total_prob > 0 and suggestion[1]>0):
                    temp_list.append((suggestion[0],(suggestion[1]/total_prob)))
                else:
                    temp_list.append((suggestion[0],0.0))
            final_dict[key]=temp_list
        #final_list.append(temp_dict)
    return final_dict

def multiwordcheck(word):
    word = word.lower()
    corr_word_list = []

    #removes emoji from string
    RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
    word = RE_EMOJI.sub(r'', word)


    if '-' in word:
        #handles '-' in string
        temp_w = word.split('-')
        if WORDS[''.join(temp_w)] > 0:
            return (''.join(temp_w),P(''.join(temp_w)))
        else:
            corr_word_list.append({word:correction(word)})
            corr_word_list = corr_word_list + ([{w:correction(w)} for w in temp_w])
            return fixlistwordandprob(corr_word_list)
    else:
        temp_w = word.split(' ')
        if WORDS[''.join(temp_w)] > 0:
            return (''.join(temp_w),P(''.join(temp_w)))
        else:
            corr_word_list = corr_word_list + ([{w:correction(w)} for w in temp_w])
            return fixlistwordandprob(corr_word_list)
