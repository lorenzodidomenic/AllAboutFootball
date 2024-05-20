from telegram import Update
from telegram.ext import ApplicationBuilder,CommandHandler,ContextTypes
import requests;
import os;

async def fixtures_function(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    payload={}
    headers = {
    'x-rapidapi-key': 'de48be3afdca7c3582798fb0273f6915',
    'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    url = "https://v3.football.api-sports.io/fixtures?season=2023&league=135"
    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)
    await update.message.reply_text('Hello, request to Football Api done')

token = os.environ["TOKEN"]    #token api telegram bot
app = ApplicationBuilder().token(token).build()


app.add_handler(CommandHandler("results",fixtures_function))

app.run_polling()


#potremmo predire risultati prossimi anni 