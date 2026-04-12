from datetime import datetime

class Record:
    def __init__(self, timestamp, score, solved, tried):
        self.score = score
        self.solved = solved
        self.tried = tried
        
        self.timestamp = timestamp if timestamp else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "score": self.score,
            "solved": self.solved,
            "tried": self.tried
        }

    @staticmethod
    def from_dict(data):
        return Record(
            data["timestamp"],
            data["score"],
            data["solved"],
            data["tried"]
        )
    
    def show_record(self):
        return f"{self.timestamp} - {self.score}점 - ({self.solved}/{self.tried})"