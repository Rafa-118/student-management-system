# EduManage agent guide

## Project purpose

EduManage is a portfolio-ready student management system for Bangladesh. It uses server-rendered Flask pages, SQLAlchemy data models, role-based authorization, and a separate static portfolio showcase.

## Architecture

- `app/__init__.py` creates the Flask application and registers blueprints.
- `app/auth/` owns sign-in, sign-out, and the public `/showcase` route.
- `app/admin/` owns administrator-only workflows.
- `app/student/` owns the private student portal.
- `app/models.py` contains the relational SQLAlchemy models.
- `app/templates/` contains Jinja templates; `app/static/` contains shared CSS and JavaScript.
- `showcase.html` is intentionally a self-contained animated marketing/portfolio page.

Keep new application code modular. Do not merge the Flask app into one Python file or replace server-rendered templates with a frontend framework.

## Local development

Use PowerShell on Windows:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
flask --app run:create_app db upgrade
flask --app run:create_app create-admin
flask --app run.py run
```

Run automated tests with:

```powershell
pytest
```

When the sandbox prevents pytest from writing to its default temporary directory, use a workspace-local base temp directory instead:

```powershell
pytest --basetemp .pytest-tmp
```

## Security rules

- Never add a default administrator password or public administrator registration.
- Keep secrets in environment variables; never commit `.env` files, database files, or credentials.
- Protect all state-changing forms with CSRF tokens.
- Apply server-side role checks to every admin and student route.
- Use SQLAlchemy relationships/constraints rather than storing related IDs in text fields.
- Validate input on the server, including duplicate IDs/emails/course codes and mark boundaries.
- Students may only access records linked to their own account.

## Product and design rules

- Preserve the navy, white, and restrained-teal visual system.
- Build responsive, keyboard-accessible interfaces with visible focus states and clear empty/error/success states.
- Respect `prefers-reduced-motion`; avoid decorative looping animation.
- Do not claim SMS, payment, biometric, RFID, upload, or notification integrations until they are implemented and configured.
- The default academic rule is the Bangladesh 5.0 GPA scale. Attendance considers `Present` and `Late` present unless an institution configuration changes that policy.

## Verification before handoff

- Run the test suite after behavioral changes.
- Test both roles: unauthenticated access, admin access, student route isolation, and logout.
- Verify new database constraints with both valid and duplicate input.
- Update `README.md` when setup, deployment, routes, or supported features change.
