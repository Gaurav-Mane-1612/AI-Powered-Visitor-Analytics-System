from backend.app.database.database import get_connection


def create_visit(visit):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            # Check if visitor exists
            cursor.execute(
                "SELECT id FROM visitors WHERE id=%s",
                (visit.visitor_id,)
            )

            visitor = cursor.fetchone()

            if not visitor:
                return {
                    "status": "error",
                    "message": "Visitor not found"
                }

            sql = """
            INSERT INTO visits
            (visitor_id, purpose, person_to_meet, department)
            VALUES (%s, %s, %s, %s)
            """

            cursor.execute(
                sql,
                (
                    visit.visitor_id,
                    visit.purpose,
                    visit.person_to_meet,
                    visit.department
                )
            )

        connection.commit()

        return {
            "status": "success",
            "message": "Visit registered successfully"
        }

    finally:
        connection.close()


def get_all_visits():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            sql = """
            SELECT
                visits.id,
                visitors.full_name,
                visits.purpose,
                visits.person_to_meet,
                visits.department,
                visits.check_in
            FROM visits
            INNER JOIN visitors
            ON visits.visitor_id = visitors.id
            ORDER BY visits.id DESC
            """

            cursor.execute(sql)

            return cursor.fetchall()

    finally:
        connection.close()
        
        
def get_visit_by_id(visit_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            sql = """
            SELECT
                visits.id,
                visitors.full_name,
                visits.purpose,
                visits.person_to_meet,
                visits.department,
                visits.check_in
            FROM visits
            INNER JOIN visitors
            ON visits.visitor_id = visitors.id
            WHERE visits.id = %s
            """

            cursor.execute(sql, (visit_id,))

            visit = cursor.fetchone()

            if visit:
                return visit

            return {
                "status": "error",
                "message": "Visit not found"
            }

    finally:
        connection.close()


def checkout_visit(visit_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            sql = """
            UPDATE visits
            SET
                check_out = NOW(),
                status = 'Checked-Out'
            WHERE id = %s
            """

            rows = cursor.execute(sql, (visit_id,))
            connection.commit()

            if rows == 0:
                return {
                    "status": "error",
                    "message": "Visit not found"
                }

            return {
                "status": "success",
                "message": "Visitor checked out successfully"
            }

    finally:
        connection.close()