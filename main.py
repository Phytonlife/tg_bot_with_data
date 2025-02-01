from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import asyncio
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JobBot:
    def __init__(self):
        self.db = Database()
        self.app = Application.builder().token(TELEGRAM_TOKEN).build()
        self.setup_handlers()

    def setup_handlers(self):
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("import", self.import_jobs))
        self.app.add_handler(CommandHandler("publish", self.publish_jobs))
        self.app.add_handler(CallbackQueryHandler(self.handle_button))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Bot started! Use /import to import jobs and /publish to publish them.")

    async def import_jobs(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            jobs = parse_xml_jobs('jobs.xml')
            for job in jobs:
                self.db.insert_job(job)
            await update.message.reply_text(f"Imported {len(jobs)} jobs successfully!")
        except Exception as e:
            await update.message.reply_text(f"Error importing jobs: {str(e)}")

    async def publish_jobs(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            # Публикация новых объявлений
            jobs = self.db.get_unpublished_jobs()
            for job in jobs:
                keyboard = [[InlineKeyboardButton("Откликнуться",
                                                  url="https://www.karriere.at/profil/anlegen")]]
                reply_markup = InlineKeyboardMarkup(keyboard)

                template = get_post_template(job['post_style'])
                message_text = template.format(**job)

                message = await context.bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=message_text,
                    reply_markup=reply_markup
                )

                telegram_link = f"https://t.me/c/{CHANNEL_ID}/{message.message_id}"
                self.db.update_job_status(job['id'], telegram_link)

            # Удаление истекших объявлений
            expired_jobs = self.db.get_expired_jobs()
            for job_id, telegram_link in expired_jobs:
                try:
                    message_id = int(telegram_link.split('/')[-1])
                    await context.bot.delete_message(chat_id=CHANNEL_ID, message_id=message_id)
                    self.db.update_job_status(job_id, None)
                except Exception as e:
                    logger.error(f"Error deleting message: {str(e)}")

            await update.message.reply_text("Jobs published and expired posts cleaned up!")
        except Exception as e:
            await update.message.reply_text(f"Error publishing jobs: {str(e)}")

    async def handle_button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

    def run(self):
        self.app.run_polling()


if __name__ == '__main__':
    bot = JobBot()