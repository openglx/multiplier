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
    story: list[str] = field(default_factory=list)
    question_time: bool = False


def add_result(session: Session, iteration: int, answer: int, received: datetime):
    expected_iteration = len(session.results) - 1
    if expected_iteration != iteration:
        raise ValueError(
            f"Iteration mismatch, wanted {expected_iteration} got {iteration}, multiple tabs open?"
        )
    result = session.results[iteration]
    result.answer = answer
    result.received = received
    score = "Correct" if answer == result.first * result.second else "Incorrect"
    score += ", too slow" if received - result.sent > timedelta(seconds=6) else ""
    result.score = score


def space_explorer():
    return [
        # 0
        """You are commanding a spacecraft and must input the
        coordinates for next sectors to explore. The coordinates
        are always the result of the multiplication of two factors.
        Enter carefully and you will reach your destination.
        """,
        # 1
        """You have reached a new sector - there is a star system nearby.
        Navigate towards it.""",
        # 2
        """As you approach the gas giants at the edge of the star system,
        avoid their gravity well.
        """,
        # 3
        """You are past the gas giants, avoid the asteroid belt.""",
        # 4
        """Scan the inner planets for any life signs.""",
        # 5
        """A faint signal was detected, reach closer.""",
        # 6
        """You are listening to the echo of your own radar, nothing else
        to see here. Move on to next star system.""",
        # 7
        """Continue searching...""",
        # 8
        """Navigate to this nebula to recharge your dilithium reserves.""",
        # 9
        """Resume your search!""",
    ]


sessions = {}


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    @app.route("/", methods=("GET", "POST"))
    def hello():
        if request.method == "POST":
            uuid = request.form["uuid"]
            session = sessions[uuid]
            session.question_time = not session.question_time

            if story := request.form.get("story"):
                if not session.story:
                    if story == "space_explorer":
                        session.story = space_explorer()
                    else:
                        raise ValueError("I don't know this story...")
            else:
                iteration = int(request.form["iteration"])
                answer = int(request.form["answer"])
                received = datetime.now()
                add_result(session, iteration, answer, received)
        else:
            uuid = str(uuid4())
            sessions[uuid] = Session()
            session = sessions[uuid]

        if len(session.results) > 9:
            return render_template("results.html", session=session)

        if not session.story:
            return render_template("pick_story.html", uuid=uuid)

        if session.question_time:
            result = OneResult()
            session.results.append(result)
            return render_template(
                "numbers.html",
                uuid=uuid,
                iteration=len(session.results) - 1,
                first=result.first,
                second=result.second,
            )
        else:
            return render_template(
                "story.html",
                uuid=uuid,
                message=session.story[len(session.results)],
            )

    return app
