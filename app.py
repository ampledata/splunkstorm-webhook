#!/usr/bin/env python
"""Webhook for Splunk Storm.

Accepts POST requests with any form data and proxies them to the Splunk Storm
API.

Usage
  1. Set Heroku config vars for your Splunk Storm Project:
    $ heroku config:add SPLUNKSTORM_ACCESS_TOKEN=xxx
    $ heroku config:add SPLUNKSTORM_PROJECT_ID=xxx
  2. Deploy to Heroku.
"""
__author__ = 'Greg Albrecht <gba@splunk.com>'
__copyright__ = 'Copyright 2012 Splunk, Inc.'
__license__ = 'Apache 2.0 License'


import base64
import datetime
import os

import flask
import simplejson

import storm_log


app = flask.Flask(__name__)


@app.route('/', methods=['POST'])
def storm():
    """Endpoint handler for POST requests."""
    sourcetype = 'generic_single_line'
    source = 'webhook'

    log = storm_log.StormLog(
        os.environ['SPLUNKSTORM_ACCESS_TOKEN'],
        os.environ['SPLUNKSTORM_PROJECT_ID'])

    post_data = flask.request.data
    if not post_data:
        post_data = flask.request.form.keys()[0]

    event_params = {
        'event_text': post_data, 'sourcetype': sourcetype, 'source': source}

    return log.send(**event_params)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
