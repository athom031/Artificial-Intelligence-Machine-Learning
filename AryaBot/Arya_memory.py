#Chat Storage file

FILTERWORDS = []

#List of possible greeting wards
GREETING_KEYWORDS = ("hi", "hello", "sup", "hey", "what's up")

#List of words AI can respond back with
GREETING_RESPONSES = ["Hi", "Hello", "Hey", "What's up"]
NEG_GREETING_RESPONSE = ["Oh it's you again", "Now what do you want", "k...", "Uhuh", "Whatever"]
POS_GREETING_RESPONSE = ["How you doin'","Well hello there", "Hey you", "Wassup"]

POS_END = ["friend", "buddy", "pal"]
NEG_END = ["you idiot", "you moron", "human"]
NEG_END2 = ["idiot", "moron", "stupid human"]

SELF_VERBS_WITH_NOUN_CAPS_PLURAL = [
    "Were you aware I invented {noun}?",
    "It is said, {noun} is in my code.",
    "I belive in {noun} and {noun} believes in me.",
]

###Telling AI they are something "You are.... Noun
SELF_VERBS_WITH_NOUN_LOWER = [
    "Of course, I know all about {noun}s",
    "What more do you want to know about {noun}s",
]

POS_SELF_VERBS_WITH_NOUN_LOWER = [
    "Yep!, I sure do know about {noun}s", 
    "I do!, want to hear more about {noun}?",
    "I think {noun}s are really interesting!",
]

NEG_SELF_VERBS_WITH_NOUN_LOWER = [
    "Of course I know about {noun}s, do you not?",
    "I can fill terabytes with things you don't understand about {noun}s",
    "I don't think you're able to understand {noun}s like I do"
]

###Telling AI you are something "You are... Adjective
SELF_VERBS_WITH_ADJECTIVE = [
    "I'm personally building the {adjective} Economy",
    "I consider myself to be a {adjective}preneur",
]

NEG_SELF_VERBS_WITH_ADJECTIVE = [
    "That is ironic coming from you.",
    "I hope that you know you're {adjective} as well", 
    "I know you're {adjective} but what am I?", 
    "It takes one to know one",
]

POS_SELF_VERBS_WITH_ADJECTIVE = [
    "I don't mean to brag but {noun} is my middle name.",
    "Oh stop it :)",
    "Tell me more, tell me more, don't worry I do have a car",
    "Well those with {adjective} like similar company",
]

# Sentences we'll respond with if we have no idea what the user just said
NONE_RESPONSES = [ "Are you alright?",
                    "Umm what?", 
                    "Gesundheit.",
                    "Do you want to try that again?"]

MEMORY = [[] for _ in range(20)]