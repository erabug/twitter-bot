#!/usr/bin/env python

from sys import argv
import random
import twitter
import os

# Twitter API keys (being pulled from the bash .sh file)
api = twitter.Api(consumer_key=os.environ.get('CONSUMER_KEY'), 
                  consumer_secret=os.environ.get('CONSUMER_SECRET_KEY'), 
                  access_token_key=os.environ.get('ACCESS_KEY_TOKEN'), 
                  access_token_secret=os.environ.get('ACCESS_SECRET_TOKEN'))

def assemble_dictionary(file_objects):
    """takes a list of opened files, cleans them up, and adds them to the dictionary"""
    
    def clean_text(input_file):
        """Takes a file as input and returns a cleaned up list of words in the file"""

        file_text = input_file.read().replace('Mr.', '').replace('Mrs.', '').split()
        stripped_text = []

        for i in range(len(file_text)):
            word = file_text[i].replace('--', ' ').replace('"', '').strip(',*[]/()"_|')
            if word:
                stripped_text.append(word)

        return stripped_text

    def add_input_to_dictionary(clean_text):
        """Adds a list of clean text to the dictionary"""
        for i in range(len(clean_text)-2):
            key = (clean_text[i], clean_text[i+1])
            value = clean_text[i+2]
            # if key exists, append value. if it doesn't, set it to an empty list
            chains.setdefault(key, []).append(value) 

        return None

    chains = {}
    for obj in file_objects:
        add_input_to_dictionary(clean_text(obj))

    return chains

def make_sentence(chain_dict):
    """Takes a dictionary of markov chains and returns a random sentence."""

    lookup = random.choice(filter(
                           lambda x: x[0][-1] not in ".?!;" and x[1][-1] not in ".?!;", 
                           chain_dict.keys()))
    sentence_list = [lookup[0], lookup[1]]

    while lookup in chain_dict:
        next_value = random.choice(chain_dict[lookup])
        sentence_list.append(next_value)
        if next_value[-1] in ".?!":
            break
        lookup = (sentence_list[-2], sentence_list[-1])

    return " ".join(sentence_list)

def make_tweet(chain_dict):
    """Creates a tweet of appropriate tweet length and format."""

    var1 = make_sentence(chain_dict)

    while len(var1) > 140 or len(var1) < 40:
        var1 = make_sentence(chain_dict)

    return var1[0].upper() + var1[1:]

def main(filenames):

    file_objs = [open(i) for i in filenames]
    chain_dict = assemble_dictionary(file_objs)

    system = True
    while system:
        tweet = make_tweet(chain_dict)
        print "\n", tweet
        validate_tweet = raw_input("Would you like to tweet this (Y or N?)? ")
        if validate_tweet.upper() == 'Y':
            api.PostUpdate(tweet)
            print "Success!"
        elif validate_tweet.upper() == 'Q':
            system = False

if __name__ == "__main__":
    main(argv[1:])