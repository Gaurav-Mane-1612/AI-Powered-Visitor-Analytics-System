from backend.app.database.database import get_connection
from backend.app.services.audit_service import create_audit_log


def create_feedback(feedback):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

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

        # ===============================
        # Audit Log
        # ===============================
        create_audit_log(
            "System",
            "FEEDBACK_SUBMIT",
            f"Feedback submitted for Visit ID '{feedback.visit_id}' with Rating '{feedback.rating}'."
        )

        return {
            "status": "success",
            "message": "Feedback submitted successfully"
        }

    finally:
        connection.close()


# ==========================================================
# Search + Pagination + Rating Filter + Sorting
# ==========================================================

def get_all_feedback(
    page=1,
    limit=10,
    search="",
    rating=0,
    sort_by="id",
    order="desc"
):

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            allowed_sort = [
                "id",
                "rating",
                "created_at"
            ]

            if sort_by not in allowed_sort:
                sort_by = "id"

            order = order.upper()

            if order not in ["ASC", "DESC"]:
                order = "DESC"

            offset = (page - 1) * limit

            keyword = f"%{search}%"

            if rating == 0:

                count_sql = """
                SELECT COUNT(*) AS total
                FROM feedback
                INNER JOIN visits
                    ON feedback.visit_id = visits.id
                INNER JOIN visitors
                    ON visits.visitor_id = visitors.id
                WHERE
                    visitors.full_name LIKE %s
                    OR feedback.feedback LIKE %s
                """

                cursor.execute(
                    count_sql,
                    (keyword, keyword)
                )

            else:

                count_sql = """
                SELECT COUNT(*) AS total
                FROM feedback
                INNER JOIN visits
                    ON feedback.visit_id = visits.id
                INNER JOIN visitors
                    ON visits.visitor_id = visitors.id
                WHERE
                (
                    visitors.full_name LIKE %s
                    OR feedback.feedback LIKE %s
                )
                AND feedback.rating=%s
                """

                cursor.execute(
                    count_sql,
                    (
                        keyword,
                        keyword,
                        rating
                    )
                )

            total = cursor.fetchone()["total"]

            if rating == 0:

                sql = f"""
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
                WHERE
                    visitors.full_name LIKE %s
                    OR feedback.feedback LIKE %s
                ORDER BY {sort_by} {order}
                LIMIT %s OFFSET %s
                """

                cursor.execute(
                    sql,
                    (
                        keyword,
                        keyword,
                        limit,
                        offset
                    )
                )

            else:

                sql = f"""
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
                WHERE
                (
                    visitors.full_name LIKE %s
                    OR feedback.feedback LIKE %s
                )
                AND feedback.rating=%s
                ORDER BY {sort_by} {order}
                LIMIT %s OFFSET %s
                """

                cursor.execute(
                    sql,
                    (
                        keyword,
                        keyword,
                        rating,
                        limit,
                        offset
                    )
                )

            feedback_list = cursor.fetchall()

            total_pages = (total + limit - 1) // limit

            return {
                "page": page,
                "limit": limit,
                "total_records": total,
                "total_pages": total_pages,
                "sort_by": sort_by,
                "order": order,
                "search": search,
                "rating_filter": rating,
                "data": feedback_list
            }

    finally:
        connection.close()


def get_feedback_analytics():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT COUNT(*) AS total_feedback
                FROM feedback
            """)

            total_feedback = cursor.fetchone()["total_feedback"]

            cursor.execute("""
                SELECT ROUND(AVG(rating),2) AS average_rating
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