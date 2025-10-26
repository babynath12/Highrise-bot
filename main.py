import os
import asyncio
import websockets
import json
from aiohttp import web

# === Configuration du bot ===
# Si tu préfères, tu peux définir les variables d'environnement sur Render au lieu d'écrire directement ici.
API_TOKEN = os.environ.get("API_TOKEN", "b64d47ce6e457d21c79703ebe5538b0a25d2a487e955dd715471547507fbc")
ROOM_ID = os.environ.get("ROOM_ID", "68d176775950634af0d55ac3")
# ============================

async def handle_message(websocket, message):
    """Réagit aux événements Highrise"""
    try:
        data = json.loads(message)

        # Quand un utilisateur rejoint
        if data.get("type") == "user_join":
            username = data["user"].get("username", "Invité")
            print(f"👋 {username} vient d'arriver !")

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
    """Connexion WebSocket à Highrise — boucle de reconnexion incluse"""
    url = f"wss://highrise.game/websocket?roomId={ROOM_ID}&apiKey={API_TOKEN}"
    print("Connexion en cours à Highrise...")

    while True:
        try:
            async with websockets.connect(url, ping_interval=None) as websocket:
                print("✅ Bot connecté avec succès !")
                async for message in websocket:
                    await handle_message(websocket, message)
        except Exception as e:
            print("⚠️ Erreur WebSocket:", e)
            print("Reconnexion dans 5 secondes...")
            await asyncio.sleep(5)


# --- Serveur HTTP minimal pour binder sur le PORT requis par Render ---
async def handle_root(request):
    # Simple endpoint pour que Render voie un port ouvert
    return web.Response(text="Bot Find Your Vibes — en ligne ✅")

async def start_http_server():
    app = web.Application()
    app.add_routes([web.get('/', handle_root)])
    port = int(os.environ.get("PORT", 8000))  # Render fournit $PORT automatiquement
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Serveur HTTP lancé sur le port {port} (endpoint /) — cela permet à Render d'accepter le déploiement.")

async def main():
    # Lancer serveur HTTP + bot en parallèle
    await asyncio.gather(
        start_http_server(),
        connect_bot()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Arrêt du bot.")
