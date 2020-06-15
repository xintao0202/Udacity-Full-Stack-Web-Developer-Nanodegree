# Full Stack API Final Project

## Full Stack Trivia

This API is to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out. Functionalities of the API includes 

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

##  Install project dependencie

1. Folk starter code and instructios from [GitHub Repo](https://github.com/udacity/FSND/tree/master/projects/02_trivia_api/starter/backend) 

2. Install Python 3, pip, node, flask, curl, Postgres.

### Backend dependencie
1. Install PIP depdendencies `pip install requirements.txt`. Key Depedences: Flask, SQLAlchemy, CURL and Flask-CORS
2. Create database `dropdb trivia` and `createdb trivia`, Then with Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run `psql trivia < trivia.psql`
3. To run unittest, run `psql trivia_test < trivia.psql` and `python test_flaskr.py` in terminal after test database created  
4. From within the backend directory first ensure using created virtual environment
5. Start backend server. Backend server location http://127.0.0.1:5000/
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
6. Working on Windows OS

```
cmd /c  'psql trivia postgres< trivia.psql'
$env:FLASK_APP = "flaskr"
set FLASK_ENV=development
python -m flask run
```
### Frontend dependencie
1. Installing Node and NPM. Node can be download from https://nodejs.com/en/download. After Node installed and system variable set, install npm `npm install`
2. Make sure backend server is running. run npm in another terminal as follows
3. The frontend app was built using create-react-app. In order to run the app in development mode use `npm start`. You can change the script in the package.json file. Open http://localhost:3000 to view it in the browser. The page will reload if you make edits.
 
## API endpoints and expected behavior
### Overview
- GET '/categories'
- GET '/questions'
- GET '/categories/<int:id>/questions'
- POST '/questions'
- POST '/search'
- DELETE '/questions/<int:id>'
- POST '/quizzes'

#### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with two keys, 'categories', that contains a object of id: category_string key:value pairs, and 'success' boolean value.
- Curl Request and Server Response example: `curl http://127.0.0.1:5000/categories`
```
 {
      "categories": {
          "1": "Science", 
          "2": "Art", 
          "3": "Geography", 
          "4": "History", 
          "5": "Entertainment", 
          "6": "Sports"
      }, 
      "success": true
  }
  ```

  #### - GET '/questions'
  - Fetches a list questions paginated of length 10. Also include categorie info and total number of questions
  - Request Arguments: None
  - Returns: An object with three keys- 'categories', 'questions', 'total_questions'. 
  - Curl Request and Server Response example: `curl http://127.0.0.1:5000/questions`

  ```
  {
   "categories":{
      "1":"Science",
      "2":"Art",
      "3":"Geography",
      "4":"History",
      "5":"Entertainment",
      "6":"Sports"
   },
   "questions":[
      {
         "answer":"Maya Angelou",
         "category":4,
         "difficulty":2,
         "id":5,
         "question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
      },
      {
         "answer":"Muhammad Ali",
         "category":4,
         "difficulty":1,
         "id":9,
         "question":"What boxer's original name is Cassius Clay?"
      },
      {
         "answer":"Tom Cruise",
         "category":5,
         "difficulty":4,
         "id":4,
         "question":"What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
      },
      {
         "answer":"Brazil",
         "category":6,
         "difficulty":3,
         "id":10,
         "question":"Which is the only team to play in every soccer World Cup tournament?"
      },
      {
         "answer":"Uruguay",
         "category":6,
         "difficulty":4,
         "id":11,
         "question":"Which country won the first ever soccer World Cup in 1930?"
      },
      {
         "answer":"George Washington Carver",
         "category":4,
         "difficulty":2,
         "id":12,
         "question":"Who invented Peanut Butter?"
      },
      {
         "answer":"Lake Victoria",
         "category":3,
         "difficulty":2,
         "id":13,
         "question":"What is the largest lake in Africa?"
      },
      {
         "answer":"The Palace of Versailles",
         "category":3,
         "difficulty":3,
         "id":14,
         "question":"In which royal palace would you find the Hall of Mirrors?"
      },
      {
         "answer":"Agra",
         "category":3,
         "difficulty":2,
         "id":15,
         "question":"The Taj Mahal is located in which Indian city?"
      },
      {
         "answer":"Escher",
         "category":2,
         "difficulty":1,
         "id":16,
         "question":"Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
      }
   ],
   "total_questions":33
}
  
```

#### GET '/categories/<int:id>/questions'
- Get the questions based on category
- Request Arguments: category_id
- Returns: An object with four keys- 'current_category', 'questions', 'total_questions' and 'success'
- Curl Request and Server Response example: `curl http://127.0.0.1:5000/categories/1/questions`

```
{
   "current_catetory":1,
   "questions":[
      {
         "answer":"The Liver",
         "category":1,
         "difficulty":4,
         "id":20,
         "question":"What is the heaviest organ in the human body?"
      },
      {
         "answer":"Alexander Fleming",
         "category":1,
         "difficulty":3,
         "id":21,
         "question":"Who discovered penicillin?"
      },
      {
         "answer":"Blood",
         "category":1,
         "difficulty":4,
         "id":22,
         "question":"Hematology is a branch of medicine involving the study of what?"
      }
   ],
   "success":true,
   "total_questions":3
}
```
#### POST '/questions'
- Create a question in the format of JSON 
- Request Arguments: A Json object contains 'question', 'answer', 'difficulty' and 'category'
- Returns: A object with two keys- 'success', and 'created' shows the id of the new question
- Curl Request and Server Response example: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{ "question": "What is higest animal the world?", "answer": "Giraffes", "difficulty": 1, "category": "3" }'`
```
{
     'success': True,
     'created': 40
}
```

#### DELETE '/questions/<int:id>'
- Delete a question by id 
- Request Arguments: question_id
- Returns: A object with two keys- 'success', and 'deleted' shows the id of the question deleted
- Curl Request and Server Response example: `curl http://127.0.0.1:5000/questions/11 -X DELETE` 
```
{
        'success': True,
        'deleted': 11
}

```

#### POST '/quizzes'
- Get questions to play the quiz
- Request Arguments: 'previous_questions' which is what question has been tested, and 'quiz_category' which is the category the quiz be set on.
- Returns: A object with two keys- 'success', and 'question' shows question object of the quiz question
- Curl Request and Server Response example: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [4, 2], "quiz_category": {"type": "Art", "id": "6"}}'`

```
{
    "success": true
    "question": {
        "answer": "Alexander Fleming", 
        "category": 1, 
        "difficulty": 3, 
        "id": 21, 
        "question": "Who discovered penicillin?"
    }
}
```

#### POST '/search'
- Search for questions using a search term
- Request Arguments:Search term from POST method
- Returns: A object with three keys- 'success', and 'questions' that is a list of question object of the search result and 'total_questions' showing number of search results
- Curl Request and Server Response example: `curl http://127.0.0.1:5000/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "who"}'`

```
 {
      "success": true,
      "questions": [
          {
              "answer": "Maya Angelou", 
              "category": 4, 
              "difficulty": 2, 
              "id": 5, 
              "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
          }, 
          {
              "answer": "George Washington Carver", 
              "category": 4, 
              "difficulty": 2, 
              "id": 12, 
              "question": "Who invented Peanut Butter?"
          }, 
          {
              "answer": "Alexander Fleming", 
              "category": 1, 
              "difficulty": 3, 
              "id": 21, 
              "question": "Who discovered penicillin?"
          }
      ],  
      "total_questions": 3
  }
```

### Error handling
- Errors are in Json format
- Type of errors: 

    400: Bad request error 
    404: Resource not found
    405: method not allowed
    500: Interal Server error
    422: unprocessable

- Example 
```
{
          'success': False,
          'error': 500,
          'message': 'An error has occured, please try again'
      }
```