import unittest
from unittest import mock
from logging import basicConfig, getLogger, DEBUG
import ivs_alarm.processors
from email.mime.text import MIMEText
from email import message_from_string, message_from_file

basicConfig(level=DEBUG, format="%(levelname)-5s - %(filename)s(L%(lineno) 3d) - %(name)s - %(message)s")

class TestProcessors_proc_nothing(unittest.TestCase):
    def setUp(self):
        self.mails = []
        with open('test/fixtures/have_one_event.eml') as f:
            self.mails.append(message_from_file(f))

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

        with open('test/fixtures/have_one_event.eml') as f:
            self.mails.append(message_from_file(f))

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

        with open('test/fixtures/have_many_events.eml') as f:
            self.mails.append(message_from_file(f))

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
        self.assertIn("event1", new_mails[0].get_payload())
        self.assertEqual(new_mails[1]['To'], 'to@example.com')
        self.assertEqual(new_mails[1]['Cc'], 'cc@example.com')
        self.assertIn("event2", new_mails[1].get_payload())

class TestProcessors_ignore_mail(unittest.TestCase):
    def setUp(self):
        self.mails = []

        with open('test/fixtures/have_one_event_to_ignore.eml') as f:
            self.mails.append(message_from_file(f))

        with open('test/fixtures/have_one_event.eml') as f:
            self.mails.append(message_from_file(f))

        mock_get_config = mock.patch('ivs_alarm.processors.get_config')
        self.mock_get_config = mock_get_config.start()
        self.addCleanup(mock_get_config.stop)

    def tearDown(self):
        pass

    def test_normal(self):

        # 準備
        self.mock_get_config.return_value = {
            "ignore":{
                "1": ["dummy pattern", "event to ignore"],
                "2": ["dummy pattern"],
            }
        }
        
        # テスト
        new_mails = ivs_alarm.processors.ignore_mail(self.mails)

        # 結果確認
        self.assertEqual(len(new_mails), 1)
        self.assertEqual(new_mails[0]['To'], 'to@example.com')
        self.assertEqual(new_mails[0]['Cc'], 'cc@example.com')
        self.assertIn('event1', new_mails[0].get_payload())