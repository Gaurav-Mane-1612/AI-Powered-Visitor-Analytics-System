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