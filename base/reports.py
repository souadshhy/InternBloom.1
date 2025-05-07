from django.db import connection


def report_total_applications_per_position():
    with connection.cursor() as cursor:
        cursor.execute("""
               SELECT 
                c.companyName,
                p.title,
                p.duration,
                p.location,
                p.paid,
                p.available,
                COUNT(a.id) AS total_applications
            FROM base_position p
            LEFT JOIN base_apps a ON a.position_id = p.id
            JOIN base_company c ON p.company_id = c.id
            GROUP BY p.id, p.title, p.duration, p.location, p.paid, p.available, c.companyName
            ORDER BY total_applications DESC;
                       """)
        result = cursor.fetchall()
        return result


def report_available_positions():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
            c.companyName,
            p.title,
            p.duration,
            p.location, 
            p.paid,
            p.available 
            FROM base_position AS p JOIN base_company AS c  ON p.company_id = c.id
            LEFT JOIN base_apps AS a ON  p.id = a.position_id 
            WHERE a.id IS NULL;
        """)
        return cursor.fetchall()


def report_apps_per_company():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
            c.companyName,
            COUNT(a.id) AS total_applications
            FROM base_company AS c
            LEFT JOIN base_apps AS a ON c.id = a.company_id
            GROUP BY c.id
            ORDER BY total_applications DESC;
        """)
        return cursor.fetchall()


def report_activity_of_student_per_month():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
            d.deptName,
            s.id,
            s.name,               
            s.surname,               
            s.major,               
            s.year,               
            COUNT(a.id) AS apps_number
            FROM base_student AS s JOIN base_depart AS d ON s.department_id = d.id
            LEFT JOIN base_apps AS a ON s.id = a.student_id
            WHERE strftime('%Y-%m', a.appliedDate) = strftime('%Y-%m', date('now'))
            GROUP BY s.id
            ORDER BY apps_number DESC;
        """)
        return cursor.fetchall()


def report_acceptance_per_company():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
            c.companyName,
            COUNT(CASE WHEN a.appStatus = 'accepted' THEN 1 END) AS accepted_applications,
            COUNT(DISTINCT p.id) AS total_positions_offered,
            ROUND(
                1.0 * COUNT(CASE WHEN a.appStatus = 'accepted' THEN 1 END) / COUNT(DISTINCT p.id), 
                2
            ) AS acceptance_rate
            FROM base_company AS c
            LEFT JOIN base_position AS p ON p.company_id = c.id
            LEFT JOIN base_apps AS a ON a.position_id = p.id
            GROUP BY c.id
            ORDER BY acceptance_rate DESC;

        """)
        return cursor.fetchall()
