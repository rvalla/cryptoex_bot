from telegram.ext import (
			Application, InlineQueryHandler, CommandHandler,
			CallbackQueryHandler, ContextTypes, ConversationHandler,
			MessageHandler, filters
)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
import traceback, logging
import json as js
from messages import Messages
from usage import Usage
from text import Text

config = js.load(open("config.json")) #The configuration file...
en_users = set() #Saving chat ids from users who prefer english...
us = Usage("usage.csv", "errors.csv") #The class to save activity data...
msg = Messages() #The class to build content of text messages...
txt = Text() #Working with text...
CAESAR_K, CAESAR_M, ERROR_1, ERROR_2 = range(4) #The conversation states...

#Welcome message fot people who start the bot...
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	id = update.effective_chat.id
	logging.info(str(hide_id(id)) + " started the bot...")
	await context.bot.send_message(chat_id=id, text=msg.get_message("hello", get_language(id)), parse_mode=ParseMode.HTML)

#Starting a caesar cipher session...
async def trigger_caesar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	id = update.effective_chat.id
	us.add_caesar()
	logging.info(str(hide_id(id)) + " starts caesar conversation...")
	await context.bot.send_message(chat_id=id, text=msg.get_message("caesar_1", get_language(id)), parse_mode=ParseMode.HTML)
	return CAESAR_K

#Asking for a caesar cipher key...
async def caesar_key(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	id = update.effective_chat.id
	text = update.message.text
	try:
		the_key = int(text)
		context.chat_data["caesar_key"] = the_key
		await context.bot.send_message(chat_id=id, text=msg.get_message("caesar_2", get_language(id)), parse_mode=ParseMode.HTML)
		return CAESAR_M
	except:
		await context.bot.send_message(chat_id=id, text=msg.get_message("caesar_3", get_language(id)), parse_mode=ParseMode.HTML)
		return CAESAR_K

#Recieving messages to encrypt...
async def caesar_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	id = update.effective_chat.id
	text = update.message.text
	key = context.chat_data["caesar_key"]
	m = txt.caesar_cypher(key, key, text, get_language(id))
	await context.bot.send_message(chat_id=id, text=m, parse_mode=ParseMode.HTML)
	return CAESAR_M

#Starting an error report session...
async def trigger_error_submit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	id = update.effective_chat.id
	logging.info(str(hide_id(id)) + " wants to report an error...")
	await context.bot.send_message(chat_id=id, text=msg.get_apology(get_language(id)), parse_mode=ParseMode.HTML)
	await context.bot.send_message(chat_id=id, text=msg.get_message("submit_error_1", get_language(id)), parse_mode=ParseMode.HTML)
	return ERROR1

#Saving error related command...
async def report_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	id = update.effective_chat.id
	m = update.message.text
	context.chat_data["error_command"] = m
	await context.bot.send_message(chat_id=id, text=msg.get_message("submit_error_2", get_language(id)), parse_mode=ParseMode.HTML)
	return ERROR2

#Saving error description...
async def report_error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	id = update.effective_chat.id
	m = context.chat_data["error_command"]
	m2 = update.message.text
	context.chat_data["error_description"] = m2
	us.add_error_report()
	us.save_error_report(m, m2, str(hide_id(id)))
	admin_msg = "Error reported:\n-command: " + m + "\n-description: " + m2
	await context.bot.send_message(chat_id=config["admin_id"], text=admin_msg, parse_mode=ParseMode.HTML)
	await context.bot.send_message(chat_id=id, text=msg.get_message("submit_error_3", get_language(id)), parse_mode=ParseMode.HTML)
	return ConversationHandler.END

#Ending any convertation...
async def end_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	id = update.effective_chat.id
	logging.info(str(hide_id(id)) + " endss a conversation...")
	await context.bot.send_message(chat_id=id, text=msg.get_message("end_conversation", get_language(id)), parse_mode=ParseMode.HTML)
	return ConversationHandler.END

#Printing help command...
async def print_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	id = update.effective_chat.id
	logging.info(str(hide_id(id)) + " asked for help...")
	await context.bot.send_message(chat_id=id, text=msg.get_message("help", get_language(id)), parse_mode=ParseMode.HTML)
	await context.bot.send_message(chat_id=id, text=msg.get_message("help2", get_language(id)), parse_mode=ParseMode.HTML)

#Getting user preffered language...
def get_language(id):
	if id in en_users:
		return 1
	else:
		return 0

#Setting up language for active user...
async def select_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	id = update.effective_chat.id
	logging.info(str(hide_id(id)) + " will set language...")
	keyboard = [[InlineKeyboardButton(text="Español", callback_data="l_0"),
				InlineKeyboardButton(text="English", callback_data="l_1")]]
	reply = InlineKeyboardMarkup(keyboard)
	await context.bot.send_message(chat_id=id, text=msg.get_message("language", get_language(id)), reply_markup=reply, parse_mode=ParseMode.HTML)

#Setting up language for active user...
async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE, query) -> None:
	id = update.effective_chat.id
	if query == "l_1":
		logging.info("English is the language selected by " + str(hide_id(id)))
		en_users.add(id)
		await context.bot.send_message(chat_id=id, text=msg.get_message("language2", get_language(id)), parse_mode=ParseMode.HTML)
	else:
		logging.info("Spanish is the language selected by " + str(hide_id(id)))
		en_users.discard(id)
		await context.bot.send_message(chat_id=id, text=msg.get_message("language3", get_language(id)), parse_mode=ParseMode.HTML)

#Processing button clicks...
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	query = update.callback_query
	query.answer()
	if query.data.startswith("l"):
		await set_language(update, context, query.data)

#Sending a message to the admin in case of any error...
async def error_notification(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	id = update.effective_chat.id
	m = "An error ocurred! While comunicating with chat " + str(hide_id(id))
	logging.info(m)
	await context.bot.send_message(chat_id=config["admin_id"], text=m, parse_mode=ParseMode.HTML)

#Hiding the first numbers of a chat id for the log...
def hide_id(id):
	s = str(id)
	return "****" + s[len(s)-4:]

#Building the conversation handler...
def build_conversation_handler():
	print("Building conversation handler...", end="\n")
	handler = ConversationHandler(
		entry_points=[CommandHandler("caesar", trigger_caesar),CommandHandler("error", trigger_error_submit)],
		states={
			CAESAR_K: [MessageHandler(filters.TEXT & ~filters.COMMAND, caesar_key)],
			CAESAR_M: [MessageHandler(filters.TEXT & ~filters.COMMAND, caesar_message)],
			ERROR_1: [MessageHandler(filters.TEXT, report_command)],
			ERROR_2: [MessageHandler(filters.TEXT & ~filters.COMMAND, report_error)],
		},
		fallbacks=[MessageHandler(filters.COMMAND, end_conversation)]
		)
	return handler

def main() -> None:
	if config["logging"] == "persistent":
		logging.basicConfig(filename="history.txt", filemode='a',level=logging.INFO,
						format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	elif config["logging"] == "debugging":
		logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	else:
		logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	app = Application.builder().token(config["token"]).build()
	#app.add_error_handler(error_notification)
	app.add_handler(CommandHandler("start", start), group=2)
	app.add_handler(CommandHandler("language", select_language), group=2)
	app.add_handler(CommandHandler("help", print_help), group=2)
	app.add_handler(CallbackQueryHandler(button_click), group=2)
	app.add_handler(build_conversation_handler(), group=1)
	#app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, out_of_context), group=1)
	if config["webhook"]:
		wh_url = "https://" + config["public_ip"] + ":" + str(config["webhook_port"]) + "/" + config["webhook_path"]
		updater.start_webhook(listen="0.0.0.0", port=config["webhook_port"], url_path=config["webhook_path"], key="webhook.key",
							cert="webhook.pem", webhook_url=wh_url, drop_pending_updates=True)
	else:
		app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
	main()
