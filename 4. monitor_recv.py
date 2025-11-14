# 모니터링 PC → Firebase(Firebase에서 content를 읽어서 로컬 파일로 저장)
from google.cloud import firestore
import os

# === 설정값 ===
COLLECTION_NAME = "file_sync"            # mainpc와 동일
DOCUMENT_ID = "mainpc_test_file"         # mainpc와 동일
OUTPUT_FILE_PATH = "received_test.txt"   # 모니터링 PC에 저장할 파일명


def fetch_file_from_firestore():
    # Firestore 클라이언트 생성
    db = firestore.Client()

    # 문서 참조
    doc_ref = db.collection(COLLECTION_NAME).document(DOCUMENT_ID)
    doc = doc_ref.get()

    if not doc.exists:
        print(f"[ERROR] 문서를 찾을 수 없습니다: {COLLECTION_NAME}/{DOCUMENT_ID}")
        return

    data = doc.to_dict()
    content = data.get("content", "")

    print("[INFO] Firestore에서 데이터 가져오기 성공")
    print("------ content (preview) ------")
    print(content)
    print("------ end preview ------")

    # 로컬 파일로 저장
    with open(OUTPUT_FILE_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[INFO] 내용이 로컬 파일로 저장되었습니다: {OUTPUT_FILE_PATH}")


if __name__ == "__main__":
    fetch_file_from_firestore()
