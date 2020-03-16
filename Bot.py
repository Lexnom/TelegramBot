from aiogram import Bot
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ContentType, AllowedUpdates, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from aiogram.utils.executor import start_webhook

import price_select
import conf
import GenerateKeyBoard
import asyncio
import cheroot.ssl.builtin

cheroot.ssl.builtin.IS_BELOW_PY37 = True

WEBHOOK_HOST = conf.ip
WEBAPP_PORT = 3001
WEBAPP_HOST = 'localhost'
WEBHOOK_PATH = "/%s/" % (conf.token)
WEBHOOK_URL = "https://%s%s"%(WEBHOOK_HOST, WEBHOOK_PATH)

loop = asyncio.get_event_loop()
bot = Bot(token=conf.token, parse_mode=types.ParseMode.MARKDOWN)
dp = Dispatcher(bot, loop=loop)

inline_btn_1 = InlineKeyboardButton('Первая кнопка!😂', callback_data='button1')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)

a = 'asdasd'
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Привет!!\nЧто бы узнать что я могу введи команду: /help")


@dp.message_handler(commands=['shop'])
async def shop_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Выбери что хочешь купить", reply_markup=GenerateKeyBoard.Generate_markup())


@dp.message_handler(commands=['help'])
async def shop_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Для того, что бы купить у меня что-то, введите команду /shop")

@dp.message_handler(commands=['1'])
async def process_key_1(message: types.Message):
    price = price_select.select_price()
    print(price['amount'])
    await bot.send_photo(message.from_user.id, photo = price['file'])
    if conf.PAY_PROVIDER_TOKEN.split(':')[1] == 'TEST':
        await bot.send_invoice(
            message.chat.id,
            title=price['name'],
            description=price['description'],
            provider_token=conf.PAY_PROVIDER_TOKEN,
            currency='rub',
            is_flexible=False,  # True если конечная цена зависит от способа доставки
            prices=[types.LabeledPrice(label=price['name'], amount=price['amount'])],
            start_parameter='time-machine-example',
            payload='some'
        )

@dp.callback_query_handler(lambda c: c.data =='button1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=a, reply_markup=inline_kb1)



@dp.message_handler()
async def chek_shop(msg: types.Message):
    name = price_select.Conncet()

    for items in name:
        if msg.text == items:
            await bot.send_message(msg.from_user.id, conf.TestPay)
            select_price = price_select.Select_price(items)
            for sp in select_price:
                name = sp[0]
                description = sp[1]
                amount = sp[2]
                link_photo = sp[3]
    if conf.PAY_PROVIDER_TOKEN.split(':')[1] == 'TEST':
        await bot.send_invoice(
            msg.chat.id,
            title=name,
            description=description,
            provider_token=conf.PAY_PROVIDER_TOKEN,
            currency='rub',
            photo_url=link_photo,
            photo_height=512,  # !=0/None, иначе изображение не покажется
            photo_width=512,
            photo_size=512,
            is_flexible=False,  # True если конечная цена зависит от способа доставки
            prices=[types.LabeledPrice(label=name, amount=amount)],
            start_parameter='time-machine-example',
            payload='some'
        )


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message):
    print('successful_payment:')
    pmnt = message.successful_payment.to_python()
    for key, val in pmnt.items():
        print('{%s} = {%s}'%(key, val))

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL, certificate=open(conf.cert, 'r'))

async def on_shutdown(dp):
    await bot.delete_webhook()

if __name__ == '__main__':
    executor.start_polling(dp)

    #start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH, on_startup=on_startup,
    #             on_shutdown=on_shutdown, skip_updates=True, host=WEBAPP_HOST, port=WEBAPP_PORT)






