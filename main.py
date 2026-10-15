import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

TOKEN = "8821471298:AAEkEoJUpbv8Uf9wNXQ5YUFF0s11NPpWAkw"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Главное меню (кнопки снизу)
def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="⭐ Пожертвовать звездами")
    builder.button(text="🎰 Крутить слот 🎰")
    builder.button(text="📈 Купить акции на моей бирже 📈")
    builder.button(text="🎁 Мои нфт 🎁")
    builder.button(text="👤 обо мне 👤")
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

# Кнопки сумм для доната
def amounts_keyboard():
    builder = InlineKeyboardBuilder()
    for amount in [1, 5, 10, 20, 50, 100]:
        builder.button(text=f"{amount} ⭐", callback_data=f"pay_{amount}")
    builder.adjust(3)
    return builder.as_markup()

# Кнопки ставок для игры в слот
def slot_bets_keyboard():
    builder = InlineKeyboardBuilder()
    for bet in [1, 5, 10, 15, 20, 50, 100]:
        builder.button(text=f"{bet} ⭐", callback_data=f"slotbet_{bet}")
    builder.adjust(3)
    return builder.as_markup()

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "💎добро пожаловать в Nell бот💎",
        reply_markup=main_menu()
    )

# === Обработка кнопок ===

@dp.message(F.text == "⭐ Пожертвовать звездами")
async def donate(message: Message):
    await message.answer(
        "Выберите сумму пожертвования:",
        reply_markup=amounts_keyboard()
    )

@dp.message(F.text == "🎰 Крутить слот 🎰")
async def slot_game_menu(message: Message):
    await message.answer(
        "Выберите вашу ставку в звездах ⭐ для игры в слот:",
        reply_markup=slot_bets_keyboard()
    )

@dp.message(F.text == "📈 Купить акции на моей бирже 📈")
async def stocks(message: Message):
    await message.answer("Если хочешь купить акции на бирже напиши в лс @Navi4563")

@dp.message(F.text == "🎁 Мои нфт 🎁")
async def nfts(message: Message):
    await message.answer("@Navi4563 здесь можно в профиле посмотреть какие нфт я продаю")

@dp.message(F.text == "👤 обо мне 👤")
async def about(message: Message):
    text = """💎✨ обо мне ✨💎

Звать Милан 

📍 Живу в Украине     
 
🎁 Занимаюсь продажей NFT

Также покупаю нфт

📲 Мой юз: @Navi4563 писать по поводу покупки или продажы нфт

💎 Спасибо, что посмотрел💎"""
    await message.answer(text)

# === Оплата за обычное пожертвование ===

@dp.callback_query(F.data.startswith("pay_"))
async def process_payment(callback: CallbackQuery):
    amount = int(callback.data.split("_")[1])
    prices = [LabeledPrice(label=f"Пожертвование {amount} звезд", amount=amount)]
    
    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title="Пожертвование звездами",
        description=f"Поддержать бота на {amount} звезд ⭐",
        payload=f"donate_{amount}",
        provider_token="",
        currency="XTR",
        prices=prices,
    )
    await callback.answer()

# === Выставление счета для ставки в слоте ===

@dp.callback_query(F.data.startswith("slotbet_"))
async def process_slot_bet(callback: CallbackQuery):
    bet = int(callback.data.split("_")[1])
    prices = [LabeledPrice(label=f"Ставка в слоте: {bet} звезд", amount=bet)]
    
    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title="🎰 Ставка в слот",
        description=f"Оплатите {bet} звезд ⭐ для вращения слота!",
        payload=f"slotbet_{bet}",
        provider_token="",
        currency="XTR",
        prices=prices,
    )
    await callback.answer()

@dp.pre_checkout_query()
async def pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# === Проведение оплаты и запуск слота ===

@dp.message(F.successful_payment)
async def successful_payment(message: Message):
    payload = message.successful_payment.invoice_payload
    amount = message.successful_payment.total_amount

    # Если это была обычная пожертвование
    if payload.startswith("donate_"):
        await message.answer(f"Спасибо за поддержку на {amount} звезд! ❤️")

    # Если это была ставка в слоте
    elif payload.startswith("slotbet_"):
        await message.answer("Оплата прошла успешно! Крутим слот... 🎰")
        msg = await message.answer_dice(emoji="🎰")
        
        await asyncio.sleep(2)  # Ждем окончания анимации
        
        # В Telegram значение 64 для эмодзи 🎰 соответствует комбинации 777
        if msg.dice.value == 64:
            await message.answer("🎉 ТЫ ВЫИГРАЛ! Напиши в лс @Navi4563 чтоб забрать приз!")
        else:
            await message.answer("😢 Не повезло! Попробуй еще раз!")

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
