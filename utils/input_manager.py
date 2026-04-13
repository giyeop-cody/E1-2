from enum import Enum
from typing import Union, Iterable, Any, Type, Optional

# 커스텀 예외 정의
class EmptyInput(Exception):
    """입력값이 비어있을 때 발생"""
    pass

class OutofRange(Exception):
    """range 범위를 벗어났을 때 발생"""
    pass

class InvalidType(Exception):
    pass

class InputManager:
    @classmethod
    def get_input(
        cls, 
        prompt: str, 
        expected_type: Type = str, 
        dataset: Optional[Union[Iterable, Type[Enum]]] = None, 
    ) -> Any:
        raw_input = input(f"{prompt.strip()} ").strip()
        
        # 1. 빈 값 검증
        if not raw_input:
            raise EmptyInput("입력값이 비어있습니다. 내용을 입력해 주세요.")

        # 2. 타입 변환
        if expected_type is bool:
            low_input = raw_input.lower()
            if low_input in ('true', '1', 'y', 'yes', 't'):
                value = True
            elif low_input in ('false', '0', 'n', 'no', 'f'):
                value = False
            else:
                raise ValueError("y/n 또는 True/False 형식으로 입력해주세요.")
        else:
            try:
                value = expected_type(raw_input)
            except ValueError:
                # 에러 메시지에 기대하는 타입 이름을 포함
                raise InvalidType(f"입력 형식이 잘못되었습니다. ({expected_type.__name__} 필요)")

        # 3. 데이터셋 검증
        if dataset is not None:
            # A. Enum 클래스인 경우
            if isinstance(dataset, type) and issubclass(dataset, Enum):
                try:
                    if value in [e.value for e in dataset]:
                        value = dataset(value)
                    else:
                        value = dataset[raw_input.upper()]
                except (KeyError, ValueError):
                    # Enum의 모든 선택지를 에러 메시지에 포함
                    options = [f"{e.name}({e.value})" for e in dataset]
                    raise ValueError(f"선택지에 없는 항목입니다. 선택 가능 목록: {options}")
            
            # B. range 객체인 경우
            elif isinstance(dataset, range):
                if value not in dataset:
                    raise OutofRange(f"범위를 벗어났습니다. (허용 범위: {dataset.start} ~ {dataset.stop - 1})")
            
            # C. 리스트, 튜플 등 일반 Iterable인 경우
            elif isinstance(dataset, (list, tuple, set)):
                if expected_type is str:
                    # 대소문자 무시 비교 로직
                    found = False
                    for item in dataset:
                        if str(item).upper() == value.upper():
                            value = item # 원래 대소문자 형태로 치환
                            found = True
                            break
                    if not found:
                        raise ValueError(f"목록에 없는 값입니다. 선택 가능 목록: {list(dataset)}")
                else:
                    if value not in dataset:
                        raise ValueError(f"허용되지 않은 값입니다. 선택 가능 목록: {list(dataset)}")

        return value