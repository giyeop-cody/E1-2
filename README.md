이 프로젝트는 단순한 퀴즈 게임을 만드는 것을 넘어서 넘어, **데이터의 흐름(Input → Process → Storage)** 과 **객체지향 설계(OOP)** 의 핵심 원리를 체득하기 위한 훈련용 프로젝트입니다.

---


# 프로젝트 개요 (Project Synopsis)

## 1. 이 프로젝트를 통해 배워야 할 것 (Learning Points)

* **객체지향 설계와 책임 분리 (Solid OOP)**
    * 각 클래스(`Quiz`, `Quiz Game` 등)가 서로 간섭하지 않고 자신의 일만 수행하도록 설계하며, 코드의 결합도를 낮추는 법을 익힙니다.
* **상태 관리와 파일 입출력(I/O) 핸들링**
    * 휘발성 메모리(Python 객체)와 비휘발성 저장소(JSON 파일) 사이의 데이터를 동기화하고, 파일이 없거나 깨졌을 때의 예외 처리 능력을 배웁니다.

---

## 2. 프로젝트 설명

### **[프로젝트명: Robust-Quiz-System]**

> **"신뢰할 수 있는 데이터 관리 기반의 CLI 퀴즈 애플리케이션"**

* **목적**: JSON 기반의 정적 데이터를 안전하게 관리하고, 사용자에게 인터랙티브한 퀴즈 경험과 기록 관리 기능을 제공하는 콘솔 시스템 구축.
* **핵심 철학**:
    1.  **안정성**: `JSONManager`를 통한 철저한 스키마 검증으로 런타임 에러 최소화.
    2.  **지속성**: 모든 퀴즈 진행 상황과 기록은 실시간으로 저장되어 영속성 유지.
    3.  **이식성**: Docker 설정을 통해 어떤 환경에서든 즉시 실행 가능한 패키지 구성.


    Architecture: MVC Pattern

    Model: Quiz, Record 클래스 및 JSONManager를 통한 데이터 영속성 관리.

    View: main.py 기반의 Interactive CLI.

    Controller: QuizGame 엔진을 통한 비즈니스 로직 처리 및 흐름 제어.

---

## 3. 왜 이렇게 하는가 (Why?)

1.  **실무 로직의 축소판**: 대규모 시스템에서도 "사용자 입력 -> 유효성 검사 -> 로직 처리 -> DB 저장"
2.  **확장성 연습**: 나중에 "문제를 서버(API)에서 받아오기"나 "기록을 DB에 저장하기"로 기능을 확장 가능(?)
3.  **나름 완성도 있는 포트폴리오**: 단순한 알고리즘 풀이보다, 파일 입출력/예외 처리/도커 배포까지 포함된 '완성된 애플리케이션'

---

# 퀴즈 주제 선정 이유
### [주제: Python Core Mastery - 기본 그 이상의 숙련도]

단순히 코드를 작성하는 것을 넘어, 파이썬스러운(Pythonic) 방식의 문법을 공부하기 위해서 해당 주제를 선정하였습니다.

---

# 기능 목록
* 퀴즈 풀기
* n개의 퀴즈 풀기
* 퀴즈 추가
* 퀴즈 삭제
* 퀴즈 목록
* 기록 확인
* 최고 점수 확인
* JSON type의 file I/O를 이용하여 데이터 저장과 불러오기
* JSON Scheme 검사를 통한 파일 위변조 및 손상 탐지

---

# 파일 구조

```text
project_root/
├── main.py                # 시스템 진입점 및 메뉴 UI (View & Entry Point)
├── models/                # 데이터 모델 정의 (Model)
│   ├── quiz.py            # Quiz 객체 클래스
│   └── record.py          # 사용자 기록 및 스코어 객체 클래스
├── engine/                # 비즈니스 로직 처리 (Controller)
│   └── quiz_engine.py     # 퀴즈 흐름 제어 및 핵심 로직 (QuizGame Class)
├── utils/                 # 공통 유틸리티
│   └── json_manager.py    # JSON 파일 I/O 및 스키마 검증 (JSONManager Class)
├── data/                  # 비휘발성 데이터 저장소 (Persistent Storage)
│   ├── state.json       # 퀴즈 목록, 점수 기록
├── tests/                 # 단위 테스트 (Unit Tests)
│   ├── test_engine.py     # 엔진 로직 테스트
│   └── test_utils.py      # 파일 입출력 및 검증 테스트
├── Dockerfile             # 컨테이너화 설정 파일
└── pyproject.toml         # 프로젝트 설정
```

---

# JSON 파일 스키마


 1. 퀴즈 콘텐츠 (quizzes)

    실제 퀴즈 문제들이 담기는 배열(Array) 형태의 리스트입니다.

    id: 각 문제를 식별하는 고유 번호입니다.

    question: 사용자에게 보여줄 질문 텍스트입니다.

    choices: 객관식 선택지 리스트입니다.

    answer: 정답의 인덱스입니다. (예시에서는 1이므로 첫 번째 항목인 "Guido"가 정답임을 의미합니다.)

    hint: 오답을 골랐거나 요청 시 제공할 힌트 메시지입니다.

2. 최고 기록 (best_score)

    사용자 혹은 시스템 전체에서 달성한 가장 높은 점수를 저장하는 숫자 데이터입니다.

3. 게임 이력 (records)

    과거에 퀴즈를 풀었던 세부 정보를 담은 객체 리스트입니다.

    timestamp: 퀴즈를 수행한 날짜와 시간입니다.

    score: 해당 회차에서 획득한 점수입니다.

    solved: 정답을 맞힌 개수입니다.

    tried: 전체 도전한 문제 수입니다.

```
{
    "quizzes": [
        {
            "id": 1,
            "question": "Python의 창시자는?",
            "choices": ["Guido", "Linus", "Bjarne", "James"],
            "answer": 1,
            "hint": "네덜란드 출신의 프로그래머입니다."
        }
    ],
    "best_score": 3,
    "records": [
        {
            "timestamp": "2026-04-10 14:00:00",
            "score": 470,
            "solved": 5,
            "tried": 10
        }
    ]
}
```