import unittest
from datetime import datetime
from models.record import Record

class TestRecord(unittest.TestCase):

    def setUp(self):
        """테스트에 사용할 공통 데이터 설정"""
        self.sample_timestamp = "2023-10-27 14:30:00"
        self.score = 85
        self.solved = 17
        self.tried = 20
        self.record = Record(self.sample_timestamp, self.score, self.solved, self.tried)

    def test_initialization_with_timestamp(self):
        """타임스탬프가 주어졌을 때 올바르게 초기화되는지 테스트"""
        self.assertEqual(self.record.timestamp, self.sample_timestamp)
        self.assertEqual(self.record.score, self.score)
        self.assertEqual(self.record.solved, self.solved)
        self.assertEqual(self.record.tried, self.tried)

    def test_initialization_without_timestamp(self):
        """타임스탬프가 없을 때(None) 현재 시간으로 생성되는지 테스트"""
        new_record = Record(None, 100, 5, 5)
        # 현재 시간과 형식이 맞는지 확인 (YYYY-MM-DD 형식 포함 여부로 간접 확인)
        current_date = datetime.now().strftime("%Y-%m-%d")
        self.assertIn(current_date, new_record.timestamp)
        self.assertEqual(len(new_record.timestamp), 19)  # "YYYY-MM-DD HH:MM:SS" 길이는 19자

    def test_to_dict(self):
        """객체를 딕셔너리로 변환했을 때 데이터가 유지되는지 테스트"""
        record_dict = self.record.to_dict()
        expected_dict = {
            "timestamp": self.sample_timestamp,
            "score": self.score,
            "solved": self.solved,
            "tried": self.tried
        }
        self.assertEqual(record_dict, expected_dict)

    def test_from_dict(self):
        """딕셔너리 데이터를 통해 Record 객체가 올바르게 생성되는지 테스트"""
        data = {
            "timestamp": "2024-01-01 12:00:00",
            "score": 50,
            "solved": 5,
            "tried": 10
        }
        new_record = Record.from_dict(data)
        self.assertEqual(new_record.timestamp, data["timestamp"])
        self.assertEqual(new_record.score, 50)
        self.assertEqual(new_record.solved, 5)

    def test_show_record_format(self):
        """문자열 출력 형식이 요구사항과 일치하는지 테스트"""
        expected_string = f"{self.sample_timestamp} - 85점 - (17/20)"
        self.assertEqual(self.record.show_record(), expected_string)

if __name__ == '__main__':
    unittest.main()
