import os
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
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

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
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(data['categories'], dict)
        self.assertEqual(data['success'], True)

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        self.assertEqual(len(data['questions']), 10)
    
    def test_delete_question(self):
        id = 1
        res = self.client().delete(f'/questions/{id}')
        data = json.loads(res.data)
        if res.status_code == 404:
            self.assertEqual(data['success'], False)
        else:
            self.assertEqual(data['deleted'], id)
            self.assertEqual(data['success'], True)

    def test_delete_question_not_exist(self):
        res=self.client().delete('questions/100000')
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 404)
    
    def test_create_question(self):
        new_question={
            'question': 'test question',
            'answer': 'test answer',
            'difficulty': 3,
            'category': 2,
        }
        res=self.client().post('/questions', json=new_question)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_create_question_not_allowed(self):
        new_question=json.dumps({})
        res=self.client().post('/questions/45', json=new_question)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_search(self):
        search_term={'searchTerm': 'what'}
        res = self.client().post('/search', json=search_term)
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(data['questions'], list)
        self.assertIsInstance(data['total_questions'], int)

    def test_get_questions_by_cateogory(self):
        res=self.client().get('/categories/2/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsInstance(data['questions'], list)
        self.assertIsInstance(data['total_questions'], int)
        self.assertEqual(data['current_catetory'], 2)

    def test_get_questions_play_quiz(self):
        test_data = {
            'previous_questions': [1, 2],
            'quiz_category': {'id': 2, 'type': 'History'}
        }
        res=self.client().post('/quizzes', json=test_data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

        # not show previous question
        self.assertNotEqual(data['question']['id'], 1)
        self.assertNotEqual(data['question']['id'], 2)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()