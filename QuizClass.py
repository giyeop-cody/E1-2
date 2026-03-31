## 퀴즈 클래스 ##
## 퀴즈 내용과 점수, 정답, 보기를 정의함 ##
## 퀴즈 추가, 퀴즈 보기, 정답 확인 기능을 가짐##



import random

class Quiz:
    def __init__(self, question, score, answer, options):
        self.question = question
        self.score = score
        self.answer = answer
        self.options = options

    def to_dict(self):
        return {
            "question": self.question,
            "score": self.score,
            "answer": self.answer,
            "options": self.options
        }

    @staticmethod
    def from_dict(data):
        return Quiz(
            data["question"],
            data["score"],
            data["answer"],
            data["options"]
        )

    def show_question(self):
        print(f"[문제] {self.question}")
        
        paired = [(opt, i == self.answer - 1) for i , opt in enumerate(self.options)]
        
        random.shuffle(paired)

        self.shuffled_options = []
        self.correct_index = None

        for i, (option, is_correct) in enumerate(paired, 1):
            print(f"{i}. {option}")
            self.shuffled_options.append(option)

            if is_correct:
                self.correct_index = i

    def check_answer(self, user_answer):
        return user_answer == self.correct_index