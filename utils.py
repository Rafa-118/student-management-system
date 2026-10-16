from functools import wraps
from flask import abort, flash, redirect, session, url_for

GRADE_SCALE = [(80, "A+", 5.0), (70, "A", 4.0), (60, "A-", 3.5), (50, "B", 3.0), (40, "C", 2.0), (33, "D", 1.0), (0, "F", 0.0)]
def grade_for(percentage):
    return next((grade for minimum, grade, _ in GRADE_SCALE if percentage >= minimum), "F")
def current_user():
    from .models import User
    return User.query.get(session.get("user_id")) if session.get("user_id") else None
def role_required(*roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            user = current_user()
            if not user:
                flash("Please sign in to continue.", "warning"); return redirect(url_for("auth.login"))
            if user.role not in roles: abort(403)
            return view(*args, **kwargs)
        return wrapped
    return decorator
