import asyncio
import websockets
import json

# === Configuration du bot ===
API_TOKEN = "b64d47ce6e457d21c79703ebe5538b0a25d2a487e955dd715471547507fbc"
ROOM_ID = "68d176775950634af0d55ac3"
# ============================

async def handle_message(websocket, message):
    """Réagit aux événements Highrise"""
    try:
        data = json.loads(message)

        # Quand un utilisateur rejoint
        if data.get("type") == "user_join":
            user = data["user"]["username"]
            print(f"👋 {user} vient d'arriver !")

            # Envoie un message fixe dans le chat
            msg = {
                "type": "chat",
                "message": "Bienvenue dans Find Your Vibes ✨"
            }
            await websocket.send(json.dumps(msg))
            print("✅ Message de bienvenue envoyé !")

    except Exception as e:
        print("Erreur dans handle_message:", e)


async def connect_bot():
    """Connexion WebSocket à Highrise"""
    url = f"wss://highrise.game/websocket?roomId={ROOM_ID}&apiKey={API_TOKEN}"
    print("Connexion en cours à Highrise...")

    async for websocket in websockets.connect(url, ping_interval=None):
        try:
            print("✅ Bot connecté avec succès !")

            async for message in websocket:
                await handle_message(websocket, message)
        except Exception as e:
            print("⚠️ Erreur:", e)
            print("Reconnexion dans 5 secondes...")
            await asyncio.sleep(5)
            continue


if __name__ == "__main__":
    asyncio.run(connect_bot())
