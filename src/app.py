import os

from telegram import Poll, Update
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    PollAnswerHandler,
)

from .utils import get_quiz_by_id, get_quiz_options

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

QUIZ_CONFIG = eval(os.getenv("QUIZ_CONFIG"))


class NestedQuiz:
    def __init__(self) -> None:
        self.application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

        start_handler = CommandHandler("start", self.start)
        self.application.add_handler(start_handler)
        self.application.add_handler(PollAnswerHandler(self.receive_poll_answer))

    def run(self):
        self.application.run_polling()

    def get_poll(self, id: str = None):
        if not id:
            id = QUIZ_CONFIG["id"]
        quiz_config = get_quiz_by_id(id=id)

        return quiz_config["id"], {
            "question": quiz_config["title"],
            "options": get_quiz_options(quiz_config),
            "type": Poll.REGULAR,
            "is_anonymous": False,
            "allows_multiple_answers": False,
        }

    async def send_poll(
        self,
        *,
        update: Update,
        chat_id: int,
        context: ContextTypes.DEFAULT_TYPE,
        quiz_id: str,
    ):
        poll_id, poll = self.get_poll(quiz_id)
        message = await context.bot.send_poll(chat_id, **poll)

        # Save some info about the poll the bot_data for later use in receive_poll_answer
        payload = {
            message.poll.id: {
                "poll_id": poll_id,
                "message_id": message.message_id,
                "chat_id": chat_id,
                "answers": 0,
            }
        }

        context.bot_data.update(payload)

        return message

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.send_poll(
            update=update,
            chat_id=update.effective_chat.id,
            context=context,
            quiz_id=None,
        )
        context.bot.send_poll()

    async def receive_poll_answer(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """ """

        answer = update.poll_answer
        answered_poll = context.bot_data[answer.poll_id]
        try:
            poll_id = answered_poll["poll_id"]
        # this means this poll answer update is from an old poll, we can't do our answering then
        except KeyError:
            return

        answered_quiz = get_quiz_by_id(id=poll_id)
        selected_option = answer.option_ids[0]
        chosed_option = answered_quiz["options"][selected_option]
        next_quiz = chosed_option.get("quiz")
        if next_quiz:
            await self.send_poll(
                update=update,
                chat_id=answered_poll["chat_id"],
                context=context,
                quiz_id=next_quiz["id"],
            )
            context.bot.send_poll()
        message_to_user = chosed_option.get("message_to_user")

        if message_to_user:
            await context.bot.send_message(
                answered_poll["chat_id"], message_to_user, parse_mode=ParseMode.HTML
            )
