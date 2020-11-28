"""app.py Server to validate client request"""
#pylint: disable=C0301
#pylint: disable=C0103
#pylint: disable=E1101
import os
import json
import random
import flask
from flask import request
import flask_socketio
import flask_sqlalchemy
import requests
import dotenv
from datetime import date, timedelta


dotenv.load_dotenv()

DICTIONARY_API_KEY = os.getenv('DICT_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

DATABASE_URI = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = flask_sqlalchemy.SQLAlchemy()
db.init_app(app)
db.app = app
import models


def messageDict(text):
    """ API call for dictionary """
    response = requests.get(f'https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{text}?key={DICTIONARY_API_KEY}')
    result = response.json()
    messageReceived = ''
    if 'shortdef' in result[0]:
        definition = result[0]['shortdef']
        messageReceived = ', '.join(definition)
    else:
        messageReceived = "Sorry, we can't find the definition of the term you are looking for."
    return messageReceived


@app.route('/')
def index():
    """ Render function """
    return flask.render_template('index.html')


@socketio.on('new feedback')
def on_new_feedback(data):
    """ when receiving new feedback """

    name = data["name"]
    feedback = data["feedback"]
    db.session.add(models.FeedbackLog(name, feedback))
    db.session.commit()

    print("Recieved name: ", name)
    print("Received feedback: ", feedback)


@socketio.on('connect user')
def on_connect(userProfile):
    """ User's profile validating """
    socketId = request.sid
    name = userProfile['name']
    email = userProfile['email']
    image = userProfile['imageUrl']

    socketio.emit('new connection', {
        "user": name,
        "userEmail": email,
        "userImage": image
    }, room=socketId)


@socketio.on('send message')
def send_message(text):
    """ finding synonym for word entered by user. """
    socketId = request.sid
    messageReceived = messageDict(text)
    socketio.emit('forward message', {
        'messageReceived': messageReceived
    }, room=socketId)


@socketio.on('request quiz')
def request_quiz():
    """ Selects random quiz questions (one per question group) and sends to user """
    
    groups = {}
    for row in db.session.query(models.QuizQuestions).all():
        if row.group_name not in groups:
            groups[row.group_name] = []
        
        groups[row.group_name].append({'text': row.text, 'multiplier': row.multiplier})

    group_names = list(groups.keys())
    random.shuffle(group_names)

    quiz_out = []

    for name in group_names:
        group = groups[name]
        question_index = random.randrange(len(group))

        quiz_out.append(group[question_index])

    sid = flask.request.sid
    socketio.emit('quiz generated', quiz_out, room=sid)


def api_call_for_news():
    """ API call for News """
    today = date.today()
    yesterday = today - timedelta(days = 1)
    url = 'https://newsapi.org/v2/everything'
    parameters = {
        'q': 'politics',  # query phrase
        'from': yesterday,
        'language': 'en',
        'sortBy': 'relevancy',
        'pageSize': 15,  # maximum is 100
        'apiKey': NEWS_API_KEY
    }

    response = requests.get(url, params=parameters)
    response_json = response.json()

    return response_json["articles"]

@socketio.on('news api call')
def news_api_call():
    """ sending news back to client """
    print("Got an event for newz:")
    news_list = api_call_for_news()
    newsObjectLst = []

    for news in news_list:
        if news["content"] == None:
            final_news_content = "To read full article... "
        else:
            news_content = news["content"].split("…")
            final_news_content = str(news_content[0]) + "(continue reading)... "
        
        newsObjectLst.append(
            {
                'title': news["title"],
                'author': news["author"],
                'content': final_news_content,
                'published': news["publishedAt"],
                'source': news["source"]["name"],
                'url': news["url"],
                'img': news["urlToImage"]
            }
        )

    socketio.emit('newsData', {
        'newsObjectLst': newsObjectLst
    })

    return newsObjectLst


def load_quiz_questions():
    """ Loads the questions for the quiz into the database from the questions JSON file """
    
    db.session.query(models.QuizQuestions).delete()
    
    questions_file = open('quiz_questions.json', 'r')
    questions_json = json.load(questions_file)
    questions_file.close()
    
    for group in questions_json['groups']:
        group_name = group['groupName']
        for question in group['questions']:
            db.session.add(models.QuizQuestions(question['text'], group_name, question['multiplier']))
    
    db.session.commit()
    

if __name__ == '__main__':
    models.db.create_all()
    load_quiz_questions()
    
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
