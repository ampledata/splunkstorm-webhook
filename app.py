#!/usr/bin/env python
"""Webhook for Splunk Storm.

Accepts POST requests with any form data and proxies them to the Splunk Storm
API.

Also supports POSTS from ckl clients to /ckl/.

Usage
  1. Set Heroku config vars for your Splunk Storm Project:
    $ heroku config:add SPLUNKSTORM_ACCESS_TOKEN=xxx
    $ heroku config:add SPLUNKSTORM_PROJECT_ID=xxx
  2. Deploy to Heroku.
"""
__author__ = 'Greg Albrecht <gba@splunk.com>'
__copyright__ = 'Copyright 2012 Splunk, Inc.'
__license__ = 'Apache License 2.0'


import os

import flask
import werkzeug

import storm_log


def send_log(event_params):
    log = storm_log.StormLog(
        os.environ['SPLUNKSTORM_ACCESS_TOKEN'],
        os.environ['SPLUNKSTORM_PROJECT_ID'])
    return log.send(**event_params)


app = flask.Flask(__name__)


@app.route('/', methods=['POST'])
def storm():
    """Endpoint handler for POST requests."""
    sourcetype = 'generic_single_line'
    source = 'webhook'

    post_data = flask.request.data
    if not post_data:
        post_data = flask.request.form.keys()[0]

    event_params = {
        'event_text': post_data, 'sourcetype': sourcetype, 'source': source}

    return send_log(event_params)


@app.route('/ckl/', methods=['POST'])
def ckl():
    if flask.request.form['secret'] != os.environ['CKL_SECRET_KEY']:
        abort(401)

    sourcetype = 'generic_multi_line'
    source = 'ckl'

    remote_ip = flask.request.environ['REMOTE_ADDR']
    script = flask.request.files.get('scriptlog', '')

    hostname = flask.request.form.get('hostname', '')
    msg = flask.request.form.get('msg', '')
    ts = flask.request.form.get('ts', 0)
    username = flask.request.form.get('username', '')

    if script:
        f_name = werkzeug.secure_filename(script.filename)
        script.save(f_name)
        script = open(f_name).read()

    event_data = ' '.join([ts, hostname, remote_ip, username, msg, script])

    event_params = {
        'event_text': event_data, 'sourcetype': sourcetype, 'source': source}

    send_log(event_params)

    return 'saved\n'



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)