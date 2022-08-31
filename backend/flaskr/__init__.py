from crypt import methods
from mimetypes import init
import random
from re import search
from unicodedata import category
from models import Category, Question
from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from models import setup_db

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


"""
@TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
"""


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route('/categories')
    def get_categories():
        try:
            data = Category.query.all()
            # categories = {}
            categories = {}
            for d in data:
                categories.update({
                    d.id: d.type
                })

            return jsonify({
                'success': True,
                'categories': categories
            })
        except:
            abort(404)

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route('/questions')
    def get_questions():
        current_cat_id = request.args.get('category', None, type=int)
        if current_cat_id:
            current_cat = Category.query.filter_by(
                id=current_cat_id).one_or_none()
            if current_cat == None:
                abort(404)
        else:
            current_cat = Category(type='All')

        questions_data = Question.query.all()
        categories_data = Category.query.all()

        all_questions = paginate_questions(request, questions_data)

        categories = {}
        for d in categories_data:
            categories.update({
                d.id: d.type
            })

        if len(all_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': all_questions,
            'totalQuestions': len(questions_data),
            'categories': categories,
            'currentCategory': current_cat.type
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @ app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(404)
            question.delete()

            return jsonify({
                'success': True,
            })
        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @ app.route('/questions', methods=['POST'])
    def create_question():
        current_cat_id = request.args.get('category', None, type=int)
        print(current_cat_id)
        if current_cat_id:
            current_cat = Category.query.filter_by(
                id=current_cat_id).one_or_none()
            if current_cat == None:
                abort(404)
        else:
            current_cat = Category(type='All')

        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)

        try:
            if search:
                if search is None or '':
                    abort(404)

                response = Question.query.order_by(Question.id).filter(
                    Question.question.ilike("%{}%".format(search)))

                questions_searched = []
                for d in response:
                    questions_searched.append({
                        "id": d.id,
                        "question": d.question,
                        "difficulty": d.difficulty,
                        "category": d.category
                    })

                return jsonify({
                    'success': True,
                    'questions': questions_searched,
                    'totalQuestions': len(questions_searched),
                    'currentCategory': current_cat.name

                })

            else:

                question = Question(
                    question=new_question,
                    answer=new_answer,
                    difficulty=new_difficulty,
                    category=new_category
                )
                question.insert()

                return jsonify({
                    'success': True,
                    'question': Question.id,
                    'answer': Question.answer,
                    'difficulty': Question.difficulty,
                    'categories': Question.categories
                })
        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @ app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):

        categories = Category.query.get(category_id).all()
        # Join(Category).filter(Category.id == category_id))

        current_questions = paginate_questions(request, categories.question)

        return jsonify({
            'questions': current_questions,
            'totalQuestions': len(current_questions),
            'currentCategory': categories.id
        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/quizzes', methods=['POST'])
    def show_quizzes():
        question = Question.query.get(Question).join(
            Category).filter(Category.id).all()

        current_question = random(question.id) + 1

        return jsonify({
            'previousQuestions': current_question - 1,
            'quiz_category': question.category
        })

    @app.route('/categories', methods=['POST'])
    def create_category():
        pass

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @ app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    @ app.errorhandler(404)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
        }), 404

    @ app.errorhandler(400)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @ app.errorhandler(405)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed"
        }), 405

    @ app.errorhandler(500)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Resource Not Found"
        }), 500

    return app
