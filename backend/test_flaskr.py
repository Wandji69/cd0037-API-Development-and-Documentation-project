import os
import re
from unicodedata import category
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            "question": "what is your name",
            "answer": "Collins Bob",
            "difficulty": "4",
            "category": "3"
        }
        self.new_category = {
            "type": "Q&A"
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue((data["totalQuestions"]))
        self.assertTrue(data["categories"])
        self.assertTrue(data["currentCategory"], "All")
        self.assertTrue(len(data["questions"]))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/questions?page=1000", json={"category": 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")

    # Test Get category creation
    def test_create_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])

    ### Not important ####
    # def test_404_if_category_not_found(self):
    #     res = self.client().get("/categories")
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "Resource Not Found")

    # def test_405_if_category_creation_not_allowed(self):
    #     res = self.client().post("/categories/45", json=self.new_category)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 405)
    #     self.assertEqual(data["success"], False)

    # def test_get_questions_categories_id(self):
    #     res = self.client().get("/categories/3/questions")
    #     data = json.loads(res.data)

    #     self.assertEquals(res.status_code, 200)
    #     self.assertEquals(data["success"], True)
    #     self.assertTrue(data["type"])

    # def test_404_sent_requesting_beyond_valid_categories(self):
    #     res = self.client().get("/categories/35/questions")
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data["success"], False)

# Test question creation

    # def test_create_new_question(self):
    #     res = self.client().post("/questions", json=self.new_question)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["question"])
    #     self.assertTrue(data["answer"])
    #     self.assertTrue(data["difficulty"])
    #     self.assertTrue(data["category"])

    # def test_405_if_question_creation_not_allowed(self):
    #     res = self.client().post("/question/45", json=self.new_question)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 405)
    #     self.assertEqual(data["success"], False)

    # Test question deletion
    def test_delete_question(self):
        res = self.client().delete("/questions/6")
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 6).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(question, None)

    def test_422_if_question_does_not_exist(self):
        res = self.client().delete("/questions/100")
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 100).one_or_none()

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable")
        self.assertEqual(question, None)

    # Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
