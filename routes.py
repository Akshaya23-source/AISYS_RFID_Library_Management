from flask import Blueprint, render_template, request, redirect, url_for
from app.services.rfid_mock import read_rfid_tag, check_rfid_connection
from app.db import get_db_connection
import sqlite3

# Create Blueprint
bp = Blueprint("main", __name__)


# ---------------------------------
# 1. HOME PAGE
# ---------------------------------

@bp.route("/")
def home():
    return render_template("index.html")


# ---------------------------------
# 2. HEALTH CHECK
# ---------------------------------

@bp.route("/health")
def health():
    return {
        "status": "running",
        "application": "AISYS RFID Library"
    }


# ---------------------------------
# 3. RFID CONNECTION STATUS
# ---------------------------------

@bp.route("/rfid-status")
def rfid_status():
    status = check_rfid_connection()
    return status


# ---------------------------------
# 4. BOOK MANAGEMENT
# ---------------------------------

@bp.route("/books", methods=["GET", "POST"])
def books():

    error = None
    message = None

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        isbn = request.form.get("isbn", "").strip()
        rfid_tag = request.form.get("rfid_tag", "").strip()

        if not title:
            error = "Book title is required."

        else:
            try:
                rfid_tag = read_rfid_tag(rfid_tag) if rfid_tag else None

                conn = get_db_connection()

                try:
                    conn.execute("""
                        INSERT INTO books
                        (title, author, isbn, rfid_tag)
                        VALUES (?, ?, ?, ?)
                    """, (title, author, isbn, rfid_tag))

                    conn.commit()
                    return redirect(url_for("main.books"))

                except sqlite3.IntegrityError:
                    error = "This RFID tag is already registered."

                finally:
                    conn.close()

            except ValueError as e:
                error = str(e)

    conn = get_db_connection()

    try:
        all_books = conn.execute(
            "SELECT * FROM books ORDER BY id DESC"
        ).fetchall()
    finally:
        conn.close()

    return render_template(
        "books.html",
        books=all_books,
        error=error,
        message=message
    )


# ---------------------------------
# 5. RFID REGISTRATION
# ---------------------------------

@bp.route("/register-rfid", methods=["GET", "POST"])
def register_rfid():

    message = None
    error = None

    conn = get_db_connection()

    try:
        if request.method == "POST":

            book_id = request.form.get("book_id")
            raw_tag = request.form.get("rfid_tag", "").strip()

            if not book_id or not raw_tag:
                error = "Please select a book and enter an RFID tag."

            else:
                try:
                    rfid_tag = read_rfid_tag(raw_tag)

                    cursor = conn.execute("""
                        UPDATE books
                        SET rfid_tag = ?
                        WHERE id = ?
                    """, (rfid_tag, book_id))

                    if cursor.rowcount == 0:
                        error = "Selected book was not found."
                    else:
                        conn.commit()
                        message = "RFID tag registered successfully!"

                except ValueError as e:
                    error = str(e)

                except sqlite3.IntegrityError:
                    error = "This RFID tag is already assigned."

        all_books = conn.execute(
            "SELECT * FROM books ORDER BY title"
        ).fetchall()

    finally:
        conn.close()

    return render_template(
        "rfid.html",
        books=all_books,
        message=message,
        error=error
    )


# ---------------------------------
# 6. MEMBER MANAGEMENT
# ---------------------------------

@bp.route("/members", methods=["GET", "POST"])
def members():

    error = None
    message = None

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()

        if not name:
            error = "Member name is required."

        elif email and (
            "@" not in email or "." not in email.split("@")[-1]
        ):
            error = "Please enter a valid email address."

        else:
            conn = get_db_connection()

            try:
                conn.execute("""
                    INSERT INTO members
                    (name, email, phone)
                    VALUES (?, ?, ?)
                """, (name, email or None, phone or None))

                conn.commit()
                return redirect(url_for("main.members"))

            except sqlite3.IntegrityError:
                error = "This email is already registered."

            finally:
                conn.close()

    conn = get_db_connection()

    try:
        all_members = conn.execute("""
            SELECT * FROM members
            ORDER BY id DESC
        """).fetchall()

    finally:
        conn.close()

    return render_template(
        "members.html",
        members=all_members,
        error=error,
        message=message
    )


# ---------------------------------
# 7. BOOK ISSUE AND RETURN
# ---------------------------------

@bp.route("/issue-return", methods=["GET", "POST"])
def issue_return():

    error = None
    message = None

    conn = get_db_connection()

    try:
        if request.method == "POST":

            action = request.form.get("action")

            # ISSUE BOOK
            if action == "issue":

                book_id = request.form.get("book_id")
                member_id = request.form.get("member_id")

                if not book_id or not member_id:
                    error = "Please select a book and a member."

                else:
                    book = conn.execute(
                        "SELECT * FROM books WHERE id = ?",
                        (book_id,)
                    ).fetchone()

                    member = conn.execute(
                        "SELECT * FROM members WHERE id = ?",
                        (member_id,)
                    ).fetchone()

                    if not book or not member:
                        error = "Book or member not found."

                    elif book["status"] != "Available":
                        error = "This book is not available."

                    else:
                        conn.execute("""
                            INSERT INTO issue_records
                            (book_id, member_id, status)
                            VALUES (?, ?, 'Issued')
                        """, (book_id, member_id))

                        conn.execute("""
                            UPDATE books
                            SET status = 'Issued'
                            WHERE id = ?
                        """, (book_id,))

                        conn.commit()
                        message = "Book issued successfully!"

            # RETURN BOOK
            elif action == "return":

                issue_id = request.form.get("issue_id")

                if not issue_id:
                    error = "Please select an issued book."

                else:
                    record = conn.execute("""
                        SELECT * FROM issue_records
                        WHERE id = ? AND status = 'Issued'
                    """, (issue_id,)).fetchone()

                    if not record:
                        error = "Issued record not found."

                    else:
                        conn.execute("""
                            UPDATE issue_records
                            SET status = 'Returned',
                                returned_at = CURRENT_TIMESTAMP
                            WHERE id = ?
                        """, (issue_id,))

                        conn.execute("""
                            UPDATE books
                            SET status = 'Available'
                            WHERE id = ?
                        """, (record["book_id"],))

                        conn.commit()
                        message = "Book returned successfully!"

            else:
                error = "Invalid action."

        # Fetch available books
        available_books = conn.execute("""
            SELECT * FROM books
            WHERE status = 'Available'
            ORDER BY title
        """).fetchall()

        # Fetch members
        all_members = conn.execute("""
            SELECT * FROM members
            ORDER BY name
        """).fetchall()

        # Fetch currently issued books
        issued_books = conn.execute("""
    SELECT
        issue_records.id,
        books.title,
        members.name AS member_name,
        issue_records.issued_at,
        issue_records.status
    FROM issue_records
    JOIN books ON issue_records.book_id = books.id
    JOIN members ON issue_records.member_id = members.id
    WHERE issue_records.status = 'Issued'
    ORDER BY issue_records.id DESC
""").fetchall()
    finally:
        conn.close()

    return render_template(
    "issue_return.html",
    available_books=available_books,
    members=all_members,
    active_issues=issued_books,
    error=error,
    message=message
)


# ---------------------------------
# 8. RFID BOOK SCANNING
# ---------------------------------

@bp.route("/scan-rfid", methods=["GET", "POST"])
def scan_rfid():

    book = None
    error = None
    rfid_tag = ""

    if request.method == "POST":

        try:
            rfid_tag = read_rfid_tag(
                request.form.get("rfid_tag", "")
            )

            conn = get_db_connection()

            try:
                book = conn.execute("""
                    SELECT * FROM books
                    WHERE rfid_tag = ?
                """, (rfid_tag,)).fetchone()

                if not book:
                    error = "RFID tag not registered."

            finally:
                conn.close()

        except ValueError:
            error = "Please enter a valid RFID tag."

    return render_template(
        "scan_rfid.html",
        book=book,
        error=error,
        rfid_tag=rfid_tag
    )


# ---------------------------------
# 9. LIBRARY DASHBOARD
# ---------------------------------
# ---------------------------------
# 9. LIBRARY DASHBOARD
# ---------------------------------

@bp.route("/dashboard")
def dashboard():

    rfid_status = check_rfid_connection()

    conn = get_db_connection()

    try:
        # Total books
        total_books = conn.execute(
            "SELECT COUNT(*) FROM books"
        ).fetchone()[0]

        # Available books
        available_books = conn.execute("""
            SELECT COUNT(*) FROM books
            WHERE status = 'Available'
        """).fetchone()[0]

        # Issued books
        issued_books_count = conn.execute("""
            SELECT COUNT(*) FROM books
            WHERE status = 'Issued'
        """).fetchone()[0]

        # Total members
        total_members = conn.execute(
            "SELECT COUNT(*) FROM members"
        ).fetchone()[0]

        # Recent transactions
        recent_issues = conn.execute("""
            SELECT
                books.title,
                members.name,
                issue_records.issued_at,
                issue_records.status
            FROM issue_records
            JOIN books
                ON issue_records.book_id = books.id
            JOIN members
                ON issue_records.member_id = members.id
            ORDER BY issue_records.id DESC
            LIMIT 5
        """).fetchall()

    finally:
        conn.close()

    return render_template(
        "dashboard.html",
        total_books=total_books,
        available_books=available_books,
        issued_books_count=issued_books_count,
        total_members=total_members,
        recent_issues=recent_issues,
        rfid_status=rfid_status
    )