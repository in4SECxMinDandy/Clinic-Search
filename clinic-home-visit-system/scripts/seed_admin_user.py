#!/usr/bin/env python3
"""
Script tạo tài khoản admin đầu tiên.

Chạy khi Postgres đang chạy (VD sau docker-compose up):
  set DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres
  python scripts/seed_admin_user.py

Mặc định tạo tài khoản:
  Email:    admin@clinicsystem.vn
  Password: Admin1234
  Role:     admin
  Name:     Quản trị viên
"""
from __future__ import annotations

import os
import sys
import uuid

try:
    import psycopg2
except ImportError:
    print("Install psycopg2-binary: pip install psycopg2-binary", file=sys.stderr)
    sys.exit(1)

try:
    import bcrypt
except ImportError:
    print("Install bcrypt: pip install bcrypt", file=sys.stderr)
    sys.exit(1)


def hash_password(password: str) -> str:
    """Hash password using bcrypt (same as auth-service)"""
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")


def run():
    db_url = os.environ.get(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/postgres",
    )

    email_input = input(f"Email admin (Enter = admin@clinicsystem.vn): ").strip()
    email = email_input or "admin@clinicsystem.vn"

    password_input = input(f"Password (Enter = Admin1234): ").strip()
    password = password_input or "Admin1234"

    name_input = input(f"Tên admin (Enter = Quản trị viên): ").strip()
    full_name = name_input or "Quản trị viên"

    try:
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cur = conn.cursor()

        # Check if email exists in auth_schema.users
        cur.execute(
            """
            SELECT id, role FROM auth_schema.users WHERE email = %s
            """,
            (email,),
        )
        existing = cur.fetchone()

        if existing:
            user_id, current_role = existing
            confirm = (
                input(
                    f"User '{email}' đã tồn tại (role={current_role}). "
                    f"Cập nhật thành admin? (y/N): "
                )
                .strip()
                .lower()
            )
            if confirm == "y":
                cur.execute(
                    """
                    UPDATE auth_schema.users
                    SET role = 'admin', is_active = true, updated_at = NOW()
                    WHERE id = %s
                    """,
                    (user_id,),
                )
                print(f"Đã cập nhật '{email}' thành admin.")
            else:
                print("Đã hủy.")
            cur.close()
            conn.close()
            return

        user_id = str(uuid.uuid4())
        pw_hash = hash_password(password)

        cur.execute(
            """
            INSERT INTO auth_schema.users
                (id, email, password_hash, full_name, phone, role, is_active,
                 failed_login_attempts, created_at, updated_at)
            VALUES
                (%s, %s, %s, %s, NULL, 'admin', true, 0, NOW(), NOW())
            """,
            (user_id, email, pw_hash, full_name),
        )

        print("")
        print("  === Tài khoản admin đã được tạo ===")
        print(f"  Email:    {email}")
        print(f"  Password: {password}")
        print(f"  Role:     admin")
        print(f"  User ID:  {user_id}")
        print("  ===================================")
        print("")
        print("  Đăng nhập tại: http://localhost/login")

        cur.close()
        conn.close()

    except psycopg2.Error as e:
        print(f"Lỗi database: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    run()
