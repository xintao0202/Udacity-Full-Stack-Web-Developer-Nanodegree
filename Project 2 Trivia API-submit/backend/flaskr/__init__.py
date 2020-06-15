import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @Set up CORS. Allow '*' for origins. 
  '''
  CORS(app, resources={'/': {'origins': '*'}})

  '''
  @Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods','GET, POST, PATCH, DELETE, OPTIONS')
    return response
  '''
  @ 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
    try:
      categories= Category.query.all()
      categories_dict = {}
      for category in categories:
        categories_dict[category.id] = category.type
      return jsonify({
          'success': True,
          'categories': categories_dict
      })
    except:
      abort(500)
  '''
  @ 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  def get_questions():
    num_questions=10
    try:
      questions=Question.query.all()
      categories=Category.query.all()
      if len(questions)==0 or len(categories)==0:
        abort(404)

      else:
        total_num_questions=len(questions)
        question_list=[]
        for question in questions:
          question_list.append(question.format())
        category_dict={}
        for c in categories:
          category_dict[c.id]=c.type
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * num_questions
        end = start + num_questions

        curr_page_questions=question_list[start:end]

        return jsonify({
            'questions': curr_page_questions,
            'total_questions': total_num_questions,
            'categories': category_dict
        })
    except:
      abort(500)


  '''
  @: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    # try:
    #   question = Question.query.filter(Question.id==question_id).one_or_more()
    #   if question is None:
    #       abort(404)

    #   question.delete()
    #   return jsonify({
    #       'success': True,
    #       'deleted': question_id
    # })
    # except:
    #   abort(422)
    question = Question.query.get(question_id)
    if not question:
        return abort(404, f'No question found with id: {question_id}')
    question.delete()
    return jsonify({
        'success': True,
        'deleted': question_id
    })
  '''
  @: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    body=request.get_json()
    new_question=body.get('question', None)
    new_answer=body.get('answer', None)
    new_category=body.get('category', None)
    new_difficulty_score=body.get('difficulty', None)

    try:
      question=Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty_score)
      question.insert()

      return jsonify(
        {
          'success': True,
          'created': question.id
        }
      )
    except:
      abort(422)


  '''
  @: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/search', methods=['POST'])
  def search():
    body=request.get_json()
    search_term=body.get('searchTerm', '')

    if len(search_term)==0:
      abort(422)

    try:
      search_results=Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
      results=[result.format() for result in search_results]

      return jsonify({
        'success': True,
        'questions': results,
        'total_questions': len(results)
      })
    except:
      abort(404)

  '''
  @: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_cateogory(category_id):
    category=Category.query.filter_by(id=category_id).one_or_none()
    if not category:
      abort(400)
    
    try:
      questions=Question.query.filter_by(category=category_id).all()
      results=[question.format() for question in questions]

      return jsonify({
              'success': True,
              'questions': results,
              'total_questions': len(results),
              'current_catetory': category.id
            })
    except:
      abort(404)


  '''
  @: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.route('/quizzes', methods=['POST'])
  def get_questions_play_quiz():
    body=request.get_json()
    prev_questions=body.get('previous_questions')
    category=body.get('quiz_category')

    # if no category is found, abort 400
    if len(category)==0:
      abort(400)
      

    try:
      # if 0 is selected return all questions
      if category['id']==0:
        questions=Question.query.all()
      else:
        questions=Question.query.filter_by(category=category['id']).all()

      next_question=questions[random.randint(0,len(questions)-1)]
      
      questions_id=[q.id for q in questions] 
      #if prev_questions contains all the questions in the current category, return None for next question
      if all(x in prev_questions for x in questions_id):
        return jsonify({
        'success': True,
        'question': None
      })
      else:
        while (next_question.id in prev_questions):
          next_question=questions[random.randint(0,len(questions)-1)]
        
        return jsonify({
          'success': True,
          'question': next_question.format()
        })
    except:
      abort(404)



  '''
  @: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          'success': False,
          'error': 400,
          'message': 'Bad request error'
      }), 400

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          'success': False,
          'error': 404,
          'message': 'Resource not found'
      }), 404

  @app.errorhandler(405)
  def not_found(error):
      return jsonify({
          'success': False,
          'error': 405,
          'message': 'method not allowed'
      }), 405

  @app.errorhandler(500)
  def internal_server_error(error):
      return jsonify({
          'success': False,
          'error': 500,
          'message': 'An error has occured, please try again'
      }), 500

  @app.errorhandler(422)
  def unprocesable_entity(error):
      return jsonify({
          'success': False,
          'error': 422,
          'message': 'unprocessable'
      }), 422


  return app

    