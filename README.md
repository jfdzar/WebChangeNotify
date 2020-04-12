# WebChangeNotify
Python Script to check if the text of a website changes and get an Email notification. The idea is to get notifty i.e. when the reservation of an event opens

For the E-Mail module you will need following file in the include folder
As this file contains credentials - protect it and do not version it
credentials.json
[
	{
		"username": "your gmail email here",
		"pass": "your gmail pass here"
	},
	{
		"email": "email to send email to here"
	}
]

For the Website module you will need following files in the include folder

web.txt
With the text of the website which will be checked

website.json
[
	{
        "url": "url to be checked here",
        "email": "email to send result here",
        "subject": "subject of the email here",
        "email_from": "Sender of the email here",
        "email_msg": "Email message here",
        "sim_thres": "similarity threshold as a float here"
	}
]