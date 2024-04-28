import os

QUIZ_CONFIG = eval(os.getenv("QUIZ_CONFIG"))


def get_quiz_options(quiz: dict):
    return [option["label"] for option in quiz.get("options", [])]


def quiz_list():
    """All quiz"""
    quizzes = [QUIZ_CONFIG]

    def helper(options):
        for option in options:
            if option.get("quiz"):
                quizzes.append(option.get("quiz"))
                helper(option.get("quiz")["options"])

    helper(QUIZ_CONFIG["options"])
    return quizzes


def get_quiz_by_id(*, id: str):
    return next(iter([quiz for quiz in quiz_list() if quiz["id"] == id]), None)
