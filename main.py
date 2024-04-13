from telebot.async_telebot import AsyncTeleBot
import logging
#import telebot
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from datetime import datetime
import openai
from gpt import gpt


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = AsyncTeleBot(token="7135290781:AAG7G2mwm0HOLnlqWyGuwIuv87QXhpSCnSY")
# Диспетчер
dp = Dispatcher()
dp["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
value = ''
old_value = ''

mylist=[1, 2, 3]
mode = ''


keyboard = bot.types.InlineKeyboardMarkup()

keyboard.row(
bot.types.InlineKeyboardButton('', callback_data='no'),
bot.types.InlineKeyboardButton('C', callback_data='C'),
bot.types.InlineKeyboardButton('<=', callback_data='<='),
bot.types.InlineKeyboardButton('/', callback_data='/'))

keyboard.row(
bot.types.InlineKeyboardButton('7', callback_data='7'),
bot.types.InlineKeyboardButton('8', callback_data='8'),
bot.types.InlineKeyboardButton('9', callback_data='9'),
bot.types.InlineKeyboardButton('*', callback_data='*') )

keyboard.row(
bot.types.InlineKeyboardButton('4', callback_data='4'),
bot.types.InlineKeyboardButton('5', callback_data='5'),
bot.types.InlineKeyboardButton ('6', callback_data='6'),
bot.types.InlineKeyboardButton('-', callback_data='-') )
                               
keyboard.row(
bot.types.InlineKeyboardButton ('1', callback_data="1"),
bot.types.InlineKeyboardButton('2', callback_data='2'),
bot.types.InlineKeyboardButton('3', callback_data='3'),
bot.types.InlineKeyboardButton('+', callback_data='+') )

keyboard.row(
bot.types.InlineKeyboardButton('', callback_data='no'),
bot.types.InlineKeyboardButton('0', callback_data='0'),
bot.types.InlineKeyboardButton(',', callback_data='.'),
bot.types.InlineKeyboardButton('=', callback_data='='))



@bot.message_handler(commands='calculater')
def getMessage(message):
    global value 
    if value == '':
        bot.send_message(message.from_user.id, '0' , reply_marcup=keyboard)
    else:
        bot.send_message(message.from_user.id, 'value' , reply_marcup=keyboard)

######bot.polling(none_stop=False, interval=0)

@bot.callback_query_handler(func=lambda call: True)
def callback_func(query):
    global value, old_value
    data = query.data
    if data == "no":
        pass
    elif data == "C":
        value - ""
    elif data == '<=':
         if value != '':
             value = value[:len(value)-1]
    elif data == '=':
        value = str( eval(value) )
    else:
        value += data
    if value != old_value:
        if value =='':
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message.id, text='0', reply_markup=keyboard) 
        else:
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message.id, text=value, reply_markup=keyboard)
    old_value = value


# def m():
#     i1 = input('что добавить?')

# @dp.message(Command("add_to_list"))
# global m()
# async def cmd_add_to_list(message: types.Message):
#     m()
#     mylist.append(i1)
#     await message.answer("Добавлено", mylist)



@dp.message(Command("show_list"))
async def cmd_show_list(message: types.Message):
    await message.answer(f"Ваш список: {mylist}")


@dp.message(Command("add_list"))
async def add_list(message: types.Message):
    global mode 
    mode = 'add1'
    await message.answer()
#                        (f"Ваш список: {mylist}")

@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="/show_list"),
            types.KeyboardButton(text="/add_list"),
            types.KeyboardButton(text="/info"),
            types.KeyboardButton(text="/"),
            types.KeyboardButton(text="/ ")

        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="///"
    )
    await message.answer("что вы хотите добаивть", reply_markup=keyboard)

@dp.message(Command("info"))
async def cmd_info(message: types.Message, started_at: str):
    await message.answer({started_at})

   
@dp.message()
async def any_mes(message: types.Message):
    global mode
    if mode  == 'add1':
         await message.answer('что вы хотите добаивть')
         mode = 'add2'
    elif mode == 'add2':
        mylist.append(message.text)
        mode = ''
    else:
        await message.answer(gpt(message.text))


        


# # Запуск процесса поллинга новых апдейтов
# async def main():
#     await dp.start_polling(bot)


# if __name__ == "__main__":
#     asyncio.run(main())

#bot.infinity_polling()
import asyncio
asyncio.run(bot.polling())