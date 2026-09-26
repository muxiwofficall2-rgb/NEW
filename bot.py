# -*- coding: utf-8 -*-
"""
Turkman fuqarolari uchun Sankt-Peterburgdagi O'zbekiston konsulligi orqali
olinadigan viza holatini tekshirish va anketa to'ldirish xizmatiga bog'lanish uchun bot.
3 tilda ishlaydi: Rus / O'zbek / Turkman.

ISHGA TUSHIRISH:
1) pip install -r requirements.txt   (yoki: pip install python-telegram-bot==21.6)
2) Pastdagi BOT_TOKEN o'rniga BotFather bergan tokenni qo'ying (yoki muhit
   o'zgaruvchisi orqali bering - bu xavfsizroq).
3) python viza_bot.py

MUHIM: Siz tokenni ushbu suhbatda ochiq yubordingiz. Xavfsizlik uchun
Telegram-da @BotFather ga kirib "/revoke" orqali eski tokenni bekor qilib,
yangi token olishni maslahat beraman, so'ng shu yangi tokenni pastga qo'ying.
"""

import logging
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Tokenni avval muhit o'zgaruvchisidan o'qishga harakat qilamiz,
# topilmasa shu yerga yozilganini ishlatamiz.
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8616201229:AAECvm032z3CQaQhRIAHgY6rCbJZopJqujI")

VISA_CHECK_URL = "https://visa.mfa.uz/ruxsat/view"
PHONE_NUMBER = "+79379499094"
PHONE_DIGITS = "79379499094"  # tel:/wa.me uchun + belgisisiz

TEXTS = {
    "ru": {
        "choose_lang": "🌐 Пожалуйста, выберите язык / Iltimos, tilni tanlang / Dilinizi saýlaň",
        "welcome": "👋 Добро пожаловать!\nВыберите нужный раздел ниже:",
        "check_visa": "🔎 Проверить визу",
        "contact": "📞 Связаться (заполнение анкеты)",
        "back": "⬅️ Назад",
        "change_lang": "🌐 Сменить язык",
        "contact_title": "📞 Связаться с оператором\n\nДля заполнения анкеты и помощи по визе свяжитесь по номеру:\n{phone}\n\nВыберите удобный способ связи:",
        "call": "📞 Позвонить",
        "whatsapp": "💬 WhatsApp",
        "telegram": "✈️ Telegram",
        "max": "🔴 MAX",
        "imo": "🟢 imo",
        "max_imo_hint": "Откройте приложение {app} и наберите номер:\n{phone}",
    },
    "uz": {
        "choose_lang": "🌐 Iltimos, tilni tanlang / Пожалуйста, выберите язык / Dilinizi saýlaň",
        "welcome": "👋 Xush kelibsiz!\nQuyidan kerakli bo'limni tanlang:",
        "check_visa": "🔎 Vizani tekshirish",
        "contact": "📞 Bog'lanish (anketa to'ldirish)",
        "back": "⬅️ Orqaga",
        "change_lang": "🌐 Tilni o'zgartirish",
        "contact_title": "📞 Operator bilan bog'lanish\n\nAnketa to'ldirish va viza masalasida yordam olish uchun quyidagi raqamga murojaat qiling:\n{phone}\n\nQulay usulni tanlang:",
        "call": "📞 Qo'ng'iroq qilish",
        "whatsapp": "💬 WhatsApp",
        "telegram": "✈️ Telegram",
        "max": "🔴 MAX",
        "imo": "🟢 imo",
        "max_imo_hint": "{app} ilovasini oching va quyidagi raqamni tering:\n{phone}",
    },
    "tm": {
        "choose_lang": "🌐 Iltimos, dili saýlaň / Пожалуйста, выберите язык / Iltimos, tilni tanlang",
        "welcome": "👋 Hoş geldiňiz!\nAşakdan gerekli bölümi saýlaň:",
        "check_visa": "🔎 Wizany barlamak",
        "contact": "📞 Habarlaşmak (anketa doldurmak)",
        "back": "⬅️ Yza",
        "change_lang": "🌐 Dili üýtgetmek",
        "contact_title": "📞 Operator bilen habarlaşmak\n\nAnketa doldurmak we wiza barada kömek almak üçin şu belgä ýüz tutuň:\n{phone}\n\nOňaýly usuly saýlaň:",
        "call": "📞 Jaň etmek",
        "whatsapp": "💬 WhatsApp",
        "telegram": "✈️ Telegram",
        "max": "🔴 MAX",
        "imo": "🟢 imo",
        "max_imo_hint": "{app} programmasyny açyň we şu belgini ýygyň:\n{phone}",
    },
}

LANG_BUTTONS = [
    ("ru", "🇷🇺 Русский"),
    ("uz", "🇺🇿 O'zbekcha"),
    ("tm", "🇹🇲 Türkmençe"),
]


def lang_keyboard() -> InlineKeyboardMarkup:
    rows = [[InlineKeyboardButton(label, callback_data=f"lang:{code}")] for code, label in LANG_BUTTONS]
    return InlineKeyboardMarkup(rows)


def main_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    t = TEXTS[lang]
    rows = [
        [InlineKeyboardButton(t["check_visa"], url=VISA_CHECK_URL)],
        [InlineKeyboardButton(t["contact"], callback_data="contact")],
        [InlineKeyboardButton(t["change_lang"], callback_data="change_lang")],
    ]
    return InlineKeyboardMarkup(rows)


def contact_keyboard(lang: str) -> InlineKeyboardMarkup:
    t = TEXTS[lang]
    rows = [
        [InlineKeyboardButton(t["call"], url=f"tel:{PHONE_NUMBER}")],
        [InlineKeyboardButton(t["whatsapp"], url=f"https://wa.me/{PHONE_DIGITS}")],
        [InlineKeyboardButton(t["telegram"], url=f"https://t.me/+{PHONE_DIGITS}")],
        [
            InlineKeyboardButton(t["max"], callback_data="hint:MAX"),
            InlineKeyboardButton(t["imo"], callback_data="hint:imo"),
        ],
        [InlineKeyboardButton(t["back"], callback_data="back_to_menu")],
    ]
    return InlineKeyboardMarkup(rows)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        TEXTS["uz"]["choose_lang"], reply_markup=lang_keyboard()
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("lang:"):
        lang = data.split(":", 1)[1]
        context.user_data["lang"] = lang
        t = TEXTS[lang]
        await query.edit_message_text(t["welcome"], reply_markup=main_menu_keyboard(lang))
        return

    lang = context.user_data.get("lang", "uz")
    t = TEXTS[lang]

    if data == "change_lang":
        await query.edit_message_text(t["choose_lang"], reply_markup=lang_keyboard())
        return

    if data == "contact":
        text = t["contact_title"].format(phone=PHONE_NUMBER)
        await query.edit_message_text(text, reply_markup=contact_keyboard(lang))
        return

    if data == "back_to_menu":
        await query.edit_message_text(t["welcome"], reply_markup=main_menu_keyboard(lang))
        return

    if data.startswith("hint:"):
        app_name = data.split(":", 1)[1]
        hint = t["max_imo_hint"].format(app=app_name, phone=PHONE_NUMBER)
        await query.answer(hint, show_alert=True)
        return


def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    logger.info("Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
