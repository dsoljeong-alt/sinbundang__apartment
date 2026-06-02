"""
WSGI 설정 파일 (PythonAnywhere 등 호스팅 서비스용)
"""

import sys
import os

# 프로젝트 경로 추가
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.append(path)

from app import app as application
