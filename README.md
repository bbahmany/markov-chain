# Implementation of a Trainable Markov Chain Model

> No dependecies on pythons NLTK, I wanted to do some of the dirty work myself to get a sense of how the tokenizing functions are implemented internally.

# Summary
Here I train a markov model to generate speech from Donald Trump using two of his speeched scraped from The Washington Post. 

The implementation supports n-grams of any length and any form of text. Simply replace *parse_text()* another scraper and youre good to go. If you already have a text corpus and don't want to scrape, simply place it in a file in the root directory and reference it in *train_markov_chain.py* for parsing. 

# Index
+ *scrape_process_text.py*: scrapes, cleans, tokenizes, and writes text to file
+ *train_markov_chain.py*: reads tokens from file, trains a markov model of the specified order, and builds a state transition probability matix
+ *generate_text.py*: uses the state transition probability matrix to generate structurally similar new text of the specified length
