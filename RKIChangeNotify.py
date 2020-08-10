from bs4 import BeautifulSoup

from urllib.request import Request, urlopen
import time
import logging
import threading
import json

import Email


def CheckWebisteStatus():
    """
    Check if the status of the webiste has changed with
    With a comparation of the cosine similarity of the text
    """
    sleep_time = 60 * 10

    with open('include/rki.json', 'r') as f:
        website = json.load(f)
    with open('include/rki.txt', 'r') as f:
        web_text = f.read()

    url = website['url']

    req = Request(url,
                  headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req)
    html_soup = BeautifulSoup(html, 'html.parser')

    ##########
    # To be done - Create Function to extract main part of website with parameters
    req = Request(url,
                  headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req)
    html_soup = BeautifulSoup(html, 'html.parser')
    attributes = {'class': 'subheadline'}
    text = html_soup.findAll(attrs=attributes)[0].find('p').getText()
    ##########

    if text == web_text:
        logging.info('No Changes in the Website')
        sleep_time = 60 * 10  # 10 Minutes checking time if nothing changes
    else:
        logging.info('Website Changed! Sending E-Mail')
        try:
            res_msg = website["email_msg"]
            res_msg = res_msg + "\n" + text + "\n" + url
            res_subject = website['subject']
            res_from = website['email_from']
            res_to = website['email']
        except Exception as e:  # skipcq: PYL-W0703
            logging.error('Error Assigning Variables \n %s', e)

        try:
            mail_args = (res_msg, res_subject, res_from, res_to, )
            res_email_thread = threading.Thread(target=Email.send_email,
                                                args=mail_args)
            res_email_thread.start()
            res_email_thread.join()
        except Exception as e:  # skipcq: PYL-W0703
            logging.error('Error Starting the Thread \n %s', e)
            logging.error(e)

        try:
            with open('include/rki.txt', 'w') as f:
                f.write(text)
        except Exception as e:  # skipcq: PYL-W0703
            logging.error('Error Saving Status \n %s', e)
            logging.error(e)

        sleep_time = 60 * 60 * 24  # 24 Hours wait if something changes

    return sleep_time


if __name__ == '__main__':

    logging.basicConfig(
        format="%(asctime)s: %(message)s",
        filemode='a',
        filename='RKIChangeNotify-Python.log',
        level=logging.INFO,
        datefmt="%d-%m-%y %H:%M:%S")

    sleep_time = 60 * 10  # Ten minutes at the beginning

    while 1:
        # Start a loop to check the Status of the Webiste
        logging.info('Checking Website')
        sleep_time = CheckWebisteStatus()
        logging.info('Going to sleep')
        time.sleep(sleep_time)

    logging.info('Exiting Loop')
    # deepcode ignore replace~exit~sys.exit: <please specify a reason of ignoring this>
    exit()
