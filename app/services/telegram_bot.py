from telegram.ext import Application, CommandHandler, MessageHandler, filters
from app.config import settings

class TelegramAgent:
    def __init__(self):
        self.app = Application.builder().token(settings.telegram_bot_token).build()
        self._setup_handlers()

    def _setup_handlers(self):
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    async def start(self, update, context):
        await update.message.reply_text("Привет! Я AI-агент. Чем помочь?")

    async def handle_message(self, update, context):
        # Логика обработки
        pass

    def run(self):
        self.app.run_polling()
