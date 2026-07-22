from backend.app.database.database import get_connection


def create_feedback(feedback):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            # Check whether visit exists
            cursor.execute(
                "SELECT id FROM visits WHERE id=%s",
                (feedback.visit_id,)
            )

            visit = cursor.fetchone()

            if not visit:
                return {
                    "status": "error",
                    "message": "Visit not found"
                }

            sql = """
            INSERT INTO feedback
            (visit_id, rating, feedback)
            VALUES (%s, %s, %s)
            """

            cursor.execute(
                sql,
                (
                    feedback.visit_id,
                    feedback.rating,
                    feedback.feedback
                )
            )

        connection.commit()

        return {
            "status": "success",
            "message": "Feedback submitted successfully"
        }

    finally:
        connection.close()


def get_all_feedback():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            sql = """
            SELECT
                feedback.id,
                visitors.full_name,
                feedback.rating,
                feedback.feedback,
                feedback.created_at
            FROM feedback
            INNER JOIN visits
                ON feedback.visit_id = visits.id
            INNER JOIN visitors
                ON visits.visitor_id = visitors.id
            ORDER BY feedback.id DESC
            """

            cursor.execute(sql)

            return cursor.fetchall()

    finally:
        connection.close()
        
        
def get_feedback_analytics():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            # Total Feedback
            cursor.execute("""
                SELECT COUNT(*) AS total_feedback
                FROM feedback
            """)
            total_feedback = cursor.fetchone()["total_feedback"]

            # Average Rating
            cursor.execute("""
                SELECT ROUND(AVG(rating), 2) AS average_rating
                FROM feedback
            """)
            average_rating = cursor.fetchone()["average_rating"]

            return {
                "total_feedback": total_feedback,
                "average_rating": average_rating
            }

    finally:
        connection.close()


def get_rating_distribution():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT
                    rating,
                    COUNT(*) AS total
                FROM feedback
                GROUP BY rating
                ORDER BY rating
            """)

            return cursor.fetchall()

    finally:
        connection.close()