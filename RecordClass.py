
class Record:
    def __init__(self):
        self.timestamp = None
        self.total_score = None
        self.solved_count = None
        self.correct_count = None

    def show_record(self):
        print(f"일시 : {self.timestamp.strftime("%Y년 %M월 %D일")} \t 획득 점수 : {self.total_score} \t 맞춘 문제 : {self.solved_count} \t 푼 문제 : {self.correct_count}")

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "total_score": self.total_score,
            "solved_count": self.solved_count,
            "correct_count": self.correct_count
        }

    @staticmethod
    def from_dict(data):
        return Record(
            data["timestamp"],
            data["total_score"],
            data["solved_count"],
            data["correct_count"]
        )