from urllib import request
import base64

from cryptography import x509
from cryptography.hazmat import backends


_SIGNED_KEYS = ('Message', 'MessageId', 'Subject', 'SubscribeURL',
                'Timestamp', 'Token', 'TopicArn', 'Type')


def validate(message):
    assert message['SignatureVersion'] == 1

    cert_url = message['SigningCertURL']
    _validate_cert_url(cert_url)
    with request.urlopen(cert_url) as response:
        pem = response.read()
    cert = x509.load_pem_x509_certificate(pem, backends.default_backend())
    public_key = cert.public_key()

    content_to_sign = _content_to_sign(message)
    signature = base64.b64decode(message['Signature'])
    public_key.verify(signature, content_to_sign.encode())


def _content_to_sign(message):
    parts = []
    for key in _SIGNED_KEYS:
        if key in message:
            parts.append(key)
            parts.append(message[key])
    parts.append('')
    return '\n'.join(parts)


def _validate_cert_url(cert_url):
    pass
