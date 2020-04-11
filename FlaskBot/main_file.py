from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import os

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from textblob import TextBlob

filenumber=int(os.listdir('saved_conversations')[-1])
filenumber=filenumber+1
file= open('saved_conversations/'+str(filenumber),"w+")
file.close()

app = Flask(__name__)

user_sentiment=0

english_bot = ChatBot('Bot',
             storage_adapter='chatterbot.storage.SQLStorageAdapter',
             logic_adapters=[
   {
       'import_path': 'chatterbot.logic.BestMatch'
   },
   
],
trainer='chatterbot.trainers.ListTrainer')
#english_bot.set_trainer(ListTrainer)
#bot = ListTrainer(english_bot)
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    global user_sentiment
    userText = request.args.get('msg')
    response = str(english_bot.get_response(userText))
    print(response)
    appendfile=os.listdir('saved_conversations')[-1]
    appendfile= open('saved_conversations/'+str(filenumber),"a")
    appendfile.write('user : '+userText+'\n')
    appendfile.write('bot : '+response+'\n')
    
    #print(TextBlob(userText).sentiment.polarity)
    sent = TextBlob(userText).sentiment.polarity
    print(sent)   
    user_sentiment = user_sentiment + sent 
    print(user_sentiment)
    appendfile.close()

    return response



if __name__ == "__main__":
    print('hi', user_sentiment)
    app.run()
    

