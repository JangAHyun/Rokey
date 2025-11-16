import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# 1. Firebase Admin SDK 초기화
SERVICE_ACCOUNT_KEY_PATH = "<Firebase Key>"  
# 2. Realtime Database URL
DATABASE_URL = "<Realtime Database URL>"
 
# 3. Firebase Admin SDK 초기화 (여러 번 import 돼도 한 번만 초기화)
if not firebase_admin._apps:
    cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
    firebase_admin.initialize_app(cred, {
        'databaseURL': DATABASE_URL
    })
    print("[INFO] Firebase 앱 초기화 완료")


def update_dish_count(dish_cnt: int):
    """
    로봇이 접시를 옮길 때마다 이 함수를 호출해서
    Realtime DB에 현재 clean_dish 값을 저장.
    """
    # robot_status/completed_jobs 경로에 바로 값 쓰기
    ref_jobs = db.reference("robot_status/completed_jobs")
    ref_jobs.set(dish_cnt)

    # (선택) 같은 /robot_status 아래에 타임스탬프도 함께 저장
    ref_root = db.reference("robot_status")
    ref_root.update({
        "last_update_timestamp": time.time(),
        "from": "mainpc"
    })

    print(f"[INFO] Firebase 업데이트: completed_jobs = {dish_cnt}")
