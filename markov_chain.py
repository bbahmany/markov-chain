import pandas as pd
import numpy as np
from itertools import tee, islice, chain

def build_ngrams(itr, n=2):
    """Return the sequence of n-grams from the source iterator."""
    ngrams = zip(*(islice(group, i, None) for i, group in enumerate(tee(itr, n))))
    return ngrams


with open('trump.txt') as f:
    tokens = chain(*map(lambda line:line.strip().split(' '),f.readlines()))
    chains = build_ngrams(tokens, 3)


# have to make two passes here to build it in matrix form :(
# the matrix has nice properties, so i will use it here instead of dict->dict->prob
def init_transition_matrix(ngrams):
    state_spaces_grouped = ((str(ngram[:-1]),str(ngram[1:])) for ngram in ngrams)
    state_spaces_ungrouped = chain(*((str(ngram[:-1]),str(ngram[1:])) for ngram in ngrams))
    state_lookup = sorted(list(set(state_spaces_ungrouped)))
    P = pd.DataFrame(0, index=state_lookup, columns=state_lookup)
    return { 'markov_process': state_spaces_grouped,
             'state_lookup': state_lookup,
             'P': P }

def populate_transition_matrix(P, markov_process, normalize=True):
    for trans in markov_process:
        P.loc[trans[0], trans[1]] =  P.loc[trans[0], trans[1]] + 1

    if normalize:
        P = P.div(P.sum(axis=1), axis=0)

    return P

result = init_transition_matrix(list(chains))
P = populate_transition_matrix(result['P'], result['markov_process'])
print(P.sum(axis=1))
