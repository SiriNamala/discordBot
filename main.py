import discord
import requests
import json
import random
import dbm

client = discord.Client()

sad_words = (
'sad', 'bitter', 'dismal', 'heartbroken', 'melancholy', 'mournful', 'sorry', 'blue', 'rejected', 'hurting', 'hurt',
'gloomy', 'grief', 'down', 'distressed', 'weep', 'cry', 'crying', 'low', 'troubled', 'dejected', 'despair', 'angry',
'depressed', 'depressing', 'miserable', 'unhappy')

starter_encouragements = ['Cheer up!', 'Hang in there', 'You are a great person!']

db = dbm.open('mydb','n')

def update_encouragements(message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(message)
        db["encouragements"] = encouragements

    else:
        db["encouragements"] = [message]


def delete_encouragement(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
    db["encouragements"] = encouragements


# helper function
def get_quote():
    response = requests.get("http://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + "-" + json_data[0]['a']
    return quote


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        await message.channel.send(message.author)

    if message.content.startswith("$inspire"):
        await message.channel.send(get_quote())

    msg = message.content

    options = starter_encouragements
    if "encouragements" in db.keys():
        options = options.extend(db["encouragements"])
    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(options))

    if msg.startswith("$new"):
        encouraging_message = msg.split("$new ", 1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send("New encouraging message added.")

    if msg.startswith("$del"):
        index = int(msg.split("$del ", 1)[1])
        # to send a list of all existing msgs after deletion
        encouragements = []
        if "encouragements" in db.keys():
            delete_encouragement(index)
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)


client.run('ODk2NDMwMDQ1NzAxMjI2NTA4.YWG_iQ.UffOA13JIkI92rhXmkvJoYqwShU')

