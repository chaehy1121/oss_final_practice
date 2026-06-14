from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="오늘의 향기 추천 API")

# CORS 설정 (Streamlit → FastAPI 통신 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 요청 데이터 모델
class RecommendRequest(BaseModel):
    mood: str       # 기분: 우울 / 상쾌 / 차분
    purpose: str    # 외출 목적: 데이트 / 휴식 / 업무
    weather: str    # 날씨: 맑음 / 흐림 / 비


# 향조별 추천 데이터
FRAGRANCE_DATA = {
    "시트러스": {
        "note": "시트러스",
        "ootd": "화이트 린넨 셔츠에 베이지 와이드 팬츠 — 청량하고 가벼운 데일리 룩",
        "effect": "기분을 환기시키고 집중력을 높여주어 활기차게 하루를 시작하게 해줍니다.",
    },
    "플로럴": {
        "note": "플로럴",
        "ootd": "플리츠 미디 스커트에 크림색 블라우스 — 우아하고 사랑스러운 로맨틱 룩",
        "effect": "긍정적인 감정을 끌어올리고 주변 분위기를 환하게 밝혀줍니다.",
    },
    "우디": {
        "note": "우디",
        "ootd": "오버사이즈 니트에 다크 데님 — 깊고 안정적인 캐주얼 무드",
        "effect": "심신을 안정시키고 내면의 평온함을 찾아주는 그라운딩 효과가 있습니다.",
    },
    "바닐라": {
        "note": "바닐라",
        "ootd": "카멜 컬러 트렌치코트에 터틀넥 — 따뜻하고 포근한 클래식 룩",
        "effect": "마음을 위로하고 감싸주는 따뜻한 정서적 안정감을 선사합니다.",
    },
    "머스크": {
        "note": "머스크",
        "ootd": "슬랙스에 모노톤 재킷 — 세련되고 신뢰감 있는 미니멀 오피스 룩",
        "effect": "차분하고 집중된 상태를 유지하게 해주어 생산성을 높여줍니다.",
    },
}


def get_fragrance_note(mood: str, purpose: str, weather: str) -> str:
    """
    입력 조건별 점수를 합산하여 가장 높은 점수의 향조를 추천합니다.
    5가지 향조 모두 도달 가능하도록 설계되었습니다.

    점수 부여 기준:
    ┌─────────────────┬────────┬──────┬──────┬──────┬──────┐
    │ 입력 조건       │시트러스│플로럴│우디  │바닐라│머스크│
    ├─────────────────┼────────┼──────┼──────┼──────┼──────┤
    │ 날씨: 맑음      │  +2   │  +1  │      │      │      │
    │ 날씨: 흐림      │       │      │  +1  │  +2  │      │
    │ 날씨: 비        │       │      │  +2  │      │      │
    │ 기분: 상쾌      │  +2   │      │      │      │      │
    │ 기분: 차분      │       │      │      │  +1  │  +2  │
    │ 기분: 우울      │       │      │  +1  │  +2  │      │
    │ 목적: 데이트    │  +1   │  +2  │      │      │      │
    │ 목적: 휴식      │       │  +1  │  +1  │  +1  │      │
    │ 목적: 업무      │       │      │      │      │  +2  │
    └─────────────────┴────────┴──────┴──────┴──────┴──────┘
    """
    scores: dict[str, int] = {
        "시트러스": 0,
        "플로럴":   0,
        "우디":     0,
        "바닐라":   0,
        "머스크":   0,
    }

    # ── 날씨별 점수 ──────────────────────────────
    if weather == "맑음":
        scores["시트러스"] += 2
        scores["플로럴"]   += 1
    elif weather == "흐림":
        scores["우디"]     += 1
        scores["바닐라"]   += 2
    elif weather == "비":
        scores["우디"]     += 2

    # ── 기분별 점수 ──────────────────────────────
    if mood == "상쾌":
        scores["시트러스"] += 2
    elif mood == "차분":
        scores["머스크"]   += 2
        scores["바닐라"]   += 1
    elif mood == "우울":
        scores["바닐라"]   += 2
        scores["우디"]     += 1

    # ── 목적별 점수 ──────────────────────────────
    if purpose == "데이트":
        scores["플로럴"]   += 2
        scores["시트러스"] += 1
    elif purpose == "휴식":
        scores["플로럴"]   += 1
        scores["우디"]     += 1
        scores["바닐라"]   += 1
    elif purpose == "업무":
        scores["머스크"]   += 2

    # 가장 높은 점수의 향조 선택
    best_note = max(scores, key=lambda k: scores[k])
    return best_note


@app.get("/")
def root():
    return {"message": "오늘의 향기 추천 API가 정상 실행 중입니다."}


@app.post("/recommend")
def recommend(request: RecommendRequest):
    """
    사용자 입력(기분, 외출 목적, 날씨)을 받아
    점수 기반 로직으로 향조 추천 결과를 JSON으로 반환합니다.
    """
    note = get_fragrance_note(
        mood=request.mood,
        purpose=request.purpose,
        weather=request.weather,
    )
    result = FRAGRANCE_DATA[note]
    return result
