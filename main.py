from fastapi import FastAPI, HTTPException
import asyncpg
import os

DATABASE_URL = "postgresql://postgres:[YOUR-PASSWORD]@db.youmrwfedlcediroejfk.supabase.co:5432/postgres"

app = FastAPI()

async def connect_db():
    return await asyncpg.connect(DATABASE_URL)

@app.post("/chat")
async def chat_endpoint(request: dict):
    user_message = request.get("message", "").lower()

    try:
        conn = await connect_db()
        result = await conn.fetchrow("SELECT response FROM intents WHERE keyword = $1", user_message)
        await conn.close()

        if result:
            return {"response": result["response"]}
        else:
            return {"response": "Sorry, I don’t understand that yet."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
