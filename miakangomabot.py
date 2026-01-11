# REMPLACE la fin de ton fichier par :
import os
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

def main():
    # Configuration
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    PORT = int(os.environ.get("PORT", 5000))
    
    # Création de l'app
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Handlers (comme avant)
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Mode webhook pour Render
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"https://telegram-falcon-bot.onrender.com/{TOKEN}"
    )

if __name__ == "__main__":
    main()
