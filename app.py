#!/usr/bin/env python


import base64
import datetime
import os

import flask
import simplejson

import storm_log


app = flask.Flask(__name__)


@app.route('/', methods=['POST'])
def storm():
    sourcetype = 'generic_single_line'
    source = 'webhook'

    log = storm_log.StormLog(
        '9exBT9VNeluwsmZgfAOEUpWCHLs35sLCv1y_DtcfQ-mEWUtiMqJaFrnHrpdT2zW79xYANdX_hRk=',
        'e0b93ede842211e18101123139335741')

    post_data = flask.request.data
    if not post_data:
        post_data = flask.request.form.keys()[0]

    event_params = {
        'event_text': post_data, 'sourcetype': sourcetype, 'source': source}

    return log.send(**event_params)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
