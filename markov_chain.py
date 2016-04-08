from itertools import tee, islice, chain

def build_ngrams(itr, n=2):
    """Return the sequence of n-grams from the source iterator."""
    ngrams = zip(*(islice(group, i, None) for i, group in enumerate(tee(itr, n))))
    return ngrams

with open('trump.txt') as f:
    tokens = chain(*map(lambda line:line.strip().split(' '),f.readlines()))
    chains = build_ngrams(tokens, 2)

temp_list = list(chains)
print(len(set(temp_list)), len(temp_list))

#for ngram in chains:
#    print(ngram)
#    key, value = ngram[:-1], ngram[1:]
#    print(key, value)
#    break
