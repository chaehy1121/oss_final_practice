# 🌸 오늘의 향기 추천 앱

날씨와 기분, 외출 목적에 따라 어울리는 향조를 추천해주는 웹 애플리케이션입니다.

**기술 스택:** Streamlit · FastAPI · Docker · AWS EC2

---

## 📁 프로젝트 구조

```
.
├── front/
│   ├── main.py            # Streamlit 프론트엔드
│   ├── Dockerfile
│   └── requirements.txt
├── back/
│   ├── main.py            # FastAPI 백엔드
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml
├── .gitignore
└── README.md
```

## 🌿 추천 향조 로직

| 조건 | 추천 향조 |
|------|---------|
| 날씨 맑음 OR 기분 상쾌 | 🍋 시트러스 |
| 날씨 비/흐림 OR 목적 휴식 | 🌲 우디 |
| 목적 데이트 OR 날씨 맑음 | 🌸 플로럴 |
| 날씨 흐림 OR 기분 우울 | 🍮 바닐라 |
| 목적 업무 OR 기분 차분 | 🕊️ 머스크 |

---

## 📡 API 명세

### `POST /recommend`

**Request Body**
```json
{
  "mood": "상쾌",
  "purpose": "데이트",
  "weather": "맑음"
}
```

**Response**
```json
{
  "note": "시트러스",
  "ootd": "화이트 린넨 셔츠에 베이지 와이드 팬츠 — 청량하고 가벼운 데일리 룩",
  "effect": "기분을 환기시키고 집중력을 높여주어 활기차게 하루를 시작하게 해줍니다."
}
```
