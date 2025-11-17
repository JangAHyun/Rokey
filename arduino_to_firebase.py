import serial
import json
import firebase_admin
from firebase_admin import credentials, db
import sys
import select

# 1) Firebase 초기화 key_name
cred = credentials.Certificate(".json")
firebase_admin.initialize_app(cred, {
    "databaseURL": " "  # 본인 프로젝트 URL
})

# 2) 아두이노 시리얼 포트 설정
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

# 3) Firebase에서 사용할 경로
data_ref = db.reference("dishwasher")

print("Arduino → Firebase 업로더 시작")
print("터미널에 접시 개수를 입력하면 아두이노로 전송됩니다. (예: 10 입력 후 Enter)\n")

while True:
    try:
        # --- 1) 아두이노 → 파이썬 → Firebase ---
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if line:
                print("받은 데이터:", line)
                try:
                    data = json.loads(line)
                    data_ref.set({
                        "target": data.get("target", 0),
                        "remaining": data.get("remaining", 0),
                        "status": data.get("status", ""),
                    })
                except json.JSONDecodeError:
                    print("JSON 파싱 실패, 무시:", line)

        # --- 2) 키보드 입력 → 파이썬 → 아두이노 ---
        # 키보드에 뭔가 입력됐는지 논블로킹으로 체크
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            user_input = sys.stdin.readline().strip()
            if user_input:
                # 예: "10" 입력하면 아두이노로 "10\n" 전송
                ser.write((user_input + "\n").encode('utf-8'))
                print(f"아두이노로 전송: {user_input}")

    except KeyboardInterrupt:
        print("\n종료")
        break
