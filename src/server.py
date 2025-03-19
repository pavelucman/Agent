from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2

app = FastAPI()

origins = [
    "http://localhost:63342",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    message_id: int
    sender_id: int
    chat_id: int
    content: str
    # timestamp: str


def connect_db():
    try:
        return psycopg2.connect(
            dbname="postgres",
            user="pavelucman",
            password="qwerty1234!@#$",
            host="localhost",
            port="5432"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database connection failed")


@app.post("/upload_data/")
async def upload_data(message: Message):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO messages (message_id, sender_id, chat_id, content) VALUES (%s, %s, %s, %s)",
            (message.message_id, message.sender_id, message.chat_id, message.content)
        )
        conn.commit()

        cursor.execute("SELECT * FROM messages WHERE message_id = %s", (message.message_id,))
        inserted_message = cursor.fetchone()
        print("Inserted message:", inserted_message)

        conn.close()
        return {"status": "success", "message": inserted_message}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/messages")
async def get_messages():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM messages")
        rows = cursor.fetchall()
        messages = [
            {
                "message_id": row[0] if row[0] is not None else "No Data",
                "sender_id": row[1] if row[1] is not None else "No Data",
                "chat_id": row[2] if row[2] is not None else "No Data",
                "content": row[3] if row[3] is not None else "No Data",
                "timestamp": row[4] if row[4] is not None else "No Data"
            }
            for row in rows
        ]
        conn.close()
        return messages
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
