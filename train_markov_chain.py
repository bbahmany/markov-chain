import pandas as pd
import numpy as np
from itertools import tee, islice, chain

def build_ngrams(tokens, n=2):
    """
    Return the sequence of n-grams from the source iterator.
    
    Args: tokens (iterator)---tokens to process
          n (int)-------------gram order

    Returns: (iterator) of n-grams
    """
    ngrams = zip(*(islice(group, idx, None) for idx, group in enumerate(tee(tokens, n))))
    return ngrams

def build_markov_states(ngrams):
    """
    Get distinct markov states and entire markov process from ngrams

    DISCLAIMER:
    Here we have to cast the generator to a list :(. This can be avoided id we implement
        the markov model as a (current_state)->(next_state)->(probability of transition).
        I chose to implement the markov model as a matrix of transition probabilities instead.
        This matrix gives us powerful linear algebra opperations to obtain probabilities
        for n-step ahead future states and unconditional marginal distribution.

    Args:   ngrams (iterator)---ngrams to process
    Returns: state_space (list) sorted state space for the markov process
    """

    state_spaces_grouped = list((str(ngram[:-1]),str(ngram[1:])) for ngram in ngrams)
    state_space = sorted(list(set(chain(*state_spaces_grouped))))

    return {'state_space': state_space, 'state_spaces_grouped':state_spaces_grouped}

def build_transition_matrix(state_space, markov_process, normalize=True):
    """
    Builds the one step ahead transition probability matrix
    - a pandas dataframe with row and col labels corresponding to the markov state space

    Args:   state_space (list)------the distinct states for the markov process
            markov_process (list)---the links between states for the entire text corpus
            normalize (boolean)-----whether or not to normalize dataframe by row

    Returns: (dataframe) the one step ahead transition probability matrix
    """

    P = pd.DataFrame(0, index=state_space, columns=state_space)
    for trans in markov_process:
        P.loc[trans[0], trans[1]] =  P.loc[trans[0], trans[1]] + 1

    if normalize:
        P = P.div(P.sum(axis=1), axis=0)

    return P

def get_transition_matrix(text_file, markov_model_order, normalize=True):
    """
    Reads tokens from file, creates ngrams, and build transition matrix

    Args:   text_file (string)--------input file name
            markov_model_order (int)--order of the markov model (=n-1)
            normalize (boolean)-------whether to normalize dataframe by row
    Returns: (dataframe) the one step ahead tramsition probability matrix
    """

    with open(text_file) as f:
        tokens = chain(*map(lambda line:line.strip().split(' '),f.readlines()))
    
    ngrams = build_ngrams(tokens, markov_model_order+1)
    states = build_markov_states(ngrams)
    P = build_transition_matrix(states['state_space'], 
                                states['state_spaces_grouped'], 
                                normalize)

    return P

