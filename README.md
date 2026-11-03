# Airtable Alert

Airtable에 등록된 제품의 주요 일정을 확인하고, 알림 대상이 되면 Telegram으로 메시지를 전송하는 자동화 프로젝트입니다. GitHub Actions를 이용해 정기적으로 실행되므로 별도의 서버를 운영하지 않아도 됩니다.

## 주요 기능

- Airtable 레코드에서 제품 및 일정 정보를 조회
- 예상 소진일, 만족 보장 종료일 등 관리 대상 날짜 확인
- 기준일이 가까워지면 Telegram 알림 전송
- GitHub Actions를 통한 예약 실행
- Python 기반의 간단한 구성으로 유지보수 가능

## 동작 방식

1. GitHub Actions가 설정된 일정에 따라 워크플로를 실행합니다.
2. `notify.py`가 Airtable API를 호출해 관리 대상 레코드를 읽습니다.
3. 각 레코드의 날짜와 현재 날짜를 비교해 알림 대상 여부를 판단합니다.
4. 알림 대상인 경우 Telegram Bot API를 통해 메시지를 전송합니다.

## 프로젝트 구조

```text
.
├── .github/
│   └── workflows/
│       └── notify.yml    # 예약 실행용 GitHub Actions 워크플로
├── notify.py             # Airtable 조회 및 Telegram 알림 처리
└── README.md
```

## 사전 준비

다음 항목이 필요합니다.

- Airtable Personal Access Token
- Airtable Base ID
- 조회할 Airtable 테이블 정보
- Telegram Bot Token
- Telegram Chat ID

### Telegram Bot 준비

1. Telegram에서 `@BotFather`를 검색합니다.
2. `/newbot` 명령으로 새 봇을 생성합니다.
3. 발급된 Bot Token을 안전하게 보관합니다.
4. 생성한 봇에게 메시지를 한 번 보낸 뒤 Chat ID를 확인합니다.

### Airtable 준비

1. Airtable에서 알림에 사용할 Base와 Table을 준비합니다.
2. Airtable Developer Hub에서 Personal Access Token을 생성합니다.
3. 대상 Base를 읽을 수 있도록 필요한 권한을 부여합니다.
4. `notify.py`가 참조하는 필드 이름과 Airtable의 실제 필드 이름이 일치하는지 확인합니다.

## GitHub Actions 설정

저장소의 **Settings > Secrets and variables > Actions**에서 `notify.py`와 `notify.yml`이 참조하는 값을 Repository Secret으로 등록합니다.

일반적으로 다음과 같은 값이 필요합니다.

| 구분 | 설명 |
|---|---|
| Airtable Token | Airtable API 인증 토큰 |
| Airtable Base ID | 대상 Airtable Base 식별자 |
| Airtable Table | 조회할 테이블 이름 또는 식별자 |
| Telegram Bot Token | BotFather에서 발급받은 봇 토큰 |
| Telegram Chat ID | 알림을 받을 개인 또는 그룹의 Chat ID |

> 실제 Secret 이름은 `.github/workflows/notify.yml`과 `notify.py`에서 사용하는 환경 변수 이름을 기준으로 등록해야 합니다.

## 실행 방법

### GitHub Actions에서 실행

1. 저장소의 **Actions** 탭을 엽니다.
2. 알림 워크플로를 선택합니다.
3. 수동 실행이 설정되어 있다면 **Run workflow**를 선택합니다.
4. 실행 로그에서 Airtable 조회 및 Telegram 전송 결과를 확인합니다.

### 로컬 실행

필요한 환경 변수를 설정한 뒤 다음 명령을 실행합니다.

```bash
python notify.py
```

Python 패키지가 추가로 필요한 경우 `notify.py`의 import 항목에 맞게 설치합니다.

## 운영 시 확인 사항

- GitHub Actions의 `cron` 시간은 기본적으로 UTC입니다. 한국 시간으로 실행하려면 UTC 기준으로 변환해야 합니다.
- Airtable의 날짜 형식과 표준 시간대가 코드의 비교 기준과 일치해야 합니다.
- Token, Chat ID와 같은 민감한 값은 코드에 직접 작성하지 말고 GitHub Actions Secrets로 관리해야 합니다.
- 동일한 일정에 대해 워크플로가 여러 번 실행되면 알림이 중복 전송될 수 있으므로 실행 주기와 중복 방지 로직을 확인해야 합니다.
- Airtable 필드 이름을 변경하면 `notify.py`의 참조 필드도 함께 수정해야 합니다.

## 문제 해결

### Airtable 데이터를 가져오지 못하는 경우

- Personal Access Token의 권한과 대상 Base 접근 범위를 확인합니다.
- Base ID, Table 이름, 필드 이름이 정확한지 확인합니다.
- GitHub Actions Secrets 이름이 워크플로의 환경 변수 이름과 일치하는지 확인합니다.

### Telegram 메시지가 전송되지 않는 경우

- Bot Token과 Chat ID가 올바른지 확인합니다.
- 개인 채팅에서는 먼저 봇에게 메시지를 보냈는지 확인합니다.
- 그룹 채팅에서는 봇이 그룹에 추가되어 있고 메시지를 보낼 수 있는지 확인합니다.

### 예약 시간과 실제 실행 시간이 다른 경우

- `notify.yml`의 `cron` 값이 UTC 기준인지 확인합니다.
- GitHub Actions는 부하 상황에 따라 예약 시각보다 몇 분 늦게 시작될 수 있습니다.

## 보안 권장 사항

- Airtable Token과 Telegram Bot Token을 저장소에 커밋하지 않습니다.
- 민감한 값은 GitHub Actions Secrets를 사용합니다.
- 토큰이 노출된 경우 즉시 폐기하고 새로 발급합니다.
- Airtable Token에는 필요한 최소 권한만 부여합니다.

## 라이선스

별도의 라이선스가 지정되어 있지 않은 경우, 사용 및 배포 조건은 저장소 소유자에게 문의하세요.
