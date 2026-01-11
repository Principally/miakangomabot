\# Telegram Falcon Bot



Bot Telegram connecté à Falcon 180B via Hugging Face API.



\## Déploiement sur Heroku



1\. Clone le dépôt

2\. Configure les variables d'environnement

3\. Déploie sur Heroku



\## Variables d'environnement

\- `TELEGRAM\_TOKEN`: Token du bot Telegram

\- `HF\_API\_KEY`: Token Hugging Face (READ)



\## Développement local

```bash

pip install -r requirements.txt

TELEGRAM\_TOKEN="xxx" HF\_API\_KEY="yyy" python bot.py

