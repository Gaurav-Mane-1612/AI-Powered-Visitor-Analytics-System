from backend.app.database.database import get_connection


def create_visitor(visitor):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            sql = """
            INSERT INTO visitors
            (full_name, mobile, email, organization, address)
            VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(sql, (
                visitor.full_name,
                visitor.mobile,
                visitor.email,
                visitor.organization,
                visitor.address
            ))

        connection.commit()

        return {
            "status": "success",
            "message": "Visitor registered successfully"
        }

    finally:
        connection.close()


def get_all_visitors():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            sql = """
            SELECT
                id,
                full_name,
                mobile,
                email,
                organization,
                address,
                created_at
            FROM visitors
            ORDER BY id DESC
            """

            cursor.execute(sql)
            visitors = cursor.fetchall()

            return visitors

    finally:
        connection.close()


def get_visitor_by_id(visitor_id: int):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            sql = """
            SELECT
                id,
                full_name,
                mobile,
                email,
                organization,
                address,
                created_at
            FROM visitors
            WHERE id = %s
            """

            cursor.execute(sql, (visitor_id,))
            visitor = cursor.fetchone()

            if visitor:
                return visitor

            return {
                "status": "error",
                "message": "Visitor not found"
            }

    finally:
        connection.close()


def update_visitor(visitor_id, visitor):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            sql = """
            UPDATE visitors
            SET full_name=%s,
                mobile=%s,
                email=%s,
                organization=%s,
                address=%s
            WHERE id=%s
            """

            rows = cursor.execute(
                sql,
                (
                    visitor.full_name,
                    visitor.mobile,
                    visitor.email,
                    visitor.organization,
                    visitor.address,
                    visitor_id
                )
            )

            connection.commit()

            if rows == 0:
                return None

            return True

    finally:
        connection.close()


def delete_visitor(visitor_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            sql = "DELETE FROM visitors WHERE id=%s"

            rows = cursor.execute(sql, (visitor_id,))

            connection.commit()

            if rows == 0:
                return None

            return True

    finally:
        connection.close()