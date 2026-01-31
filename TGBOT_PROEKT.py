import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Токен бота
bot = Bot(token="8346411165:AAGdDbYOsJqg26Ete_BxkC_1lVZ8ODVp4bY")
dp = Dispatcher()

# Словарь героев Dota 2 с полными именами и возможными сокращениями
HEROES = {
    "abaddon": ["aba", "abbadon"],
    "alchemist": ["alch", "alche"],
    "ancient_apparition": ["aa", "ancient"],
    "anti_mage": ["am", "antimage", "anti"],
    "arc_warden": ["arc", "warden"],
    "axe": ["axe"],
    "bane": ["bane"],
    "batrider": ["bat", "batrider"],
    "beastmaster": ["bm", "beast"],
    "bloodseeker": ["bs", "blood", "seeker"],
    "bounty_hunter": ["bh", "bounty"],
    "brewmaster": ["brew", "panda"],
    "bristleback": ["bb", "bristle"],
    "broodmother": ["brood", "bm", "spider"],
    "centaur_warrunner": ["centaur", "cw"],
    "chaos_knight": ["ck", "chaos"],
    "chen": ["chen"],
    "clinkz": ["clinkz", "bone"],
    "clockwerk": ["clock", "cw", "rattletrap"],
    "crystal_maiden": ["cm", "crystal"],
    "dark_seer": ["ds", "dark"],
    "dark_willow": ["dw", "willow"],
    "dawnbreaker": ["dawn", "db"],
    "dazzle": ["dazzle"],
    "death_prophet": ["dp", "prophet"],
    "disruptor": ["disruptor"],
    "doom": ["doom", "doom_bringer"],
    "dragon_knight": ["dk", "dragon"],
    "drow_ranger": ["drow", "dr"],
    "earth_spirit": ["earth", "es"],
    "earthshaker": ["shaker", "es"],
    "elder_titan": ["et", "elder", "titan"],
    "ember_spirit": ["ember", "es"],
    "enchantress": ["enchant", "ench"],
    "enigma": ["enigma"],
    "faceless_void": ["void", "fv"],
    "grimstroke": ["grim", "stroke"],
    "gyrocopter": ["gyro", "copter"],
    "hoodwink": ["hood", "wink"],
    "huskar": ["huskar"],
    "invoker": ["invoker", "voker", "invo"],
    "io": ["io", "wisp"],
    "jakiro": ["jakiro", "twin"],
    "juggernaut": ["jugg", "jugger"],
    "keeper_of_the_light": ["kotl", "keeper"],
    "kunkka": ["kunkka", "admiral"],
    "legion_commander": ["lc", "legion"],
    "leshrac": ["lesh", "leshrac"],
    "lich": ["lich"],
    "life_stealer": ["ls", "naix", "lifestealer"],
    "lina": ["lina"],
    "lion": ["lion"],
    "lone_druid": ["ld", "lone", "druid"],
    "luna": ["luna"],
    "lycan": ["lycan", "wolf"],
    "magnus": ["magnus", "mag"],
    "marci": ["marci"],
    "mars": ["mars"],
    "medusa": ["medusa", "dusa"],
    "meepo": ["meepo"],
    "mirana": ["mirana", "potm"],
    "monkey_king": ["mk", "monkey"],
    "morphling": ["morph", "morphling"],
    "muerta": ["muerta"],
    "naga_siren": ["naga", "siren"],
    "nature's_prophet": ["np", "furion", "prophet"],
    "necrophos": ["necro", "necrophos"],
    "night_stalker": ["ns", "night"],
    "nyx_assassin": ["nyx", "assassin"],
    "ogre_magi": ["ogre", "om"],
    "omniknight": ["omni", "omniknight"],
    "oracle": ["oracle"],
    "outworld_destroyer": ["od", "outworld"],
    "pangolier": ["pango", "pangolier"],
    "phantom_assassin": ["pa", "phantom"],
    "phantom_lancer": ["pl", "lancer"],
    "phoenix": ["phoenix"],
    "primal_beast": ["pb", "primal"],
    "puck": ["puck"],
    "pudge": ["pudge"],
    "pugna": ["pugna"],
    "queen_of_pain": ["qop", "queen"],
    "razor": ["razor"],
    "riki": ["riki"],
    "rubick": ["rubick"],
    "sand_king": ["sk", "sand"],
    "shadow_demon": ["sd", "shadow"],
    "shadow_fiend": ["sf", "nevermore"],
    "shadow_shaman": ["ss", "rhasta"],
    "silencer": ["silencer"],
    "skywrath_mage": ["sky", "swm"],
    "slardar": ["slardar"],
    "slark": ["slark"],
    "snapfire": ["snap", "fire"],
    "sniper": ["sniper"],
    "spectre": ["spec", "spectre"],
    "spirit_breaker": ["sb", "bara", "spirit"],
    "storm_spirit": ["storm", "ss"],
    "sven": ["sven"],
    "techies": ["tech", "techies"],
    "templar_assassin": ["ta", "templar"],
    "terrorblade": ["tb", "terror"],
    "tidehunter": ["tide", "th"],
    "timbersaw": ["timber", "saw"],
    "tinker": ["tinker"],
    "tiny": ["tiny"],
    "treant_protector": ["treant", "tree"],
    "troll_warlord": ["troll", "tw"],
    "tusk": ["tusk"],
    "underlord": ["ul", "underlord"],
    "undying": ["undying", "dirge"],
    "ursa": ["ursa"],
    "vengeful_spirit": ["vs", "venge"],
    "venomancer": ["veno", "venom"],
    "viper": ["viper"],
    "visage": ["visage"],
    "void_spirit": ["voids", "vs"],
    "warlock": ["warlock"],
    "weaver": ["weaver"],
    "windranger": ["wr", "wind"],
    "winter_wyvern": ["ww", "wyvern"],
    "witch_doctor": ["wd", "witch"],
    "wraith_king": ["wk", "skeleton"],
    "zeus": ["zeus"]
}

def find_hero_by_alias(alias):
    """Находит полное имя героя по алиасу или сокращению"""
    alias = alias.lower().strip()
    
    #проверка имени
    if alias in HEROES:
        return alias
    
    # Проверка алиасов и сокращений
    for full_name, aliases in HEROES.items():
        if alias == full_name or alias in aliases:
            return full_name
    
    # Проверяем частичное совпадение
    for full_name in HEROES.keys():
        if alias in full_name or any(alias in a for a in HEROES[full_name]):
            return full_name
    
    return None

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "🎮 Привет! Я бот для поиска гайдов по героям Dota 2.\n\n"
        "Напиши название героя (можно сокращенно) и я пришлю ссылки на сайты с закупами и гайдами.\n\n"
        "Примеры:\n"
        "• pa (Phantom Assassin)\n"
        "• am (Anti-Mage)\n"
        "• invoker (полное имя)\n"
        
    )

@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "🎯 Как использовать бота:\n\n"
        "Просто напиши имя героя или его сокращение:\n"
        "• Полное имя: phantom_assassin\n"
        "• Сокращение: pa, am, dk\n"
        "• Часть имени: phoen, invo, venge\n\n"
        "📋 Популярные сокращения:\n"
        "• AM = Anti-Mage\n"
        "• PA = Phantom Assassin\n"
        "• DK = Dragon Knight\n"
        "• TA = Templar Assassin\n"
        "• NP = Nature's Prophet\n\n"
        "🛠 Команды:\n"
        "/start - начать работу\n"
        "/help - помощь"
    )

@dp.message()
async def handle_hero_request(message: Message):
    user_input = message.text.strip()
    
    # поиск героя по введенному значению
    hero_name = find_hero_by_alias(user_input)
    
    if not hero_name:
        await message.answer(
            f"Ошибка❌ герой '{user_input}' не найден!\n\n"
            f"📝 Попробуйте:\n"
            f"• Использовать сокращение (pa, am, dk)\n"
            f"• Написать полное имя с нижним подчеркиванием\n"
            f"• Проверить правильность написания\n\n"
            f"💡 Примеры: 'pa', 'antimage', 'phantom_assassin'\n"
            f"🆘 Для помощи используйте /help"
        )
        return
    
    # Получаем красивое отображаемое имя
    display_name = hero_name.replace('_', ' ').title()
    
    # Сайты с гайдами
    sites = {
        "Dotabuff": f"https://www.dotabuff.com/heroes/{hero_name}",
        "Dota2Protracker": f"https://www.dota2protracker.com/hero/{hero_name}",
        "OPendota": f"https://www.opendota.com/heroes/{hero_name}",
        "Stratz": f"https://stratz.com/heroes/{hero_name}",
        "Dota2Wiki": f"https://dota2.fandom.com/wiki/{display_name.replace(' ', '_')}"
    }
    
    # Формирование ответа
    response = f"✅ Герой найден: {display_name}\n"
    if user_input.lower() != hero_name:
        response += f"📌 Ваш запрос: '{user_input}'\n"
    
    response += "\n🔗 Ссылки на гайды и статистику:\n\n"
    
    for site_name, url in sites.items():
        response += f"• {site_name}: {url}\n"
    
    response += "\n💡 Совет: Изучите несколько гайдов для лучшего понимания героя!"
    
    await message.answer(response)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())