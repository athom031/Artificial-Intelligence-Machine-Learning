## Artifical Intelligence - Neural Networks

### Arya the ChatBot

<div align="center">
<img src="https://github.com/athom031/Artificial_Intelligence/blob/master/AryaBot/demo_img/aryaWanderer.jpg" width = "50%"/> 
</div><br/>

Arya is a chat bot that learns a 'negative', 'neutral', or 'positive' personality and responds occordingly. <br/>

![Demo_Personality](https://github.com/athom031/Artificial_Intelligence/blob/master/AryaBot/demo_img/aryaSoccer.png)
<br/>

Each line, her personality 'score' is at a positive, netural, and negative level accordingly. Though the user input changes, Arya 'feels' like responding in a different way.

## Abstract

This is a simple AI interface that responds to user entries based on the conversation and personality of the AI. If the user enters positive entries, the AI personality will slowly rise. But if the user starts sending negative messages, Arya's personality will start to drop.


## Getting Started

This is a python project that makes use of tkinter for a simple GUI.<br/>
First install python on to your system. <br/>
[Mac Python 3 Download](https://opensource.com/article/19/5/python-3-default-mac#what-to-do)


### Prerequisites

Install the following python modules:
	pip install requests
	pip install tweepy
	pip install -U textblob
	python -m textblob.download_corpora

### Compile

To run and start a conversation with Arya:
	python AryaGUI.py
	
## Reflection

### Warnings

There will most likely be some warnings when you run the program:
* Deprecation warning of tkinter():
	DEPRECATION WARNING: The system version of Tk is deprecated and may be removed in a future release. Please don't rely on it. Set TK_SILENCE_DEPRECATION=1 to suppress this warning.
* I experienced several CoreText warnings but the font ended up working just fine:
	2020-08-28 16:31:16.387 python[63904:1351710] CoreText note: Client requested name ".SFNSMono-Regular", it will get Times-Roman rather than the intended font. All system UI font access should be through proper APIs such as CTFontCreateUIFontForLanguage() or +[NSFont systemFontOfSize:].
	2020-08-28 16:31:16.387 python[63904:1351710] CoreText note: Set a breakpoint on CTFontLogSystemFontNameRequest to debug.
	2020-08-28 16:31:16.464 python[63904:1351710] CoreText note: Client requested name ".SF NS Mono", it will get Times-Roman rather than the intended font. All system UI font access should be through proper APIs such as CTFontCreateUIFontForLanguage() or +[NSFont systemFontOfSize:].

### Limitations

AI is a complex field which is the reason for the Turing Test to exist. <br/>
Because of that there are limitations on Arya.

* Arya's vocabulary is off a database of words and this is character specific, therefore capitalization does change understanding
* Some phrases will simply not be understood because of the limits of the words understood by Arya.
* Because of this can crash and just not respond on some user input.

### User Input Examples

Some output stays the same no matter the personality:
* "What time is it?" will return standard time of clock
The other output will change based on how Arya feels:
* "Who am I?"
* "Who are you?"
* "I am good at <insert noun>"
Finally input will affect Arya's personality beyond setting it manually:
* "You are a <insert adj>"

## Inpsiration

Input parser and output creating inspired by Liza Daly's python chat bot fundamentals example.
* [brobot](https://github.com/lizadaly/brobot)
