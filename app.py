#!/usr/bin/env python3
import os, asyncio, datetime, json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

APP_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(APP_DIR, "index.html")

app = FastAPI(title="AIGE OneClick v8.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve index
@app.get("/")
async def root():
    return FileResponse(HTML_PATH, media_type="text/html")

# Health
@app.get("/healthz")
async def health():
    return {"status": "ok", "ts": datetime.datetime.utcnow().isoformat() + "Z"}

# Simple API echo
@app.get("/api/echo")
async def echo(q: str = ""):
    return {"you_said": q, "at": datetime.datetime.utcnow().isoformat() + "Z"}

# WebSocket for chat & deploy commands
@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        await websocket.send_text("مرحبًا، قناة AIGE جاهزة. اكتب أمرك.")
        while True:
            text = await websocket.receive_text()
            t = text.strip()
            if not t:
                continue
            # Simple command router
            if t.startswith("deploy "):
                domain = t.split(" ", 1)[1].strip() or "your-domain.com"
                await websocket.send_text(f"جارٍ تجهيز نشر إلى {domain} ...")
                # Simulate steps
                steps = [
                    "تحقق المتطلبات...",
                    "بناء الحزمة...",
                    "رفع الأصول...",
                    "تهيئة SSL/Proxy...",
                    "اختبارات ما بعد النشر...",
                ]
                for s in steps:
                    await websocket.send_text("• " + s)
                    await asyncio.sleep(0.4)
                await websocket.send_text(f"تم — النشر التجريبي مهيأ لـ {domain}. صِل خطّك الحقيقي هنا لاحقًا.")
            elif t.lower() in {"ابدأ النشر", "ابدأ", "انشر", "deploy"}:
                await websocket.send_text("اكتب: deploy example.com")
            elif t.lower() in {"فعّل الكاميرا", "الكاميرا"}:
                await websocket.send_text("إضغط زر 📸 تشغيل الكاميرا من الواجهة — المتصفح سيطلب إذن.")
            else:
                # Basic AI stub/echo
                reply = f"سمعتك: “{t}”. هذه نسخة المصنع — اربطها بالمحرك الحقيقي لردود ذكية."
                await websocket.send_text(reply)
    except WebSocketDisconnect:
        pass

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)
