import json
import os.path
import unittest

import sns


class Test(unittest.TestCase):
    def _message(self, name):
        path = os.path.join('static', name)
        with open(path) as f:
            raw = f.read()
        return json.loads(raw)

    def test__content_to_sign_sub(self):
        message = self._message('subscription_confirmation.sample')
        result = sns._content_to_sign(message)
        expected = ('Message\n'
                    'You have chosen to subscribe to the topic'
                    ' arn:aws:sns:us-west-2:123456789012:MyTopic.\nTo'
                    ' confirm the subscription, visit the SubscribeURL'
                    ' included in this message.\n'
                    'MessageId\n'
                    '165545c9-2a5c-472c-8df2-7ff2be2b3b1b\n'
                    'SubscribeURL\n'
                    'https://sns.us-west-2.amazonaws.com/'
                    '?Action=ConfirmSubscription'
                    '&TopicArn=arn:aws:sns:us-west-2:123456789012:MyTopic'
                    '&Token=2336412f37fb687f5d51e6e241d09c805a5a57b30d7'
                    '12f794cc5f6a988666d92768dd60a747ba6f3beb71854e285d'
                    '6ad02428b09ceece29417f1f02d609c582afbacc99c583a916'
                    'b9981dd2728f4ae6fdb82efd087cc3b7849e05798d2d2785c0'
                    '3b0879594eeac82c01f235d0e717736\n'
                    'Timestamp\n'
                    '2012-04-26T20:45:04.751Z\n'
                    'Token\n'
                    '2336412f37fb687f5d51e6e241d09c805a5a57b30d712f794c'
                    'c5f6a988666d92768dd60a747ba6f3beb71854e285d6ad0242'
                    '8b09ceece29417f1f02d609c582afbacc99c583a916b9981dd'
                    '2728f4ae6fdb82efd087cc3b7849e05798d2d2785c03b08795'
                    '94eeac82c01f235d0e717736\n'
                    'TopicArn\n'
                    'arn:aws:sns:us-west-2:123456789012:MyTopic\n'
                    'Type\n'
                    'SubscriptionConfirmation\n')
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
