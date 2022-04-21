
from datetime import timedelta, datetime
import datetime

from aiogram import Bot, Dispatcher, executor, types

import logging
logging.basicConfig(level=logging.INFO)

token = "TOKEN"
bot = Bot(token = token)
dp = Dispatcher(bot)
users = []
muted = []
spam = []
def adduser(userinfo,users):
   if userinfo not in users:
       users.append(userinfo)
@dp.message_handler(content_types=["left_chat_member","new_chat_members"])
async def ff(message:types.Message):
    await bot.delete_message(message.chat.id,message.message_id)

@dp.message_handler(commands=["ban"])
async  def kick(message:types.Message):

    admins = await message.chat.get_administrators()

    for i in admins:
        if i['user']['first_name'].strip() == message.from_user.first_name.strip():

            await bot.ban_chat_member(message.chat.id,message.reply_to_message.from_user.id,timedelta(minutes=1))
    await  bot.delete_message(message.chat.id, message.message_id)
@dp.message_handler(commands=["kick"])
async  def kick(message:types.Message):

    admins = await message.chat.get_administrators()

    for i in admins:
        if i['user']['first_name'].strip() == message.from_user.first_name.strip():

            await bot.kick_chat_member(message.chat.id,message.reply_to_message.from_user.id)
    await  bot.delete_message(message.chat.id, message.message_id)
@dp.message_handler(commands=["unmute"])
async def mute(message: types.Message):

    admins = await message.chat.get_administrators()

    for i in admins:
        if i['user']['first_name'].strip() == message.from_user.first_name.strip():

            muted.remove(message.from_user.id)
    await  bot.delete_message(message.chat.id, message.message_id)
@dp.message_handler(commands=["mute"])
async  def mute(message : types.Message):
    if  message.reply_to_message:


        admins = await message.chat.get_administrators()

        for i in admins:
            if i['user']['first_name'].strip() == message.from_user.first_name.strip():
                muted.append(message.from_user.id)


        await  bot.delete_message(message.chat.id, message.message_id)

@dp.message_handler(commands=["write"])
async  def write(message : types.Message,users = users):
    with open(f"userslist{datetime.date.today()}.txt","w") as file:
        file.write("----------------------------\n")
        file.write(str(users))

@dp.message_handler()
async def cenz(message : types.Message):
    
    msg = message.text.lower().replace('.','').replace(' ','').replace('/',' ')
    bad = open("badwords.txt",'r').readlines()

    userinfo = message.from_user.mention + " "  + str(message.from_user.id)
    adduser(userinfo,users)
    for i in muted:
        if i == message.from_user.id:
            await bot.delete_message(message.chat.id,message.message_id)
    for i in bad:
        if i.encode("windows-1251").decode("utf-8").replace('\n','') in msg:
            print(message.from_user.first_name + " " + message.from_user.last_name + " "  + str(message.from_user.id))
            try:
                await  bot.delete_message(message.chat.id,message.message_id)
            except:
                print("пользователь в муте")

            #await bot.kick_chat_member(message.chat.id,message.from_user.id)
    print(users)
    spam.append(message.text.lower())
    if len(spam) > 1:
        if spam[-1] == spam[-2] :
            await bot.delete_message(message.chat.id,message.message_id)
            spam.pop(-1)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
