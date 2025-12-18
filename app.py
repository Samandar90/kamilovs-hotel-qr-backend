import os
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = (os.getenv("BOT_TOKEN") or "").strip()
CHAT_ID = (os.getenv("CHAT_ID") or "").strip()

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN missing in .env")
if not CHAT_ID:
    raise RuntimeError("CHAT_ID missing in .env")

TG_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

app = FastAPI(title="Kamilovs QR API", version="1.0.0")

# На проде лучше заменить "*" на домен GitHub Pages
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ReviewPayload(BaseModel):
    lang: str = Field(default="ru", max_length=8)
    room: str = Field(min_length=1, max_length=32)
    rating: int = Field(ge=1, le=5)
    name: str = Field(min_length=1, max_length=64)
    phone: Optional[str] = Field(default=None, max_length=32)
    text: str = Field(min_length=1, max_length=1200)
    client_ts: Optional[str] = Field(default="")

def format_review(p: ReviewPayload) -> str:
    lines = []
    lines.append("🟦 Kamilovs’ Hotel — Review")
    lines.append(f"Room: {p.room}")
    lines.append(f"Rating: {'★'*p.rating}{'☆'*(5-p.rating)} ({p.rating}/5)")
    lines.append(f"Name: {p.name}")
    if p.phone:
        lines.append(f"Phone: {p.phone}")
    if p.client_ts:
        lines.append(f"Time: {p.client_ts}")
    lines.append("")
    lines.append(p.text)
    return "\n".join(lines)

@app.get("/health")
async def health():
    return {"ok": True}

@app.post("/api/review")
async def send_review(payload: ReviewPayload):
    text = format_review(payload)
    try:
        async with httpx.AsyncClient(timeout=12) as client:
            r = await client.post(
                f"{TG_API}/sendMessage",
                json={"chat_id": CHAT_ID, "text": text, "disable_web_page_preview": True},
            )
            data = r.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Telegram request failed: {e}")

    if not data.get("ok"):
        raise HTTPException(status_code=502, detail=data.get("description", "Telegram error"))

    return {"ok": True}
