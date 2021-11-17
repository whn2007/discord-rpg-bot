import os
import discord
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

#allows bot to track members and actions
intents = discord.Intents()
intents.members = True

#words that bot will react to
trigger_words = [
  "attack",
  "magic"
]

commands = [
  "$help",
  "$new",
  "$del",
  "attack",
  "magic",
  "$attack_list",
  "$magic_list",
  "responding"
]

#turns on automatically
if "responding" not in db.keys():
  db["responding"] = True

#add to list of abilities, such as attacks or magic
def update_whatever(category, some_message):
  if category == "attacks":
    if "attacks" in db.keys():
      attacks = db["attacks"]
      attacks.append(some_message)
      db["attacks"] = attacks
    else:
      db["attacks"] = [some_message]
    
  elif category == "magic":
    if "magic" in db.keys():
      magic = db["magic"]
      magic.append(some_message)
      db["magic"] = magic
    else:
      db["magic"] = [some_message]

#deletes an ability from list
def delete_ability(category, index):
  if category == "attacks":
    if "attacks" in db.keys():
      attacks = db["attacks"]
      if len(attacks) > index:
        attacks.pop(index)
        db["attacks"] = attacks
        return True
  
  elif category == "magic":
    if "magic" in db.keys():
      magic = db["magic"]
      if len(magic) > index:
        magic.pop(index)
        db["magic"] = magic
        return True
  
  else:
    return False

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  attacks = []
  magic = []

  #adds possibile abilities to lists
  if "attacks" in db.keys():
    attacks += db["attacks"]
  if "magic" in db.keys():
    magic += db["magic"]

  #if program is on
  if db["responding"]:

    if any(word in msg.lower() for word in trigger_words):
      temp_msg = msg.lower()
      if "$" not in temp_msg:
        if "attack" in temp_msg:
          await message.channel.send(random.choice(attacks))
        elif "magic" in msg.lower():
          await message.channel.send(random.choice(magic))

    if msg.lower().startswith("hello"):
      await message.channel.send("Hello!")

    #add to list with command: $new 'ability' 'name'
    if msg.startswith("$new"):
      new_message = msg.split()
      if len(new_message) == 3:
        update_whatever(new_message[1], new_message[2])
        await message.channel.send("Successfully added.")
      else:
        await message.channel.send("Failed to add.")

    if msg.startswith("$del"):
      new_message = msg.split()
      if len(new_message) == 3 and new_message[2] in "0123456789":
        if delete_ability(new_message[1],int(new_message[2])):
          await message.channel.send("Successfully deleted.")
        else:
          await message.channel.send("Failed to delete.")
      else:
        await message.channel.send("Failed to delete.")
  
    #lists attack list
    if msg.startswith("$attack_list"):
      temp = attacks
      await message.channel.send("Attacks: {}".format(temp))

    #lists magic list
    if msg.startswith("$magic_list"):
      await message.channel.send("Magic: {}".format(magic))

    #lists commands and further help
    if msg.startswith("$help"):
      await message.channel.send("For more help, type $help/<name of command> ")
      await message.channel.send("Commands:")
      for command in commands:
        await message.channel.send(command)

  if msg.startswith("$responding"):
    value = msg.split("$responding ", 1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Bot responding!")

    elif value.lower() == "false":
      db["responding"] = False
      await message.channel.send("Bot shutting down.")


keep_alive()
client.run(os.getenv('TOKEN'))