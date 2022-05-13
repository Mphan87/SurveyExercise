from flask import Flask, request, render_template, redirect, flash, jsonify, session
from random import randint, choice, sample
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey
RESPONSES = "responses"

app = Flask(__name__)

app.config['SECRET_KEY'] = "you can put something here"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    instructions = satisfaction_survey.instructions
    return render_template('home.html', instructions = instructions)


@app.route('/tracker')
def tracker():
    session[RESPONSES] = []
    return redirect("/question/0")


@app.route("/answer", methods=["POST"])
def handle_question():
    print(request.form)
    responses = session.get(RESPONSES)
    if "ANSWERNOW" in request.form:   
        choice = request.form["ANSWERNOW"]
    else:
        return redirect(f"/question/{len(responses)}")

    
    responses = session[RESPONSES]
    responses.append(choice)
    session[RESPONSES] = responses
    print(session[RESPONSES])
    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect("/complete")
 
    else:
        return redirect(f"/question/{len(responses)}")

@app.route("/question/<int:num>")
def pick_questions(num):
    responses = session.get(RESPONSES)
    questions = satisfaction_survey.questions[num]
    print(len(responses))

    # if (responses == None):
    #     return redirect("/")
    

    return render_template("questions.html", questions=questions)


@app.route("/complete")
def complete():
        return render_template("complete.html")
      