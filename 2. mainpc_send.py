from datetime import datetime
import os

import firebase_admin
from firebase_admin import credentials, db

# 1. 서비스 계정 키 JSON 절대 경로
SERVICE_ACCOUNT_KEY_PATH = "/home/roeky/firebase/rokey-d198f-firebase-adminsdk-fbsvc-f417016fee.json"

# 2. Realtime Database URL (콘솔에서 복사한 그대로)
DATABASE_URL = "https://rokey-d198f-default-rtdb.asia-southeast1.firebasedatabase.app"

# 3. mainpc에서 보낼 파일 경로
LOCAL_FILE_PATH = "/home/roeky/firebase/test.txt"   # 실제 위치에 맞게 수정


# Firebase Admin SDK 초기화
try:
    cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
    firebase_admin.initialize_app(cred, {
        'databaseURL': DATABASE_URL
    })
    print("[INFO] Firebase 앱 초기화 완료")
except ValueError:
    print("[INFO] Firebase 앱이 이미 초기화되어 있습니다.")


def send_file_to_realtimedb():
    if not os.path.exists(LOCAL_FILE_PATH):
        print(f"[ERROR] 파일을 찾을 수 없습니다: {LOCAL_FILE_PATH}")
        return

    with open(LOCAL_FILE_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Realtime DB 경로 지정
    ref = db.reference("/robot_status")

    ref.set(
        {
            "content": content,
            "from": "mainpc",
            "filename": LOCAL_FILE_PATH,
            "updated_at": datetime.utcnow().isoformat(),
        }
    )

    print("[INFO] Realtime Database에 데이터 전송 완료: /robot_status")


if __name__ == "__main__":
    send_file_to_realtimedb()
