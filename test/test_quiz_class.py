import unittest
from models.quiz import Quiz 

class TestQuiz(unittest.TestCase):

    def setUp(self):
        """테스트에 사용할 공통 Quiz 객체 설정"""
        self.question_text = "대한민국의 수도는?"
        self.score = 10
        self.answer_index = 1  # 서울
        self.choices = ["서울", "부산", "대구", "인천"]
        self.hint = "ㅅㅇ"
        self.quiz = Quiz(self.question_text, self.score, self.answer_index, self.choices, self.hint)

    def test_initialization(self):
        """객체 생성 및 속성 할당 테스트"""
        self.assertEqual(self.quiz.question, self.question_text)
        self.assertEqual(self.quiz.score, self.score)
        self.assertEqual(self.quiz.choices, self.choices)
        self.assertEqual(self.quiz.hint, self.hint)

    def test_to_dict(self):
        """to_dict 메서드가 올바른 딕셔너리를 반환하는지 테스트"""
        expected_dict = {
            "question": self.question_text,
            "score": self.score,
            "answer": self.answer_index,
            "choices": self.choices,
            "hint": self.hint
        }
        self.assertEqual(self.quiz.to_dict(), expected_dict)

    def test_from_dict(self):
        """from_dict 정적 메서드가 딕셔너리로부터 객체를 올바르게 생성하는지 테스트"""
        data = {
            "question": "파이썬의 창시자는?",
            "score": 20,
            "answer": 2,
            "choices": ["제임스 고슬링", "귀도 반 로섬"],
            "hint": "ㄱㄷ"
        }
        new_quiz = Quiz.from_dict(data)
        self.assertEqual(new_quiz.question, "파이썬의 창시자는?")
        self.assertEqual(new_quiz.score, 20)
        self.assertEqual(new_quiz.choices[1], "귀도 반 로섬")

    def test_show_question_shuffling(self):
        """문제 출력 시 선택지가 섞이고 correct_index가 갱신되는지 테스트"""
        output = self.quiz.show_question()
        
        # 1. 출력 문자열에 질문이 포함되어 있는지 확인
        self.assertIn(self.question_text, output)
        
        # 2. 셔플된 리스트에서 정답 위치(correct_index)의 값이 실제 정답("서울")인지 확인
        actual_correct_choice = self.quiz.shuffled_choices[self.quiz.correct_index - 1]
        self.assertEqual(actual_correct_choice, "서울")

    def test_check_answer_correct(self):
        """사용자가 정답을 맞혔을 때 True를 반환하는지 테스트"""
        self.quiz.show_question()  # correct_index 생성을 위해 선행 실행
        user_input = self.quiz.correct_index
        self.assertTrue(self.quiz.check_answer(user_input))

    def test_check_answer_incorrect(self):
        """사용자가 오답을 입력했을 때 False를 반환하는지 테스트"""
        self.quiz.show_question()
        # 정답이 아닌 번호 생성
        wrong_input = 1 if self.quiz.correct_index != 1 else 2
        self.assertFalse(self.quiz.check_answer(wrong_input))

    def test_show_hint(self):
        """힌트 반환 테스트"""
        self.assertEqual(self.quiz.show_hint(), self.hint)

if __name__ == '__main__':
    unittest.main()
