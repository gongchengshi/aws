import unittest
import aws.sns


class SnsTest(unittest.TestCase):
    def test_topic_name_from_topic_arn(self):
        expected = 'dummy_crawl_job'
        actual = aws.sns.topic_name_from_topic_arn('yeah:' + expected)
        self.assertEqual(actual, expected)

    def test_format_message(self):
        msg = aws.sns.format_message(
            '%s MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM %s',
            '1234567890', '2345678901')
        self.assertEqual(len(msg), 140)
        self.assertEqual('12345 MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM 23456', msg)

        msg = aws.sns.format_message(
            '%s MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM %s',
            '1234567890', '2345678901')
        self.assertEqual(len(msg), 138)
        self.assertEqual('1234567890 MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM 2345678901', msg)
