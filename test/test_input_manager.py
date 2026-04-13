import unittest
from unittest.mock import patch
from enum import Enum

# 테스트 대상 클래스와 예외들을 가져옵니다.
# (위에서 작성한 코드가 input_manager.py에 있다고 가정하거나 같은 파일에 두어야 합니다.)

class Color(Enum):
    RED = 1
    BLUE = 2

class TestInputManager(unittest.TestCase):

    def print_test_result(self, case_name, user_input, expected, actual, status="PASS"):
        """테스트 결과를 포맷에 맞춰 출력합니다."""
        print(f"[{case_name}]")
        print(f"  - 입력값: {user_input}")
        print(f"  - 기대치: {expected}")
        print(f"  - 결과값: {actual}")
        print(f"  - 상태: {status}\n")

    @patch('builtins.input')
    def test_01_normal_int(self, mock_input):
        """정상적인 정수 입력 테스트"""
        user_input = "25"
        mock_input.return_value = user_input
        
        result = InputManager.get_input("나이:", int)
        
        self.assertEqual(result, 25)
        self.print_test_result("정상 정수 테스트", user_input, 25, result)

    @patch('builtins.input')
    def test_02_empty_input_exception(self, mock_input):
        """빈 입력 시 EmptyInput 예외 발생 테스트"""
        user_input = ""
        mock_input.return_value = user_input
        
        with self.assertRaises(EmptyInput) as cm:
            InputManager.get_input("입력:")
        
        self.print_test_result("빈 값 예외 테스트", "''", "EmptyInput Exception", type(cm.exception).__name__)

    @patch('builtins.input')
    def test_03_value_error_type(self, mock_input):
        """정수형을 기대했으나 문자열을 입력했을 때 InvalidType 발생 테스트"""
        user_input = "hello_world"
        mock_input.return_value = user_input
        
        # InvalidType이 발생하는지 확인
        with self.assertRaises(InvalidType) as cm:
            InputManager.get_input("숫자 입력:", expected_type=int)
            
        self.print_test_result(
            "타입 에러 테스트", 
            user_input, 
            "InvalidType", 
            type(cm.exception).__name__
        )

    @patch('builtins.input')
    def test_04_range_out_of_error(self, mock_input):
        """범위 초과 시 OutofRange 예외 발생 테스트"""
        user_input = "15"
        mock_input.return_value = user_input
        
        with self.assertRaises(OutofRange) as cm:
            InputManager.get_input("1~10 입력:", int, dataset=range(1, 11))
            
        self.print_test_result("범위 초과 테스트", user_input, "OutofRange", type(cm.exception).__name__)

    @patch('builtins.input')
    def test_05_enum_mapping(self, mock_input):
        """Enum 이름으로 입력 시 객체 반환 테스트"""
        user_input = "red"
        mock_input.return_value = user_input
        
        result = InputManager.get_input("색상:", str, dataset=Color)
        
        self.assertEqual(result, Color.RED)
        self.print_test_result("Enum 매핑 테스트", user_input, Color.RED, result)

    @patch('builtins.input')
    def test_06_list_case_insensitive(self, mock_input):
        """리스트 대소문자 무시 및 원본 반환 테스트"""
        user_input = "apple"
        mock_input.return_value = user_input
        dataset = ["Apple", "Banana"]
        
        result = InputManager.get_input("과일:", str, dataset=dataset)
        
        self.assertEqual(result, "Apple") # 입력은 소문자이나 원본인 대문자로 나와야 함
        self.print_test_result("리스트 대소문자 테스트", user_input, "Apple", result)

    @patch('builtins.input')
    def test_08_bool_invalid_type(self, mock_input):
        """bool 타입을 기대했으나 엉뚱한 문자열 입력 시 테스트"""
        user_input = "maybe"
        mock_input.return_value = user_input
        
        with self.assertRaises(InvalidType) as cm:
            InputManager.get_input("동의하십니까?:", expected_type=bool)
            
        self.print_test_result(
            "Bool 타입 에러 테스트", 
            user_input, 
            "InvalidType", 
            type(cm.exception).__name__
        )

if __name__ == '__main__':
    unittest.main()