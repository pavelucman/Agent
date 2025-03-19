import sqlite3
import requests
from pydantic import BaseModel

# SECRET_KEY = os.urandom(16)
API_URL = "http://localhost:8000/upload_data/"
BATCH_SIZE = 2


def connect_db():
    conn = sqlite3.connect("whatsapp.db")
    cursor = conn.cursor()
    return conn, cursor


def extract_data(batch_size=100, offset=0):
    conn, cursor = connect_db()
    query = f"""
        SELECT message_id, sender_id, chat_id, content
        FROM Messages
        LIMIT {batch_size} OFFSET {offset};
    """
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data


def extract_data_in_batches(batch_size=2):
    offset = 0
    while True:
        data = extract_data(batch_size=batch_size, offset=offset)
        if not data:
            break
        yield data
        offset += batch_size


# Encryption Function
# def encrypt_data(data):
#     cipher = AES.new(SECRET_KEY, AES.MODE_EAX)
#     nonce = cipher.nonce
#     ciphertext, tag = cipher.encrypt_and_digest(str(data).encode('utf-8'))
#     return base64.b64encode(nonce + ciphertext).decode('utf-8')


class Message(BaseModel):
    message_id: int
    sender_id: int
    chat_id: int
    content: str
    # timestamp: str


def send_data_to_server(message_data):
    response = requests.post(API_URL, json=message_data)
    if response.status_code == 200:
        print("Data sent successfully:", response.json())
    else:
        print("Failed to send data:", response.status_code, response.text)


def handle_missing_fields(data):
    return [
        {
            'message_id': message[0] if message[0] is not None else 0,
            'sender_id': message[1] if message[1] is not None else 0,
            'chat_id': message[2] if message[2] is not None else 0,
            'content': message[3] if message[3] is not None else '',
        }
        for message in data
    ]


for batch in extract_data_in_batches(batch_size=BATCH_SIZE):
    cleaned_batch = handle_missing_fields(batch)
    for message in cleaned_batch:
        send_data_to_server(message)

for batch in extract_data_in_batches(batch_size=2):
    print("Extracted Batch:", batch)


def send_encrypted_data_to_server(encrypted_data):
    response = requests.post(API_URL, json={"message": encrypted_data})
    print("Response Status:", response.status_code)
    print("Response Content:", response.text)
    if response.status_code == 200:
        print("Data sent successfully:", response.json())
    else:
        print("Failed to send data:", response.status_code, response.text)
