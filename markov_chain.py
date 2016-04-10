import pandas as pd
import numpy as np
from itertools import tee, islice, chain

def build_ngrams(itr, n=2):
    """Return the sequence of n-grams from the source iterator."""
    ngrams = zip(*(islice(group, i, None) for i, group in enumerate(tee(itr, n))))
    return ngrams

# have to make two passes here to build it in matrix form :(
# the matrix has nice properties, so i will use it here instead of dict->dict->prob
def build_markov_states(ngrams):

    state_spaces_grouped = list((str(ngram[:-1]),str(ngram[1:])) for ngram in ngrams)
    state_space = sorted(list(set(chain(*state_spaces_grouped))))
    return {'state_space': state_space, 'state_spaces_grouped':state_spaces_grouped}

def build_transition_matrix(state_space, markov_process, normalize=True):

    P = pd.DataFrame(0, index=state_space, columns=state_space)
    for trans in markov_process:
        P.loc[trans[0], trans[1]] =  P.loc[trans[0], trans[1]] + 1

    if normalize:
        P = P.div(P.sum(axis=1), axis=0)

    return P

def get_transition_matrix(text_file, markov_model_order, normalize=True):
    
    with open(text_file) as f:
        tokens = chain(*map(lambda line:line.strip().split(' '),f.readlines()))
    
    ngrams = build_ngrams(tokens, markov_model_order+1)
    states = build_markov_states(ngrams)
    P = build_transition_matrix(states['state_space'], 
                                states['state_spaces_grouped'], 
                                normalize)

    return P

