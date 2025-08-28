# -*- coding: utf-8 -*-
import os
import ast
import operator as op
import telebot
from telebot import types
from typing import Dict, Optional

# ---------- Configuration ----------
TOKEN = os.getenv("BOT_TOKEN", "PUT YOUR TELEGRAM BOT TOKEN HERE")
AUTHOR_NAME = "Hamid Yarali"
GITHUB_LINK = "https://github.com/HamidYaraliOfficial"
INSTAGRAM_LINK = "https://www.instagram.com/hamidyaraliofficial?igsh=MWpxZjhhMHZuNnlpYQ=="
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# Language translations
LANGUAGES = {
    'fa': {
        'welcome': '🧮 <b>ماشین حساب آماده است</b>',
        'done': 'انجام شد',
        'division_by_zero': '❌ تقسیم بر صفر',
        'invalid_expression': '❌ عبارت نامعتبر',
        'incomplete_expression': '❌ عبارت ناقص',
        'closed': 'بسته شد',
        'footer': f"\n\nتوسعه‌دهنده: {AUTHOR_NAME}\nگیت‌هاب: {GITHUB_LINK}"
    },
    'en': {
        'welcome': '🧮 <b>Calculator Menu Ready</b>',
        'done': 'Done',
        'division_by_zero': '❌ Division by zero',
        'invalid_expression': '❌ Invalid expression',
        'incomplete_expression': '❌ Incomplete expression',
        'closed': 'Closed',
        'footer': f"\n\nDeveloped by: {AUTHOR_NAME}\nGitHub: {GITHUB_LINK}"
    },
    'zh': {
        'welcome': '🧮 <b>计算器菜单已准备好</b>',
        'done': '完成',
        'division_by_zero': '❌ 除以零',
        'invalid_expression': '❌ 无效表达式',
        'incomplete_expression': '❌ 不完整表达式',
        'closed': '已关闭',
        'footer': f"\n\n开发者: {AUTHOR_NAME}\nGitHub: {GITHUB_LINK}"
    }
}

# State storage
STATE: Dict[int, Dict[str, any]] = {}  # chat_id -> {"expr": str, "msg_id": int, "lang": str}
LANG_FILE = "_s/{}.lang"

# ---------- Safe Evaluation ----------
ALLOWED_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}
ALLOWED_NODES = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant, ast.Expr, ast.Load, ast.Subscript)

def safe_eval(expr: str) -> Optional[float]:
    """
    Safely evaluates a mathematical expression.
    Only +, -, *, /, and unary operators are allowed.
    """
    expr = expr.replace("×", "*").replace("÷", "/")
    try:
        node = ast.parse(expr, mode="eval")
        return _eval(node)
    except Exception as e:
        raise ValueError(f"Invalid expression: {str(e)}")

def _eval(n):
    if isinstance(n, ast.Expression):
        return _eval(n.body)
    if isinstance(n, ast.Num):  # Py<3.8
        return n.n
    if isinstance(n, ast.Constant):
        if isinstance(n.value, (int, float)):
            return n.value
        raise ValueError("Invalid constant")
    if isinstance(n, ast.BinOp):
        left = _eval(n.left)
        right = _eval(n.right)
        op_type = type(n.op)
        if op_type not in ALLOWED_OPS:
            raise ValueError("Operator not allowed")
        if op_type is ast.Div and right == 0:
            raise ZeroDivisionError("Division by zero")
        return ALLOWED_OPS[op_type](left, right)
    if isinstance(n, ast.UnaryOp):
        operand = _eval(n.operand)
        op_type = type(n.op)
        if op_type not in ALLOWED_OPS:
            raise ValueError("Unary operator not allowed")
        return ALLOWED_OPS[op_type](operand)
    raise ValueError("Bad expression")

# ---------- Utilities ----------
DIGITS = set("0123456789")
OPS = set("+-×÷")
PARENS = set("()")

def pretty(expr: str, lang: str) -> str:
    """
    Formats the display text: first line is the expression, second line is the result (if calculable).
    """
    if not expr:
        return "0" + LANGUAGES[lang]['footer']
    view = expr
    try:
        if is_expression_complete(expr):
            result = safe_eval(expr)
            if result is not None:
                if abs(result - int(result)) < 1e-12:
                    result = int(result)
                return f"{view}\n<b>= {result}</b>" + LANGUAGES[lang]['footer']
    except Exception:
        pass
    return view + LANGUAGES[lang]['footer']

def is_expression_complete(expr: str) -> bool:
    """Checks if the expression has balanced parentheses and doesn't end with an operator/decimal."""
    if not expr:
        return False
    bal = 0
    for ch in expr:
        if ch == "(":
            bal += 1
        elif ch == ")":
            bal -= 1
            if bal < 0:
                return False
    if bal != 0:
        return False
    if expr[-1] in OPS or expr[-1] == "." or expr[-1] == "(":
        return False
    return True

def can_append(expr: str, token: str) -> bool:
    """Rules to prevent common bugs."""
    if token in DIGITS:
        if expr.endswith("0") and (len(expr) == 1 or expr[-2] in OPS + {"("}) and token != ".":
            return True
        return True
    if token in OPS:
        if not expr:
            return token in "+-"
        if expr[-1] in OPS or expr[-1] == "(" or expr[-1] == ".":
            return False
        return True
    if token == ".":
        i = len(expr) - 1
        while i >= 0 and expr[i] not in OPS and expr[i] not in PARENS:
            if expr[i] == ".":
                return False
            i -= 1
        if not expr or expr[-1] in OPS + {"("}:
            return True
        return True
    if token == "(":
        if not expr:
            return True
        return (expr[-1] in OPS) or (expr[-1] == "(")
    if token == ")":
        if not expr:
            return False
        bal = 0
        for ch in expr:
            if ch == "(":
                bal += 1
            elif ch == ")":
                bal -= 1
        if bal <= 0:
            return False
        if expr[-1] in OPS or expr[-1] == "(" or expr[-1] == ".":
            return False
        return True
    if token == "=":
        return is_expression_complete(expr)
    return True

def apply_token(expr: str, token: str) -> str:
    if token == "C":
        return ""
    if token == "⌫":
        return expr[:-1]
    if token in {"=", "Close"}:
        return expr
    if can_append(expr, token):
        if token == "." and (not expr or expr[-1] in OPS or expr[-1] == "("):
            return expr + "0."
        return expr + token
    return expr

# ---------- Keyboard ----------
def make_kb(lang: str) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=4)
    rows = [
        ["7", "8", "9", "÷"],
        ["4", "5", "6", "×"],
        ["1", "2", "3", "−"],
        ["0", ".", "=", "+"],
        ["(", ")", "⌫", "C"],
    ]
    mapping = {"−": "-"}
    for row in rows:
        kb.row(*[
            types.InlineKeyboardButton(text=txt, callback_data=mapping.get(txt, txt))
            for txt in row
        ])
    kb.add(
        types.InlineKeyboardButton("Close", callback_data="Close"),
        types.InlineKeyboardButton("🌐 Language", callback_data="lang")
    )
    return kb

# ---------- Language Management ----------
def save_lang(chat_id: int, lang: str):
    os.makedirs("_s", exist_ok=True)
    with open(LANG_FILE.format(chat_id), "w") as f:
        f.write(lang)

def load_lang(chat_id: int) -> str:
    try:
        with open(LANG_FILE.format(chat_id), "r") as f:
            lang = f.read().strip()
            return lang if lang in LANGUAGES else 'fa'
    except FileNotFoundError:
        return 'fa'

# ---------- Routes ----------
@bot.message_handler(commands=["start"])
def start(m: types.Message):
    chat_id = m.chat.id
    lang = load_lang(chat_id)
    STATE[chat_id] = {"expr": "", "lang": lang}
    
    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton("🇮🇷 فارسی", callback_data="lang_fa"),
        types.InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
        types.InlineKeyboardButton("🇨🇳 简体中文", callback_data="lang_zh")
    )
    bot.send_message(chat_id, LANGUAGES[lang]['welcome'] + LANGUAGES[lang]['footer'], reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data.startswith("lang_"))
def set_language(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    lang = call.data.split("_")[1]
    save_lang(chat_id, lang)
    STATE[chat_id] = {"expr": "", "lang": lang, "msg_id": None}
    
    text = LANGUAGES[lang]['welcome'] + "\n" + pretty("", lang)
    msg = bot.send_message(chat_id, text, reply_markup=make_kb(lang))
    STATE[chat_id]["msg_id"] = msg.message_id
    bot.answer_callback_query(call.id, "Language changed")

@bot.callback_query_handler(func=lambda c: True)
def on_press(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    if chat_id not in STATE:
        lang = load_lang(chat_id)
        STATE[chat_id] = {"expr": "", "lang": lang, "msg_id": call.message.message_id}
    
    token = call.data
    lang = STATE[chat_id]["lang"]
    
    if token == "lang":
        kb = types.InlineKeyboardMarkup()
        kb.add(
            types.InlineKeyboardButton("🇮🇷 فارسی", callback_data="lang_fa"),
            types.InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
            types.InlineKeyboardButton("🇨🇳 简体中文", callback_data="lang_zh")
        )
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=STATE[chat_id]["msg_id"],
            text=LANGUAGES[lang]['welcome'] + LANGUAGES[lang]['footer'],
            reply_markup=kb
        )
        bot.answer_callback_query(call.id, "Select language")
        return

    if token == "Close":
        try:
            bot.edit_message_reply_markup(chat_id, STATE[chat_id]["msg_id"], reply_markup=None)
        except Exception:
            pass
        bot.answer_callback_query(call.id, LANGUAGES[lang]['closed'])
        del STATE[chat_id]
        return

    if token == "=":
        if is_expression_complete(STATE[chat_id]["expr"]):
            try:
                result = safe_eval(STATE[chat_id]["expr"])
                if abs(result - int(result)) < 1e-12:
                    result = int(result)
                bot.answer_callback_query(call.id, LANGUAGES[lang]['done'])
                bot.send_message(
                    chat_id,
                    f"{STATE[chat_id]['expr']}\n<b>= {result}</b>" + LANGUAGES[lang]['footer']
                )
            except ZeroDivisionError:
                bot.answer_callback_query(call.id, LANGUAGES[lang]['division_by_zero'], show_alert=True)
            except Exception:
                bot.answer_callback_query(call.id, LANGUAGES[lang]['invalid_expression'], show_alert=True)
        else:
            bot.answer_callback_query(call.id, LANGUAGES[lang]['incomplete_expression'], show_alert=True)
        return

    new_expr = apply_token(STATE[chat_id]["expr"], token)
    STATE[chat_id]["expr"] = new_expr
    new_text = LANGUAGES[lang]['welcome'] + "\n" + pretty(new_expr, lang)

    try:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=STATE[chat_id]["msg_id"],
            text=new_text,
            reply_markup=make_kb(lang),
            parse_mode="HTML"
        )
    except Exception:
        msg = bot.send_message(chat_id, new_text, reply_markup=make_kb(lang))
        STATE[chat_id]["msg_id"] = msg.message_id

    if token in {"+", "-", "×", "÷", "(", ")", ".", "⌫"} or token in DIGITS:
        bot.answer_callback_query(call.id, token)
    else:
        bot.answer_callback_query(call.id)

# ---------- Error Logging ----------
def log_error(e: Exception, context: str):
    with open("error.log", "a") as f:
        f.write(f"[{time.ctime()}] {context}: {str(e)}\n")

# ---------- Execution ----------
if __name__ == "__main__":
    import time
    print(f"Bot is running ...\nDeveloped by: {AUTHOR_NAME}\nGitHub: {GITHUB_LINK}")
    try:
        bot.infinity_polling(skip_pending=True, timeout=30)
    except Exception as e:
        log_error(e, "Bot polling error")
        print(f"Error occurred: {str(e)}")
        time.sleep(5)  # Retry after delay
        bot.infinity_polling(skip_pending=True, timeout=30)

# Developed by: Hamid Yarali
# GitHub: https://github.com/HamidYaraliOfficial