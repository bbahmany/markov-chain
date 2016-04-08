import itertools
import requests
from bs4 import BeautifulSoup

# Simple NLP tokenizer

def sanitize_words(words, 
                   punctuation='`~!@#$%^&*()_-+={[}]|\:;"<,>.?/}\t\n',
                   stop_words=['ph']):

    """
    Removes punction from words

    Args:   words (iterator)-------words to remove punctuation from
            punctuation (string)---punctuation to remove
    Returns: (generator) cleaned words
    """
    for word in words:
        if not word.isupper() or 'ISIS' in word:
            yield word.strip(punctuation).lower()

def tokenize_line(line):
    """
    Split a string into a list of words, removing punctuation and stop words.
    """
    return sanitize_words(line.split(' '))

def parse_speeches(urls, skips, text_body_tag='article'):
    for url, skip in zip(urls, skips):
        index = requests.get(url)
        soup = BeautifulSoup(index.text, 'html.parser')
        article = soup.find(text_body_tag)
        for paragraph in article.findAll('p')[skip:]:
            yield sanitize_words((paragraph.text).split(' '))

def write_tokens_to_file(output_file, tokens, line_split=50):
    with open(output_file, 'w') as out:
        for token_count, token in enumerate(tokens):
            if token:
                out.write(token + ' ')
            if token_count is not 0 and token_count % 50 == 0:
                out.write('\n')

#        for line in token_lines: 
#            out.write(' '.join(line) + '\n')
        #out.writelines((' '.join(line)+'\n') for line in token_lines if line is not [])
urls = ['https://www.washingtonpost.com/news/post-politics/wp/2015/06/16/full-text-donald-trump-announces-a-presidential-bid/','https://www.washingtonpost.com/news/post-politics/wp/2016/02/20/transcript-donald-trumps-victory-speech-after-the-south-carolina-gop-primary/']
skips = [1,1]

tokens = itertools.chain(*parse_speeches(urls, skips))
write_tokens_to_file('trump.txt', tokens)
