import os
import shutil
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

# Vercel Hack: Vercel has a read-only filesystem except for /tmp
tmp_db_path = '/tmp/platform.db'
original_db_path = os.path.join(basedir, 'instance', 'platform.db')

if os.environ.get('VERCEL') == '1':
    if not os.path.exists(tmp_db_path) and os.path.exists(original_db_path):
        try:
            shutil.copy(original_db_path, tmp_db_path)
        except Exception:
            pass
    db_uri = 'sqlite:///' + tmp_db_path
else:
    db_uri = 'sqlite:///' + original_db_path

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    WTF_CSRF_ENABLED = False
    SESSION_COOKIE_SAMESITE = 'None'
    SESSION_COOKIE_SECURE = True
