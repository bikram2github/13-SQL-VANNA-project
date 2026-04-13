from fastapi import FastAPI
from vanna.servers.base import ChatHandler
from vanna.servers.fastapi.routes import register_chat_routes
from vanna_setup import setup_vanna
from fastapi.responses import RedirectResponse

app = FastAPI()

agent, _ = setup_vanna()
chat_handler = ChatHandler(agent)

cache = {}

@app.post("/ask")
async def ask_question(query: str):

    if not query.strip():
        return {"error": "Query cannot be empty"}
    
    if len(query) > 500:
        return {"error": "Query too long"}


    if query in cache:
        return {
            "cached": True,
            "response": cache[query]
        }

    try:

        response = agent.run(input=query)
        cache[query] = response

        return {
            "cached": False,
            "response": response
        }

    except Exception as e:
        return {"error": str(e)}


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