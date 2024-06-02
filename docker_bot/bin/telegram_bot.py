from telegram import Update
from telegram.ext import ApplicationBuilder,CommandHandler,ContextTypes
import requests;

#queste due sono librerie già inglobate in python
import os;
import json 

i = 2016

#il bot ad una richiesta dell'utente fa richiesta all'api e li manda a logstash 
async def fixtures_function(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global i

    payload={}
    headers = {
    'x-rapidapi-key': str(os.environ["API-KEY"]),
    'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    #url = "https://v3.football.api-sports.io/standings?league=135&season=202"
    if( i < 2023):
       url = str(os.environ["URL"])+str(i)
       response = requests.request("GET", url, headers=headers, data=payload)

       json_object = json.loads(response.text)  #questo lo devo inviare a logstash
       r = requests.request("POST",url='http://10.0.100.22:8080',json=json_object)  #indirizzo ip di logstash nella rete dei container

       i = i +1

       await update.message.reply_text('Ok')
    else:
       await update.message.reply_text('Years Error')

    
token = os.environ["TOKEN"]    #token api telegram bot
app = ApplicationBuilder().token(token).build()

app.add_handler(CommandHandler("results",fixtures_function))

app.run_polling()

#potremmo predire risultati prossimi anni 