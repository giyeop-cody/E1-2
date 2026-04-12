import sys
import os
import unittest
from unittest.mock import patch
from enum import Enum

from utils.input_manager import InputManager

# 테스트용 Enum
class Color(Enum):
    RED = "1"
    BLUE = "2"

class TestInputManager(unittest.TestCase):

    # 1. 숫자(int) 테스트
    @patch('builtins.input', side_effect=[' 25'])
    def test_get_input_int(self, mock_input):
        result = InputManager.get_input("나이:", expected_type=int)
        self.assertEqual(result, 25)
        self.assertIsInstance(result, int)
        print(f"입력 : int 25 출력 : {type(result)} {result}")

    # 2. 문자/문자열(str) 테스트
    @patch('builtins.input', side_effect=['Gemini '])
    def test_get_input_str(self, mock_input):
        result = InputManager.get_input("이름:", expected_type=str)
        self.assertEqual(result, "Gemini")
        print(f"입력 : str Gemini 출력 : {type(result)} {result}")

    # 3. 참/거짓(bool) 테스트 - 긍정 케이스
    @patch('builtins.input', side_effect=['y'])
    def test_get_input_bool_true(self, mock_input):
        result = InputManager.get_input("동의하십니까?:", expected_type=bool)
        self.assertTrue(result)
        print(f"입력 : bool y 출력 : {type(result)} {result}")

    # 4. 참/거짓(bool) 테스트 - 부정 케이스
    @patch('builtins.input', side_effect=['0'])
    def test_get_input_bool_false(self, mock_input):
        result = InputManager.get_input("취소하시겠습니까?:", expected_type=bool)
        self.assertFalse(result)
        print(f"입력 : bool 0 출력 : {type(result)} {result}")

    # 5. 데이터셋(리스트) 테스트
    @patch('builtins.input', side_effect=['Apple'])
    def test_get_input_dataset_list(self, mock_input):
        fruits = ["Apple", "Banana", "Orange"]
        result = InputManager.get_input("과일 선택:", dataset=fruits)
        self.assertEqual(result, "Apple")
        print(f"입력 : fruits Apple 출력 : {type(result)} {result}")

    # 6. 데이터셋(Enum) 테스트 - 값(Value)으로 입력
    @patch('builtins.input', side_effect=['1'])
    def test_get_input_enum_value(self, mock_input):
        result = InputManager.get_input("색상 코드:", dataset=Color)
        self.assertEqual(result, Color.RED)
        print(f"입력 : Color {Color.RED} 출력 : {type(result)} {result}")

    # 7. 데이터셋(Enum) 테스트 - 이름(Name)으로 입력
    @patch('builtins.input', side_effect=['blue']) # 소문자로 입력해도 내부에서 처리
    def test_get_input_enum_name(self, mock_input):
        result = InputManager.get_input("색상 이름:", dataset=Color)
        self.assertEqual(result, Color.BLUE)
        print(f"입력 : Color Color.Blue 출력 : {type(result)} {result}")

    # 8. 예외 처리 테스트 - 공백 입력 후 정상 입력
    @patch('builtins.input', side_effect=['', 'Valid Input'])
    def test_get_input_empty_retry(self, mock_input):
        # 첫 번째는 공백이라 건너뛰고 두 번째 값인 'Valid Input'을 반환해야 함
        result = InputManager.get_input("입력:")
        self.assertEqual(result, "Valid Input")
        print(f"입력 : str Valid Input 출력 : {type(result)} {result}")


    @patch('builtins.input', side_effect=['9', '3']) # 9는 범위 밖, 3은 범위 안
    def test_range_input(self, mock_input):
        # 첫 번째 '9' 입력 시 [에러]가 출력되고 루프가 돌아야 함
        # 두 번째 '3' 입력 시 정상 반환되어야 함
        result = InputManager.get_input("숫자:", int, range(1, 7))
        self.assertEqual(result, 3)
        print(f"입력 : int 3 출력 : {type(result)} {result}")

    @patch('builtins.input', side_effect=['f', 'b']) # f는 범위 밖, b는 범위 안
    def test_char_dataset(self, mock_input):
        result = InputManager.get_input("문자:", str, ['a', 'b', 'c', 'd'])
        self.assertEqual(result, 'b')
        print(f"입력 : str b 출력 : {type(result)} {result}")

if __name__ == '__main__':
    unittest.main()