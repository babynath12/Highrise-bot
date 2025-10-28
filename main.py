import os
import asyncio
import websockets
import json
from aiohttp import web

# === Configuration du bot (tes données) ===
API_TOKEN = "b64d47ce6e457d21c79703ebe5538b0a25d2a487e955dd715471547507fbc"
ROOM_ID = "68d176775950634af0d55ac3"
# ==========================================

async def handle_message(websocket, message):
    try:
        data = json.loads(message)
        if data.get("type") == "user_join":
            username = data["user"].get("username", "Invité")
            print(f"👋 {username} vient d'arriver !")
            await websocket.send(json.dumps({
                "type": "chat",
                "message": f"Bienvenue {username} ✨"
            }))
    except Exception as e:
        print("Erreur dans handle_message:", e)

async def connect_bot_once():
    url = f"wss://highrise.game/websocket?roomId={ROOM_ID}&apiKey={API_TOKEN}"
    print("Connexion en cours à Highrise...")
    try:
        async with websockets.connect(url, ping_interval=None) as websocket:
            print("✅ Bot connecté avec succès ! (test 5 min)")
            try:
                async with asyncio.timeout(300):  # reste connecté 5 minutes
                    async for message in websocket:
                        await handle_message(websocket, message)
            except asyncio.TimeoutError:
                print("⏰ Fin du test : déconnexion du bot.")
    except Exception as e:
        print("⚠️ Erreur WebSocket:", e)

async def handle_root(request):
    return web.Response(text="Bot Find Your Vibes (test 5 min) — en ligne ✅")

async def start_http_server():
    app = web.Application()
    app.add_routes([web.get('/', handle_root)])
    port = int(os.environ.get("PORT", 8000))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"🌐 Serveur HTTP lancé sur le port {port}")

async def main():
    await asyncio.gather(
        start_http_server(),
        connect_bot_once()
    )

if __name__ == "__main__":
    asyncio.run(main())
