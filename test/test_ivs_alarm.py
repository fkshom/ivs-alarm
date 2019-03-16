import unittest
from unittest import mock
import ivs_alarm.ivs_alarm
import poplib

class TestMain(unittest.TestCase):
    def setUp(self):
        mock_appconfig = mock.patch('ivs_alarm.ivs_alarm.get_config')
        mock_pop3 = mock.patch('poplib.POP3')
        mock_smtp = mock.patch('smtplib.SMTP')
        mock_pcoesss_mail = mock.patch('ivs_alarm.ivs_alarm.process_mail')
        self.mock_appconfig = mock_appconfig.start()
        self.mock_pop3 = mock_pop3.start()
        self.mock_smtp = mock_smtp.start()
        self.mock_process_mail = mock_pcoesss_mail.start()
        self.addCleanup(mock_appconfig.stop)
        self.addCleanup(mock_pop3.stop)
        self.addCleanup(mock_smtp.stop)
        self.addCleanup(mock_pcoesss_mail.stop)

    def tearDown(self):
        pass

    def test_normal(self):

        # 準備
        mail_count = 5
        pop3 = self.mock_pop3.return_value
        pop3.pass_.return_value = (mail_count, None)
        pop3.retr.return_value = (None, ['line1', 'line2'])

        smtp = self.mock_smtp.return_value

        process_mail = self.mock_process_mail
        process_mail.return_value = ['newmail1', 'newmail2']
        
        # テスト
        ivs_alarm.ivs_alarm.main()

        # 結果確認
        self.assertEqual(process_mail.call_count, mail_count)
        self.assertEqual(smtp.send_message.call_count, mail_count * 2)

    def test_raise_exception_when_connect_pop3_server(self):

        # 準備
        self.mock_pop3.side_effect = OSError("Mock Exception")

        # テスト＆結果確認
        with self.assertRaises(OSError):
            ivs_alarm.ivs_alarm.main()

    def test_raise_exception_when_password_is_invalid(self):

        # 準備
        pop3 = self.mock_pop3.return_value
        pop3.pass_.side_effect = poplib.error_proto("Invalid password")

        # テスト＆結果確認
        with self.assertRaises(poplib.error_proto):
            ivs_alarm.ivs_alarm.main()

