import unittest
from unittest import mock
from logging import basicConfig, getLogger, DEBUG
import ivs_alarm.processors
from email.mime.text import MIMEText

basicConfig(level=DEBUG, format="%(levelname)-5s - %(filename)s(L%(lineno) 3d) - %(name)s - %(message)s")

class TestProcessors_proc_nothing(unittest.TestCase):
    def setUp(self):
        self.mails = []

        msg = MIMEText('This is mail body')
        msg['To'] = 'to@example.com'
        msg['Cc'] = 'cc@example.com'
        msg['Subject'] = 'Subject'
        msg['From'] = 'from@example.com'
        self.mails.append(msg)

    def tearDown(self):
        pass

    def test_normal(self):

        # 準備
        
        # テスト
        new_mails = ivs_alarm.processors.proc_nothing(self.mails)

        # 結果確認
        self.assertEqual(len(new_mails), len(self.mails))
        self.assertEqual(new_mails[0]['Subject'], self.mails[0]['Subject'])

class TestProcessors_change_to_address(unittest.TestCase):
    def setUp(self):
        self.mails = []

        msg = MIMEText('This is mail body')
        msg['To'] = 'to@example.com'
        msg['Cc'] = 'cc@example.com'
        msg['Subject'] = 'Subject'
        msg['From'] = 'from@example.com'
        self.mails.append(msg)

        mock_get_config = mock.patch('ivs_alarm.processors.get_config')
        self.mock_get_config = mock_get_config.start()
        self.addCleanup(mock_get_config.stop)

    def tearDown(self):
        pass

    def test_normal(self):

        # 準備
        self.mock_get_config.return_value = {
            "global":{'new_to_address': 'new_to@example.com'}
        }
        
        # テスト
        new_mails = ivs_alarm.processors.change_to_address(self.mails)

        # 結果確認
        self.assertEqual(len(new_mails), len(self.mails))
        self.assertEqual(new_mails[0]['To'], 'new_to@example.com')
        self.assertEqual(new_mails[0]['Cc'], None)

class TestProcessors_split_body_by_event(unittest.TestCase):
    def setUp(self):
        self.mails = []

        msg = MIMEText("event1\r\nSEPARATOR\r\nevent2\r\nSEPARATOR\r\n")
        msg['To'] = 'to@example.com'
        msg['Cc'] = 'cc@example.com'
        msg['Subject'] = 'Subject'
        msg['From'] = 'from@example.com'
        self.mails.append(msg)

        mock_get_config = mock.patch('ivs_alarm.processors.get_config')
        self.mock_get_config = mock_get_config.start()
        self.addCleanup(mock_get_config.stop)

    def tearDown(self):
        pass

    def test_normal(self):

        # 準備
        self.mock_get_config.return_value = {
        }
        
        # テスト
        new_mails = ivs_alarm.processors.split_body_by_event(self.mails)

        # 結果確認
        self.assertEqual(len(new_mails), 2)
        self.assertEqual(new_mails[0]['To'], 'to@example.com')
        self.assertEqual(new_mails[0]['Cc'], 'cc@example.com')
        self.assertEqual(new_mails[0].get_payload(), "event1\r\nSEPARATOR\r\n")
        self.assertEqual(new_mails[1]['To'], 'to@example.com')
        self.assertEqual(new_mails[1]['Cc'], 'cc@example.com')
        self.assertEqual(new_mails[1].get_payload(), "event2\r\nSEPARATOR\r\n")

class TestProcessors_ignore_mail(unittest.TestCase):
    def setUp(self):
        self.mails = []

        msg = MIMEText('This is mail body to ignore')
        msg['To'] = 'to@example.com'
        msg['Cc'] = 'cc@example.com'
        msg['Subject'] = 'Subject'
        msg['From'] = 'from@example.com'
        self.mails.append(msg)

        msg = MIMEText('This is mail body')
        msg['To'] = 'to@example.com'
        msg['Cc'] = 'cc@example.com'
        msg['Subject'] = 'Subject'
        msg['From'] = 'from@example.com'
        self.mails.append(msg)

        mock_get_config = mock.patch('ivs_alarm.processors.get_config')
        self.mock_get_config = mock_get_config.start()
        self.addCleanup(mock_get_config.stop)

    def tearDown(self):
        pass

    def test_normal(self):

        # 準備
        self.mock_get_config.return_value = {
            "ignore":{
                "1": ["dummy pattern", "body to ignore"],
                "2": ["dummy pattern"],
            }
        }
        
        # テスト
        new_mails = ivs_alarm.processors.ignore_mail(self.mails)

        # 結果確認
        self.assertEqual(len(new_mails), 1)
        self.assertEqual(new_mails[0]['To'], 'to@example.com')
        self.assertEqual(new_mails[0]['Cc'], 'cc@example.com')
        self.assertEqual(new_mails[0].get_payload(), 'This is mail body')