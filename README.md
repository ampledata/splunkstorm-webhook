About
=====
This repository contains a small [Flask](http://flask.pocoo.org/) app that
acts as a [Webhook](http://www.webhooks.org/). When this app receives a HTTP
POST it will deserialize the contents and convert the into a Splunk Storm log
event.

Requirements
============

1. A [Splunk Storm](https://www.splunkstorm.com) Account.
2. A Python operating environment. 
3. A server on which to host this app.
  - Possible servers are local, Heroku, App Engine, et al.

Usage
=====
To use this app on Heroku:

1. Retrieve your [Splunk Storm Access Token and Project
   ID](http://docs.splunk.com/Documentation/Storm/latest/User/UseStormsRESTAPI).
2. Install & Configure the [heroku toolbelt](https://toolbelt.herokuapp.com/).
3. From within this directory create a Heroku app: 

        heroku create --stack cedar

4. Set your Splunk Storm Access Token and Project ID as [Heroku Config
   Variables](https://devcenter.heroku.com/articles/config-vars):

        heroku config:add SPLUNKSTORM_ACCESS_TOKEN=xxx
        heroku config:add SPLUNKSTORM_PROJECT_ID=xxx

5. Push this app to [Heroku's git
   repository](https://devcenter.heroku.com/articles/git):

        git push heroku master

6. Your app will now be accessible to HTTP POST requests!

Testing
=======
To test and ensure this app is functioning properly you can try
variations of the following `curl` commands (given that your app is
hot-dogs-123.herokuapp.com):

```bash
curl -d '{"test_data": "this is test json data"}' http://hot-dogs-123.herokuapp.com/
```
Should return: `{"length": 39}`

Your event should be viewable from the 'Explore Data' search:
!['Explore Data' search
results](http://dl.dropbox.com/u/4036736/Screenshots/2nfd.png)

Author
======
Greg Albrecht <gba@splunk.com> http://ampledata.org/

License
=======
Apache License 2.0.

Copyright
=========
Copyright 2012 Splunk, Inc.
