from fastapi import FastAPI
from backend.app.database.database import get_connection

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "AI-Powered Visitor Analytics System API is Running"
    }


@app.get("/health")
def health_check():
    try:
        connection = get_connection()
        connection.close()

        return {
            "status": "success",
            "database": "Connected"
        }

    except Exception as e:
        return {
            "status": "error",
            "database": "Disconnected",
            "message": str(e)
        }