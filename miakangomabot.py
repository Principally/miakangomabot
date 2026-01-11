import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# 🔧 Configuration
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
HF_API_KEY = os.getenv("HF_API_KEY")

# 🔗 API Falcon 180B
FALCON_API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-180B-chat"

HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

# 📝 Configuration du logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def ask_falcon(prompt: str) -> str:
    """
    Interroge le modèle Falcon via Hugging Face API
    """
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 300,
            "temperature": 0.7,
            "top_p": 0.9,
            "return_full_text": False
        }
    }
    
    try:
        response = requests.post(
            FALCON_API_URL, 
            headers=HEADERS, 
            json=payload, 
            timeout=90
        )
        response.raise_for_status()
        
        data = response.json()
        return data[0]["generated_text"]
        
    except requests.exceptions.Timeout:
        return "⚠️ Le modèle met trop de temps à répondre. Réessaie avec une question plus courte."
    except Exception as e:
        logger.error(f"Erreur Falcon API: {e}")
        return f"❌ Erreur technique: {str(e)}"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Gère les messages entrants sur Telegram
    """
    user = update.effective_user
    user_text = update.message.text
    
    logger.info(f"Message de {user.first_name}: {user_text}")
    
    # Afficher "typing..." pendant la génération
    await update.message.chat.send_action(action="typing")
    
    prompt = f"""
Tu es Falcon, un assistant IA intelligent, clair et utile.
Réponds en français de manière précise et concise.

Question : {user_text}

Réponse :
"""
    
    try:
        answer = ask_falcon(prompt)
        
        # Tronquer si trop long pour Telegram (max 4096 caractères)
        if len(answer) > 4000:
            answer = answer[:3997] + "..."
            
        await update.message.reply_text(answer)
        
    except Exception as e:
        logger.error(f"Erreur: {e}")
        await update.message.reply_text(
            "⚠️ Désolé, une erreur est survenue. "
            "Réessaie dans quelques instants."
        )

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Commande /start
    """
    welcome_text = """
🤖 *Bonjour ! Je suis FalconBot*

Je suis connecté à Falcon 180B, un modèle d'IA avancé.

*Comment m'utiliser :*
• Pose-moi n'importe quelle question
• Je répondrai de manière détaillée
• Sois patient, les réponses peuvent prendre 15-30 secondes

_Pose ta première question !_
"""
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Commande /help
    """
    help_text = """
📚 *Aide*

• Envoie simplement un message et je te répondrai
• Les réponses sont générées par Falcon 180B
• Limite : ~300 tokens par réponse
• Temps de réponse : 15-30 secondes

_Problèmes ? Contacte mon créateur._
"""
    await update.message.reply_text(help_text, parse_mode="Markdown")

def main():
    """
    Point d'entrée principal
    """
    # Vérification des tokens
    if not TELEGRAM_TOKEN or not HF_API_KEY:
        logger.error("Tokens manquants ! Configure TELEGRAM_TOKEN et HF_API_KEY")
        return
    
    # Création de l'application
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Gestionnaires
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Commandes
    from telegram.ext import CommandHandler
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    
    # Démarrer le bot
    logger.info("🚀 Bot démarré...")
    app.run_polling(
        drop_pending_updates=True,
        allowed_updates=Update.ALL_TYPES
    )

if __name__ == "__main__":
    main()