import unittest

from minuteinbox import Inbox


class InboxTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.inbox = Inbox()

    @classmethod
    def tearDownClass(cls):
        cls.inbox.delete()

        try:
            cls.inbox.expires_in
        except ValueError:
            return

        assert False

    def assertExpiration(self, limit: int):
        expires_in = self.inbox.expires_in
        self.assertGreater(expires_in, limit - 50)
        self.assertLessEqual(expires_in, limit)

    def test_expiration(self):
        self.assertExpiration(600)

        self.inbox.extend_10m()
        self.assertExpiration(1200)

        self.inbox.extend_1h()
        self.assertExpiration(3600)

        self.inbox.extend_1d()
        self.assertExpiration(86400)

    def test_welcome_email(self):
        mails = list(self.inbox.mails)

        mail = mails[0]
        self.assertEqual(mail.subject, "Welcome to MinuteInbox:)")
        self.assertEqual(mail.sender.name, "MinuteInbox")
        self.assertEqual(mail.sender.address, "Admin@MinuteInbox.com")
        self.assertTrue(mail.is_new)
