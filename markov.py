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

# print api.VerifyCredentials()


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
            chains.setdefault(key, []).append(value)

    chains = {}
    for obj in file_objects:
        stripped = clean_text(obj)
        add_input_to_dictionary(stripped)
    return chains



def make_text(chain_dict):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""
    # filter_by_caps = filter(lambda x: x[0][0].isupper(), chain_dict.keys())
    # lookup = random.choice(filter(lambda x: x[0][-1] != ".", filter_by_caps))

    lookup = random.choice(filter(lambda x: x[0][-1] not in (".?!") and x[1][-1] not in ("."), chain_dict.keys()))

    # lookup = random.choice(filter(lambda x: x[0][0].isupper(), chain_dict.keys()))
    sentence_list = [lookup[0], lookup[1]]

    while lookup in chain_dict:
        next_value = random.choice(chain_dict[lookup])
        sentence_list.append(next_value)
        if next_value[-1] in ".?!":
            break
        lookup = (sentence_list[-2], sentence_list[-1])

    return " ".join(sentence_list)

def main(filenames):
    file_objs = [open(i) for i in filenames]

    chain_dict = assemble_dictionary(file_objs)

    # two sentences
    # var1 = make_text(chain_dict)
    # var2 = make_text(chain_dict)
    # while len(var1 + var2) > 140:
    #     var1 = make_text(chain_dict)
    #     var2 = make_text(chain_dict)
    # tweet = var1[0].upper() + var1[1:] + " " + var2[0].upper() + var2[1:]

    # one sentence
    var1 = make_text(chain_dict)
    while len(var1) > 140:
        var1 = make_text(chain_dict)
    tweet = var1[0].upper() + var1[1:]

    # normal tweet prompt
    print "\n", tweet
    # validate_tweet = raw_input("Would you like to tweet this quote? Y or N? ")
    # if validate_tweet.upper() == 'Y':
    #     api.PostUpdate(tweet)
    #     print "Success!"


    

if __name__ == "__main__":
    # script, filename = argv
    # main(filename)
    main(argv[1:])