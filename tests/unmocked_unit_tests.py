"""Unmocked unit test"""
#pylint: disable=C0103
#pylint: disable=C0301
import unittest
from os.path import dirname, join
import sys

sys.path.insert(1, join(dirname(__file__), '../'))
import app
import models


class UnmockedTest(unittest.TestCase):
    """Unmocked unit test cases """
    def setUp(self):
        self.feedback_test_user = models.FeedbackLog('Jay Amin', 'I learned a lot about politics')
        self.quiz_test_question = models.QuizQuestions('Test question for unit test', 'test group', -32)
        self.test_user = models.UserInfo("test@test.com", "Test McTestface", "http://this-is-a-fake-url.com")
        self.test_quiz_score = models.QuizScore("test@test.com", -99)

    def test_app_mock(self):
        """ News api unmocked test cases """
        r_json = (app.news_api_call())

        assert len(r_json) > 1

        for i in r_json:
            self.assertFalse(i["source"] == " ", "False or True")
            self.assertFalse(i["author"] == " ", "False or True")
            self.assertFalse(i["title"] == " ", "False or True")
            self.assertFalse(i["img"] == " ", "False or True")
            self.assertFalse(i["url"] == " ", "False or True")
            self.assertFalse(i["published"] == " ", "False or True")
            self.assertFalse(i["content"] == " ", "False or True")

    def test_models(self):
        """ Test instances of models from models.py """
        self.assertEqual(self.feedback_test_user.feedback, 'I learned a lot about politics')
        self.assertEqual(self.feedback_test_user.name, 'Jay Amin')
        self.assertEqual(self.quiz_test_question.text, 'Test question for unit test')
        self.assertEqual(self.quiz_test_question.group_name, 'test group')
        self.assertEqual(self.quiz_test_question.multiplier, -32)
        self.assertEqual(self.test_user.email, "test@test.com")
        self.assertEqual(self.test_user.name, "Test McTestface")
        self.assertEqual(self.test_user.img_url, "http://this-is-a-fake-url.com")
        self.assertEqual(self.test_quiz_score.email, "test@test.com")
        self.assertEqual(self.test_quiz_score.score, -99)

    def test_repr(self):
        """ Test string form of model instances from models.py """
        test_repr = self.feedback_test_user.__repr__()
        correct_repr = "{'name': 'Jay Amin', 'feedback': 'I learned a lot about politics'}"
        self.assertEqual(test_repr, correct_repr)
        test_repr = self.quiz_test_question.__repr__()
        correct_repr = "{'text': 'Test question for unit test', 'group name': 'test group', 'multiplier': -32}"
        self.assertEqual(test_repr, correct_repr)
        test_repr = self.test_user.__repr__()
        correct_repr = "{'email': 'test@test.com', 'name': 'Test McTestface', 'img_url': 'http://this-is-a-fake-url.com'}"
        self.assertEqual(test_repr, correct_repr)
        test_repr = self.test_quiz_score.__repr__()
        correct_repr = "{'email': 'test@test.com', 'score': -99}"
        self.assertEqual(test_repr, correct_repr)


if __name__ == '__main__':
    unittest.main()
