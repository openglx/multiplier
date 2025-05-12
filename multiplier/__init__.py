from flask import Flask, render_template, request
from uuid import uuid4, UUID
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import random

random.seed()

class OneResult:
    first: int
    second: int
    sent: datetime
    answer: int
    received: datetime
    score: str

    def __init__(self):
        self.first = random.randint(1, 12)
        self.second = random.randint(1, 12)
        self.sent = datetime.now()
        self.answer = None
        self.received = None
        self.score = None

@dataclass
class Session:
    results: list[OneResult] = field(default_factory=list)

def add_result(sessions: dict, uuid: UUID, iteration: int, answer: int, received: datetime):
    if not uuid in sessions:
        raise IndexError("We seem to have lost your session...")
    session = sessions[uuid]
    expected_iteration = len(session.results) - 1
    if expected_iteration != iteration:
        raise ValueError(f"Iteration mismatch, wanted {expected_iteration} got {iteration}, multiple tabs open?")
    result = session.results[iteration]
    result.answer = answer
    result.received = received
    score = "Correct" if answer == result.first * result.second else "Incorrect"
    score += ", too slow" if received - result.sent > timedelta(seconds=6) else ""
    result.score = score

sessions = {}

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    @app.route('/', methods=('GET', 'POST'))
    def hello():
        if request.method == 'POST':
            uuid = request.form['uuid']
            iteration = int(request.form['iteration'])
            answer = int(request.form['answer'])
            received = datetime.now()
            add_result(sessions, uuid, iteration, answer, received)
        else:
            uuid = str(uuid4())
            sessions[uuid] = Session()

        if len(sessions[uuid].results) > 9:
            return render_template("results.html", session=sessions[uuid])

        result = OneResult()
        sessions[uuid].results.append(result)
        return render_template(
            "numbers.html",
            uuid=uuid,
            iteration=len(sessions[uuid].results) - 1,
            first=result.first,
            second=result.second,
        )

    return app

