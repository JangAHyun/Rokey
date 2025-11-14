# mainPC → Firebase (test.txt 파일 Firebase 송신)
from google.cloud import firestore
from datetime import datetime
import os

COLLECTION_NAME = "file_sync"      # Firestore 컬렉션 이름
DOCUMENT_ID = "mainpc_test_file"   # 문서 ID (모니터링 PC와 공유할 이름)
LOCAL_FILE_PATH = "test.txt"       # mainpc에서 보낼 파일 경로


def send_file_to_firestore():
    db = firestore.Client()

    # 파일 존재 여부 확인
    if not os.path.exists(LOCAL_FILE_PATH):
        print(f"[ERROR] 파일을 찾을 수 없습니다: {LOCAL_FILE_PATH}")
        return

    with open(LOCAL_FILE_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    doc_ref = db.collection(COLLECTION_NAME).document(DOCUMENT_ID)

    doc_ref.set(
        {
            "content": content,                 
            "from": "mainpc",                 
            "filename": LOCAL_FILE_PATH,      
            "updated_at": datetime.utcnow().isoformat(), 
        }
    )

    print(f"[INFO] Firestore에 데이터 전송 완료: {COLLECTION_NAME}/{DOCUMENT_ID}")


if __name__ == "__main__":
    send_file_to_firestore()
