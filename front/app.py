import os
import time
import streamlit as st
import requests

# ──────────────────────────────────────────────
# 페이지 기본 설정
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="오늘의 향기 추천",
    page_icon="🌸",
    layout="centered",
)

# ──────────────────────────────────────────────
# 커스텀 CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
    /* 전체 배경 */
    .stApp {
        background: linear-gradient(135deg, #fdf6f0 0%, #f5e6f0 50%, #ede6f7 100%);
    }

    /* 헤더 타이틀 */
    .main-title {
        font-family: 'Georgia', serif;
        font-size: 2.4rem;
        font-weight: 700;
        color: #4a2c4a;
        text-align: center;
        letter-spacing: 0.04em;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-family: 'Georgia', serif;
        font-size: 1.0rem;
        color: #9a7aaa;
        text-align: center;
        margin-bottom: 2rem;
        letter-spacing: 0.08em;
    }

    /* 입력 폼 카드 */
    .form-card {
        padding: 1rem 1rem;
        margin-bottom: 1.5rem;
    }

    /* 결과 카드 */
    .result-card {
        padding: 2rem 1rem;
        text-align: center;
        margin-top: 0;
    }
    .note-badge {
        display: inline-block;
        background: linear-gradient(135deg, #b06090, #7b4f9e);
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        padding: 1rem 2.5rem;
        border-radius: 50px;
        letter-spacing: 0.08em;
        margin-bottom: 1.5rem;
        font-family: 'Georgia', serif;
    }
    .result-label {
        font-size: 1.1rem;
        font-weight: 700;
        color: #9a7aaa;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    .result-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #3d2050;
        margin-bottom: 1.1rem;
        line-height: 1.65;
    }

    /* 구분선 */
    .divider {
        border: none;
        border-top: 1px solid #e0c8e8;
        margin: 1.2rem 0;
    }

    /* Streamlit 기본 버튼 오버라이드 */
    .stButton > button {
        background: linear-gradient(135deg, #b06090, #7b4f9e);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 1.2rem 3rem;
        font-size: 1.5rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        width: 100%;
        transition: opacity 0.2s;
        margin-top: 1.5rem;
    }
    .stButton > button:hover {
        opacity: 0.88;
        color: white;
    }

    /* selectbox 레이블 */
    label {
        color: #5a3060 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    /* 에러 메시지 */
    .error-box {
        background: #fff0f0;
        border: 1.5px solid #e8b0b0;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        color: #8b2020;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# FastAPI 엔드포인트
# ──────────────────────────────────────────────
FASTAPI_HOST="98.94.222.157"
FASTAPI_URL = f"http://{FASTAPI_HOST}:8000/recommend"

# ──────────────────────────────────────────────
# 헤더
# ──────────────────────────────────────────────
st.markdown('<div class="main-title">🌸 오늘의 향기 추천</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">날씨와 기분에 어울리는 향조를 찾아드립니다</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────
# 입력 폼
# ──────────────────────────────────────────────
st.markdown('<div class="form-card">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    mood = st.selectbox(
        "🌙 지금 기분은?",
        options=["상쾌", "차분", "우울"],
        index=0,
    )

with col2:
    purpose = st.selectbox(
        "👟 오늘의 외출 목적",
        options=["데이트", "휴식", "업무"],
        index=0,
    )

with col3:
    weather = st.selectbox(
        "☁️ 오늘 날씨는?",
        options=["맑음", "흐림", "비"],
        index=0,
    )

st.markdown('</div>', unsafe_allow_html=True)

recommend_btn = st.button("✨ 나에게 맞는 향기 추천 요청")

# ──────────────────────────────────────────────
# 추천 요청 및 결과 표시
# ──────────────────────────────────────────────

# 향조 이모지 매핑
NOTE_EMOJI = {
    "시트러스": "🍋",
    "플로럴": "🌸",
    "우디": "🌲",
    "바닐라": "🍮",
    "머스크": "🕊️",
}

if recommend_btn:
    payload = {
        "mood": mood,
        "purpose": purpose,
        "weather": weather,
    }

    try:
        with st.spinner("향기를 조합하는 중..."):
            time.sleep(5)
            response = requests.post(FASTAPI_URL, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()

        note = data.get("note", "")
        effect = data.get("effect", "")
        emoji = NOTE_EMOJI.get(note, "🌿")

        st.divider()

        st.markdown('<div class="result-card">', unsafe_allow_html=True)

        st.markdown('<div class="result-label">✨ 향기 추천 결과</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="note-badge">{emoji} {note}</div>',
            unsafe_allow_html=True,
        )

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        st.markdown('<div class="result-label">💜 심리적 효과</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-value">{effect}</div>', unsafe_allow_html=True)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        st.markdown(
            f'<div style="font-size:0.82rem; color:#b090c0; text-align:right;">'
            f'기분: {mood} &nbsp;|&nbsp; 목적: {purpose} &nbsp;|&nbsp; 날씨: {weather}'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.markdown('</div>', unsafe_allow_html=True)

    except requests.exceptions.ConnectionError:
        st.markdown(
            '<div class="error-box">⚠️ FastAPI 서버에 연결할 수 없습니다.<br>'
            'FastAPI 서버(포트 8000)가 실행 중인지 확인해주세요.</div>',
            unsafe_allow_html=True,
        )
    except requests.exceptions.Timeout:
        st.markdown(
            '<div class="error-box">⏱️ 요청 시간이 초과되었습니다. 잠시 후 다시 시도해주세요.</div>',
            unsafe_allow_html=True,
        )
    except Exception as e:
        st.markdown(
            f'<div class="error-box">❌ 오류가 발생했습니다: {e}</div>',
            unsafe_allow_html=True,
        )