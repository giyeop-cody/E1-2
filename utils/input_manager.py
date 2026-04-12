from enum import Enum
from typing import Union, Iterable, Any, Type, Optional

class InputManager:
    @classmethod
    def get_input(
        cls, 
        prompt: str, 
        expected_type: Type = str, 
        dataset: Optional[Union[Iterable, Type[Enum]]] = None, 
        error_msg: str = "잘못된 입력입니다. 다시 시도해주세요."
    ) -> Any:
        while True:
            try:
                raw_input = input(f"{prompt.strip()} ").strip()
                
                if not raw_input:
                    print("[오류] 입력값이 비어있습니다. 다시 입력해주세요.")
                    continue

                # 1. 타입 변환
                if expected_type is bool:
                    low_input = raw_input.lower()
                    if low_input in ('true', '1', 'y', 'yes', 't'):
                        value = True
                    elif low_input in ('false', '0', 'n', 'no', 'f'):
                        value = False
                    else:
                        raise ValueError
                else:
                    # str인 경우 그대로 들어가고, int/float 등은 형변환 시도
                    value = expected_type(raw_input)

                # 2. 데이터셋 검증
                if dataset is not None:
                    if isinstance(dataset, type) and issubclass(dataset, Enum):
                        try:
                            # Enum 값(Value) 중 일치하는 게 있는지 확인
                            if value in [e.value for e in dataset]:
                                value = dataset(value)
                            # Enum 이름(Name) 중 일치하는 게 있는지 확인 (대소문자 무시)
                            else:
                                value = dataset[raw_input.upper()]
                        except (KeyError, ValueError):
                            raise ValueError
                            
                    elif isinstance(dataset, (list, tuple, set, range)):
                        # 문자열 리스트인 경우, 입력값과 데이터셋의 값을 모두 대문자로 비교하여 편의성 증대
                        if expected_type is str:
                            if not any(str(item).upper() == value.upper() for item in dataset):
                                raise ValueError
                            # 실제 반환은 데이터셋에 있는 원래 형태(대소문자)로 반환하거나 입력값 그대로 반환
                        elif value not in dataset:
                            raise ValueError

                return value

            except (ValueError, TypeError):
                print(f"[에러] {error_msg}")