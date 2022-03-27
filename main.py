import discord #imports discord.py library
import os #imports os library; only used for getting the token. If you aren't using .env files, you don't need this
import requests #allows code to ake an HTTP request to get data fro the APU
import json #makes the data returned from the * request easier to work with
import random #allows the bot to choose randomly from a list of responses
from replit import db

client = discord.Client() #create an instance of a cient (connection to Discord)

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable"]

starter_encouragements = [
"Cheer up!",
"Hang in there.",
"You are a great person / bot"
]

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data =json.loads(response.text) #converts response from API to JSON
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  
  return(quote)

def update_encouragements(encouraging_message): #accepts an encouraging message as an argument
  if "encouragments" in db.keys(): #checks to see if "encouragements" already in the database. If so, it grabs the encouragement database and adds the message to the list
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragemets"] = encouragements
  else: #otherwise it creates a new key by that name nd the message is added as the first element in the list
    db["encouragements"] = [encouraging_message]

def deete_encouragement(index): #accepts an index as an argument
  encouragements = db["encouragements"]
  if len(encouragements) > index: #if the list is longer than the index provided, it deletes the encouragement at that index
    del encouragements[index]
  db["encouragements"] = encouragements
  
@client.event #registers an event; asynchronous, so done via callbacks
#A Callback is a function that is called when something else happens
async def on_ready():
  print('We have loggend in as  {0.user}'.format(client))

@client.event
async def on_message(message): #triggers each time a message is received, but we don't want it to if its from ourselves
  if message.author == client.user:
    return #if its sent from the same user, it does nothing

  msg = message.content
  
  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  optionss = starter_encouragements #making a copy of starter_encouragements;going to add the user_submitted messages to that before randomly picking one
  if "encouragements" in db.keys(): #"the user has submitted at least one custom message"
    options = options + db["encouragements"] #"add the custom message"

  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(starter_encouragements))

  if msg.startswith("$new"): 
    encouraging_message = msg.split("$new",1)[1] #message after $new will be split and used as a new encouraging_message
    update_encouragements(encouraging_message)
  await message.channel.send("New encouraging message added")

  if msg.startswith("$del"):
    encouoragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
      await message.channel.send(encouragements)
    

  if message.content.startswith('$hello'): #checks message content
    await message.channel.send('Hello!')


client.run(os.getenv('TOKEN'))
#.env files are used for declaring environment variables

