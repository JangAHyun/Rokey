# move2rack.py
from mainpc_send import update_dish_count

dish_cnt = 0  # 닦은 접시 수 카운트 변수


def move_one_dish():
    global dish_cnt

    # 1. 여기서 로봇 실제 동작 수행
    #    로봇이 랙에 접시 하나 올리는 동작 끝나는 지점까지 코드…

    # 로봇 동작이 정상적으로 끝났다고 판단되는 시점에:
    dish_cnt += 1

    # 2. Firebase에 현재 카운트 업로드
    update_dish_count(dish_cnt)


def run_all_dishes():
    """
    예시: 접시 10개를 순차 이동한다 가정
    실제로는 dish list / rack 위치에 따라 루프를 돌겠지?
    """
    target_dish_cnt = 10

    for i in range(target_dish_cnt):
        print(f"[INFO] {i+1} 번째 접시 이동 시작")
        move_one_dish()
        # 필요시 중간 딜레이 / 오류 체크 추가


if __name__ == "__main__":
    run_all_dishes()
