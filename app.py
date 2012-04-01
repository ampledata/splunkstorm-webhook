import datetime
import os

import flask

import storm_log

app = flask.Flask(__name__)

@app.route('/')
def hello():
    return "Hello from Python!"

@app.route('/storm')
def storm():
    log = StormLog(
        '9exBT9VNeluwsmZgfAOEUpWCHLs35sLCv1y_DtcfQ-mEWUtiMqJaFrnHrpdT2zW79xYANdX_hRk=',
        'c7570d5a745411e1810e123139335bf7')

    ts = datetime.now().isoformat()
    log.send("%s hello world" % ts)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
