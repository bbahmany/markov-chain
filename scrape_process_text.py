import re
import string
import itertools
import requests
from bs4 import BeautifulSoup

def sanitize_words(words,
                   punctuation="`~!@#$%^&*()_-+={[}]|\:;'<,>.?/}\t\n",
                   stop_words=['ph']):
    """
    Removes punction and stop words from an iterator of words

    Args:   words (iterator)-------words to remove punctuation, stop words from
            punctuation (string)---punctuation to remove
            stop_words (list)------stop words to remove
    
    Returns: (generator) cleaned words
    """
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    for word in words:
        if word not in stop_words and (not word.isupper() or 'ISIS' in word):
            yield regex.sub('', word).lower()

def parse_text(urls, skips):
    """
    Parses donald trump speeches from washington post pages
    ==> this layer is independent from the program flow, re-implement for different text

    Args:   urls (list)---urls to scrape from (ones with similar HTML structure)
            skips (list)--a list of HTML sections to skip corresponding to the urls
                          (ex. it is used here to skip trumps intoduction before his speech)
    
    Returns: (generator) 
    """
    for url, skip in zip(urls, skips):
       
       index = requests.get(url)
       soup = BeautifulSoup(index.text, 'html.parser')
       
        article = soup.find('article')
        for paragraph in article.findAll('p')[skip:]:
            yield sanitize_words((paragraph.text).split(' '))

def write_tokens_to_file(output_file, tokens, line_split=50):
    """
    Writes sanitized tokens to an output file, so we dont have to hit the server everytime

    Args:   output_file (string)---file name to output tokens to
            tokens (iterator)------sanitized tokens
            line_split (int)-------how often to insert a new line in the output file
    
    Returns: (None) writes tokens to output file
    """
    with open(output_file, 'w') as out:
        for token_count, token in enumerate(tokens):
            if token:
                out.write(token + ' ')
            if token_count is not 0 and token_count % 50 == 0:
                out.write('\n')

def process_trump_text():
    # urls where trumps speeches are hosted
    urls = [
    'https://www.washingtonpost.com/news/post-politics/wp/2015/06/16/full-text-donald-trump-announces-a-presidential-bid/',
    'https://www.washingtonpost.com/news/post-politics/wp/2016/02/20/transcript-donald-trumps-victory-speech-after-the-south-carolina-gop-primary/']
    skips = [1,1] # skip the first paragraph on each page (doesnt contain trump's words)
    
     # chain each paragraph's token generator to a single iterator
    tokens = itertools.chain(*parse_speeches(urls, skips))
    
    # write tokens to file
    write_tokens_to_file('trump.txt', tokens) 

if __name__ == '__main__':
    process_trump_text()

