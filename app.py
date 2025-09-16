#!/usr/bin/env python3
import os, asyncio, datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

APP_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(APP_DIR, "index.html")

app = FastAPI(title="AIGE OneClick v8.1")

# CORS (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend
@app.get("/")
async def root():
    return FileResponse(HTML_PATH, media_type="text/html")

# Health check
@app.get("/healthz")
async def health():
    return {"status": "ok", "ts": datetime.datetime.utcnow().isoformat() + "Z"}

# Simple API echo
@app.get("/api/echo")
async def echo(q: str = ""):
    return {"you_said": q, "at": datetime.datetime.utcnow().isoformat() + "Z"}

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        await websocket.send_text("مرحبًا، قناة AIGE جاهزة. اكتب أمرك.")
        while True:
            text = await websocket.receive_text()
            t = text.strip()
            if not t:
                continue

            # Command routing
            if t.startswith("deploy "):
                domain = t.split(" ", 1)[1].strip() or "your-domain.com"
                await websocket.send_text(f"جارٍ تجهيز نشر إلى {domain} ...")
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
                await websocket.send_text(f"تم — النشر التجريبي مهيأ لـ {domain}.")
            elif t.lower() in {"ابدأ النشر", "ابدأ", "انشر", "deploy"}:
                await websocket.send_text("اكتب: deploy example.com")
            elif t.lower() in {"فعّل الكاميرا", "الكاميرا"}:
                await websocket.send_text("اضغط زر 📸 تشغيل الكاميرا من الواجهة.")
            else:
                await websocket.send_text(f"سمعتك: “{t}”. هذه نسخة المصنع — اربطها بالمحرك الحقيقي لردود ذكية.")
    except WebSocketDisconnect:
        pass

# Start app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)
