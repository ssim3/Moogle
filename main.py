import asyncio
import telegram
from dotenv import load_dotenv
import os

load_dotenv(override=True)
BOT_API_KEY = os.getenv("BOT_API_KEY")

async def main():
    print(BOT_API_KEY)
    bot = telegram.Bot(BOT_API_KEY)
    async with bot:
        updates = (await bot.get_updates())[0]
        print(updates)

if __name__ == "__main__":
    asyncio.run(main())
