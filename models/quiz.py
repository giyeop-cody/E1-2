import random

class Quiz:
    def __init__(self, question, score, answer, choices, hint):
        self.question = question
        self.score = score
        self.answer = answer
        self.choices = choices
        self.hint = hint

    def to_dict(self):
        return {
            "question": self.question,
            "score": self.score,
            "answer": self.answer,
            "choices": self.choices,
            "hint": self.hint
        }

    @staticmethod
    def from_dict(data):
        return Quiz(
            data["question"],
            data["score"],
            data["answer"],
            data["choices"],
            data["hint"]
        )

    def show_question(self):
        paired = [(choice, i == self.answer - 1) for i, choice in enumerate(self.choices)]
        random.shuffle(paired)

        self.shuffled_choices = []
        lines = [f"[문제] {self.question}"]

        for i, (choice, is_correct) in enumerate(paired, 1):
            lines.append(f"{i}. {choice}")
            self.shuffled_choices.append(choice)
            if is_correct:
                self.correct_index = i

        return "\n".join(lines)


    def show_hint(self):
        return self.hint

    def check_answer(self, user_answer):
        return user_answer == self.correct_index