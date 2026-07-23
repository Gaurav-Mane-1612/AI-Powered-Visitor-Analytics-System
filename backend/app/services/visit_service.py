from backend.app.database.database import get_connection
from backend.app.services.audit_service import create_audit_log


def create_visit(visit):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            # Check Visitor Exists
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

        # ===========================
        # Audit Log
        # ===========================
        create_audit_log(
            "System",
            "VISIT_CHECKIN",
            f"Visitor ID '{visit.visitor_id}' checked in for '{visit.person_to_meet}' ({visit.department})."
        )

        return {
            "status": "success",
            "message": "Visit registered successfully"
        }

    finally:
        connection.close()


def get_all_visits(
    page=1,
    limit=10,
    search="",
    department="",
    person_to_meet="",
    sort_by="id",
    order="desc"
):

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            allowed_sort = [
                "id",
                "purpose",
                "department",
                "person_to_meet",
                "check_in",
                "created_at"
            ]

            if sort_by not in allowed_sort:
                sort_by = "id"

            order = order.upper()

            if order not in ["ASC", "DESC"]:
                order = "DESC"

            offset = (page - 1) * limit

            keyword = f"%{search}%"
            dept_keyword = f"%{department}%"
            person_keyword = f"%{person_to_meet}%"

            count_sql = """
            SELECT COUNT(*) AS total
            FROM visits
            INNER JOIN visitors
            ON visits.visitor_id = visitors.id
            WHERE
            (
                visitors.full_name LIKE %s
                OR visits.purpose LIKE %s
            )
            AND visits.department LIKE %s
            AND visits.person_to_meet LIKE %s
            """

            cursor.execute(
                count_sql,
                (
                    keyword,
                    keyword,
                    dept_keyword,
                    person_keyword
                )
            )

            total = cursor.fetchone()["total"]

            sql = f"""
            SELECT
                visits.id,
                visitors.full_name,
                visits.purpose,
                visits.person_to_meet,
                visits.department,
                visits.check_in,
                visits.check_out,
                visits.status
            FROM visits
            INNER JOIN visitors
            ON visits.visitor_id = visitors.id
            WHERE
            (
                visitors.full_name LIKE %s
                OR visits.purpose LIKE %s
            )
            AND visits.department LIKE %s
            AND visits.person_to_meet LIKE %s
            ORDER BY {sort_by} {order}
            LIMIT %s OFFSET %s
            """

            cursor.execute(
                sql,
                (
                    keyword,
                    keyword,
                    dept_keyword,
                    person_keyword,
                    limit,
                    offset
                )
            )

            visits = cursor.fetchall()

            total_pages = (total + limit - 1) // limit

            return {
                "page": page,
                "limit": limit,
                "total_records": total,
                "total_pages": total_pages,
                "sort_by": sort_by,
                "order": order,
                "search": search,
                "department_filter": department,
                "person_filter": person_to_meet,
                "data": visits
            }

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
                visits.check_in,
                visits.check_out,
                visits.status
            FROM visits
            INNER JOIN visitors
            ON visits.visitor_id = visitors.id
            WHERE visits.id=%s
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
            WHERE id=%s
            """

            rows = cursor.execute(sql, (visit_id,))

            connection.commit()

            if rows == 0:
                return {
                    "status": "error",
                    "message": "Visit not found"
                }

            # ===========================
            # Audit Log
            # ===========================
            create_audit_log(
                "System",
                "VISIT_CHECKOUT",
                f"Visit ID '{visit_id}' checked out successfully."
            )

            return {
                "status": "success",
                "message": "Visitor checked out successfully"
            }

    finally:
        connection.close()