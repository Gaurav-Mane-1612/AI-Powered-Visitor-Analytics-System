from fastapi import HTTPException
from backend.app.database.database import get_connection
from backend.app.services.audit_service import create_audit_log


def create_visitor(visitor):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            # Check duplicate mobile
            cursor.execute(
                "SELECT id FROM visitors WHERE mobile=%s",
                (visitor.mobile,)
            )

            if cursor.fetchone():
                raise HTTPException(
                    status_code=400,
                    detail="Mobile number already exists"
                )

            # Check duplicate email
            if visitor.email:
                cursor.execute(
                    "SELECT id FROM visitors WHERE email=%s",
                    (visitor.email,)
                )

                if cursor.fetchone():
                    raise HTTPException(
                        status_code=400,
                        detail="Email already exists"
                    )

            sql = """
            INSERT INTO visitors
            (full_name, mobile, email, organization, address)
            VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(
                sql,
                (
                    visitor.full_name,
                    visitor.mobile,
                    visitor.email,
                    visitor.organization,
                    visitor.address
                )
            )

        connection.commit()

        create_audit_log(
            user_email="System",
            action="VISITOR_REGISTER",
            description=f"Visitor '{visitor.full_name}' registered successfully."
        )

        return {
            "status": "success",
            "message": "Visitor registered successfully"
        }

    finally:
        connection.close()


def get_all_visitors(
    page=1,
    limit=10,
    search="",
    organization="",
    sort_by="id",
    order="desc"
):

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            allowed_sort_columns = [
                "id",
                "full_name",
                "mobile",
                "email",
                "organization",
                "created_at"
            ]

            if sort_by not in allowed_sort_columns:
                sort_by = "id"

            order = order.upper()

            if order not in ["ASC", "DESC"]:
                order = "DESC"

            offset = (page - 1) * limit

            keyword = f"%{search}%"
            org_keyword = f"%{organization}%"

            count_sql = """
            SELECT COUNT(*) AS total
            FROM visitors
            WHERE
            (
                full_name LIKE %s
                OR mobile LIKE %s
                OR email LIKE %s
                OR organization LIKE %s
            )
            AND organization LIKE %s
            """

            cursor.execute(
                count_sql,
                (
                    keyword,
                    keyword,
                    keyword,
                    keyword,
                    org_keyword
                )
            )

            total = cursor.fetchone()["total"]

            sql = f"""
            SELECT
                id,
                full_name,
                mobile,
                email,
                organization,
                address,
                created_at
            FROM visitors
            WHERE
            (
                full_name LIKE %s
                OR mobile LIKE %s
                OR email LIKE %s
                OR organization LIKE %s
            )
            AND organization LIKE %s
            ORDER BY {sort_by} {order}
            LIMIT %s OFFSET %s
            """

            cursor.execute(
                sql,
                (
                    keyword,
                    keyword,
                    keyword,
                    keyword,
                    org_keyword,
                    limit,
                    offset
                )
            )

            visitors = cursor.fetchall()

            total_pages = (total + limit - 1) // limit

            return {
                "page": page,
                "limit": limit,
                "total_records": total,
                "total_pages": total_pages,
                "sort_by": sort_by,
                "order": order,
                "search": search,
                "organization_filter": organization,
                "data": visitors
            }

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
            WHERE id=%s
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
            SET
                full_name=%s,
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

            create_audit_log(
                user_email="System",
                action="VISITOR_UPDATE",
                description=f"Visitor '{visitor.full_name}' updated successfully."
            )

            return True

    finally:
        connection.close()


def delete_visitor(visitor_id):

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            # Get visitor name before delete
            cursor.execute(
                "SELECT full_name FROM visitors WHERE id=%s",
                (visitor_id,)
            )

            visitor = cursor.fetchone()

            if not visitor:
                return None

            rows = cursor.execute(
                "DELETE FROM visitors WHERE id=%s",
                (visitor_id,)
            )

            connection.commit()

            if rows == 0:
                return None

            create_audit_log(
                user_email="System",
                action="VISITOR_DELETE",
                description=f"Visitor '{visitor['full_name']}' deleted successfully."
            )

            return True

    finally:
        connection.close()