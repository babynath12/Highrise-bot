import asyncio
from highrise import BaseBot, RoomEvent, User

# === Tes données personnelles ===
API_TOKEN = "b64d47ce6e457d21c79703ebe5538b0a25d2a487e955dd715471547507fbc"
ROOM_ID = "68d176775950634af0d55ac3"
# ================================

class TianaBot(BaseBot):
    async def on_ready(self):
        print("✅ Bot connecté avec succès !")

    async def on_user_join(self, event: RoomEvent):
        try:
            user: User = event.user
            username = getattr(user, "username", "Invité inconnu")
            message = f"Bienvenue {username} ✨ dans la salle !"
            await self.send_message(ROOM_ID, message)
            print(f"Message envoyé à {username}")
        except Exception as e:
            print("Erreur dans on_user_join:", e)

async def main():
    bot = TianaBot(token=API_TOKEN)
    await bot.start()
    await bot.wait_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
