from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

active_users = {}

@app.get("/", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login_post(request: Request, username: str = Form(...)):
    if username in active_users:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Username already taken"})
    return RedirectResponse(url=f"/chat/{username}", status_code=302)

@app.get("/chat/{username}", response_class=HTMLResponse)
async def chat(request: Request, username: str):
    return templates.TemplateResponse("chat.html", {"request": request, "username": username, "users": list(active_users.keys())})

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await websocket.accept()
    active_users[username] = websocket
    try:
        while True:
            data = await websocket.receive_json()
            to_user = data["to"]
            message = data["message"]
            # মেসেজ প্রেরণ
            if to_user in active_users:
                await active_users[to_user].send_json({"from": username, "message": message})
    except WebSocketDisconnect:
        del active_users[username]

