import numpy as np
from markov_chain import get_transition_matrix

def simulate_markov_states(P, num_states):
    """
    Simulates markov states, with respect to transition probabilities

    Args:   P (dataframe)------the one step ahead transition matrix
            num_states (int)---number of states to simulate
    Returns: (generator) the simulates states
    """

    state_space = P.columns.values.tolist()
    cur_state = np.random.choice(state_space)
    yield cur_state

    for index in range(num_words-1):
        possible_next_states = P.loc[cur_state,:][P.loc[cur_state,:]>0]

        next_state = np.random.choice(a=possible_next_states.index.values, 
                                      p=possible_next_states.values)
        cur_state = next_state
        yield cur_state

def get_text(state_chain):
    """
    Takes a chain of markov states and turns them into a readable generator of words

    Args:   state_chain (iterator)----simulated states of the markov process
    Returns: (generator) simulated text
    """

    initial_state = next(state_chain)
    yield from eval(initial_state)

    for state in state_chain:
        yield eval(state)[-1]

P = get_transition_matrix('trump.txt', 3)
chain = simulate_markov_states(P, 100)
print(list(get_text(chain)))
