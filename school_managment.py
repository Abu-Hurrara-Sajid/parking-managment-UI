
import tkinter as tk
from datetime import datetime

import pyodbc

DRIVER = "ODBC Driver 17 for SQL Server"
SERVER = "DESKTOP-KUT14B4\SQLEXPRESS"
DATABASE = "StudentDB"
DATE_FORMAT = "%Y-%m-%d"


class Student:
    def __init__(self, first_name, last_name, date_of_birth, grade_level, guardian_contact, student_id=None):
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.grade_level = grade_level
        self.guardian_contact = guardian_contact

    def to_values(self):
        return (
            self.first_name,
            self.last_name,
            self.date_of_birth,
            self.grade_level,
            self.guardian_contact,
        )


class Teacher:
    def __init__(self, first_name, last_name, subject, email, teacher_id=None):
        self.teacher_id = teacher_id
        self.first_name = first_name
        self.last_name = last_name
        self.subject = subject
        self.email = email


class AttendanceRecord:
    def __init__(self, student_id, attendance_date, status, record_id=None):
        self.record_id = record_id
        self.student_id = student_id
        self.attendance_date = attendance_date
        self.status = status


class FeeRecord:
    def __init__(self, student_id, amount_due, amount_paid, due_date, fee_id=None):
        self.fee_id = fee_id
        self.student_id = student_id
        self.amount_due = amount_due
        self.amount_paid = amount_paid
        self.due_date = due_date

    def balance(self):
        return round(self.amount_due - self.amount_paid, 2)


class PerformanceRecord:
    def __init__(self, student_id, subject, assessment_name, score, total, term, performance_id=None):
        self.performance_id = performance_id
        self.student_id = student_id
        self.subject = subject
        self.assessment_name = assessment_name
        self.score = score
        self.total = total
        self.term = term

    def percentage(self):
        if self.total == 0:
            return 0.0
        return round((self.score / self.total) * 100, 2)


def connection_string(include_database=True):
    pieces = ["DRIVER={" + DRIVER + "}", "SERVER=" + SERVER, "Trusted_Connection=yes"]
    if include_database:
        pieces.append("DATABASE=" + DATABASE)
    return ";".join(pieces)


def get_connection(include_database=False):
    return pyodbc.connect(connection_string(include_database), autocommit=True)


def ensure_database():
    conn = get_connection(False)
    cursor = conn.cursor()
    cursor.execute("IF DB_ID('" + DATABASE + "') IS NULL CREATE DATABASE " + DATABASE)
    cursor.close()
    conn.close()


def ensure_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("IF OBJECT_ID('dbo.attendance') IS NOT NULL DROP TABLE dbo.attendance")
    cursor.execute("IF OBJECT_ID('dbo.fees') IS NOT NULL DROP TABLE dbo.fees")
    cursor.execute("IF OBJECT_ID('dbo.performance') IS NOT NULL DROP TABLE dbo.performance")
    cursor.execute(
        """
        IF OBJECT_ID('dbo.students') IS NOT NULL AND (
            COL_LENGTH('dbo.students', 'first_name') IS NULL OR
            COL_LENGTH('dbo.students', 'last_name') IS NULL OR
            COL_LENGTH('dbo.students', 'date_of_birth') IS NULL OR
            COL_LENGTH('dbo.students', 'grade_level') IS NULL OR
            COL_LENGTH('dbo.students', 'guardian_contact') IS NULL
        )
        DROP TABLE dbo.students
        """
    )
    cursor.execute(
        """
        IF OBJECT_ID('dbo.students') IS NULL
        CREATE TABLE dbo.students (
            student_id INT IDENTITY(1,1) PRIMARY KEY,
            first_name NVARCHAR(50) NOT NULL,
            last_name NVARCHAR(50) NOT NULL,
            date_of_birth DATE NOT NULL,
            grade_level NVARCHAR(10) NOT NULL,
            guardian_contact NVARCHAR(100) NOT NULL
        )
        """
    )
    cursor.execute(
        """
        IF OBJECT_ID('dbo.teachers') IS NOT NULL AND (
            COL_LENGTH('dbo.teachers', 'first_name') IS NULL OR
            COL_LENGTH('dbo.teachers', 'last_name') IS NULL OR
            COL_LENGTH('dbo.teachers', 'subject') IS NULL OR
            COL_LENGTH('dbo.teachers', 'email') IS NULL
        )
        DROP TABLE dbo.teachers
        """
    )
    cursor.execute(
        """
        IF OBJECT_ID('dbo.teachers') IS NULL
        CREATE TABLE dbo.teachers (
            teacher_id INT IDENTITY(1,1) PRIMARY KEY,
            first_name NVARCHAR(50) NOT NULL,
            last_name NVARCHAR(50) NOT NULL,
            subject NVARCHAR(50) NOT NULL,
            email NVARCHAR(100) NOT NULL
        )
        """
    )
    cursor.execute(
        """
        IF OBJECT_ID('dbo.student_records') IS NOT NULL AND (
            COL_LENGTH('dbo.student_records', 'event_type') IS NULL OR
            COL_LENGTH('dbo.student_records', 'event_date') IS NULL OR
            COL_LENGTH('dbo.student_records', 'detail1') IS NULL OR
            COL_LENGTH('dbo.student_records', 'number1') IS NULL OR
            COL_LENGTH('dbo.student_records', 'number2') IS NULL
        )
        DROP TABLE dbo.student_records
        """
    )
    cursor.execute(
        """
        IF OBJECT_ID('dbo.student_records') IS NULL
        CREATE TABLE dbo.student_records (
            record_id INT IDENTITY(1,1) PRIMARY KEY,
            student_id INT NOT NULL,
            event_type NVARCHAR(20) NOT NULL,
            event_date DATE NOT NULL,
            detail1 NVARCHAR(100),
            detail2 NVARCHAR(100),
            detail3 NVARCHAR(100),
            detail4 NVARCHAR(100),
            number1 DECIMAL(10,2),
            number2 DECIMAL(10,2),
            term NVARCHAR(20)
        )
        """
    )
    cursor.close()
    conn.close()


def add_student(student):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO dbo.students(first_name, last_name, date_of_birth, grade_level, guardian_contact) VALUES (?, ?, ?, ?, ?)",
        student.first_name,
        student.last_name,
        student.date_of_birth,
        student.grade_level,
        student.guardian_contact,
    )
    cursor.execute("SELECT MAX(student_id) FROM dbo.students")
    new_id = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return new_id


def update_student(student):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE dbo.students SET first_name = ?, last_name = ?, date_of_birth = ?, grade_level = ?, guardian_contact = ? WHERE student_id = ?",
        student.first_name,
        student.last_name,
        student.date_of_birth,
        student.grade_level,
        student.guardian_contact,
        student.student_id,
    )
    cursor.close()
    conn.close()


def delete_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM dbo.student_records WHERE student_id = ?", student_id)
    cursor.execute("DELETE FROM dbo.students WHERE student_id = ?", student_id)
    cursor.close()
    conn.close()


def get_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT student_id, first_name, last_name, date_of_birth, grade_level, guardian_contact FROM dbo.students ORDER BY student_id"
    )
    results = []
    for row in cursor.fetchall():
        results.append(
            Student(
                row.first_name,
                row.last_name,
                row.date_of_birth.strftime(DATE_FORMAT),
                row.grade_level,
                row.guardian_contact,
                row.student_id,
            )
        )
    cursor.close()
    conn.close()
    return results


def add_teacher(teacher):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO dbo.teachers(first_name, last_name, subject, email) VALUES (?, ?, ?, ?)",
        teacher.first_name,
        teacher.last_name,
        teacher.subject,
        teacher.email,
    )
    cursor.execute("SELECT MAX(teacher_id) FROM dbo.teachers")
    new_id = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return new_id


def update_teacher(teacher):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE dbo.teachers SET first_name = ?, last_name = ?, subject = ?, email = ? WHERE teacher_id = ?",
        teacher.first_name,
        teacher.last_name,
        teacher.subject,
        teacher.email,
        teacher.teacher_id,
    )
    cursor.close()
    conn.close()


def delete_teacher(teacher_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM dbo.teachers WHERE teacher_id = ?", teacher_id)
    cursor.close()
    conn.close()


def get_teachers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT teacher_id, first_name, last_name, subject, email FROM dbo.teachers ORDER BY teacher_id"
    )
    results = []
    for row in cursor.fetchall():
        results.append(
            Teacher(
                row.first_name,
                row.last_name,
                row.subject,
                row.email,
                row.teacher_id,
            )
        )
    cursor.close()
    conn.close()
    return results


def add_attendance(record):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO dbo.student_records (student_id, event_type, event_date, detail1) VALUES (?, ?, ?, ?)",
        record.student_id,
        "attendance",
        record.attendance_date,
        record.status,
    )
    cursor.execute("SELECT TOP 1 record_id FROM dbo.student_records WHERE event_type = 'attendance' ORDER BY record_id DESC")
    new_id = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return new_id


def get_attendance():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT record_id, student_id, event_date, detail1 FROM dbo.student_records WHERE event_type = 'attendance' ORDER BY event_date DESC, record_id DESC"
    )
    records = []
    for row in cursor.fetchall():
        date_value = row.event_date.strftime(DATE_FORMAT) if row.event_date else ""
        records.append(AttendanceRecord(row.student_id, date_value, row.detail1 or "", row.record_id))
    cursor.close()
    conn.close()
    return records


def add_fee(record):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO dbo.student_records (student_id, event_type, event_date, number1, number2) VALUES (?, ?, ?, ?, ?)",
        record.student_id,
        "fee",
        record.due_date,
        record.amount_due,
        record.amount_paid,
    )
    cursor.execute("SELECT TOP 1 record_id FROM dbo.student_records WHERE event_type = 'fee' ORDER BY record_id DESC")
    new_id = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return new_id


def update_fee_payment(record_id, amount_paid):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE dbo.student_records SET number2 = ? WHERE record_id = ? AND event_type = 'fee'",
        amount_paid,
        record_id,
    )
    cursor.close()
    conn.close()


def get_fees():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT record_id, student_id, event_date, number1, number2 FROM dbo.student_records WHERE event_type = 'fee' ORDER BY event_date DESC, record_id DESC"
    )
    records = []
    for row in cursor.fetchall():
        due = row.event_date.strftime(DATE_FORMAT) if row.event_date else ""
        amount_due = float(row.number1 or 0)
        amount_paid = float(row.number2 or 0)
        records.append(FeeRecord(row.student_id, amount_due, amount_paid, due, row.record_id))
    cursor.close()
    conn.close()
    return records


def add_performance(record):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO dbo.student_records (student_id, event_type, event_date, detail1, detail2, number1, number2, term) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        record.student_id,
        "performance",
        datetime.today().strftime(DATE_FORMAT),
        record.subject,
        record.assessment_name,
        record.score,
        record.total,
        record.term,
    )
    cursor.close()
    conn.close()


def get_performance(student_id, term):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT record_id, student_id, detail1, detail2, number1, number2, term FROM dbo.student_records WHERE event_type = 'performance' AND student_id = ? AND term = ? ORDER BY record_id",
        student_id,
        term,
    )
    records = []
    for row in cursor.fetchall():
        records.append(
            PerformanceRecord(
                row.student_id,
                row.detail1 or "",
                row.detail2 or "",
                float(row.number1 or 0),
                float(row.number2 or 0),
                row.term or "",
                row.record_id,
            )
        )
    cursor.close()
    conn.close()
    return records


def grade_from_percentage(value):
    if value >= 90:
        return "A"
    if value >= 80:
        return "B"
    if value >= 70:
        return "C"
    if value >= 60:
        return "D"
    if value > 0:
        return "F"
    return "N/A"


def calculate_average(student_id, term):
    records = get_performance(student_id, term)
    if not records:
        return {"average": 0.0, "grade": "N/A", "details": []}
    total = sum(record.percentage() for record in records)
    average = round(total / len(records), 2)
    grade = grade_from_percentage(average)
    return {"average": average, "grade": grade, "details": records}


class RecordsView(tk.Frame):
    def __init__(self, master, status_variable):
        tk.Frame.__init__(self, master)
        self.status_variable = status_variable
        self.active_section = None
        self.fee_records = []
        self.selected_fee = None

        button_row = tk.Frame(self)
        button_row.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(button_row, text="Attendance", width=14, command=self._show_attendance).pack(side=tk.LEFT, padx=5)
        tk.Button(button_row, text="Fees", width=14, command=self._show_fees).pack(side=tk.LEFT, padx=5)
        tk.Button(button_row, text="Performance", width=14, command=self._show_performance).pack(side=tk.LEFT, padx=5)

        self.section_container = tk.Frame(self)
        self.section_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self._show_attendance()

    def _clear_section(self):
        if self.active_section is not None:
            self.active_section.destroy()
            self.active_section = None

    def _show_attendance(self):
        self._clear_section()
        frame = tk.Frame(self.section_container)
        frame.pack(fill=tk.BOTH, expand=True)

        student_var = tk.StringVar()
        date_var = tk.StringVar(value=datetime.today().strftime(DATE_FORMAT))
        status_var = tk.StringVar(value="Present")

        tk.Label(frame, text="Student ID").grid(row=0, column=0, sticky="w", pady=3)
        tk.Entry(frame, textvariable=student_var).grid(row=0, column=1, pady=3)
        tk.Label(frame, text="Date (YYYY-MM-DD)").grid(row=1, column=0, sticky="w", pady=3)
        tk.Entry(frame, textvariable=date_var).grid(row=1, column=1, pady=3)
        tk.Label(frame, text="Status (Present / Absent / Late)").grid(row=2, column=0, sticky="w", pady=3)
        tk.Entry(frame, textvariable=status_var).grid(row=2, column=1, pady=3)

        display = tk.Text(frame, width=60, height=15)
        display.grid(row=0, column=2, rowspan=7, padx=10, pady=5)

        def refresh():
            records = get_attendance()
            display.delete("1.0", tk.END)
            if not records:
                display.insert(tk.END, "No attendance records\n")
                return
            for item in records:
                display.insert(
                    tk.END,
                    f"ID {item.record_id} | Student {item.student_id} | {item.attendance_date} | {item.status}\n",
                )

        def clear_inputs():
            student_var.set("")
            date_var.set(datetime.today().strftime(DATE_FORMAT))
            status_var.set("Present")

        def add_action():
            try:
                student_id = int(student_var.get().strip())
                datetime.strptime(date_var.get().strip(), DATE_FORMAT)
                record = AttendanceRecord(student_id, date_var.get().strip(), status_var.get().strip())
                add_attendance(record)
                self.status_variable.set("Attendance saved")
                refresh()
            except Exception as error:
                self.status_variable.set(f"Attendance error: {error}")

        tk.Button(frame, text="Record", width=12, command=add_action).grid(row=3, column=0, columnspan=2, pady=4)
        tk.Button(frame, text="Clear", width=12, command=clear_inputs).grid(row=4, column=0, columnspan=2, pady=4)
        tk.Button(frame, text="Refresh", width=12, command=refresh).grid(row=5, column=0, columnspan=2, pady=4)

        refresh()
        self.active_section = frame

    def _show_fees(self):
        self._clear_section()
        frame = tk.Frame(self.section_container)
        frame.pack(fill=tk.BOTH, expand=True)

        record_id_var = tk.StringVar()
        student_var = tk.StringVar()
        amount_due_var = tk.StringVar()
        amount_paid_var = tk.StringVar()
        due_date_var = tk.StringVar(value=datetime.today().strftime(DATE_FORMAT))

        tk.Label(frame, text="Record ID (for update)").grid(row=0, column=0, sticky="w", pady=3)
        tk.Entry(frame, textvariable=record_id_var).grid(row=0, column=1, pady=3)
        tk.Label(frame, text="Student ID").grid(row=1, column=0, sticky="w", pady=3)
        tk.Entry(frame, textvariable=student_var).grid(row=1, column=1, pady=3)
        tk.Label(frame, text="Amount Due").grid(row=2, column=0, sticky="w", pady=3)
        tk.Entry(frame, textvariable=amount_due_var).grid(row=2, column=1, pady=3)
        tk.Label(frame, text="Amount Paid").grid(row=3, column=0, sticky="w", pady=3)
        tk.Entry(frame, textvariable=amount_paid_var).grid(row=3, column=1, pady=3)
        tk.Label(frame, text="Due Date (YYYY-MM-DD)").grid(row=4, column=0, sticky="w", pady=3)
        tk.Entry(frame, textvariable=due_date_var).grid(row=4, column=1, pady=3)

        listbox = tk.Listbox(frame, height=15, width=70)
        listbox.grid(row=0, column=2, rowspan=9, padx=10, pady=5, sticky="nsew")
        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=listbox.yview)
        scrollbar.grid(row=0, column=3, rowspan=9, sticky="ns")
        listbox.config(yscrollcommand=scrollbar.set)

        frame.grid_columnconfigure(2, weight=1)
        frame.grid_rowconfigure(8, weight=1)

        def refresh():
            self.fee_records = get_fees()
            listbox.delete(0, tk.END)
            if not self.fee_records:
                listbox.insert(tk.END, "No fee records")
                return
            for item in self.fee_records:
                listbox.insert(
                    tk.END,
                    f"ID {item.fee_id} | Student {item.student_id} | Due {item.amount_due:.2f} | "
                    f"Paid {item.amount_paid:.2f} | Balance {item.balance():.2f} | Due {item.due_date}",
                )

        def clear_inputs():
            record_id_var.set("")
            student_var.set("")
            amount_due_var.set("")
            amount_paid_var.set("")
            due_date_var.set(datetime.today().strftime(DATE_FORMAT))
            listbox.selection_clear(0, tk.END)
            self.selected_fee = None

        def add_action():
            try:
                student_id = int(student_var.get().strip())
                amount_due = float(amount_due_var.get().strip())
                amount_paid = float(amount_paid_var.get().strip() or 0)
                datetime.strptime(due_date_var.get().strip(), DATE_FORMAT)
                record = FeeRecord(student_id, amount_due, amount_paid, due_date_var.get().strip())
                record_id = add_fee(record)
                self.status_variable.set(f"Added record {record_id}")
                refresh()
                clear_inputs()
            except Exception as error:
                self.status_variable.set(f"Fee error: {error}")

        def update_action():
            if not record_id_var.get().strip():
                self.status_variable.set("Enter the record ID to update")
                return
            try:
                amount_paid = float(amount_paid_var.get().strip())
                update_fee_payment(int(record_id_var.get().strip()), amount_paid)
                self.status_variable.set(f"Updated record {record_id_var.get().strip()}")
                refresh()
            except Exception as error:
                self.status_variable.set(f"Fee error: {error}")

        def on_select(event):
            if not listbox.curselection() or not self.fee_records:
                return
            index = listbox.curselection()[0]
            selected = self.fee_records[index]
            record_id_var.set(str(selected.fee_id))
            student_var.set(str(selected.student_id))
            amount_due_var.set(f"{selected.amount_due:.2f}")
            amount_paid_var.set(f"{selected.amount_paid:.2f}")
            due_date_var.set(selected.due_date)
            self.selected_fee = selected

        listbox.bind("<<ListboxSelect>>", on_select)

        tk.Button(frame, text="Add", width=12, command=add_action).grid(row=5, column=0, pady=4)
        tk.Button(frame, text="Update Payment", width=14, command=update_action).grid(row=5, column=1, pady=4)
        tk.Button(frame, text="Clear", width=12, command=clear_inputs).grid(row=6, column=0, columnspan=2, pady=4)
        tk.Button(frame, text="Refresh", width=12, command=refresh).grid(row=7, column=0, columnspan=2, pady=4)

        refresh()
        self.active_section = frame

    def _show_performance(self):
        self._clear_section()
        frame = tk.Frame(self.section_container)
        frame.pack(fill=tk.BOTH, expand=True)

        student_var = tk.StringVar()
        subject_var = tk.StringVar()
        assessment_var = tk.StringVar()
        score_var = tk.StringVar()
        total_var = tk.StringVar()
        term_var = tk.StringVar()
        report_term_var = tk.StringVar()

        entries = [
            ("Student ID", student_var),
            ("Subject", subject_var),
            ("Assessment", assessment_var),
            ("Score", score_var),
            ("Total", total_var),
            ("Term", term_var),
        ]

        for index, (label, var) in enumerate(entries):
            tk.Label(frame, text=label).grid(row=index, column=0, sticky="w", pady=3)
            tk.Entry(frame, textvariable=var).grid(row=index, column=1, pady=3)

        tk.Label(frame, text="Report Term").grid(row=len(entries), column=0, sticky="w", pady=3)
        tk.Entry(frame, textvariable=report_term_var).grid(row=len(entries), column=1, pady=3)

        report_text = tk.Text(frame, width=60, height=18)
        report_text.grid(row=0, column=2, rowspan=9, padx=10, pady=5)

        def clear_inputs():
            subject_var.set("")
            assessment_var.set("")
            score_var.set("")
            total_var.set("")
            term_var.set("")

        def add_action():
            try:
                student_id = int(student_var.get().strip())
                score = float(score_var.get().strip())
                total = float(total_var.get().strip())
                record = PerformanceRecord(
                    student_id,
                    subject_var.get().strip(),
                    assessment_var.get().strip(),
                    score,
                    total,
                    term_var.get().strip(),
                )
                add_performance(record)
                self.status_variable.set("Performance saved")
                clear_inputs()
            except Exception as error:
                self.status_variable.set(f"Performance error: {error}")

        def report_action():
            try:
                student_id = int(student_var.get().strip())
                chosen_term = report_term_var.get().strip() or term_var.get().strip()
                result = calculate_average(student_id, chosen_term)
                report_text.delete("1.0", tk.END)
                if not result["details"]:
                    report_text.insert(tk.END, f"No performance data for student {student_id} in term {chosen_term}\n")
                else:
                    report_text.insert(
                        tk.END,
                        f"Student {student_id} | Term {chosen_term}\nAverage: {result['average']}% | "
                        f"Grade: {result['grade']}\n\n",
                    )
                    for item in result["details"]:
                        report_text.insert(
                            tk.END,
                            f"{item.subject} - {item.assessment_name}: {item.score}/{item.total} "
                            f"({item.percentage()}%)\n",
                        )
                self.status_variable.set("Report ready")
            except Exception as error:
                self.status_variable.set(f"Report error: {error}")

        tk.Button(frame, text="Add Record", width=12, command=add_action).grid(row=len(entries) + 1, column=0, pady=4)
        tk.Button(frame, text="Generate Report", width=14, command=report_action).grid(row=len(entries) + 1, column=1, pady=4)
        tk.Button(frame, text="Clear Form", width=12, command=clear_inputs).grid(row=len(entries) + 2, column=0, columnspan=2, pady=4)

        self.active_section = frame


class SchoolApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("School Management System")
        self.status_variable = tk.StringVar(value="")
        self.active_frame = None
        ensure_database()
        ensure_tables()
        self._build_login()

    def _build_login(self):
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.login_frame, text="School Management Login", font=("Arial", 18, "bold")).pack(pady=20)

        tk.Label(self.login_frame, text="Username").pack()
        self.login_user = tk.Entry(self.login_frame)
        self.login_user.pack()

        tk.Label(self.login_frame, text="Password").pack()
        self.login_pass = tk.Entry(self.login_frame, show="*")
        self.login_pass.pack()

        self.login_status = tk.Label(self.login_frame, text="", fg="red")
        self.login_status.pack(pady=10)

        tk.Button(self.login_frame, text="Login", command=self._attempt_login).pack(pady=10)

    def _attempt_login(self):
        username = self.login_user.get().strip()
        password = self.login_pass.get().strip()
        if username == "admin" and password == "1234":
            self.login_frame.destroy()
            self._build_dashboard()
            self.status_variable.set("Welcome!")
        else:
            self.login_status.config(text="Invalid credentials")

    def _build_dashboard(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill=tk.X)

        buttons = [
            ("Students", self.show_students),
            ("Teachers", self.show_teachers),
            ("Student Records", self.show_records),
        ]
        for text, callback in buttons:
            tk.Button(top_frame, text=text, width=14, command=callback).pack(side=tk.LEFT, padx=5, pady=5)

        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        status_frame = tk.Frame(self.root)
        status_frame.pack(fill=tk.X)
        tk.Label(status_frame, textvariable=self.status_variable, anchor="w").pack(fill=tk.X, padx=5, pady=5)

        self.show_students()

    def _swap_frame(self, new_frame):
        if self.active_frame is not None:
            self.active_frame.destroy()
        self.active_frame = new_frame
        self.active_frame.pack(fill=tk.BOTH, expand=True)

    def show_students(self):
        frame = tk.Frame(self.content_frame)

        tk.Label(frame, text="Student ID (for update/delete)").grid(row=0, column=0, sticky="w", pady=2)
        id_entry = tk.Entry(frame)
        id_entry.grid(row=0, column=1, pady=2)

        tk.Label(frame, text="First Name").grid(row=1, column=0, sticky="w", pady=2)
        first_entry = tk.Entry(frame)
        first_entry.grid(row=1, column=1, pady=2)

        tk.Label(frame, text="Last Name").grid(row=2, column=0, sticky="w", pady=2)
        last_entry = tk.Entry(frame)
        last_entry.grid(row=2, column=1, pady=2)

        tk.Label(frame, text="Date of Birth (YYYY-MM-DD)").grid(row=3, column=0, sticky="w", pady=2)
        dob_entry = tk.Entry(frame)
        dob_entry.grid(row=3, column=1, pady=2)

        tk.Label(frame, text="Grade").grid(row=4, column=0, sticky="w", pady=2)
        grade_entry = tk.Entry(frame)
        grade_entry.grid(row=4, column=1, pady=2)

        tk.Label(frame, text="Guardian Contact").grid(row=5, column=0, sticky="w", pady=2)
        guardian_entry = tk.Entry(frame)
        guardian_entry.grid(row=5, column=1, pady=2)

        display = tk.Text(frame, width=60, height=15)
        display.grid(row=0, column=2, rowspan=8, padx=10, pady=5)

        def refresh():
            records = get_students()
            display.delete("1.0", tk.END)
            if not records:
                display.insert(tk.END, "No students found\n")
                return
            for student in records:
                display.insert(
                    tk.END,
                    f"ID {student.student_id} | {student.first_name} {student.last_name} | "
                    f"DOB {student.date_of_birth} | Grade {student.grade_level} | "
                    f"Contact {student.guardian_contact}\n",
                )

        def clear():
            id_entry.delete(0, tk.END)
            first_entry.delete(0, tk.END)
            last_entry.delete(0, tk.END)
            dob_entry.delete(0, tk.END)
            grade_entry.delete(0, tk.END)
            guardian_entry.delete(0, tk.END)

        def add_action():
            try:
                datetime.strptime(dob_entry.get().strip(), DATE_FORMAT)
                student = Student(
                    first_entry.get().strip(),
                    last_entry.get().strip(),
                    dob_entry.get().strip(),
                    grade_entry.get().strip(),
                    guardian_entry.get().strip(),
                )
                new_id = add_student(student)
                self.status_variable.set(f"Added student {new_id}")
                refresh()
                clear()
            except Exception as error:
                self.status_variable.set(f"Student error: {error}")

        def update_action():
            try:
                student_id = int(id_entry.get().strip())
                datetime.strptime(dob_entry.get().strip(), DATE_FORMAT)
                student = Student(
                    first_entry.get().strip(),
                    last_entry.get().strip(),
                    dob_entry.get().strip(),
                    grade_entry.get().strip(),
                    guardian_entry.get().strip(),
                    student_id,
                )
                update_student(student)
                self.status_variable.set(f"Updated student {student_id}")
                refresh()
            except Exception as error:
                self.status_variable.set(f"Student error: {error}")

        def delete_action():
            try:
                student_id = int(id_entry.get().strip())
                delete_student(student_id)
                self.status_variable.set(f"Deleted student {student_id}")
                refresh()
                clear()
            except Exception as error:
                self.status_variable.set(f"Student error: {error}")

        tk.Button(frame, text="Add", width=12, command=add_action).grid(row=6, column=0, pady=4)
        tk.Button(frame, text="Update", width=12, command=update_action).grid(row=6, column=1, pady=4)
        tk.Button(frame, text="Delete", width=12, command=delete_action).grid(row=7, column=0, pady=4)
        tk.Button(frame, text="Clear", width=12, command=clear).grid(row=7, column=1, pady=4)
        tk.Button(frame, text="Refresh", width=12, command=refresh).grid(row=8, column=0, columnspan=2, pady=4)

        refresh()
        self._swap_frame(frame)

    def show_teachers(self):
        frame = tk.Frame(self.content_frame)

        tk.Label(frame, text="Teacher ID (for update/delete)").grid(row=0, column=0, sticky="w", pady=2)
        id_entry = tk.Entry(frame)
        id_entry.grid(row=0, column=1, pady=2)

        tk.Label(frame, text="First Name").grid(row=1, column=0, sticky="w", pady=2)
        first_entry = tk.Entry(frame)
        first_entry.grid(row=1, column=1, pady=2)

        tk.Label(frame, text="Last Name").grid(row=2, column=0, sticky="w", pady=2)
        last_entry = tk.Entry(frame)
        last_entry.grid(row=2, column=1, pady=2)

        tk.Label(frame, text="Subject").grid(row=3, column=0, sticky="w", pady=2)
        subject_entry = tk.Entry(frame)
        subject_entry.grid(row=3, column=1, pady=2)

        tk.Label(frame, text="Email").grid(row=4, column=0, sticky="w", pady=2)
        email_entry = tk.Entry(frame)
        email_entry.grid(row=4, column=1, pady=2)

        display = tk.Text(frame, width=60, height=15)
        display.grid(row=0, column=2, rowspan=8, padx=10, pady=5)

        def refresh():
            records = get_teachers()
            display.delete("1.0", tk.END)
            if not records:
                display.insert(tk.END, "No teachers found\n")
                return
            for teacher in records:
                display.insert(
                    tk.END,
                    f"ID {teacher.teacher_id} | {teacher.first_name} {teacher.last_name} | "
                    f"Subject {teacher.subject} | Email {teacher.email}\n",
                )

        def clear():
            id_entry.delete(0, tk.END)
            first_entry.delete(0, tk.END)
            last_entry.delete(0, tk.END)
            subject_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)

        def add_action():
            try:
                teacher = Teacher(
                    first_entry.get().strip(),
                    last_entry.get().strip(),
                    subject_entry.get().strip(),
                    email_entry.get().strip(),
                )
                new_id = add_teacher(teacher)
                self.status_variable.set(f"Added teacher {new_id}")
                refresh()
                clear()
            except Exception as error:
                self.status_variable.set(f"Teacher error: {error}")

        def update_action():
            try:
                teacher_id = int(id_entry.get().strip())
                teacher = Teacher(
                    first_entry.get().strip(),
                    last_entry.get().strip(),
                    subject_entry.get().strip(),
                    email_entry.get().strip(),
                    teacher_id,
                )
                update_teacher(teacher)
                self.status_variable.set(f"Updated teacher {teacher_id}")
                refresh()
            except Exception as error:
                self.status_variable.set(f"Teacher error: {error}")

        def delete_action():
            try:
                teacher_id = int(id_entry.get().strip())
                delete_teacher(teacher_id)
                self.status_variable.set(f"Deleted teacher {teacher_id}")
                refresh()
                clear()
            except Exception as error:
                self.status_variable.set(f"Teacher error: {error}")

        tk.Button(frame, text="Add", width=12, command=add_action).grid(row=5, column=0, pady=4)
        tk.Button(frame, text="Update", width=12, command=update_action).grid(row=5, column=1, pady=4)
        tk.Button(frame, text="Delete", width=12, command=delete_action).grid(row=6, column=0, pady=4)
        tk.Button(frame, text="Clear", width=12, command=clear).grid(row=6, column=1, pady=4)
        tk.Button(frame, text="Refresh", width=12, command=refresh).grid(row=7, column=0, columnspan=2, pady=4)

        refresh()
        self._swap_frame(frame)

    def show_records(self):
        frame = RecordsView(self.content_frame, self.status_variable)
        self._swap_frame(frame)

    def run(self):
        self.root.mainloop()


def main():
    app = SchoolApp()
    app.run()


if __name__ == "__main__":
    main()
