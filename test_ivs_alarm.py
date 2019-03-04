import unittest
from unittest import mock
import ivs_alarm
import poplib

class TestGetMails(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @mock.patch('poplib.POP3')
    def test_normal(self, mock_pop3):
        """
        クラスをモックする
        https://docs.python.org/ja/3/library/unittest.mock-examples.html#mocking-classes
        """
        mail_count = 5
        pop3 = mock_pop3.return_value
        pop3.stat.return_value = (mail_count, None)
        pop3.retr.return_value = (None, ['line1', 'line2'])

        kwargs = {'server':'server','user':'user','password':'pass'}
        result = list(ivs_alarm.get_mails(**kwargs))
        self.assertEqual(len(result), mail_count)
    
    @mock.patch('poplib.POP3')
    def test_raise_exception_when_connect_pop3_server(self, mock_pop3):
        mock_pop3.side_effect = OSError("Mock Exception")

        with self.assertRaises(OSError):
            kwargs = {'server':'server','user':'user','password':'pass'}
            list(ivs_alarm.get_mails(**kwargs))

    @mock.patch('poplib.POP3')
    def test_raise_exception_when_password_is_invalid(self, mock_pop3):
        pop3 = mock_pop3.return_value
        pop3.pass_.side_effect = poplib.error_proto("Invalid password")

        with self.assertRaises(poplib.error_proto):
            kwargs = {'server':'server','user':'user','password':'pass'}
            list(ivs_alarm.get_mails(**kwargs))
