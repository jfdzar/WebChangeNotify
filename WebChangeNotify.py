from urllib.request import urlopen
from unidecode import unidecode
from bs4 import BeautifulSoup
from collections import defaultdict

import re
import time
import logging
import threading
import inflection
import numpy as np
import math
import json

import Email

# Using cosine_similarity, own faster implementation, inspired by
# https://towardsdatascience.com/calculating-string-similarity-in-python-276e18a7d33a
# Code from https://gist.github.com/gallir/e719f8c816b8c7d349a8d69d3678acbb 

_tokens_cache = defaultdict(lambda: None)
_phone_regex = re.compile(r'[^\d]|^0+')
# last is a subset from string.punctuation
_nopunctuation = str.maketrans('()[]-&:;./-.', '            ', '\'`´!"#$%*+,<=>?@\\^_`{|}~')

def cosine_similarity(text1, text2, cache=False, stopwords=None, enders=None):
    # Return cosine similarity between text1 and text2

    tok1 = tok2 = None
    if cache:
        tok1 = _tokens_cache[text1]
        tok2 = _tokens_cache[text2]

    if tok1 is None:
        tok1 = get_tokens(text1,stopwords=stopwords,enders=enders)
        if cache:
            _tokens_cache[text1] = tok1
    if tok2 is None:
        tok2 = get_tokens(text2,stopwords=stopwords,enders=enders)
        if cache:
            _tokens_cache[text2] = tok2

    if not tok1 or not tok2:
        return 0.0
    if tok1 == tok2:
        return 1.0

    vocabulary = set(tok1 + tok2)
    if len(vocabulary) == len(tok1) + len(tok2):
        # No intersections
        return 0.0
    v1 = np.zeros(len(vocabulary))
    v2 = np.zeros(len(vocabulary))
    for i, w in enumerate(vocabulary):
        if w in tok1:
            v1[i] = 1
        if w in tok2:
            v2[i] = 1
    # This the cosine = v1 DOT v2 / (norm-2(v1) * norm-2(v2))
    # equivalent but +2x faster than np.dot(v1, v2) / (np.linalg.norm(v1) *  np.linalg.norm(v2))
    return np.dot(v1, v2) / (math.sqrt(np.dot(v1, v1)) * math.sqrt(np.dot(v2, v2)))

def get_tokens(text, stopwords=None, enders=None):
    text = text.translate(_nopunctuation)
    text = unidecode(text)
    text = text.lower()
    tokens = [inflection.singularize(w) for w in text.split() if len(w) > 1 and (not stopwords or w not in stopwords)]
    if enders:
        for i, w in enumerate(tokens):
            if w in enders:
                tokens = tokens[:i]
                break
    return sorted(tokens)

def phonenumber_equal(a, b):
    a = _phone_regex.sub('', a)
    b = _phone_regex.sub('', b)
    if len(a) > 8 or len(b) > 8 and a == b:  # Only if at least they hav 9 digits
        return True
    return False

def CheckWebisteStatus():
    with open('include/website.json', 'r') as f:
        website = json.load(f)
    with open('include/web.txt', 'r') as f:
        web_text = f.read()
    
    url = website[0]['url']

    html = urlopen(url)
    html_soup = BeautifulSoup(html, 'html.parser')

    ##########
    #To be done - Create Function to extract main part of website with parameters
    post_body_section = html_soup.findAll(attrs={'class' : 'post-entry post-entry-type-page post-entry-91'})[1]
    text = post_body_section.findAll(attrs={'class' : 'av_textblock_section'})[0]
    text = str(text)
    ##########

    cosine_similarty_value = cosine_similarity(text,web_text)

    if (cosine_similarty_value >= float(website[0]['sim_thres'])):
        logging.info('No Changes in the Website')
    else:
        logging.info('Website Changed! Sending E-Mail')
        try:
            res_msg = website[0]["email_msg"]
            res_msg = res_msg + text

            res_subject = website[0]['subject']
            res_from = website[0]['email_from']
            res_to = website[0]['email']

            res_email_thread = threading.Thread(target=Email.send_email, args=(res_msg,res_subject,res_from,res_to,))
            res_email_thread.start()
            res_email_thread.join()
        except Exception as e:
            logging.error(e)


if __name__ == '__main__':
    format = '%(asctime)s: %(message)s'
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt='%H:%M:%S')

    while(1):
        #Start a loop to check the Status of the Webiste 
        logging.info('Checking Webiste')
        CheckWebisteStatus()
        logging.info('Going to sleep')
        time.sleep(43200) 

    logging.info('Exiting Loop') 
    exit()
