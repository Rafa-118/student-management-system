from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from .extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="student")
    student = db.relationship("Student", back_populates="user", uselist=False)
    def set_password(self, password): self.password_hash = generate_password_hash(password)
    def check_password(self, password): return check_password_hash(self.password_hash, password)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(30), nullable=False, unique=True, index=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(30))
    department = db.Column(db.String(100), nullable=False)
    program = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.String(50), nullable=False)
    enrollment_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default="Active")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True)
    user = db.relationship("User", back_populates="student")
    enrollments = db.relationship("Enrollment", back_populates="student", cascade="all, delete-orphan")
    attendance_records = db.relationship("Attendance", back_populates="student", cascade="all, delete-orphan")
    results = db.relationship("Result", back_populates="student", cascade="all, delete-orphan")

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(30), nullable=False, unique=True, index=True)
    title = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    credit_hours = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.String(50), nullable=False)
    instructor_name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    enrollments = db.relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")
    attendance_records = db.relationship("Attendance", back_populates="course", cascade="all, delete-orphan")
    results = db.relationship("Result", back_populates="course", cascade="all, delete-orphan")

class Enrollment(db.Model):
    __table_args__ = (db.UniqueConstraint("student_id", "course_id", name="uq_enrollment"),)
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    student = db.relationship("Student", back_populates="enrollments")
    course = db.relationship("Course", back_populates="enrollments")

class Attendance(db.Model):
    __table_args__ = (db.UniqueConstraint("student_id", "course_id", "date", name="uq_attendance"),)
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(10), nullable=False)
    student = db.relationship("Student", back_populates="attendance_records")
    course = db.relationship("Course", back_populates="attendance_records")

class Result(db.Model):
    __table_args__ = (db.UniqueConstraint("student_id", "course_id", "assessment_type", "term", name="uq_result"),)
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    assessment_type = db.Column(db.String(60), nullable=False)
    marks_obtained = db.Column(db.Float, nullable=False)
    maximum_marks = db.Column(db.Float, nullable=False)
    grade = db.Column(db.String(4), nullable=False)
    term = db.Column(db.String(50), nullable=False)
    remarks = db.Column(db.Text)
    student = db.relationship("Student", back_populates="results")
    course = db.relationship("Course", back_populates="results")
    @property
    def percentage(self): return round((self.marks_obtained / self.maximum_marks) * 100, 2) if self.maximum_marks else 0

class Setting(db.Model):
    key = db.Column(db.String(100), primary_key=True)
    value = db.Column(db.Text, nullable=False)
