from fastapi import FastAPI
from app.api.routes import users, tasks, categories, auth
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="FastAPI Tasks", version="1.0.0")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


# === CONFIGURAR CORS ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(categories.router)


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API rodando perfeitamente 🚀"}
