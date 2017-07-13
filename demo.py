import requests

from flask import Flask, request


app = Flask(__name__)


@app.route('/')
def root():
    return 'All OK'


@app.route('/target', methods=['POST'])
def target():
    app.logger.error('Received message')

    app.logger.error('Getting JSON')
    message = request.get_json(force=True)
    app.logger.error('Message: {!r}'.format(message))

    # TODO: Verify signature
    app.logger.error('Verifying signature')

    message_type = message['Type']
    app.logger.error('Message type: {!r}'.format(message_type))
    if message_type == 'SubscriptionConfirmation':
        subscribe_url = message['SubscribeURL']
        app.logger.error('Subscribe URL: {!r}'.format(subscribe_url))
        #requests.get(subscribe_url)
    elif message_type == 'Notification':
        pass
    return 'OK'


if __name__ == '__main__':
    import logging
    app.logger.setLevel(logging.DEBUG)

    app.run(host='els049', port=5000, use_reloader=True)#, ssl_context=('cert.crt', 'key.key'))
