import sys
from utils.input_manager import InputManager

def cleanup():
    """프로그램 종료 전 자원을 정리하거나 메시지를 출력하는 함수"""
    print("\n[시스템] 프로그램을 안전하게 종료합니다. 이용해 주셔서 감사합니다.")
    # 필요한 경우 파일 닫기나 DB 연결 해제 로직을 여기에 추가합니다.
    sys.exit(0)

def main_menu():
    """메뉴 인터페이스를 무한 루프로 실행"""
    while True:
        try:
            print("\n--- 메인 메뉴 ---")
            print("1. 서비스 시작")
            print("2. 설정 변경")
            print("3. 프로그램 종료")
            
            choice = InputManager.get_input(
                prompt="번호 입력", 
                expected_type=int, 
                dataset=range(1, 4),  # 1, 2, 3만 허용 (레인지 기능 활용)
                error_msg="1~3번 사이의 번호를 입력해주세요."
            )

            if choice == 1:  # 숫자로 비교
                print("[알림] 서비스를 시작합니다...")
            elif choice == 2:
                print("[알림] 설정 메뉴로 진입합니다...")
            elif choice == 3:
                cleanup()
        except KeyboardInterrupt:
            # Ctrl+C 입력 시 발생
            print("\n\n[중단] 사용자에 의해 강제 종료 요청됨 (KeyboardInterrupt)")
            cleanup()
        
        except EOFError:
            # Ctrl+D (Unix) 또는 Ctrl+Z (Windows) 입력 시 발생
            print("\n\n[중단] 입력 스트림이 종료됨 (EOF)")
            cleanup()
            
        except Exception as e:
            # 기타 예기치 못한 에러 처리
            print(f"[에러] 알 수 없는 오류가 발생했습니다: {e}")
            cleanup()

if __name__ == "__main__":
    main_menu()