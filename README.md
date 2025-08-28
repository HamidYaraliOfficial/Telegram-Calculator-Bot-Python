# Telegram Calculator Bot

## English

### Overview
This project is a Telegram bot developed in Python using the `python-telegram-bot` library. It provides a simple yet secure calculator interface for performing basic arithmetic operations (+, -, *, /) with support for parentheses and decimal numbers. The bot supports three languages (English, Persian, and Chinese) and includes features like safe expression evaluation, error handling, and a multilingual interface. Users can interact with the bot via an inline keyboard, and the bot maintains user state and language preferences.

### Features
- **Calculator Interface**: Supports basic arithmetic operations (+, -, *, /), parentheses, and decimal numbers.
- **Safe Evaluation**: Securely evaluates mathematical expressions using Python’s `ast` module, preventing unsafe code execution.
- **Multilingual Support**: Interface available in English, Persian (Farsi), and Simplified Chinese, with language selection on startup.
- **Error Handling**: Handles division by zero, invalid expressions, and incomplete inputs with user-friendly messages.
- **State Management**: Tracks user expressions and language preferences per chat session.
- **Logging**: Errors are logged to `error.log` for debugging purposes.

### Prerequisites
- Python 3.6 or higher
- `python-telegram-bot` library
- Telegram Bot Token (obtained from BotFather)

### Installation
1. Install dependencies:
   ```bash
   pip install python-telegram-bot
   ```
2. Configure the bot:
   - Replace `"PUT YOUR TELEGRAM BOT TOKEN HERE"` in the code with your actual Telegram Bot Token.
   - Alternatively, set the `BOT_TOKEN` environment variable.
3. Run the bot:
   ```bash
   python bot.py
   ```

### Usage
- **Start the Bot**: Use the `/start` command to select a language and access the calculator.
- **Language Selection**: Choose from English, Persian, or Chinese via inline buttons.
- **Calculator Operations**:
  - Input numbers, operators (+, -, ×, ÷), parentheses, or decimals using the inline keyboard.
  - Press `=` to compute the result of a valid expression.
  - Use `⌫` to delete the last character, `C` to clear the expression, or `Close` to hide the keyboard.
  - Switch languages anytime using the `Language` button.
- **Error Handling**: The bot provides clear feedback for invalid inputs, division by zero, or incomplete expressions.

### File Structure
- `bot.py`: Main bot script containing all logic.
- `_s/`: Directory storing language preference files for each user (`{chat_id}.lang`).
- `error.log`: Log file for debugging errors.

### Developer
Developed by **Hamid Yarali**  
GitHub: [HamidYaraliOfficial](https://github.com/HamidYaraliOfficial)

---

## فارسی

### بررسی اجمالی
این پروژه یک ربات تلگرامی است که با استفاده از پایتون و کتابخانه `python-telegram-bot` توسعه یافته است. این ربات یک رابط کاربری ماشین حساب ساده و امن ارائه می‌دهد که از عملیات حسابی پایه (+، -، *، /) به همراه پرانتز و اعداد اعشاری پشتیبانی می‌کند. ربات از سه زبان (فارسی، انگلیسی و چینی) پشتیبانی می‌کند و شامل قابلیت‌هایی مانند ارزیابی امن عبارات، مدیریت خطا و رابط کاربری چندزبانه است. کاربران می‌توانند از طریق کیبورد اینلاین با ربات تعامل کنند و ربات حالت و تنظیمات زبان هر کاربر را حفظ می‌کند.

### ویژگی‌ها
- **رابط کاربری ماشین حساب**: پشتیبانی از عملیات حسابی پایه (+، -، *، /)، پرانتز و اعداد اعشاری.
- **ارزیابی امن**: ارزیابی امن عبارات ریاضی با استفاده از ماژول `ast` پایتون برای جلوگیری از اجرای کد ناامن.
- **پشتیبانی چندزبانه**: رابط کاربری در زبان‌های فارسی، انگلیسی و چینی ساده‌شده، با انتخاب زبان در شروع.
- **مدیریت خطا**: مدیریت خطاهایی مانند تقسیم بر صفر، عبارات نامعتبر و ورودی‌های ناقص با پیام‌های کاربرپسند.
- **مدیریت حالت**: پیگیری عبارات و تنظیمات زبان برای هر جلسه چت.
- **ثبت خطاها**: خطاها در فایل `error.log` برای اهداف دیباگ ثبت می‌شوند.

### پیش‌نیازها
- پایتون نسخه 3.6 یا بالاتر
- کتابخانه `python-telegram-bot`
- توکن ربات تلگرام (دریافت‌شده از BotFather)

### نصب
1. نصب وابستگی‌ها:
   ```bash
   pip install python-telegram-bot
   ```
2. پیکربندی ربات:
   - مقدار `"PUT YOUR TELEGRAM BOT TOKEN HERE"` را در کد با توکن واقعی ربات تلگرام جایگزین کنید.
   - یا متغیر محیطی `BOT_TOKEN` را تنظیم کنید.
3. اجرای ربات:
   ```bash
   python bot.py
   ```

### استفاده
- **شروع ربات**: از دستور `/start` برای انتخاب زبان و دسترسی به ماشین حساب استفاده کنید.
- **انتخاب زبان**: از بین فارسی، انگلیسی یا چینی از طریق دکمه‌های اینلاین انتخاب کنید.
- **عملیات ماشین حساب**:
  - اعداد، عملگرها (+، -، ×، ÷)، پرانتز یا اعشار را با استفاده از کیبورد اینلاین وارد کنید.
  - برای محاسبه نتیجه یک عبارت معتبر، دکمه `=` را فشار دهید.
  - از `⌫` برای حذف آخرین کاراکتر، `C` برای پاک کردن عبارت یا `Close` برای مخفی کردن کیبورد استفاده کنید.
  - با دکمه `Language` در هر زمان زبان را تغییر دهید.
- **مدیریت خطا**: ربات برای ورودی‌های نامعتبر، تقسیم بر صفر یا عبارات ناقص بازخورد واضحی ارائه می‌دهد.

### ساختار فایل‌ها
- `bot.py`: اسکریپت اصلی ربات حاوی تمام منطق.
- `_s/` : پوشه‌ای برای ذخیره فایل‌های تنظیمات زبان هر کاربر (`{chat_id}.lang`).
- `error.log` : فایل ثبت خطاها برای دیباگ.

### توسعه‌دهنده
توسعه‌یافته توسط **حمید یارعلی**  
گیت‌هاب: [HamidYaraliOfficial](https://github.com/HamidYaraliOfficial)

---

## 简体中文

### 概述
本项目是一个使用 Python 和 `python-telegram-bot` 库开发的 Telegram 机器人。它提供了一个简单而安全的计算器界面，支持基本算术运算（+、-、*、/）、括号和十进制数。该机器人支持三种语言（英语、波斯语和简体中文），并具有安全的表达式评估、错误处理和多语言界面等功能。用户可以通过内联键盘与机器人交互，机器人会维护用户的状态和语言偏好。

### 功能
- **计算器界面**：支持基本算术运算（+、-、*、/）、括号和十进制数。
- **安全评估**：使用 Python 的 `ast` 模块安全地评估数学表达式，防止不安全代码执行。
- **多语言支持**：界面支持英语、波斯语（波斯语）和简体中文，启动时可选择语言。
- **错误处理**：处理除以零、无效表达式和不完整输入，并提供用户友好的消息。
- **状态管理**：跟踪每个聊天会话的表达式和语言偏好。
- **日志记录**：错误记录在 `error.log` 文件中以便调试。

### 前提条件
- Python 3.6 或更高版本
- `python-telegram-bot` 库
- Telegram 机器人令牌（通过 BotFather 获取）

### 安装
1. 安装依赖项：
   ```bash
   pip install python-telegram-bot
   ```
2. 配置机器人：
   - 将代码中的 `"PUT YOUR TELEGRAM BOT TOKEN HERE"` 替换为您实际的 Telegram 机器人令牌。
   - 或者设置环境变量 `BOT_TOKEN`。
3. 运行机器人：
   ```bash
   python bot.py
   ```

### 使用
- **启动机器人**：使用 `/start` 命令选择语言并访问计算器。
- **语言选择**：通过内联按钮选择英语、波斯语或简体中文。
- **计算器操作**：
  - 使用内联键盘输入数字、运算符（+、-、×、÷）、括号或十进制。
  - 按 `=` 计算有效表达式的结果。
  - 使用 `⌫` 删除最后一个字符，`C` 清除表达式，或 `Close` 隐藏键盘。
  - 随时使用 `Language` 按钮切换语言。
- **错误处理**：机器人为无效输入、除以零或不完整表达式提供清晰的反馈。

### 文件结构
- `bot.py`：包含所有逻辑的主机器人脚本。
- `_s/`：存储每个用户的语言偏好文件（`{chat_id}.lang`）。
- `error.log`：用于调试的错误日志文件。

### 开发者
由 **Hamid Yarali** 开发  
GitHub: [HamidYaraliOfficial](https://github.com/HamidYaraliOfficial)