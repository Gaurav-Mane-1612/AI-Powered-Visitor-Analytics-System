from backend.app.database.database import get_connection
from backend.app.auth.jwt_handler import create_access_token
import bcrypt


def register_user(user):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            # Check if email already exists
            cursor.execute(
                "SELECT id FROM users WHERE email=%s",
                (user.email,)
            )

            existing_user = cursor.fetchone()

            if existing_user:
                return {
                    "status": "error",
                    "message": "Email already registered"
                }

            # Password Hashing
            hashed_password = bcrypt.hashpw(
                user.password.encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

            sql = """
            INSERT INTO users
            (full_name, email, password, role)
            VALUES (%s, %s, %s, %s)
            """

            cursor.execute(
                sql,
                (
                    user.full_name,
                    user.email,
                    hashed_password,
                    user.role
                )
            )

        connection.commit()

        return {
            "status": "success",
            "message": "User registered successfully"
        }

    finally:
        connection.close()


def get_all_users():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            sql = """
            SELECT
                id,
                full_name,
                email,
                role,
                created_at
            FROM users
            ORDER BY id DESC
            """

            cursor.execute(sql)

            return cursor.fetchall()

    finally:
        connection.close()


def login_user(login_data):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            sql = """
            SELECT
                id,
                full_name,
                email,
                password,
                role
            FROM users
            WHERE email=%s
            """

            cursor.execute(sql, (login_data.email,))
            user = cursor.fetchone()

            # Email not found
            if user is None:
                return {
                    "status": "error",
                    "message": "Invalid email or password"
                }

            # Verify Password
            if not bcrypt.checkpw(
                login_data.password.encode("utf-8"),
                user["password"].encode("utf-8")
            ):
                return {
                    "status": "error",
                    "message": "Invalid email or password"
                }

            # Generate JWT Token
            token = create_access_token(
                {
                    "user_id": user["id"],
                    "email": user["email"],
                    "role": user["role"]
                }
            )

            # Login Success
            return {
                "status": "success",
                "message": "Login successful",
                "access_token": token,
                "token_type": "Bearer",
                "user": {
                    "id": user["id"],
                    "full_name": user["full_name"],
                    "email": user["email"],
                    "role": user["role"]
                }
            }

    finally:
        connection.close()