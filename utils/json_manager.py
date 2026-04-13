import json
import os

class JSONSchemaError(Exception):
    """스키마 검증 실패 시 발생하는 예외"""
    pass

class JSONManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def save(self, data, schema = None):
        """데이터를 UTF-8 형식의 JSON 파일로 저장"""
        tmp_path = f"{self.file_path}.tmp"
        backup_path = f"{self.file_path}.bak"

        if schema:
            self.validate(data, schema)

        try:
            # 1. 임시 파일에 데이터 쓰기
            with open(tmp_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            # 2. 기존 파일이 존재하면 백업 파일로 이름 변경 (이미 백업이 있다면 덮어씌움)
            if os.path.exists(self.file_path):
                if os.path.exists(backup_path):
                    os.remove(backup_path)
                os.rename(self.file_path, backup_path)

            # 3. 임시 파일을 원본 파일 이름으로 변경
            os.rename(tmp_path, self.file_path)

        except Exception as e:
            # 오류 발생 시 임시 파일이 남아있다면 삭제 (정리 작업)
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            # 4. 예외를 호출자에게 다시 던짐 (raise)
            raise e

    def load(self, schema=None, restore_from_backup=False):
        """
        파일을 읽고 선택적으로 스키마를 검증합니다.
        원본 파일이 없고 백업 파일이 존재할 경우, restore_from_backup이 True라면 복원을 시도합니다.
        """
        backup_path = f"{self.file_path}.bak"
        
        # 1. 원본 파일이 없는 경우 처리
        if not os.path.exists(self.file_path):
            # 백업 파일이 존재하고 복원 옵션이 켜져 있는 경우
            if restore_from_backup and os.path.exists(backup_path):
                try:
                    os.rename(backup_path, self.file_path)
                    # print(f"알림: 원본 파일이 없어 백업 파일({backup_path})에서 복원되었습니다.")
                except Exception as e:
                    raise IOError(f"백업 파일 복원 중 오류 발생: {e}")
            else:
                raise FileNotFoundError(f"'{self.file_path}' 파일이 존재하지 않습니다.")

        # 2. 파일 읽기 로직
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            raise ValueError("오류: 파일이 유효한 JSON 형식이 아니거나 손상되었습니다.")
        except PermissionError:
            raise PermissionError(f"'{self.file_path}'를 읽을 권한이 없습니다.")

        # 3. 스키마 검증
        if schema:
            self.validate(data, schema)
        
        return data

    def validate(self, data, schema, path="root"):
        """
        재귀적으로 데이터의 타입과 구조를 스키마와 비교 검증
        """
        # 1. 리스트 검증 (객체 리스트, 단순 값 리스트 포함)
        if isinstance(schema, list):
            if not isinstance(data, list):
                raise JSONSchemaError(f"'{path}'는 list 타입이어야 합니다.")
            if len(schema) > 0:
                item_schema = schema[0]
                for i, item in enumerate(data):
                    self.validate(item, item_schema, f"{path}[{i}]")
        
        # 2. 객체(딕셔너리) 검증
        elif isinstance(schema, dict):
            if not isinstance(data, dict):
                raise JSONSchemaError(f"'{path}'는 dict 타입이어야 합니다.")
            for key, expected_type in schema.items():
                if key not in data:
                    raise JSONSchemaError(f"필수 키 '{key}'가 '{path}'에 누락되었습니다.")
                self.validate(data[key], expected_type, f"{path}.{key}")
        
        # 3. 기본 값 및 타입 검증
        else:
            if not isinstance(data, schema):
                raise JSONSchemaError(
                    f"'{path}'의 타입이 맞지 않습니다. (기대: {schema.__name__}, 실제: {type(data).__name__})"
                )

        return True