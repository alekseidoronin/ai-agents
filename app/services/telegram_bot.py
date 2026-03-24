import logging

from telegram.ext import Application, CommandHandler, MessageHandler, filters

from app.config import settings

logger = logging.getLogger("ai_agents.telegram")


class TelegramAgent:
    HELP_TEXT = (
        "Доступные команды:\n"
        "/start — начать работу\n"
        "/help — список команд\n"
        "/plan — создать контент-план\n"
        "/funnel — создать воронку продаж\n"
        "/analytics — запустить аналитику\n"
    )

    def __init__(self):
        self.app = Application.builder().token(settings.telegram_bot_token).build()
        self._setup_handlers()

    def _setup_handlers(self):
        self.app.add_handler(CommandHandler("start", self.cmd_start))
        self.app.add_handler(CommandHandler("help", self.cmd_help))
        self.app.add_handler(CommandHandler("plan", self.cmd_plan))
        self.app.add_handler(CommandHandler("funnel", self.cmd_funnel))
        self.app.add_handler(CommandHandler("analytics", self.cmd_analytics))
        self.app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )

    async def cmd_start(self, update, context):
        await update.message.reply_text(
            "Привет! Я AI-агент для бизнеса.\n\n" + self.HELP_TEXT
        )

    async def cmd_help(self, update, context):
        await update.message.reply_text(self.HELP_TEXT)

    async def cmd_plan(self, update, context):
        await update.message.reply_text(
            "Для создания контент-плана напишите:\n"
            "Продукт: <название>\nЦА: <описание аудитории>"
        )

    async def cmd_funnel(self, update, context):
        await update.message.reply_text(
            "Для создания воронки продаж напишите:\n"
            "Продукт: <название>\nЦА: <описание>\nТип: standard / webinar / tripwire"
        )

    async def cmd_analytics(self, update, context):
        await update.message.reply_text(
            "Для аналитики напишите:\n"
            "Данные: <описание данных>\nЦель: <что хотите узнать>"
        )

    async def handle_message(self, update, context):
        logger.info("Message from user %s: %s", update.effective_user.id, update.message.text)
        await update.message.reply_text(
            "Получил ваше сообщение. Используйте /help для списка команд."
        )

    def run(self):
        logger.info("Starting Telegram bot polling")
        self.app.run_polling()
