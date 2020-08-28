from __future__ import print_function, unicode_literals
import random
import logging
import time

from textblob import TextBlob
from Arya_memory import *

#Global Personality
personality = 50
i = 0

# Load sentiment analysis into ai memory
with open("positive.txt",'r') as f:
    data = f.read().replace(",",'')
    pos = [s.strip() for s in data.split(' ') if s]

with open("negative.txt", 'r') as g:
    data2 = g.read().replace(",", '')
    neg = [t.strip() for t in data2.split(' ') if t]

# User logs
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def check_for_greeting(sentence):
    #if we are given a greeeting, respond with a greetin (according to current personality)
    
    greeting = any(substring in sentence.lower() for substring in GREETING_KEYWORDS)

    global personality

    if greeting == True and personality >= 45 and personality <= 55:
        return random.choice(GREETING_RESPONSES) #neutral

    if greeting == True and personality > 55:    #positive
        return random.choice(POS_GREETING_RESPONSE) + " " + random.choice(POS_END)

    if greeting == True and personality < 45:    #negative
        return random.choice(NEG_GREETING_RESPONSE) + " " + random.choice(NEG_END2)



# Response to user telling us something about ourselves
COMMENTS_ABOUT_SELF = [
    "You're just jealous",
    "I worked really hard on that",
    "My Klout score is {}".format(random.randint(100, 500)),
]

class UnacceptableUtteranceException(Exception):
    #response will trigger blacklist
    pass

def starts_with_vowel(word):
    #if we should start with a or an based on vowel of word
    return True if word[0] in 'aeiou' else False

### MAIN LOOP ###
def broback(sentence):
    #gets setence and selects response
    resp = respond(sentence)
    logger.info("Broback: respond to %s", sentence)
    return resp

def find_pronoun(sent): 
    # From sentence find preferred pronoun -> returns none in none found
    pronoun = None

    for word, part_of_speech in sent.pos_tags:
        # Disambiguate pronouns
        if part_of_speech == 'PRP' and word.lower() == 'you': 
            pronoun = 'I'
        elif part_of_speech == 'PRP' and word == 'I':
            #If the user mentioned themselves, then they will definitely be the pronoun###
            pronoun = 'You' 
    return pronoun

def find_verb(sent):
    # From sentence pick candidate verb
    verb = None
    pos = None
    for word, part_of_speech in sent.pos_tags:
        if part_of_speech.startswith('VB'): # This is a verb
            verb = word
            pos = part_of_speech
            break
    return verb, pos


def find_noun(sent):
    # From sentence pick candidate noun
    noun = None

    if not noun:
        for w, p in sent.pos_tags:
            if p == 'NN':  # This is a noun
                noun = w
                break
    if noun:
        logger.info("Found noun: %s", noun)

    return noun

def find_adjective(sent):
    # From sentence pick candidate adjective
    adj = None
    
    for w, p in sent.pos_tags:
        if p == 'JJ':  # This is an adjective
            adj = w
            break
    return adj



# start:example-construct-response.py
def construct_response(pronoun, noun, verb, adjective):
    #special case has not been matched -> construct our own setence with user input
    resp = []

    # respond in present tense
    if verb:
        verb_word = verb[0]
        if verb_word in ('be', 'am', 'is', "'m"): 
            if pronoun.lower() == 'you' and personality >= 55:
                resp.append("Thats great to hear")
                resp.append(noun)
                resp.append("is awesome")
            if pronoun.lower() == 'you' and personality <= 45:
                resp.append("You arent really")
                resp.append(adjective)
                resp.append("at")
                resp.append(noun)
            if pronoun.lower() == 'you' and personality == 50:
                resp.append("Oh") ##Oh, sweet, etc
        if verb_word in ('went'): ##LIMITATION -> I went to dinner case
            if pronoun.lower() == 'you':
                resp.append("No way")
    if noun:
        pronoun = "an" if starts_with_vowel(noun) else "a" ## LIMITATION -> Replace

    if personality >= 55:
        resp.append(random.choice(POS_END)) ##friend buddy, pal, etc
    if personality <= 45:
        resp.append(random.choice(NEG_END)) #you idiot, you imbecile, who cares punk
    if personality == 50:
        print (noun)
        resp.append("Thats awesome")
        resp.append(noun)
        resp.append("is cool!")
    
    return " ".join(resp)

def check_for_comment_about_bot(pronoun, noun, adjective):
    # user input about bot, based on input and personality construct response
    resp = None
    if pronoun == 'I' and (noun or adjective):
        if noun:
            if personality == 45 or personality == 55 or personality == 50:
                resp = random.choice(SELF_VERBS_WITH_NOUN_LOWER).format(**{'noun': noun})
            if personality > 55:
                resp = random.choice(POS_SELF_VERBS_WITH_NOUN_LOWER).format(**{'noun': noun})
            if personality < 45:
                resp = random.choice(NEG_SELF_VERBS_WITH_NOUN_LOWER).format(**{'noun': noun})
        if noun == None:
            if personality == 45 or personality == 55 or personality == 50:
                resp = random.choice(SELF_VERBS_WITH_ADJECTIVE).format(**{'adjective': adjective})
            if personality > 55:
                resp = random.choice(POS_SELF_VERBS_WITH_ADJECTIVE).format(**{'adjective': adjective})
            if personality < 45:
                resp = random.choice(NEG_SELF_VERBS_WITH_ADJECTIVE).format(**{'adjective': adjective})
    return resp


# Limitation -> capitalization matters -> fix capitalization errors
def preprocess_text(sentence):
    # parsing edge cases -> i not pronoun I is
    cleaned = []
    words = sentence.split(' ')
    for w in words:
        if w == 'i':
            w = 'I'
        if w == "i'm":
            w = "I'm"
        if w == 'im' or w == 'Im':
            w = "I'm"
        if w == 'your':
            w = 'you are'
        cleaned.append(w)

    return ' '.join(cleaned)

def respond(sentence):
    # take user input sentence and find candidate terms to construct ideal response
    cleaned = preprocess_text(sentence)
    parsed = TextBlob(cleaned)

    # Loop through sentences, if more than one. 
    # extract most relevant text (even across multiple sentences)
    pronoun, noun, adjective, verb = find_candidate_parts_of_speech(parsed)

    # if somethings said about bot respond appropriately
    resp = check_for_comment_about_bot(pronoun, noun, adjective)

    # If user just greeted the bot, we'll use a return greeting
    if not resp:
        resp = check_for_greeting(parsed)

    if not resp:
        # if here -> try to construct new response
        if not pronoun:
            resp = random.choice(NONE_RESPONSES)
        elif pronoun == 'I' and not verb:
            resp = random.choice(COMMENTS_ABOUT_SELF)
        else:
            resp = construct_response(pronoun, noun, verb, adjective)

    # resp still not defined -> random response
    if not resp:
        resp = random.choice(NONE_RESPONSES)

    logger.info("Returning phrase '%s'", resp)
   
    return resp

def find_candidate_parts_of_speech(parsed):
    #with parsed input find candidate words
    pronoun = None
    noun = None
    adjective = None
    verb = None
    for sent in parsed.sentences:
        pronoun = find_pronoun(sent)
        noun = find_noun(sent)
        adjective = find_adjective(sent)
        verb = find_verb(sent)
    logger.info("Pronoun=%s, noun=%s, adjective=%s, verb=%s", pronoun, noun, adjective, verb)
    return pronoun, noun, adjective, verb

###############MAIN########################
Welcome = "Welcome to the Arya Program!" '\n' "You can start talking to the AI. Type 'end' to exit the program" '\n'
print (Welcome)