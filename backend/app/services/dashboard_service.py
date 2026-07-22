from backend.app.database.database import get_connection


def get_dashboard_statistics():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            # Total Visitors
            cursor.execute(
                "SELECT COUNT(*) AS total_visitors FROM visitors"
            )
            total_visitors = cursor.fetchone()["total_visitors"]

            # Today's Visits
            cursor.execute("""
                SELECT COUNT(*) AS today_visits
                FROM visits
                WHERE DATE(check_in) = CURDATE()
            """)
            today_visits = cursor.fetchone()["today_visits"]

            # Checked-In Visitors
            cursor.execute("""
                SELECT COUNT(*) AS checked_in
                FROM visits
                WHERE status='Checked-In'
            """)
            checked_in = cursor.fetchone()["checked_in"]

            # Checked-Out Visitors
            cursor.execute("""
                SELECT COUNT(*) AS checked_out
                FROM visits
                WHERE status='Checked-Out'
            """)
            checked_out = cursor.fetchone()["checked_out"]

            return {
                "total_visitors": total_visitors,
                "today_visits": today_visits,
                "checked_in": checked_in,
                "checked_out": checked_out
            }

    finally:
        connection.close()