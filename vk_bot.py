import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from flask import Flask, jsonify
from threading import Thread
import re
import random
import time
from datetime import datetime
import json
import os

# ===== НАСТРОЙКИ =====
# Токен берется из переменных окружения (для безопасности на Render)
VK_TOKEN = os.environ.get("VK_TOKEN")

# ===== Flask для поддержки работы =====
app = Flask("")
start_time = time.time()

@app.route("/")
def home():
    return "✅ Бот AI Nexus 2026 работает!"

@app.route("/status")
def status():
    return jsonify({
        "status": "online",
        "bot": "AI Nexus 2026",
        "community": "https://vk.com/ai_cherem7",
        "site": "https://ai-toolkit.ru",
        "uptime": int(time.time() - start_time)
    })

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ===== ХРАНИЛИЩЕ ДАННЫХ =====
user_stats = {}

def save_stats():
    try:
        with open("user_stats.json", "w", encoding="utf-8") as f:
            json.dump(user_stats, f, ensure_ascii=False, indent=2)
    except:
        pass

def load_stats():
    global user_stats
    if os.path.exists("user_stats.json"):
        try:
            with open("user_stats.json", "r", encoding="utf-8") as f:
                user_stats = json.load(f)
        except:
            user_stats = {}

load_stats()

# ===== ОТВЕТЫ БОТА =====
RESPONSES = {
    "привет": [
        "🤖 Привет! Я бот AI Nexus 2026! Чем могу помочь?",
        "🌟 Здравствуйте! Добро пожаловать в мир AI-заработка!",
        "👋 Хай! Готовы узнать секреты заработка на нейросетях?"
    ],
    "промокоды": (
        "🎁 АКТУАЛЬНЫЕ ПРОМОКОДЫ 2026:\n\n"
        "🤖 ЯНДЕКС GPT 2.0\n"
        "Промокод: YGPT2026-3FREE\n"
        "→ 3 месяца бесплатно\n\n"
        "🎨 KANDINSKY 4.0\n"
        "Промокод: KANDY60\n"
        "→ Скидка 60% на первый месяц\n\n"
        "✨ MIDJOURNEY V8\n"
        "Промокод: MJV8FREE2026\n"
        "→ 1 месяц бесплатно\n\n"
        "💬 CHATGPT 5\n"
        "Промокод: GPT5FREE30\n"
        "→ 30 дней бесплатно\n\n"
        "💻 GITHUB COPILOT X+\n"
        "Промокод: COPILOT40\n"
        "→ Скидка 40% на годовую подписку\n\n"
        "🏦 GIGACHAT PRO\n"
        "Промокод: GIGAPRO30\n"
        "→ 30 дней бесплатно\n\n"
        "📚 CLAUDE 4\n"
        "Промокод: CLAUDE4FREE\n"
        "→ 14 дней бесплатно\n\n"
        "☁️ GEMINI 2.0\n"
        "Промокод: GEMINI2026\n"
        "→ 2 месяца бесплатно\n\n"
        "🎬 RUNWAY GEN-3\n"
        "Промокод: RUNWAY30\n"
        "→ 30 дней бесплатно\n\n"
        "🎵 SUNO AI\n"
        "Промокод: SUNO50\n"
        "→ Скидка 50% на подписку\n\n"
        "🔍 PERPLEXITY AI\n"
        "Промокод: PERPLEXITY30\n"
        "→ 30 дней Pro\n\n"
        "➡️ ВСЕ ПРОМОКОДЫ НА САЙТЕ:\n"
        "🔗 https://ai-toolkit.ru"
    ),
    "партнерки": (
        "💼 ПАРТНЁРСКИЕ ПРОГРАММЫ ДЛЯ ЗАРАБОТКА:\n\n"
        "☁️ REG.RU CLOUD\n"
        "→ До 40% с заказов\n"
        "→ Вывод от 200 рублей\n"
        "→ Промокод: 8B77-0FF0-E6ED-E300 (скидка 5%)\n"
        "🔗 https://reg.cloud/?rlink=reflink-31250911\n\n"
        "📊 ЯНДЕКС.ДИРЕКТ\n"
        "→ Заработок на рекламе\n"
        "🔗 https://trk.ppdu.ru/click/rc3KcPKq?erid=Kra23uVC3\n\n"
        "🌐 ЯНДЕКС.БРАУЗЕР\n"
        "→ Установите браузер и зарабатывайте\n"
        "🔗 https://browser.yandex.ru/corp/builds?refid=14628861\n\n"
        "💳 ВТБ КРЕДИТНАЯ КАРТА\n"
        "→ Кешбэк и бонусы\n"
        "🔗 https://trk.ppdu.ru/click/SlJRlpVP?erid=2SDnjeGCc2T\n\n"
        "💰 ЗАРАБАТЫВАЙТЕ ДО 500,000 ₽/МЕС!\n"
        "🔥 Регистрируйтесь прямо сейчас!"
    ),
    "сайт": (
        "🌐 НАШ САЙТ: https://ai-toolkit.ru\n\n"
        "📌 ЧТО ВЫ НАЙДЁТЕ:\n"
        "✅ Все актуальные промокоды на нейросети\n"
        "✅ Каталог AI-инструментов\n"
        "✅ Инструкции по заработку\n"
        "✅ Партнёрские программы\n"
        "✅ Новости мира AI\n\n"
        "🔥 Переходите и пользуйтесь бесплатно!"
    ),
    "идеи": (
        "💡 ТОП-5 СПОСОБОВ ЗАРАБОТКА НА НЕЙРОСЕТЯХ:\n\n"
        "1️⃣ Генерация изображений (Midjourney, Kandinsky)\n"
        "   → Продажа на стоках, дизайн, NFT\n\n"
        "2️⃣ Написание текстов (ChatGPT, Claude)\n"
        "   → Копирайтинг, сценарии, посты\n\n"
        "3️⃣ Создание видео (Runway, Pika)\n"
        "   → Ролики для YouTube, Reels, TikTok\n\n"
        "4️⃣ Музыка и озвучка (Suno, ElevenLabs)\n"
        "   → Треки на заказ, подкасты\n\n"
        "5️⃣ Обучение и консультации\n"
        "   → Курсы по работе с нейросетями\n\n"
        "🚀 Начните зарабатывать уже сегодня!"
    ),
    "инструменты": (
        "🛠️ ПОПУЛЯРНЫЕ AI-ИНСТРУМЕНТЫ 2026:\n\n"
        "📝 ТЕКСТ:\n"
        "• ChatGPT — https://chat.openai.com\n"
        "• Claude — https://claude.ai\n"
        "• Gemini — https://gemini.google.com\n\n"
        "🎨 ИЗОБРАЖЕНИЯ:\n"
        "• Midjourney — https://midjourney.com\n"
        "• Kandinsky — https://fusionbrain.ai\n\n"
        "🎬 ВИДЕО:\n"
        "• Runway — https://runwayml.com\n\n"
        "🎵 МУЗЫКА:\n"
        "• Suno — https://suno.ai\n\n"
        "💻 КОД:\n"
        "• GitHub Copilot — https://github.com/features/copilot\n\n"
        "➡️ Все промокоды на сайте ai-toolkit.ru"
    ),
    "обучение": (
        "📚 БЕСПЛАТНОЕ ОБУЧЕНИЕ ПО НЕЙРОСЕТЯМ:\n\n"
        "🎓 КУРСЫ:\n"
        "• Яндекс.Практикум — Нейросети для начинающих\n"
        "• Stepik — Введение в ИИ\n"
        "• Нейростарт — Заработок на нейросетях\n\n"
        "📺 КАНАЛЫ YOUTUBE:\n"
        "• AI простыми словами\n"
        "• Нейрохакинг\n"
        "• Промпт-инжиниринг для всех\n\n"
        "📖 ТЕЛЕГРАМ-КАНАЛЫ:\n"
        "• AI News — @ai_news_rf\n"
        "• Промокоды AI — @aipromokody\n\n"
        "🚀 Начинайте обучение прямо сейчас!"
    ),
    "контакты": (
        "📞 КОНТАКТНАЯ ИНФОРМАЦИЯ:\n\n"
        "🌐 Сайт: https://ai-toolkit.ru\n"
        "📧 Почта: support@ai-toolkit.ru\n"
        "📱 ВК Сообщество: @ai_cherem7\n"
        "👤 Админ: Иван Черемных\n\n"
        "⏰ Время ответа: до 24 часов\n"
        "⚠️ По техническим вопросам пишите сюда!"
    ),
}

# ===== РАЗВЛЕЧЕНИЯ =====
FACTS = [
    "🧠 Первая нейросеть была создана в 1943 году!",
    "💡 ChatGPT набрал 1 млн пользователей за 5 дней — рекорд в истории!",
    "🎨 Midjourney генерирует более 10 млн изображений в день!",
    "💰 Рынок ИИ вырастет до $1.8 трлн к 2030 году",
    "🤖 77% компаний уже используют или планируют внедрить ИИ",
    "📝 Нейросети пишут код быстрее человека в 10 раз",
    "🎬 Runway создал первый фильм, сгенерированный полностью нейросетью",
    "🇷🇺 Кандинский — первый российский генератор изображений"
]

JOKES = [
    "🤖 Почему нейросеть не ходит в школу?\n→ Потому что она и так всё знает!",
    "💻 Сколько нейросетей нужно, чтобы заменить программиста?\n→ Одну, но она ещё не дописана.",
    "🎨 ChatGPT спрашивает у Midjourney:\n→ Нарисуй меня красивым!\n→ Ты же текст, тебя не видно!\n→ Вот именно!",
    "🤖 Какая любимая игра нейросети?\n→ Угадай промпт!",
]

MOTIVATION = [
    "💪 Вы уже на пути к успеху! Продолжайте в том же духе!",
    "🚀 Каждый эксперт когда-то был новичком. Главное — начать!",
    "💰 Ваш первый заработок на нейросетях ближе, чем кажется!",
    "🌟 Ошибки — это опыт. Опыт — это знания. Знания — это деньги!",
    "🔥 Не сравнивайте себя с другими. Сравнивайте себя с собой вчерашним!"
]

# ===== ФУНКЦИИ =====
def normalize_text(text: str) -> str:
    """Очищает текст от лишних символов"""
    text = text.lower().strip()
    text = re.sub(r'[^\w\sа-я]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def update_user_stats(user_id, command):
    """Обновляет статистику пользователя"""
    if user_id not in user_stats:
        user_stats[user_id] = {
            "first_seen": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "commands": {},
            "total": 0
        }
    user_stats[user_id]["commands"][command] = user_stats[user_id]["commands"].get(command, 0) + 1
    user_stats[user_id]["total"] += 1
    save_stats()

def get_stats_text(user_id):
    """Возвращает статистику пользователя"""
    if user_id not in user_stats:
        return "📊 У вас пока нет статистики. Напишите что-нибудь боту!"
    
    stats = user_stats[user_id]
    return (
        f"📊 ВАША СТАТИСТИКА:\n\n"
        f"📅 Первое обращение: {stats['first_seen']}\n"
        f"💬 Всего команд: {stats['total']}\n"
        f"🎯 Чаще всего спрашивали: {max(stats['commands'], key=stats['commands'].get)}\n\n"
        f"🔥 Продолжайте в том же духе!"
    )

def send_message(vk, user_id: int, text: str, keyboard=None) -> None:
    """Отправляет сообщение (с возможностью клавиатуры)"""
    params = {
        "user_id": user_id,
        "message": text,
        "random_id": random.randint(1, 999999999)
    }
    if keyboard:
        params["keyboard"] = keyboard
    vk.messages.send(**params)

# ===== КЛАВИАТУРА =====
def get_main_keyboard():
    """Создаёт клавиатуру для бота"""
    return json.dumps({
        "one_time": False,
        "buttons": [
            [{"action": {"type": "text", "label": "🎁 Промокоды"}, "color": "positive"}],
            [{"action": {"type": "text", "label": "💼 Партнерки"}, "color": "primary"}],
            [{"action": {"type": "text", "label": "🌐 Сайт"}, "color": "secondary"}],
            [{"action": {"type": "text", "label": "💡 Идеи"}, "color": "secondary"}],
            [{"action": {"type": "text", "label": "🛠️ Инструменты"}, "color": "secondary"}]
        ]
    })

# ===== ОТВЕТЫ =====
def handle_message(vk, event) -> None:
    text = normalize_text(event.text)
    user_id = event.user_id
    
    # Убираем эмодзи для правильного сравнения
    clean_text = re.sub(r'[^\w\s]', '', text).strip()
    
    # Словарь с командами
    command_map = {
        "привет": lambda: random.choice(RESPONSES["привет"]),
        "промокоды": lambda: RESPONSES["промокоды"],
        "партнерки": lambda: RESPONSES["партнерки"],
        "сайт": lambda: RESPONSES["сайт"],
        "идеи": lambda: RESPONSES["идеи"],
        "инструменты": lambda: RESPONSES["инструменты"],
        "обучение": lambda: RESPONSES["обучение"],
        "контакты": lambda: RESPONSES["контакты"],
        "факт": lambda: random.choice(FACTS),
        "шутка": lambda: random.choice(JOKES),
        "мотивация": lambda: random.choice(MOTIVATION),
        "статистика": lambda: get_stats_text(user_id),
        "помощь": lambda: (
            "🤖 КОМАНДЫ БОТА AI NEXUS 2026:\n\n"
            "📌 ОСНОВНЫЕ:\n"
            "• привет — приветствие\n"
            "• промокоды — все промокоды\n"
            "• партнерки — ссылки для заработка\n"
            "• сайт — ссылка на ai-toolkit.ru\n\n"
            "💡 ПОЛЕЗНЫЕ:\n"
            "• идеи — способы заработка\n"
            "• инструменты — популярные AI\n"
            "• обучение — ресурсы для изучения\n\n"
            "🎲 РАЗВЛЕЧЕНИЯ:\n"
            "• факт — интересный факт\n"
            "• шутка — пошутить\n"
            "• мотивация — поднять настроение\n\n"
            "📊 СТАТИСТИКА:\n"
            "• статистика — ваша активность\n\n"
            "🔥 Напишите любую команду!"
        )
    }
    
    # Проверяем команды из кнопок
    for cmd_key, cmd_func in command_map.items():
        if cmd_key in clean_text or clean_text == cmd_key:
            response = cmd_func()
            update_user_stats(user_id, cmd_key)
            send_message(vk, user_id, response, get_main_keyboard())
            print(f"[{user_id}] «{event.text}» -> {cmd_key}")
            return
    
    # Проверяем ключевые слова
    keywords = {
        "промокод": "промокоды",
        "скидка": "промокоды",
        "заработ": "идеи",
        "деньг": "идеи",
        "как": "идеи",
        "нейросет": "инструменты",
        "ai": "инструменты",
        "чат": "инструменты"
    }
    
    for keyword, command in keywords.items():
        if keyword in text.lower():
            response = command_map.get(command, lambda: RESPONSES[command])()
            update_user_stats(user_id, command)
            send_message(vk, user_id, response, get_main_keyboard())
            print(f"[{user_id}] «{event.text}» -> {command} (по ключу)")
            return
    
    # Если ничего не подошло
    fallback = (
        "❓ Не понимаю команду.\n\n"
        "📝 Напишите «помощь», чтобы увидеть список всех команд.\n\n"
        "🔥 Или сразу переходите на сайт: https://ai-toolkit.ru"
    )
    send_message(vk, user_id, fallback, get_main_keyboard())
    print(f"[{user_id}] «{event.text}» -> неизвестная команда")

# ===== ЗАПУСК БОТА =====
def main():
    if not VK_TOKEN:
        print("❌ ОШИБКА: Токен VK_TOKEN не найден!")
        print("Установите переменную окружения VK_TOKEN")
        return
    
    print("=" * 50)
    print("🤖 AI NEXUS 2026 — ПРОДВИНУТЫЙ БОТ")
    print("=" * 50)
    print(f"📱 Сообщество: https://vk.com/ai_cherem7")
    print(f"🌐 Сайт: https://ai-toolkit.ru")
    print("-" * 50)
    
    vk_session = vk_api.VkApi(token=VK_TOKEN)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    
    print("✅ БОТ УСПЕШНО ЗАПУЩЕН!")
    print("📨 Ожидание сообщений...")
    print("=" * 50)
    
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            handle_message(vk, event)

# ===== ЗАПУСК =====
if __name__ == "__main__":
    keep_alive()
    main()
