from fastapi import FastAPI
from vanna.servers.base import ChatHandler
from vanna.servers.fastapi.routes import register_chat_routes
from vanna_setup import setup_vanna

app = FastAPI()

agent, _ = setup_vanna()

chat_handler = ChatHandler(agent)

from fastapi.responses import RedirectResponse

@app.get("/static/vanna-components.js")
def redirect_js():
    return RedirectResponse(
        url="https://img.vanna.ai/vanna-components.js"
    )

register_chat_routes(
    app,
    chat_handler,
    config={
        "dev_mode": True,
        "cdn_url": "https://img.vanna.ai/vanna-components.js"
    }
)

@app.get("/health")
def health():
    return {"status": "ok"}