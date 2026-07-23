from backend.app.database.database import get_connection


def create_audit_log(user_email, action, description):

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            sql = """
            INSERT INTO audit_logs
            (
                user_email,
                action,
                description
            )
            VALUES
            (
                %s,
                %s,
                %s
            )
            """

            cursor.execute(
                sql,
                (
                    user_email,
                    action,
                    description
                )
            )

        connection.commit()

    finally:
        connection.close()


def get_all_audit_logs(limit=50):

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            sql = """
            SELECT
                id,
                user_email,
                action,
                description,
                created_at
            FROM audit_logs
            ORDER BY created_at DESC
            LIMIT %s
            """

            cursor.execute(sql, (limit,))

            return cursor.fetchall()

    finally:
        connection.close()