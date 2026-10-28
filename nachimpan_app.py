# ================================================================================
# [Module 1.00.00] 시스템 환경 및 전역 테마 엔진 (System & Theming Engine)
# ================================================================================

# ------------------------------------------------------------------------------
# 1.01.00 | 라이브러리 로드 및 기본 페이지 설정
# ------------------------------------------------------------------------------

# 1.01.01 | 필수 및 서드파티 라이브러리 임포트
import os
import random
import json
import base64
import requests
import re
import zlib
from datetime import date
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

# 1.01.02 | Streamlit 기본 페이지 및 레이아웃 설정
st.set_page_config(
    page_title="나침반 — 나의 삶을 바라보는 산책로",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ------------------------------------------------------------------------------
# 1.02.00 | 전역 통합 테마 디자인 시스템 CSS
# ------------------------------------------------------------------------------


# 1.02.01 | 전역 스크롤 안정화 및 상단 시스템 헤더 다크 일체화
st.markdown("""
<style>
/* Streamlit 실제 스크롤 컨테이너의 스크롤 안정화 */
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.stMain {
    overflow-y: scroll !important;
    scrollbar-gutter: stable;
}

/* Streamlit 상단 헤더: 불투명한 딥 네이비 배경 */
header[data-testid="stHeader"] {
    display: flex !important;
    background: #0b1120 !important;
    background-color: #0b1120 !important;
    opacity: 1 !important;
    -webkit-backdrop-filter: none !important;
    backdrop-filter: none !important;
    height: 2.8rem !important;
    border-bottom: 1px solid #334155 !important;
}

/* 헤더 내부 도구 영역에도 배경 효과가 남지 않도록 처리 */
header[data-testid="stHeader"] [data-testid="stToolbar"] {
    background: #0b1120 !important;
    background-color: #0b1120 !important;
    opacity: 1 !important;
    -webkit-backdrop-filter: none !important;
    backdrop-filter: none !important;
}

/* 헤더 내부 아이콘과 버튼 색상 유지 */
header[data-testid="stHeader"] * {
    color: #94a3b8 !important;
}

header[data-testid="stHeader"] button:hover {
    color: #f8fafc !important;
}

/* 메인 콘텐츠 상단 여백 */
div[data-testid="stMainBlockContainer"] {
    padding-top: 0.8rem !important;
}

/* 하단 Streamlit 푸터 숨기기 */
footer {
    visibility: hidden !important;
}
</style>
""", unsafe_allow_html=True)

# 1.02.02 | 전역 색상 디자인 토큰 및 17px 가독성 폰트 설정
st.markdown("""
<style>
:root {
    color-scheme: light dark;
    --nc-bg: #0b1120;
    --nc-sidebar-bg: #0f172a;
    --nc-text: #f8fafc;
    --nc-subtext: #94a3b8;
    --nc-border: #334155;
    --nc-card-bg: #151e2f;
    --nc-hero-bg: radial-gradient(circle at top, #1e293b 0%, #0f172a 75%);
    --nc-primary: #ea580c;
    --nc-primary-hover: #c2410c;
    --nc-accent-gold: #f59e0b;
    --nc-quad-bg: #172033;
    
    --nc-panel-income: #163b35;
    --nc-panel-income-border: #2f806d;
    --nc-panel-expense: #442a2d;
    --nc-panel-expense-border: #a34c56;
    --nc-panel-asset: #183653;
    --nc-panel-asset-border: #3b82b5;
    --nc-panel-debt: #44351d;
    --nc-panel-debt-border: #a8792d;
    --nc-panel-retire: #34264a;
    --nc-panel-retire-border: #8761b3;
}

.stApp {
    background-color: var(--nc-bg) !important;
    color: var(--nc-text) !important;
}

.block-container {
    padding-top: 2.8rem !important;
    padding-bottom: 2rem;
    max-width: 1180px;
}
.stApp, .stApp p, .stApp label, .stApp [data-testid="stMarkdownContainer"] {
    font-size: 17px !important;
    color: var(--nc-text);
}
/* 간편 새로고침 버튼: 내용 크기만 사용하고 오른쪽 정렬 */
.st-key-compass_refresh_area {
    display: flex !important;
    justify-content: flex-end !important;
    align-items: center !important;
    margin: 0 0 4px 0 !important;
}

.st-key-compass_quick_refresh {
    width: auto !important;
    flex: 0 0 auto !important;
}

.st-key-compass_quick_refresh button {
    width: 42px !important;
    min-width: 42px !important;
    max-width: 42px !important;
    height: 36px !important;
    min-height: 36px !important;
    padding: 0 !important;
    margin: 0 !important;
    border-radius: 8px !important;
    font-size: 21px !important;
    line-height: 1 !important;
}

/* 앱 내부 헤더와 도구 영역의 반투명·블러 효과 제거 시도 */
header[data-testid="stHeader"],
header[data-testid="stHeader"] [data-testid="stToolbar"] {
    background: #0b1120 !important;
    background-color: #0b1120 !important;
    opacity: 1 !important;
    -webkit-backdrop-filter: none !important;
    backdrop-filter: none !important;
    box-shadow: none !important;
}
</style>
""", unsafe_allow_html=True)

# 1.02.03 | 패널 및 위젯 (pills, 입력창, 버튼, 사이드바) 스타일링
st.markdown("""
<style>
.soft-card {
    background: var(--nc-card-bg);
    border: 1px solid var(--nc-border);
    border-radius: 14px;
    padding: 18px 20px;
    margin: 10px 0;
    color: var(--nc-text);
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.st-key-job-panel { 
    background: rgba(30, 41, 59, 0.45) !important; 
    border: 1.5px solid #475569 !important; 
    border-radius: 12px; 
    padding: 20px 22px !important;
}
.st-key-job-panel * { color: var(--nc-text) !important; }

.st-key-income-panel { background: var(--nc-panel-income) !important; border: 1px solid var(--nc-panel-income-border) !important; border-radius: 12px; }
.st-key-expense-panel { background: var(--nc-panel-expense) !important; border: 1px solid var(--nc-panel-expense-border) !important; border-radius: 12px; }
.st-key-asset-panel { background: var(--nc-panel-asset) !important; border: 1px solid var(--nc-panel-asset-border) !important; border-radius: 12px; }
.st-key-debt-panel { background: var(--nc-panel-debt) !important; border: 1px solid var(--nc-panel-debt-border) !important; border-radius: 12px; }
.st-key-retirement-panel { background: var(--nc-panel-retire) !important; border: 1px solid var(--nc-panel-retire-border) !important; border-radius: 12px; }

.st-key-income-panel *, .st-key-expense-panel *, .st-key-asset-panel *,
.st-key-debt-panel *, .st-key-retirement-panel * {
    color: var(--nc-text) !important;
}

[data-testid="stMetricLabel"] *, [data-testid="stMetricLabel"] { color: var(--nc-subtext) !important; font-size: 15px !important; font-weight: 600 !important; }
[data-testid="stMetricValue"] *, [data-testid="stMetricValue"] { color: var(--nc-text) !important; font-weight: 800 !important; font-size: 26px !important; }

button[kind="primary"], .stApp [data-testid="stFormSubmitButton"] button[kind="primary"] {
    background-color: var(--nc-primary) !important;
    border-color: var(--nc-primary) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 17px !important;
    border-radius: 8px !important;
    padding: 10px !important;
}

[data-testid="stSidebar"] { background-color: var(--nc-sidebar-bg) !important; border-right: 1px solid var(--nc-border) !important; }
[data-testid="stSidebar"] * { color: var(--nc-text) !important; }

.stApp input, .stApp textarea {
    background-color: var(--nc-card-bg) !important;
    color: var(--nc-text) !important;
    border-color: var(--nc-border) !important;
    font-size: 17px !important;
    padding: 10px 12px !important;
}

input::placeholder, textarea::placeholder,
.stApp input::placeholder, .stApp textarea::placeholder {
    color: #94a3b8 !important;
    -webkit-text-fill-color: #94a3b8 !important;
    opacity: 1 !important;
    font-size: 15px !important;
}

div[data-testid="stButtonGroup"],
div[data-testid="stPills"],
div[data-testid="stSegmentedControl"] {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 8px !important;
    overflow-x: visible !important;
}

div[data-testid="stButtonGroup"] button,
div[data-testid="stPills"] button,
div[data-testid="stSegmentedControl"] button {
    background-color: #1E293B !important;
    background: #1E293B !important;
    color: #CBD5E1 !important;
    border: 1px solid #334155 !important;
    font-size: 15.5px !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    padding: 9px 15px !important;
    margin: 0 !important;
    box-shadow: none !important;
}

div[data-testid="stButtonGroup"] button:hover,
div[data-testid="stPills"] button:hover {
    background-color: #334155 !important;
    color: #F8FAFC !important;
}

div[data-testid="stButtonGroup"] button[aria-checked="true"],
div[data-testid="stButtonGroup"] button[aria-selected="true"],
div[data-testid="stPills"] button[aria-checked="true"],
div[data-testid="stPills"] button[aria-selected="true"] {
    background-color: #EA580C !important;
    background: linear-gradient(135deg, #EA580C 0%, #C2410C 100%) !important;
    color: #FFFFFF !important;
    border-color: #EA580C !important;
    font-weight: 800 !important;
    box-shadow: 0 2px 8px rgba(234, 88, 12, 0.35) !important;
}

div[data-testid="stNumberInput"] button { display: none !important; }
div[data-testid="stNumberInput"] input { padding-right: 12px !important; }

div[data-testid="stForm"]:has(input[id*="start_person"]) {
    border: none !important;
    padding: 0 !important;
    background: transparent !important;
}

input[id*="start_person"] {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    border: 1.5px solid #94A3B8 !important;
    border-radius: 8px !important;
    text-align: center !important;
    font-size: 16px !important;
    height: 44px !important;
}

div[data-testid="stForm"]:has(input[id*="start_person"]) button {
    height: 44px !important;
    font-size: 17px !important;
    font-weight: 800 !important;
    border-radius: 8px !important;
    padding: 0 10px !important;
}

.stApp button:not([kind="primary"]) {
    background-color: #1E293B !important;
    color: #F8FAFC !important;
    border: 1.5px solid #475569 !important;
    font-weight: 700 !important;
}

.stApp button:not([kind="primary"]):hover {
    background-color: #EA580C !important;
    border-color: #EA580C !important;
    color: #FFFFFF !important;
}
</style>
""", unsafe_allow_html=True)

# 1.02.04 | 특수 컴포넌트(카카오 옐로우 코드블록 & expander 다크 고대비)
st.markdown("""
<style>
/* st.code 코드블록: 카카오톡 전용 톤다운 웜 옐로우 배색 */
[data-testid="stCodeBlock"] {
    background-color: #e9d362 !important;
    background: #e9d362 !important;
    border: 1.5px solid #bda738 !important;
    border-radius: 12px !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25) !important;
}

[data-testid="stCodeBlock"] pre,
[data-testid="stCodeBlock"] code,
.stCode pre,
.stCode code {
    background-color: #e9d362 !important;
    background: #e9d362 !important;
    color: #1a1a1a !important;
    font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Malgun Gothic", sans-serif !important;
    font-weight: 600 !important;
    font-size: 14.5px !important;
    line-height: 1.65 !important;
    white-space: pre-wrap !important;
    word-break: break-word !important;
    overflow-x: hidden !important;
}

[data-testid="stCodeBlock"] button {
    background-color: rgba(26, 26, 26, 0.12) !important;
    border: 1px solid rgba(26, 26, 26, 0.25) !important;
    color: #1a1a1a !important;
    border-radius: 6px !important;
}
[data-testid="stCodeBlock"] button:hover {
    background-color: rgba(26, 26, 26, 0.25) !important;
}
[data-testid="stCodeBlock"] button svg {
    fill: #1a1a1a !important;
}

/* st.expander 헤더 다크 고대비 스타일 (화이트/화이트 박멸) */
[data-testid="stExpander"] {
    background-color: transparent !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
}

[data-testid="stExpander"] details {
    border: none !important;
    background-color: transparent !important;
}

[data-testid="stExpander"] summary {
    background-color: #1E293B !important;
    color: #F8FAFC !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    padding: 12px 16px !important;
}

[data-testid="stExpander"] summary:hover {
    background-color: #334155 !important;
    color: #FFFFFF !important;
}

[data-testid="stExpander"] summary svg {
    fill: #F8FAFC !important;
}

[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
    background-color: rgba(15, 23, 42, 0.6) !important;
    border-top: 1px solid #334155 !important;
    border-radius: 0 0 10px 10px !important;
    padding: 16px !important;
}
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# 1.03.00 | 공식 통계 벤치마크 및 전역 상수 (NTA 데이터셋)
# ------------------------------------------------------------------------------

# 1.03.01 | 국민이전계정(NTA) 생애주기 벤치마크 데이터 및 공식 URL
LIFECYCLE_BENCHMARK = pd.DataFrame([
    {"age": 20, "labor_income": 45,  "consumption": 130}, 
    {"age": 25, "labor_income": 180, "consumption": 150},
    {"age": 28, "labor_income": 260, "consumption": 170},
    {"age": 35, "labor_income": 360, "consumption": 220},
    {"age": 43, "labor_income": 435, "consumption": 265},
    {"age": 50, "labor_income": 410, "consumption": 280},
    {"age": 55, "labor_income": 330, "consumption": 280},
    {"age": 60, "labor_income": 220, "consumption": 250},
    {"age": 61, "labor_income": 190, "consumption": 240},
    {"age": 65, "labor_income": 120, "consumption": 230}, 
    {"age": 70, "labor_income": 60,  "consumption": 210},
    {"age": 75, "labor_income": 25,  "consumption": 195},
    {"age": 80, "labor_income": 10,  "consumption": 185},
])

OFFICIAL_PDF_URL = "https://mods.go.kr/boardDownload.es?bid=11898&list_no=447028&seq=3#page=7"
OFFICIAL_RELEASE_URL = "https://mods.go.kr/board.es?act=view&bid=11898&list_no=447028&mid=a10301130100"



# ================================================================================
# [Module 2.00.00] 상태 관리 및 재무 유틸리티 엔진 (State & Finance Engine)
# ================================================================================

# ------------------------------------------------------------------------------
# 2.01.00 | 세션 상태 및 진단 동기화(NC-코드) 엔진
# ------------------------------------------------------------------------------

# 2.01.01 | 세션 키 초기화 및 안전 조회 헬퍼 (getv, advanced_mode 기본값 탑재)
if "anonymous_id" not in st.session_state:
    st.session_state.anonymous_id = f"#{random.choice('ABCDE')}-{random.randint(101,999)}"
if "started" not in st.session_state:
    st.session_state.started = False
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "advanced_mode" not in st.session_state:
    st.session_state.advanced_mode = False  # 기본값: 누구나 부담 없는 기본 모드로 시작

def getv(key, default=0):
    val = st.session_state.get(key, default)
    return default if val is None else val
    
# 2.01.02 | 동기화 키 목록 및 압축 인코더 (export_diagnosis_code, advanced_mode 포함)
SYNC_KEYS = [
    "anonymous_id", "person_name", "person_age", "gender", "job_form", "job_spouse_form", "career_stage",
    "income_self", "income_spouse", "income_other", "income_bonus", "income_pension",
    "expense_living", "expense_loan", "expense_other", "retirement_monthly_expenses",
    "asset_cash", "asset_financial", "asset_home", "asset_deposit", "asset_other",
    "debt_home", "debt_other", "retirement_age", "spouse_age", "child_count",
    "child_age", "child_age2", "child_age3", "child_age4", "father_age", "mother_age",
    "marriage_plan", "child_plan", "housing_plan", "sibling_items", "advanced_mode"
]

def export_diagnosis_code():
    data = {}
    for k in SYNC_KEYS:
        if k in st.session_state:
            data[k] = st.session_state[k]
    json_bytes = json.dumps(data, ensure_ascii=False).encode('utf-8')
    compressed = zlib.compress(json_bytes, level=9)
    b64 = base64.urlsafe_b64encode(compressed).decode('utf-8')
    return f"NC-{b64}"

# 2.01.03 | NC-코드 정규식 디코더 및 세션 복원기 (import_diagnosis_code)
def import_diagnosis_code(raw_input):
    if not raw_input or not isinstance(raw_input, str):
        return False, "입력된 텍스트가 없습니다."
    
    clean_text = raw_input.strip()
    match = re.search(r"NC-([A-Za-z0-9_\-=]+)", clean_text)
    if not match:
        return False, "유효한 나침반 복원코드(NC-...)를 찾지 못했습니다."
    
    b64_str = match.group(1).strip()
    try:
        missing_padding = len(b64_str) % 4
        if missing_padding:
            b64_str += '=' * (4 - missing_padding)
        compressed = base64.urlsafe_b64decode(b64_str.encode('utf-8'))
        json_bytes = zlib.decompress(compressed)
        data = json.loads(json_bytes.decode('utf-8'))
        
        for k, v in data.items():
            st.session_state[k] = v
        st.session_state.started = True
        return True, f"'{data.get('person_name', '인터뷰이')}'님의 가계부·생애주기 데이터가 완벽히 동기화되었습니다."
    except Exception as e:
        return False, f"데이터 복원 실패: {e}"

# 2.01.04 | 개발용 테스트 사례 및 Google Sheets 저장/불러오기
from datetime import datetime

DEV_CASES = {
    "A. 30대 1인 가구 (여성, 초년생 M자 검증)": {
        "person_name": "테스트 A (여성)",
        "person_age": 32,
        "gender": "🙋‍♀️ 여성",
        "job_form": "직장인",
        "job_spouse_form": "해당 없음",
        "career_stage": "🌱 3년 이하 (초년생)",
        "income_self": 320, "income_spouse": 0,
        "income_other": 0, "income_bonus": 300, "income_pension": 0,
        "expense_living": 150, "expense_loan": 0, "expense_other": 30,
        "retirement_monthly_expenses": 180,
        "asset_cash": 800, "asset_financial": 300,
        "asset_home": 0, "asset_deposit": 3000, "asset_other": 0,
        "debt_home": 0, "debt_other": 200,
        "retirement_age": 60, "spouse_age": 0,
        "child_count": "없음", "child_age": 0, "child_age2": 0,
        "child_age3": 0, "child_age4": 0,
        "father_age": 67, "mother_age": 65,
        "marriage_plan": "1~3년 내 결혼 생각 있음",
        "child_plan": "자녀 계획 있음",
        "housing_plan": "전세·월세 이동 고려",
    },
    "B. 40~50대 부부와 자녀 2명 (남성 가장)": {
        "person_name": "테스트 B (남성)",
        "person_age": 48,
        "gender": "🙋‍♂️ 남성",
        "job_form": "직장인",
        "job_spouse_form": "직장인",
        "career_stage": "🌳 10년 이상 (베테랑)",
        "income_self": 450, "income_spouse": 300,
        "income_other": 30, "income_bonus": 1200, "income_pension": 0,
        "expense_living": 280, "expense_loan": 130, "expense_other": 80,
        "retirement_monthly_expenses": 350,
        "asset_cash": 3000, "asset_financial": 4000,
        "asset_home": 50000, "asset_deposit": 0, "asset_other": 0,
        "debt_home": 18000, "debt_other": 1000,
        "retirement_age": 62, "spouse_age": 46,
        "child_count": "2명", "child_age": 18, "child_age2": 14,
        "child_age3": 0, "child_age4": 0,
        "father_age": 83, "mother_age": 81,
        "marriage_plan": "미정", "child_plan": "미정",
        "housing_plan": "현재 주거 유지",
    },
    "C. 50~60대 부부와 성인 자녀 (여성 워킹맘)": {
        "person_name": "테스트 C (여성)",
        "person_age": 58,
        "gender": "🙋‍♀️ 여성",
        "job_form": "직장인",
        "job_spouse_form": "직장인",
        "career_stage": "🌳 10년 이상 (베테랑)",
        "income_self": 500, "income_spouse": 200,
        "income_other": 50, "income_bonus": 1000, "income_pension": 220,
        "expense_living": 300, "expense_loan": 50, "expense_other": 100,
        "retirement_monthly_expenses": 300,
        "asset_cash": 5000, "asset_financial": 10000,
        "asset_home": 65000, "asset_deposit": 0, "asset_other": 0,
        "debt_home": 5000, "debt_other": 0,
        "retirement_age": 62, "spouse_age": 56,
        "child_count": "2명", "child_age": 28, "child_age2": 25,
        "child_age3": 0, "child_age4": 0,
        "father_age": 93, "mother_age": 91,
        "marriage_plan": "미정", "child_plan": "미정",
        "housing_plan": "현재 주거 유지",
    },
    "D. 70~90대 노년기 부부": {
        "person_name": "테스트 D",
        "person_age": 78,
        "gender": "🙋‍♂️ 남성",
        "job_form": "그외",
        "job_spouse_form": "해당 없음",
        "career_stage": "🌳 10년 이상 (베테랑)",
        "income_self": 0, "income_spouse": 0,
        "income_other": 40, "income_bonus": 0, "income_pension": 220,
        "expense_living": 200, "expense_loan": 0, "expense_other": 40,
        "retirement_monthly_expenses": 220,
        "asset_cash": 4000, "asset_financial": 12000,
        "asset_home": 45000, "asset_deposit": 0, "asset_other": 0,
        "debt_home": 0, "debt_other": 0,
        "retirement_age": 78, "spouse_age": 75,
        "child_count": "2명", "child_age": 50, "child_age2": 47,
        "child_age3": 0, "child_age4": 0,
        "father_age": 0, "mother_age": 0,
        "marriage_plan": "미정", "child_plan": "미정",
        "housing_plan": "현재 주거 유지",
    },
}

def get_test_cases():
    """기본 A~D 사례 + Google Sheets 저장 사례(최신순 정렬) 통합 반환"""
    cases = dict(DEV_CASES)
    try:
        from streamlit_gsheets import GSheetsConnection
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(ttl=0)
        if df is not None and not df.empty:
            saved_dict = {}
            for _, row in df.iloc[::-1].iterrows():
                name = str(row.get("case_name", "")).strip()
                payload = row.get("payload_json", "")
                if name and isinstance(payload, str) and payload.strip():
                    try:
                        saved_dict[f"📁 저장 사례: {name}"] = json.loads(payload)
                    except (ValueError, TypeError):
                        pass
            cases.update(saved_dict)
    except Exception:
        pass
    return cases

def save_test_case(case_name):
    """현재 진단 데이터를 익명 사례로 Google Sheets에 저장"""
    from streamlit_gsheets import GSheetsConnection

    conn = st.connection("gsheets", type=GSheetsConnection)
    try:
        df = conn.read(ttl=0)
        if df is None:
            df = pd.DataFrame()
    except Exception:
        df = pd.DataFrame()

    if df.empty or not {"case_name", "payload_json"}.issubset(df.columns):
        df = pd.DataFrame(columns=["case_name", "updated_at", "payload_json"])

    payload = {
        key: st.session_state[key]
        for key in SYNC_KEYS
        if key in st.session_state and key != "person_name"
    }
    payload["person_name"] = case_name

    df = df[df["case_name"].astype(str) != case_name]
    new_row = pd.DataFrame([{
        "case_name": case_name,
        "updated_at": datetime.now().isoformat(timespec="seconds"),
        "payload_json": json.dumps(payload, ensure_ascii=False, default=str),
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    conn.update(data=df)

# ------------------------------------------------------------------------------
# 2.02.00 | 재무 포맷팅 및 집계 로직
# ------------------------------------------------------------------------------

# 2.02.01 | 금액 및 억 단위 표시 포맷터
def money(value):
    return f"{value:,.0f}만 원"

def fmt_eok(value):
    if abs(value) >= 10000:
        return f"{value / 10000:,.2f}억 원"
    return money(value)

# 2.02.02 | 직업-ESBI 사분면 매핑 함수
def active_quadrant(job):
    mapping = {
        "직장인": "E", "공무원": "E", "근로소득자": "E",
        "자영업": "S", "전문직": "S", "프리랜서": "S",
        "사업가": "B", "사업자": "B", "시스템 사업": "B",
        "투자자": "I", "임대소득자": "I", "연금·배당 중심": "I",
    }
    for word, code in mapping.items():
        if word in str(job):
            return code
    return ""

# 2.02.03 | 가계 종합 재무 집계 엔진
def current_financial_summary():
    regular_income = sum(float(getv(k, 0)) for k in ["income_self", "income_spouse", "income_other"])
    annual_bonus = float(getv("income_bonus", 0))
    
    annual_total_income = (regular_income * 12.0) + annual_bonus
    monthly_effective_income = annual_total_income / 12.0
    
    expenses = sum(float(getv(k, 0)) for k in ["expense_living", "expense_loan", "expense_other"])
    annual_total_expenses = expenses * 12.0
    
    monthly_regular_surplus = regular_income - expenses
    annual_net_surplus = annual_total_income - annual_total_expenses
    monthly_effective_surplus = annual_net_surplus / 12.0
    
    assets = sum(float(getv(k, 0)) for k in ["asset_cash", "asset_financial", "asset_home", "asset_deposit", "asset_other"])
    debts = sum(float(getv(k, 0)) for k in ["debt_home", "debt_other"])
    net_worth = assets - debts
    
    return {
        "regular_income": regular_income,
        "annual_bonus": annual_bonus,
        "annual_total_income": annual_total_income,
        "monthly_effective_income": monthly_effective_income,
        "income": regular_income,
        "expenses": expenses,
        "annual_total_expenses": annual_total_expenses,
        "surplus": monthly_regular_surplus,
        "monthly_regular_surplus": monthly_regular_surplus,
        "annual_net_surplus": annual_net_surplus,
        "monthly_effective_surplus": monthly_effective_surplus,
        "assets": assets,
        "debts": debts,
        "net_worth": net_worth
    }



# ================================================================================
# [Module 3.00.00] 외부 AI 연동 서비스 (Gemini API Pipeline)
# ================================================================================

# ------------------------------------------------------------------------------
# 3.01.00 | Gemini 초고속 자율 매칭 엔진
# ------------------------------------------------------------------------------

# 3.01.01 | API 키 정제 및 텍스트 생성 파이프라인 (call_gemini_text)
def call_gemini_text(prompt_text):
    raw_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("Gemini_API_KEY")
    if not raw_key:
        try:
            raw_key = st.secrets.get("GEMINI_API_KEY", "") or st.secrets.get("Gemini_API_KEY", "")
        except Exception:
            raw_key = ""
            
    if not raw_key:
        return "", "Streamlit Secrets에서 GEMINI_API_KEY를 찾지 못했습니다. 앱 대시보드의 Secrets 설정을 확인해 주세요."

    api_key = str(raw_key).strip().strip("'").strip('"')

    payload = {
        "contents": [{"parts": [{"text": prompt_text}]}],
        "generationConfig": {"maxOutputTokens": 8192, "temperature": 0.45},
    }

    active_endpoints = []
    discovery_error = ""
    for ver in ["v1beta", "v1"]:
        try:
            res = requests.get(
                f"https://generativelanguage.googleapis.com/{ver}/models?key={api_key}",
                timeout=6,
            )
            if res.status_code == 200:
                for m in res.json().get("models", []):
                    if "generateContent" in m.get("supportedGenerationMethods", []):
                        m_full_name = m.get("name", "")
                        if "flash" in m_full_name and "exp" not in m_full_name and "preview" not in m_full_name:
                            active_endpoints.append((ver, m_full_name))
            else:
                discovery_error = f"[{ver} 목록 조회 {res.status_code}]: {res.text[:120]}"
        except Exception as exc:
            discovery_error = f"통신 지연: {exc}"

    active_endpoints.sort(key=lambda item: (
        0 if "1.5-flash" in item[1] else
        1 if "2.0-flash" in item[1] else 2
    ))

    if not active_endpoints:
        active_endpoints = [
            ("v1beta", "models/gemini-1.5-flash"),
            ("v1beta", "models/gemini-2.0-flash"),
            ("v1", "models/gemini-1.5-flash")
        ]

    last_error = ""
    for api_version, model_full_path in active_endpoints:
        try:
            url = f"https://generativelanguage.googleapis.com/{api_version}/{model_full_path}:generateContent?key={api_key}"
            response = requests.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=25,
            )
            if response.status_code == 200:
                result = response.json()
                parts = result.get("candidates", [{}])[0].get("content", {}).get("parts", [])
                text_parts = [p.get("text", "") for p in parts if p.get("text")]
                if text_parts:
                    return "".join(text_parts).strip(), ""
            else:
                last_error = f"[{model_full_path} {response.status_code}]: {response.text[:140]}"
        except Exception as exc:
            last_error = f"[{model_full_path} 요청 오류]: {exc}"

    final_err_msg = last_error or discovery_error or "구글 Gemini 서버 응답 없음"
    return "", f"Gemini 연결 실패: {final_err_msg}"



# ================================================================================
# [Module 4.00.00] 사이드바 및 진입 표지 (Sidebar & Cover Entry)
# ================================================================================

# ------------------------------------------------------------------------------
# 4.01.00 | 사이드바 프로필 요약 및 복원
# ------------------------------------------------------------------------------

# 4.01.01 | 사이드바 컴포넌트 렌더링 (사이드바 고급 모드 토글 버튼 탑재)
with st.sidebar:
    st.markdown(f"""
<div style="background: rgba(30, 41, 59, 0.4); border: 1px solid #334155; border-radius: 10px; padding: 12px 14px; text-align: center; margin-bottom: 20px;">
<div style="font-size: 11.5px; color: #94a3b8; font-weight: 600; letter-spacing: 0.04em;">익명 진단 고유번호</div>
<div style="font-size: 20px; font-weight: 750; color: #cbd5e1; letter-spacing: 1px; margin-top: 3px;">{st.session_state.anonymous_id}</div>
</div>
""", unsafe_allow_html=True)

    if st.session_state.started:
        st.markdown("#### 나의 기본 정보")
        st.markdown(f"**나의 이름/별칭:** {st.session_state.get('person_name','')}")
        st.markdown(f"**나의 나이:** {st.session_state.get('person_age','')}세")

        q_self = active_quadrant(st.session_state.get("job_form", ""))
        q_spouse = active_quadrant(st.session_state.get("job_spouse_form", ""))
        types_desc = []
        if q_self: types_desc.append(f"나({q_self})")
        if q_spouse: types_desc.append(f"배우자({q_spouse})")
        dual_income_str = " + ".join(types_desc) if types_desc else "아직 미선택"
        st.markdown(f"**우리집 소득 형태:** {dual_income_str}")

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    with st.expander("📥 카톡 리포트 불러오기"):
        st.markdown("<div style='font-size: 13px; color: #CBD5E1; margin-bottom: 6px;'>전달받은 <b>리포트 전문</b> 또는 <b>NC-코드</b>를 붙여넣으세요.</div>", unsafe_allow_html=True)
        pasted_code_sb = st.text_area("카톡 내용 붙여넣기", placeholder="NC-코드를 붙여넣으세요", height=90, key="sb_pasted_code", label_visibility="collapsed")
        if st.button("🔄 데이터 동기화", type="primary", use_container_width=True, key="sb_btn_sync"):
            ok, msg = import_diagnosis_code(pasted_code_sb)
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    
    # [사이드바 모드 전환 버튼: 심플한 정식 이름표 장착]
    is_currently_adv = st.session_state.get("advanced_mode", False)
    mode_btn_label = "🌿 기본 모드로 전환" if is_currently_adv else "🧭 고급 모드로 전환"
    if st.button(mode_btn_label, key="sidebar_mode_toggle_btn", use_container_width=True):
        st.session_state.advanced_mode = not is_currently_adv
        st.rerun()

    st.caption("※ 나침반은 외부 서버에 저장되지 않는 일회성 안전 세션입니다.")

# 4.01.02 | 개발용 테스트 메뉴
_dev_enabled = (
    st.secrets.get("DEV_MODE", False)
    or st.query_params.get("dev") == "1"
)

if _dev_enabled:
    with st.sidebar:
        st.divider()
        st.markdown("### 🧪 개발용 테스트")
        
        if st.button("↻ 개발용 새로고침", key="dev_menu_refresh", use_container_width=True):
            st.rerun()

        st.caption("테스트 사례의 금액은 기능 검증을 위한 예시입니다.")

        _cases = get_test_cases()
        _all_names = list(_cases.keys())

        # [실명 박멸] 가명 '혜림'으로 검색 placeholder 교체
        _search_kw = st.text_input(
            "🔍 사례 검색 (이름 또는 키워드)",
            placeholder="예: 여성, 혜림, 30대...",
            key="dev_search_keyword",
            label_visibility="visible"
        ).strip()

        if _search_kw:
            _filtered_names = [n for n in _all_names if _search_kw.lower() in n.lower()]
            if not _filtered_names:
                st.caption("검색 결과가 없습니다.")
                _filtered_names = _all_names
        else:
            _filtered_names = _all_names

        _selected_case = st.selectbox(
            f"불러올 사례 (총 {len(_all_names)}개 중 {len(_filtered_names)}개)",
            _filtered_names,
            key="dev_case_selector",
        )

        if st.button("📂 사례 불러오기", use_container_width=True):
            _data = dict(_cases[_selected_case])

            for k, v in _data.items():
                st.session_state[k] = v

            if "gender" in _data:
                st.session_state["pills_gender"] = _data["gender"]
            if "job_form" in _data:
                st.session_state["pills_job_self"] = _data["job_form"]
            if "career_stage" in _data:
                st.session_state["pills_career_stage"] = _data["career_stage"]
            if "job_spouse_form" in _data:
                st.session_state["pills_job_spouse"] = _data["job_spouse_form"]

            st.session_state["started"] = True
            st.session_state["answers"] = {}
            st.session_state["anonymous_id"] = f"#DEV-{random.randint(100, 999)}"
            st.session_state["active_navigation_default"] = "우리집\n가계부"
            st.session_state["active_navigation_key"] = "main_navigation"
            st.session_state["_pending_nav"] = "우리집 가계부"
            st.session_state["_dev_loaded_notice"] = _selected_case
            st.rerun()

        st.divider()
        st.markdown("#### 💾 현재 사례 저장")
        _save_name = st.text_input(
            "저장할 별칭",
            placeholder="예: 인터뷰 사례 01",
            key="dev_save_case_name",
        )

        if st.button(
            "☁️ Google Sheets에 저장",
            use_container_width=True,
            disabled=not st.session_state.get("started", False)
            or not _save_name.strip(),
        ):
            try:
                save_test_case(_save_name.strip())
                st.success(f"'{_save_name.strip()}' 사례를 저장했습니다.")
                st.rerun()
            except Exception as e:
                st.error(
                    "저장에 실패했습니다. Google Sheets 연결과 "
                    f"권한을 확인해 주세요. ({type(e).__name__}: {e})"
                )

# ------------------------------------------------------------------------------
# 4.02.00 | 첫 진입 표지 및 인라인 시작 바
# ------------------------------------------------------------------------------

# 4.02.01 | 커버 이미지 렌더링 및 2줄 3칸 슬림 폼 제어
cover_file_path = None
possible_covers = [
    "cover.png", "cover.jpg", "cover.jpeg",
    "나침반_표지_배경.png", "나침판_표지_배경.png"
]

for c_name in possible_covers:
    c_path = os.path.join(os.path.dirname(__file__), c_name)
    if os.path.exists(c_path):
        cover_file_path = c_path
        break

if not st.session_state.started:
    col_left, col_center, col_right = st.columns([1, 1.8, 1])
    
    with col_center:
        if cover_file_path:
            st.image(cover_file_path, use_container_width=True)
        else:
            st.markdown("""
<div style="background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%); border-radius: 18px; padding: 60px 20px; text-align: center; border: 1px solid #334155;">
<div style="font-size: 40px; margin-bottom: 10px;">🧭</div>
<h1 style="color: #FFFFFF; font-size: 32px; font-weight: 850; margin: 0 0 10px 0;">나 침 반</h1>
<div style="color: #94A3B8; font-size: 15px;">당신의 삶을 위한 질문과 시간의 산책로</div>
</div>
""", unsafe_allow_html=True)

        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
        
        with st.form("start_inline_form", clear_on_submit=False):
            in_col1, in_col2, in_col3 = st.columns([2.0, 1.1, 1.1])
            
            with in_col1:
                st.markdown("<div style='font-size: 18px; font-weight: 800; color: #F8FAFC; margin-bottom: 6px; text-align: center;'>이름(별칭)</div>", unsafe_allow_html=True)
                name = st.text_input("이름(별칭)", placeholder="이름 또는 별칭", key="start_person_name", label_visibility="collapsed")
                
            with in_col2:
                st.markdown("<div style='font-size: 18px; font-weight: 800; color: #F8FAFC; margin-bottom: 6px; text-align: center;'>나이</div>", unsafe_allow_html=True)
                age_text = st.text_input("나이", placeholder="예: 38", key="start_person_age_text", max_chars=3, label_visibility="collapsed")
                
            with in_col3:
                st.markdown("<div style='font-size: 18px; font-weight: 800; margin-bottom: 6px; text-align: center;'>&nbsp;</div>", unsafe_allow_html=True)
                submitted = st.form_submit_button("시작", use_container_width=True, type="primary")

            try:
                age = int(age_text) if age_text.strip() else None
                if age is not None and not (1 <= age <= 120):
                    age = None
            except ValueError:
                age = None

            if submitted:
                if not name.strip() or age is None:
                    st.warning("이름(별칭)과 나이를 올바르게 입력해 주세요.")
                else:
                    st.session_state.person_name = name.strip()
                    st.session_state.person_age = int(age)
                    st.session_state.started = True
                    st.rerun()
            
    st.stop()



# ================================================================================
# [Module 5.00.00] 메인 네비게이션 헤더 (Main Navigation)
# ================================================================================

# ------------------------------------------------------------------------------
# 5.01.00 | 나침반 전용 헤더 및 상단 4대 탭 네비게이터
# ------------------------------------------------------------------------------

# 5.01.01 | 사이드바 새로고침 기능

# 5.01.02 | 네비게이션 옵션 및 streamlit_option_menu 렌더링
_pending_nav = st.session_state.pop("_pending_nav", None)

nav_options = [
    "우리집\n가계부",
    "삶과\n생계수단",
    "인생의\n사계절",
    "AI\n시선"
]

_nav_targets = {
    "우리집 가계부": nav_options[0],
    "삶과 생계수단": nav_options[1],
    "인생의 사계절": nav_options[2],
    "AI 시선": nav_options[3]
}

if "active_navigation_key" not in st.session_state:
    st.session_state.active_navigation_key = "main_navigation"

if _pending_nav in _nav_targets:
    st.session_state.active_navigation_key = (
        "main_navigation_"
        + str(list(_nav_targets.keys()).index(_pending_nav))
    )
    st.session_state.active_navigation_default = _nav_targets[_pending_nav]

_nav_widget_key = st.session_state.active_navigation_key
_nav_default = st.session_state.get(
    "active_navigation_default",
    nav_options[0]
)
_nav_index = (
    nav_options.index(_nav_default)
    if _nav_default in nav_options
    else 0
)

selected = option_menu(
    menu_title=None,
    options=nav_options,
    icons=["", "", "", ""],
    default_index=_nav_index,
    orientation="horizontal",
    key=_nav_widget_key,
    styles={
        "container": {
            "padding": "16px 6px 8px 6px",
            "background-color": "#0F172A",
            "border": "none",
            "border-radius": "0px",
            "margin": "0px",
            "width": "100%"
        },
        "icon": {"display": "none"},
        "nav-link": {
            "font-size": "15px",
            "white-space": "pre-line",
            "line-height": "1.25",
            "text-align": "center",
            "margin": "0px 3px",
            "padding": "8px 4px",
            "color": "#CBD5E1",
            "--hover-color": "#1E293B",
            "border-radius": "8px",
            "min-height": "48px",
            "flex": "1"
        },
        "nav-link-selected": {
            "background-color": "#EA580C",
            "color": "#FFFFFF",
            "font-weight": "800",
            "box-shadow": "none"
        }
    }
)

selected_page = {
    "우리집\n가계부": "우리집 가계부",
    "삶과\n생계수단": "삶과 생계수단",
    "인생의\n사계절": "인생의 사계절",
    "AI\n시선": "AI 시선"
}.get(selected, selected)



# ================================================================================
# [Module 6.00.00] 메인 뷰 페이지 (Main View Tabs: 기본 3분 산책 vs 고급 정밀 모드)
# ================================================================================

# ==============================================================================
# 6.01.00 | Tab 1 — 우리집 가계부
# ==============================================================================
if selected_page == "우리집 가계부":
    is_adv = st.session_state.get("advanced_mode", False)
    
    if not is_adv:
        # [기본 모드] 중복 제목 없이 바로 본론으로 진입하는 3분 일상 수지 산책
        st.caption("가벼운 3분 산책: 가장 핵심적인 우리 집의 한 달 현금흐름 밸런스만 살펴봅니다.")
        
        with st.form("basic_finance_form"):
            with st.container(border=True, key="income-panel"):
                st.markdown("### 들어오고 나가는 돈 (월, 만원)")
                b_in_col, b_ex_col = st.columns(2)
                with b_in_col:
                    basic_income = st.number_input(
                        "나의 월 실수령액 (월급·기본소득)",
                        min_value=0, value=int(st.session_state.get("income_self", 0) or 0), step=10,
                        placeholder="월 실수령액"
                    )
                with b_ex_col:
                    basic_expense = st.number_input(
                        "우리집 기본 생활비",
                        min_value=0, value=int(st.session_state.get("expense_living", 0) or 0), step=10,
                        placeholder="월 생활비"
                    )
            save_basic = st.form_submit_button("입력 내용 반영하기", use_container_width=True, type="primary")

        if save_basic:
            st.session_state["income_self"] = basic_income
            st.session_state["expense_living"] = basic_expense
            st.rerun()

        surplus_val = int(st.session_state.get("income_self", 0) or 0) - int(st.session_state.get("expense_living", 0) or 0)
        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
        st.markdown("### 우리집 월 현금흐름 밸런스")
        b_c1, b_c2, b_c3 = st.columns(3)
        b_c1.metric("월 실수령 소득", money(st.session_state.get("income_self", 0) or 0))
        b_c2.metric("월 기본 생활비", money(st.session_state.get("expense_living", 0) or 0))
        b_c3.metric("월 저축여력 (잉여)", money(surplus_val), delta=f"{'+' if surplus_val >= 0 else ''}{money(surplus_val)}")

        _, next_col = st.columns([5, 1])
        with next_col:
            if st.button("다음 →", key="basic_fin_next", use_container_width=True, type="primary"):
                st.session_state["_pending_nav"] = "삶과 생계수단"
                st.rerun()

    else:
        # [고급 모드] 모든 마이크로 모듈(6.01.01 ~ 6.01.07) 완전 탑재
        with st.form("finance_form"):
            # 6.01.01 | ⓪ 우리집 소득 성격 및 재무 입력 폼
            with st.container(border=True, key="job-panel"):
                st.markdown("### ⓪ 우리집 소득 성격")
                gender_options = ["🙋‍♂️ 남성", "🙋‍♀️ 여성"]
                prev_gender = st.session_state.get("gender", "🙋‍♂️ 남성")
                if prev_gender not in gender_options: prev_gender = "🙋‍♂️ 남성"
                    
                st.markdown("<div style='font-size: 17px; font-weight: 700; color: #F8FAFC; margin-bottom: 6px;'>나의 성별은?</div>", unsafe_allow_html=True)
                gender_selected = st.pills("나의 성별은?", gender_options, default=prev_gender, key="pills_gender", label_visibility="collapsed")
                st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

                job_options = ["직장인", "자영업", "전문직", "사업가", "투자자", "임대소득자", "전업주부", "그외"]
                job_spouse_options = ["해당 없음", "직장인", "자영업", "전문직", "사업가", "투자자", "임대소득자", "전업주부", "그외"]
                career_options = ["🌱 3년 이하 (초년생)", "🌿 4~9년 (성장기)", "🌳 10년 이상 (베테랑)"]
                
                prev_job = st.session_state.get("job_form", "직장인")
                if prev_job not in job_options: prev_job = "직장인"
                prev_spouse_job = st.session_state.get("job_spouse_form", "해당 없음")
                if prev_spouse_job not in job_spouse_options: prev_spouse_job = "해당 없음"
                prev_career = st.session_state.get("career_stage", "🌱 3년 이하 (초년생)")
                if prev_career not in career_options: prev_career = "🌱 3년 이하 (초년생)"
                
                st.markdown("<div style='font-size: 17px; font-weight: 700; color: #F8FAFC; margin-bottom: 6px;'>나의 직업은?</div>", unsafe_allow_html=True)
                job_selected = st.pills("나의 직업은?", job_options, default=prev_job, key="pills_job_self", label_visibility="collapsed")
                st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
                
                st.markdown("<div style='font-size: 17px; font-weight: 700; color: #F8FAFC; margin-bottom: 6px;'>나의 현업 경력(연차)은?</div>", unsafe_allow_html=True)
                career_selected = st.pills("나의 현업 경력(연차)은?", career_options, default=prev_career, key="pills_career_stage", label_visibility="collapsed")
                st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
                
                st.markdown("<div style='font-size: 17px; font-weight: 700; color: #F8FAFC; margin-bottom: 6px;'>배우자의 직업은? (선택)</div>", unsafe_allow_html=True)
                job_spouse_selected = st.pills("배우자의 직업은?", job_spouse_options, default=prev_spouse_job, key="pills_job_spouse", label_visibility="collapsed")

            st.write("")

            # 6.01.02 | ① 들어오는 돈 vs ② 나가는 돈 입력 패널
            income_col, expense_col = st.columns(2)
            with income_col:
                with st.container(border=True, key="income-panel"):
                    st.markdown("### ① 들어오는 돈 (만원)")
                    income_self = st.number_input("나의 월 실수령액 (월급·기본소득)", min_value=0, value=st.session_state.get("income_self"), step=10, placeholder="월 금액")
                    income_spouse = st.number_input("배우자 월 실수령액", min_value=0, value=st.session_state.get("income_spouse"), step=10, placeholder="월 금액")
                    income_other = st.number_input("그 밖의 월 정기소득 (임대·부업 등)", min_value=0, value=st.session_state.get("income_other"), step=10, placeholder="월 금액")
                    income_bonus = st.number_input("연간 비정기 소득 (상여금·성과급·연말수입)", min_value=0, value=st.session_state.get("income_bonus"), step=100, placeholder="1년 합계 금액 (없으면 빈칸)")
            with expense_col:
                with st.container(border=True, key="expense-panel"):
                    st.markdown("### ② 나가는 돈 (월, 만원)")
                    expense_living = st.number_input("기본 생활비 (식비·관리비·통신비·가족생활)", min_value=0, value=st.session_state.get("expense_living"), step=10, placeholder="월 생활 유지비")
                    expense_loan = st.number_input("대출 원리금 상환액 (원금+이자 합계)", min_value=0, value=st.session_state.get("expense_loan"), step=10, placeholder="은행 납입 합계")
                    expense_other = st.number_input("그 밖의 월평균 지출 (연간 여행·경조사·세금÷12)", min_value=0, value=st.session_state.get("expense_other"), step=10, placeholder="비정기 지출 월평균")

            # 6.01.03 | ③ 가지고 있는 것 vs ④ 갚아야 할 돈 입력 패널
            asset_col, debt_col = st.columns(2)
            with asset_col:
                with st.container(border=True, key="asset-panel"):
                    st.markdown("### ③ 가지고 있는 것 (시세, 만원)")
                    asset_cash = st.number_input("현금·예적금", min_value=0, value=st.session_state.get("asset_cash"), step=100, placeholder="금액")
                    asset_financial = st.number_input("주식·채권 등 금융자산", min_value=0, value=st.session_state.get("asset_financial"), step=100, placeholder="금액")
                    asset_home = st.number_input("부동산 시세", min_value=0, value=st.session_state.get("asset_home"), step=100, placeholder="금액")
                    asset_deposit = st.number_input("전세보증금", min_value=0, value=st.session_state.get("asset_deposit"), step=100, placeholder="금액")
                    asset_other = st.number_input("그 밖의 자산 (현금화 가능한 사업체·지분 등)", min_value=0, value=st.session_state.get("asset_other"), step=100, placeholder="금액")
            with debt_col:
                with st.container(border=True, key="debt-panel"):
                    st.markdown("### ④ 갚아야 할 돈 (원금, 만원)")
                    debt_home = st.number_input("주택담보·전세대출 잔액", min_value=0, value=st.session_state.get("debt_home"), step=100, placeholder="금액")
                    debt_other = st.number_input("그 밖의 부채 잔액 (신용·마이너스통장)", min_value=0, value=st.session_state.get("debt_other"), step=100, placeholder="금액")

            # 6.01.04 | 은퇴 후 가정 입력 및 세션 상태 저장
            with st.container(border=True, key="retirement-panel"):
                st.markdown("### 은퇴 후에는? (월, 만원)")
                pension_col, retirement_expense_col = st.columns(2)
                with pension_col:
                    income_pension = st.number_input("은퇴 후 받을 월 연금", min_value=0, value=st.session_state.get("income_pension"), step=10, placeholder="모르면 빈칸으로 두세요")
                with retirement_expense_col:
                    retirement_monthly_expenses = st.number_input("은퇴 후 한 달 생활비", min_value=0, value=int(st.session_state.get("retirement_monthly_expenses", 200) or 0), step=10)

            save_finance = st.form_submit_button("입력 내용 반영하기", use_container_width=True, type="primary")

        if save_finance:
            final_gender = gender_selected if gender_selected else "🙋‍♂️ 남성"
            final_job = job_selected if job_selected else "직장인"
            final_career = career_selected if career_selected else "🌱 3년 이하 (초년생)"
            final_spouse_job = "" if (not job_spouse_selected or job_spouse_selected == "해당 없음") else job_spouse_selected
            
            submitted_values = {
                "gender": final_gender, "job_form": final_job, "career_stage": final_career, "job_spouse_form": final_spouse_job,
                "income_self": income_self, "income_spouse": income_spouse, "income_other": income_other, "income_bonus": income_bonus,
                "income_pension": income_pension, "expense_living": expense_living, "expense_loan": expense_loan, "expense_other": expense_other,
                "retirement_monthly_expenses": retirement_monthly_expenses, "asset_cash": asset_cash, "asset_financial": asset_financial,
                "asset_home": asset_home, "asset_deposit": asset_deposit, "asset_other": asset_other, "debt_home": debt_home, "debt_other": debt_other,
            }
            for k, v in submitted_values.items(): st.session_state[k] = v
            st.session_state["finance_saved_notice"] = True

        # 6.01.05 | 우리집 재무 현황 2x2 ESBI 매트릭스 카드 UI
        q_self = active_quadrant(st.session_state.get("job_form", "직장인"))
        q_spouse = active_quadrant(st.session_state.get("job_spouse_form", ""))
        st.markdown("### 우리집 재무 현황")
        st.markdown("<div id='selected-esbi'></div>", unsafe_allow_html=True)
        if st.session_state.pop("finance_saved_notice", False):
            st.success("입력하신 재무 정보가 반영되었습니다.")
            st.components.v1.html("<script>try { window.parent.document.getElementById('selected-esbi').scrollIntoView({behavior:'smooth',block:'center'}); } catch(e) {}</script>", height=0)

        def get_quad_ui(code, title, desc):
            is_self = (q_self == code)
            is_spouse = (q_spouse == code)
            if is_self and is_spouse: border_style = "border: 2.5px solid #EA580C; outline: 2.5px dashed #38BDF8; outline-offset: -5px; background: rgba(234, 88, 12, 0.16);"
            elif is_self: border_style = "border: 2.5px solid #EA580C; background: rgba(234, 88, 12, 0.14);"
            elif is_spouse: border_style = "border: 2.5px dashed #38BDF8; background: rgba(56, 189, 248, 0.14);"
            else: border_style = "border: 1px solid #334155; background: rgba(15, 23, 42, 0.7);"
            badges = []
            if is_self: badges.append("<span style='background:#EA580C; color:#FFFFFF; font-size:12px; font-weight:800; padding:2px 8px; border-radius:4px;'>나</span>")
            if is_spouse: badges.append("<span style='background:#0284C7; color:#FFFFFF; font-size:12px; font-weight:800; padding:2px 8px; border-radius:4px;'>배우자</span>")
            badge_row = f"<div style='min-height:24px; margin-bottom:4px; display:flex; justify-content:center; gap:6px;'>{' '.join(badges)}</div>" if badges else "<div style='min-height:24px; margin-bottom:4px;'></div>"
            return f'<div style="{border_style} border-radius: 12px; padding: 18px 12px; text-align: center; display: flex; flex-direction: column; justify-content: center; align-items: center; height: 165px; box-sizing: border-box; width: 100%;">{badge_row}<div style="font-size: 28px; font-weight: 850; color: #F8FAFC; line-height: 1.1;">{code}</div><div style="font-size: 17.5px; font-weight: 700; color: #F1F5F9; margin: 4px 0 6px 0;">{title}</div><div style="font-size: 14px; color: #CBD5E1; line-height: 1.4; word-break: keep-all; text-align: center;">{desc}</div></div>'

        card_e = get_quad_ui("E", "직장인", "나의 시간과 돈을 바꿈.<br><span style='color:#F59E0B; font-weight:600;'>(작은 물통)</span>")
        card_s = get_quad_ui("S", "자영업·전문직", "나의 시간과 돈을 바꿈.<br><span style='color:#F59E0B; font-weight:600;'>(큰 물통)</span>")
        card_b = get_quad_ui("B", "사업가", "나의 회사가 돈을 만듦.<br><span style='color:#38BDF8; font-weight:600;'>(파이프라인)</span>")
        card_i = get_quad_ui("I", "투자자·임대소득자", "나의 자산이 돈을 만듦.<br><span style='color:#38BDF8; font-weight:600;'>(파이프라인)</span>")

        st.markdown(f"""
<div style="margin: 16px 0 24px 0;">
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0px; align-items: stretch;">
<div style="display: flex; flex-direction: column; gap: 14px; padding-right: 14px; border-right: 3.5px dashed #475569;">
<div>{card_e}</div><div>{card_s}</div>
</div>
<div style="display: flex; flex-direction: column; gap: 14px; padding-left: 14px;">
<div>{card_b}</div><div>{card_i}</div>
</div></div>
</div>
""", unsafe_allow_html=True)

        # 6.01.06 | 현재 재무 요약 메트릭
        s = current_financial_summary()
        st.markdown("### 현재 재무 요약")
        cols = st.columns(4)
        cols[0].metric("월 정기수입", money(s["regular_income"]))
        cols[1].metric("월 현금지출", money(s["expenses"]))
        bonus_help = f"연간 상여금 {money(s['annual_bonus'])} 반영" if s['annual_bonus'] > 0 else "월 정기수지 기준"
        cols[2].metric("연간 순저축 여력", money(s["annual_net_surplus"]), delta=f"월평균 {money(s['monthly_effective_surplus'])}", help=bonus_help)
        cols[3].metric("순자산", fmt_eok(s["net_worth"]))

        # 6.01.07 | 미래 순자산·연금 궤적 Plotly 차트
        st.markdown("### 미래 순자산·연금 궤적")
        cur_age = int(st.session_state.person_age)
        retire_val = st.session_state.get("retirement_age")
        retire_age = int(retire_val) if retire_val is not None else 65
        retire_age = max(cur_age, min(retire_age, 90))
        start_asset_eok = s["net_worth"] / 10000.0
        base_annual_surplus_eok = s["annual_net_surplus"] / 10000.0
        career_st = st.session_state.get("career_stage", "🌱 3년 이하 (초년생)")
        user_gender = st.session_state.get("gender", "🙋‍♂️ 남성")
        is_female = ("여성" in user_gender)
        m_plan = st.session_state.get("marriage_plan", "미정")
        c_plan = st.session_state.get("child_plan", "미정")
        is_single_young = (int(getv("spouse_age", 0)) == 0 and cur_age < 40)
        life_expectancy = 87 if is_female else 81

        ages_accum = list(range(cur_age, retire_age + 1))
        vals_accum_eok = []
        current_asset = start_asset_eok
        for a in ages_accum:
            vals_accum_eok.append(current_asset)
            if a < 45: growth_step = 0.025 if "초년생" in career_st else 0.018; lifecycle_weight = 1.0 + (growth_step * (a - cur_age))
            elif 45 <= a <= 53: lifecycle_weight = 1.0 + (0.02 * (45 - cur_age)) - 0.15
            else: lifecycle_weight = max(0.65, 1.0 + (0.02 * (45 - cur_age)) - 0.25)
            if is_single_young:
                if m_plan in ["1~3년 내 결혼 생각 있음", "결혼 예정/준비 중"] and (cur_age + 1 <= a <= cur_age + 3): lifecycle_weight *= 0.75
                if is_female and c_plan in ["자녀 계획 있음", "출산 예정/준비 중", "추가 자녀 계획 있음"] and (33 <= a <= 36): lifecycle_weight *= 0.65
            annual_save = base_annual_surplus_eok * max(0.05, lifecycle_weight)
            current_asset += annual_save

        peak_asset_eok = vals_accum_eok[-1]
        ret_pension = float(getv("income_pension", 0) or 0)
        ret_expenses = float(getv("retirement_monthly_expenses", 200) or 0)
        annual_ret_cashflow_eok = ((ret_pension - ret_expenses) * 12) / 10000.0
        ages_retire = list(range(retire_age, max(retire_age + 1, life_expectancy + 1)))
        vals_retire_eok = []
        ret_asset = peak_asset_eok
        depletion_age = None
        for idx, a in enumerate(ages_retire):
            vals_retire_eok.append(ret_asset)
            if idx > 0 and ret_asset <= 0 and depletion_age is None: depletion_age = a
            ret_asset += annual_ret_cashflow_eok

        max_val_eok = max(max(vals_accum_eok), max(vals_retire_eok) if vals_retire_eok else 0)
        use_cheonman = (max_val_eok < 1.0 and max_val_eok > 0)
        mult = 10.0 if use_cheonman else 1.0
        unit_str = "천만" if use_cheonman else "억"
        y_accum = [v * mult for v in vals_accum_eok]
        y_retire = [v * mult for v in vals_retire_eok]
        peak_disp = f"{peak_asset_eok * mult:.0f}천만 원" if use_cheonman else (f"{peak_asset_eok:.0f}억 원" if abs(peak_asset_eok) >= 10 else f"{peak_asset_eok:.1f}억 원")
        hover_tmpl = f"나이: %{{x}}세<br>추정 순자산: <b>%{{y:.{0 if use_cheonman else 1}f}}{unit_str} 원</b><extra></extra>"

        fig_asset = go.Figure()
        fig_asset.add_hline(y=0, line_dash="solid", line_color="#334155", line_width=1.5)
        fig_asset.add_trace(go.Scatter(x=ages_accum, y=y_accum, mode="lines+markers", line=dict(color="#F59E0B", width=3.5), marker=dict(size=6), fill='tozeroy', fillcolor='rgba(245, 158, 11, 0.12)', name="🌱 자산 축적기", hovertemplate=hover_tmpl))
        fig_asset.add_trace(go.Scatter(x=ages_retire, y=y_retire, mode="lines+markers", line=dict(color="#38BDF8", width=3.5), marker=dict(size=6), fill='tozeroy', fillcolor='rgba(56, 189, 248, 0.08)', name="🍂 자산 인출기", hovertemplate=hover_tmpl))
        fig_asset.add_vline(x=retire_age, line_dash="dash", line_color="#F8FAFC", line_width=2)
        fig_asset.add_annotation(x=retire_age, y=peak_asset_eok * mult, text=f"은퇴 정점 {retire_age}세 ({peak_disp})", showarrow=True, arrowhead=2, arrowcolor="#F59E0B", font=dict(size=13, color="#FDE68A"), ay=-38, bgcolor="rgba(15, 23, 42, 0.85)", bordercolor="#F59E0B", borderpad=4)
        if depletion_age and depletion_age <= life_expectancy:
            fig_asset.add_annotation(x=depletion_age, y=0, text=f"자산 소진 ({depletion_age}세)", showarrow=True, arrowhead=2, arrowcolor="#EF4444", font=dict(size=12.5, color="#FCA5A5"), ay=35, bgcolor="rgba(15, 23, 42, 0.85)", bordercolor="#EF4444", borderpad=3)
        fig_asset.update_layout(height=380, margin=dict(l=20, r=20, t=30, b=35), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#E2E8F0", size=13), xaxis=dict(title=dict(text="나이 (세)", font=dict(size=14, color="#94A3B8")), tickfont=dict(size=13, color="#94A3B8"), gridcolor="rgba(100, 116, 139, 0.2)", tickmode="linear", tick0=20, dtick=5, fixedrange=True), yaxis=dict(title=dict(text="추정 순자산", font=dict(size=14, color="#94A3B8")), tickfont=dict(size=13, color="#94A3B8"), ticksuffix=unit_str, tickformat=",.0f", gridcolor="rgba(100, 116, 139, 0.2)", fixedrange=True), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=12.5, color="#F1F5F9")), hovermode="x unified")
        st.plotly_chart(fig_asset, use_container_width=True, config={"displayModeBar": False, "scrollZoom": False, "doubleClick": False, "showAxisDragHandles": False})

        _, next_col = st.columns([5, 1])
        with next_col:
            if st.button("다음 →", key="finance_next", use_container_width=True, type="primary"):
                st.session_state["_pending_nav"] = "삶과 생계수단"
                st.rerun()


# ==============================================================================
# 6.02.00 | Tab 2 — 삶과 생계수단
# ==============================================================================
elif selected_page == "삶과 생계수단":
    is_adv = st.session_state.get("advanced_mode", False)
    
    if not is_adv:
        # [기본 모드] 중복 제목 없이 '돌쇠와 똘똘이' 우화 단독 노출
        st.caption("가벼운 3분 산책: 소득의 크기보다 중요한 '소득의 성격'을 한 편의 지혜로운 이야기로 마주합니다.")
        
        # 6.02.02 | 지혜로운 산책: 돌쇠와 똘똘이 우화 카드
        st.markdown("""
<div style="background: rgba(45, 35, 20, 0.55); border: 1.5px solid #6d4a1a; border-radius: 14px; padding: 24px 26px; margin: 16px 0 24px 0;">
<div style="font-size: 21px; font-weight: 850; color: #FDE68A; margin-bottom: 12px;">🌾 지혜로운 산책: 돌쇠와 똘똘이</div>
<div style="font-size: 14.5px; color: #E2E8F0; margin-bottom: 16px;">옛날 어느 마을, 머슴을 구하는 대감댁에 두 젊은이가 찾아왔습니다.</div>

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
<div style="background: rgba(15, 23, 42, 0.75); border: 1px solid #78350f; border-radius: 10px; padding: 16px 18px;">
<div style="font-size: 17.5px; font-weight: 800; color: #F59E0B; margin-bottom: 6px;">💪 돌쇠의 선택 (물통의 삶)</div>
<div style="font-size: 14px; color: #CBD5E1; line-height: 1.6; word-break: keep-all;">
"대감마님, 저는 첫 달부터 매달 <b>쌀 한 가마(80kg)</b>씩을 주십시오."<br>
돌쇠는 첫 달부터 쌀 한 가마를 받아 가족을 부양했습니다. 하지만 늙어 힘이 빠질 때까지 지게를 내려놓지 못했습니다.
</div>
</div>

<div style="background: rgba(15, 23, 42, 0.75); border: 1px solid #0369a1; border-radius: 10px; padding: 16px 18px;">
<div style="font-size: 17.5px; font-weight: 800; color: #38BDF8; margin-bottom: 6px;">🧠 똘똘이의 선택 (파이프라인의 삶)</div>
<div style="font-size: 14px; color: #CBD5E1; line-height: 1.6; word-break: keep-all;">
"저는 첫 달에 <b>쌀 한 되(1kg)</b>만 주시고, 매달 곱절(2되, 4되, 8되...)로 주십시오."<br>
똘똘이는 <b>'복리의 지혜'(파이프라인의 속성)</b>로 훗날 힘겨운 물통으로부터 자유로워졌습니다. <b>하지만 당장 첫 달에 쌀 한 되만 받았다면 굶어 죽었을 것입니다.</b>
</div>
</div>
</div>

<div style="background: rgba(234, 88, 12, 0.14); border-left: 4px solid #EA580C; border-radius: 4px; padding: 14px 18px;">
<div style="font-size: 15px; font-weight: 750; color: #F8FAFC; line-height: 1.6; word-break: keep-all;">
💡 <b>나침반의 성찰</b>: 누구의 선택이 옳다는 것이 아닙니다.<br>
낮에는 돌쇠처럼 성실하게 가족의 생계(쌀 한 가마)를 책임지면서, 저녁과 주말의 시간에 똘똘이의 지혜(파이프라인)를 한 되, 두 되 차근차근 놓아가는 <b>'현명한 플랜 B'</b>가 필요한 이유입니다.
</div>
</div>
</div>
""", unsafe_allow_html=True)

        _, next_col = st.columns([5, 1])
        with next_col:
            if st.button("다음 →", key="basic_livelihood_next", use_container_width=True, type="primary"):
                st.session_state["_pending_nav"] = "인생의 사계절"
                st.rerun()

    else:
        # [고급 모드] 모든 마이크로 모듈(6.02.01 ~ 6.02.04) 완전 탑재
        # 6.02.01 | 소득의 모습 2x2 사분면 (헤더 심플화: '물통과 파이프라인')
        st.markdown("""
<div style="background: rgba(30, 41, 59, 0.45); border: 1.5px solid #334155; border-radius: 14px; padding: 18px 22px; margin-bottom: 22px;">
<div style="font-size: 20px; font-weight: 850; color: #F8FAFC; margin-bottom: 14px;">물통과 파이프라인</div>
""", unsafe_allow_html=True)
        
        q_self = active_quadrant(st.session_state.get("job_form", "직장인"))
        q_spouse = active_quadrant(st.session_state.get("job_spouse_form", ""))
        
        def get_quad_badge(target_code):
            badges = []
            if q_self == target_code: badges.append("<span style='background:#EA580C; color:#FFFFFF; font-size:12px; font-weight:800; padding:2px 8px; border-radius:4px;'>나</span>")
            if q_spouse == target_code: badges.append("<span style='background:#0284C7; color:#FFFFFF; font-size:12px; font-weight:800; padding:2px 8px; border-radius:4px;'>배우자</span>")
            return f"<div style='min-height:22px; margin-bottom:4px; display:flex; justify-content:center; gap:6px;'>{' '.join(badges)}</div>" if badges else "<div style='min-height:22px; margin-bottom:4px;'></div>"

        def render_livelihood_quad(code, icon_html, title, sub_title, desc, is_right=False):
            is_self = (q_self == code)
            is_spouse = (q_spouse == code)
            if is_self and is_spouse: border_style = "border: 2.5px solid #EA580C; outline: 2.5px dashed #38BDF8; outline-offset: -5px; background: rgba(234, 88, 12, 0.16);"
            elif is_self: border_style = "border: 2.5px solid #EA580C; background: rgba(234, 88, 12, 0.14);"
            elif is_spouse: border_style = "border: 2.5px dashed #38BDF8; background: rgba(56, 189, 248, 0.14);"
            else:
                border_color = "#38BDF8" if is_right else "#334155"
                bg_color = "rgba(14, 165, 233, 0.06)" if is_right else "rgba(15, 23, 42, 0.7)"
                border_style = f"border: 1px solid {border_color}; background: {bg_color};"
            badge_html = get_quad_badge(code)
            accent_color = "#38BDF8" if is_right else "#F59E0B"
            return f'<div style="{border_style} border-radius: 12px; padding: 14px 10px; text-align: center; display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100%; min-height: 195px; box-sizing: border-box; width: 100%;">{badge_html}<div style="font-size: 26px; margin-bottom: 2px;">{icon_html}</div><div style="font-size: 17.5px; font-weight: 850; color: #F8FAFC; line-height: 1.2;">{title}</div><div style="font-size: 13px; font-weight: 700; color: {accent_color}; margin: 3px 0 5px 0; line-height: 1.3;">{sub_title}</div><div style="font-size: 12.5px; color: #CBD5E1; line-height: 1.4; word-break: keep-all; text-align: center;">{desc}</div></div>'

        card_e = render_livelihood_quad("E", "🪣🪣🪣", "작은 물통 (E)", "나의 시간과 돈을 1:1 맞교환", "직접 일한 시간만큼 소득 창출<br><span style='color:#F59E0B; font-weight:600;'>(노동을 멈추면 수입도 멈춤)</span>", is_right=False)
        card_s = render_livelihood_quad("S", "🛢️", "큰 물통 (S)", "전문성과 몸값으로 키운 물통", "한 번에 담는 물통의 양을 키운 모습<br><span style='color:#F59E0B; font-weight:600;'>(큰 물통이지만 여전히 지고 다님)</span>", is_right=False)
        card_b = render_livelihood_quad("B", "⚙️", "파이프라인<br>구축 (B)", "시스템 소유", "스스로 굴러가는 비즈니스 소유<br><span style='color:#38BDF8; font-weight:600;'>(내가 멈추어도 시스템이 일함)</span>", is_right=True)
        card_i = render_livelihood_quad("I", "🚰➰", "파이프라인<br>접속 (I)", "플랫폼·자본 접속", "이미 구축된 플랫폼에 접속 레버리지<br><span style='color:#38BDF8; font-weight:600;'>(자산과 네트워크가 소득을 만듦)</span>", is_right=True)

        st.markdown(f"""
<div style="margin: 6px 0 16px 0;">
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px 0px; align-items: stretch;">
<div style="padding-right: 12px; border-right: 3.5px dashed #475569; display: flex; box-sizing: border-box;">{card_e}</div>
<div style="padding-left: 12px; display: flex; box-sizing: border-box;">{card_b}</div>
<div style="padding-right: 12px; border-right: 3.5px dashed #475569; display: flex; box-sizing: border-box;">{card_s}</div>
<div style="padding-left: 12px; display: flex; box-sizing: border-box;">{card_i}</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

        # 6.02.02 | 지혜로운 산책: 돌쇠와 똘똘이 우화 카드 (수정 멘트 반영)
        st.markdown("""
<div style="background: rgba(45, 35, 20, 0.55); border: 1.5px solid #6d4a1a; border-radius: 14px; padding: 22px 24px; margin-bottom: 22px;">
<div style="font-size: 20px; font-weight: 850; color: #FDE68A; margin-bottom: 12px;">🌾 지혜로운 산책: 돌쇠와 똘똘이</div>
<div style="font-size: 14.5px; color: #E2E8F0; margin-bottom: 16px;">옛날 어느 마을, 머슴을 구하는 대감댁에 두 젊은이가 찾아왔습니다.</div>
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
<div style="background: rgba(15, 23, 42, 0.75); border: 1px solid #78350f; border-radius: 10px; padding: 16px 18px;">
<div style="font-size: 17px; font-weight: 800; color: #F59E0B; margin-bottom: 6px;">💪 돌쇠의 선택 (물통의 삶)</div>
<div style="font-size: 14px; color: #CBD5E1; line-height: 1.6; word-break: keep-all;">
"대감마님, 저는 첫 달부터 매달 <b>쌀 한 가마(80kg)</b>씩을 주십시오."<br>
돌쇠는 첫 달부터 쌀 한 가마를 받아 가족을 부양했습니다. 하지만 늙어 힘이 빠질 때까지 지게를 내려놓지 못했습니다.
</div></div>
<div style="background: rgba(15, 23, 42, 0.75); border: 1px solid #0369a1; border-radius: 10px; padding: 14px 16px;">
<div style="font-size: 17px; font-weight: 800; color: #38BDF8; margin-bottom: 6px;">🧠 똘똘이의 선택 (파이프라인의 삶)</div>
<div style="font-size: 14px; color: #CBD5E1; line-height: 1.6; word-break: keep-all;">
"저는 첫 달에 <b>쌀 한 되(1kg)</b>만 주시고, 매달 곱절(2되, 4되, 8되...)로 주십시오."<br>
똘똘이는 <b>'복리의 지혜'(파이프라인의 속성)</b>로 훗날 힘겨운 물통으로부터 자유로워졌습니다. <b>하지만 당장 첫 달에 쌀 한 되만 받았다면 굶어 죽었을 것입니다.</b>
</div></div></div>
<div style="background: rgba(234, 88, 12, 0.14); border-left: 4px solid #EA580C; border-radius: 4px; padding: 12px 16px;">
<div style="font-size: 15px; font-weight: 750; color: #F8FAFC; line-height: 1.6; word-break: keep-all;">
💡 <b>나침반의 성찰</b>: 누구의 선택이 옳다는 것이 아닙니다.<br>
낮에는 돌쇠처럼 성실하게 가족의 생계(쌀 한 가마)를 책임지면서, 저녁과 주말의 시간에 똘똘이의 지혜(파이프라인)를 한 되, 두 되 차근차근 놓아가는 <b>'현명한 플랜 B'</b>가 필요한 이유입니다.
</div></div></div>
""", unsafe_allow_html=True)

        # 6.02.03 | 더 생각해보기 4가지 질문 리스트 (가로 1줄 대형화)
        st.markdown("""
<div style="margin: 28px 0 26px 0; padding: 4px 2px;">
<div style="font-size: 21px; font-weight: 850; color: #F8FAFC; margin-bottom: 6px;">더 생각해보기</div>
<div style="font-size: 14px; color: #94A3B8; margin-bottom: 18px; line-height: 1.6;">우리가 당연하게 여겨온 것들을 잠시 멈추어 생각해 봅니다.</div>
<div style="display: flex; flex-direction: column; gap: 14px;">
<div style="background: rgba(30, 41, 59, 0.35); border-left: 3.5px solid #64748B; border-radius: 4px; padding: 12px 16px; display: flex; align-items: baseline; gap: 12px;"><span style="font-size: 14px; font-weight: 800; color: #94A3B8; min-width: 24px;">01</span><span style="font-size: 18.5px; font-weight: 800; color: #F8FAFC; line-height: 1.5; word-break: keep-all;">'일을 하고 있는 것'과 '생계를 위해 반드시 일해야 하는 것'은 같은가?</span></div>
<div style="background: rgba(30, 41, 59, 0.35); border-left: 3.5px solid #64748B; border-radius: 4px; padding: 12px 16px; display: flex; align-items: baseline; gap: 12px;"><span style="font-size: 14px; font-weight: 800; color: #94A3B8; min-width: 24px;">02</span><span style="font-size: 18.5px; font-weight: 800; color: #F8FAFC; line-height: 1.5; word-break: keep-all;">'소득이 발생하는 것'과 '내가 직접 일해야 소득이 발생하는 것'은 같은가?</span></div>
<div style="background: rgba(30, 41, 59, 0.35); border-left: 3.5px solid #64748B; border-radius: 4px; padding: 12px 16px; display: flex; align-items: baseline; gap: 12px;"><span style="font-size: 14px; font-weight: 800; color: #94A3B8; min-width: 24px;">03</span><span style="font-size: 18.5px; font-weight: 800; color: #F8FAFC; line-height: 1.5; word-break: keep-all;">'직장을 그만두는 것'과 '은퇴'는 같은가?</span></div>
<div style="background: rgba(30, 41, 59, 0.35); border-left: 3.5px solid #64748B; border-radius: 4px; padding: 12px 16px; display: flex; align-items: baseline; gap: 12px;"><span style="font-size: 14px; font-weight: 800; color: #94A3B8; min-width: 24px;">04</span><span style="font-size: 18.5px; font-weight: 800; color: #F8FAFC; line-height: 1.5; word-break: keep-all;">'은퇴'란 무엇이며, '나'는 은퇴를 어떻게 바라볼 수 있을까?</span></div>
</div></div>
""", unsafe_allow_html=True)

        # 6.02.04 | 내가 생각하는 은퇴 예상 나이 (질문 순서 위아래 교체)
        st.markdown("""
<div style="background: rgba(24, 32, 47, 0.65); border: 1.5px solid #3b4b66; border-radius: 14px; padding: 20px 22px; margin-bottom: 22px;">
<div style="font-size: 17px; font-weight: 750; color: #FDE68A; line-height: 1.6; word-break: keep-all; margin-bottom: 6px;">나는 언제부터 생계를 위해 반드시 일해야 하는 삶에서 벗어날 수 있을까?</div>
<div style="font-size: 20px; font-weight: 850; color: #F8FAFC; margin-bottom: 12px;">내가 생각하는 은퇴 예상 나이</div>
""", unsafe_allow_html=True)

        cur_user_age = int(st.session_state.person_age)
        default_retire = int(st.session_state.get("retirement_age") or 60)
        if default_retire < cur_user_age: default_retire = cur_user_age

        with st.form("retirement_inline_form"):
            r_col1, r_col2 = st.columns([3.2, 1.0])
            with r_col1:
                retirement_input = st.number_input("지금 하는 현업을 졸업(은퇴)하고 싶은 나이", min_value=cur_user_age, max_value=100, value=default_retire, step=1, label_visibility="collapsed")
            with r_col2:
                retirement_saved = st.form_submit_button("은퇴 나이 확인", use_container_width=True, type="primary")

        if retirement_saved:
            st.session_state["retirement_age"] = int(retirement_input)
            st.success(f"은퇴 예상 나이({retirement_input}세)가 반영되었습니다.")

        st.markdown("</div>", unsafe_allow_html=True)

        _, next_col = st.columns([5, 1])
        with next_col:
            if st.button("다음 →", key="livelihood_next", use_container_width=True, type="primary"):
                st.session_state["retirement_age"] = int(st.session_state.get("retirement_age_input", retirement_input))
                st.session_state["_pending_nav"] = "인생의 사계절"
                st.session_state["_scroll_to_top_once"] = True
                st.rerun()


# ==============================================================================
# 6.03.00 | Tab 3 — 인생의 사계절
# ==============================================================================
elif selected_page == "인생의 사계절":
    if st.session_state.pop("_scroll_to_top_once", False):
        st.components.v1.html("<script>try { window.parent.scrollTo({top: 0, behavior: 'instant'}); } catch(e) {}</script>", height=0)
    
    is_adv = st.session_state.get("advanced_mode", False)
    cur_age = int(st.session_state.person_age)
    user_gender = st.session_state.get("gender", "🙋‍♂️ 남성")
    is_female = ("여성" in user_gender)
    life_expectancy = 87 if is_female else 81
    retire_val = st.session_state.get("retirement_age")
    retire_age = int(retire_val) if retire_val is not None else 60
    retire_age = max(cur_age, min(retire_age, 90))
    years_left = max(0, retire_age - cur_age)
    winter_years = max(0, life_expectancy - retire_age)
    winter_months = winter_years * 12

    def build_official_nta_chart():
        
        fig_official_nta = go.Figure()
        official_ages = [0, 5, 10, 14, 17, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 61, 65, 70, 75, 80, 85]
        official_income = [0, 0, 0, 0, 0, 3, 10, 18, 28, 27, 28, 38, 35, 39, 36, 26, 21, 14, 7, 2, 0.5, 0]
        official_expense = [4, 5, 18, 20, 22, 15, 19, 18, 22, 20, 19, 23, 20, 24, 26, 23, 23, 25, 16, 11, 7, 5]
        official_deficit = [e - i for e, i in zip(official_expense, official_income)]
        fig_official_nta.add_trace(go.Scatter(x=official_ages, y=official_deficit, mode="lines", line=dict(color="rgba(147, 197, 253, 0.0)", width=0), fill='tozeroy', fillcolor='rgba(147, 197, 253, 0.45)', name="생애주기적자 (소비 - 노동소득)", hovertemplate="나이: %{x}세<br>생애주기적자: <b>%{y:.1f}조 원</b><extra></extra>"))
        fig_official_nta.add_trace(go.Scatter(x=official_ages, y=official_expense, mode="lines", line=dict(color="#65A30D", width=3, dash="dash"), name="소비", hovertemplate="나이: %{x}세<br>소비: <b>%{y:.1f}조 원</b><extra></extra>"))
        fig_official_nta.add_trace(go.Scatter(x=official_ages, y=official_income, mode="lines", line=dict(color="#2563EB", width=3.5), name="노동소득", hovertemplate="나이: %{x}세<br>노동소득: <b>%{y:.1f}조 원</b><extra></extra>"))
        fig_official_nta.add_hline(y=0, line_dash="solid", line_color="#475569", line_width=1.5)
        fig_official_nta.add_vline(x=17, line_dash="dash", line_color="#94A3B8", line_width=1.5)
        fig_official_nta.add_vline(x=65, line_dash="dash", line_color="#94A3B8", line_width=1.5)
        fig_official_nta.add_annotation(x=8, y=50, text="유년층", showarrow=False, font=dict(size=12, color="#E2E8F0"), bgcolor="rgba(30, 41, 59, 0.8)", bordercolor="#475569")
        fig_official_nta.add_annotation(x=41, y=50, text="노동연령층", showarrow=False, font=dict(size=12, color="#E2E8F0"), bgcolor="rgba(30, 41, 59, 0.8)", bordercolor="#475569")
        fig_official_nta.add_annotation(x=75, y=50, text="노년층", showarrow=False, font=dict(size=12, color="#E2E8F0"), bgcolor="rgba(30, 41, 59, 0.8)", bordercolor="#475569")
        fig_official_nta.add_annotation(x=12, y=10, text="적자", showarrow=False, font=dict(size=13, color="#93C5FD", weight="bold"))
        fig_official_nta.add_annotation(x=45, y=-16, text="흑자", showarrow=False, font=dict(size=13, color="#93C5FD", weight="bold"))
        fig_official_nta.add_annotation(x=73, y=5, text="적자", showarrow=False, font=dict(size=13, color="#93C5FD", weight="bold"))

        fig_official_nta.update_layout(
            title=dict(text="&lt; 생 애 주 기 적 자 &gt;", x=0.5, xanchor="center", font=dict(size=16, color="#F8FAFC")),
            height=390,
            margin=dict(l=20, r=20, t=45, b=80),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E2E8F0", size=13),
            xaxis=dict(
                title=dict(text="연령 (세)", font=dict(size=13, color="#94A3B8")),
                tickfont=dict(size=12, color="#94A3B8"),
                gridcolor="rgba(100, 116, 139, 0.2)",
                tickmode="linear", tick0=0, dtick=5,
                fixedrange=True
            ),
            yaxis=dict(
                title=None,
                tickfont=dict(size=12, color="#94A3B8"),
                gridcolor="rgba(100, 116, 139, 0.2)",
                range=[-22, 54],
                fixedrange=True
            ),
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.28,
                xanchor="center",
                x=0.5,
                font=dict(size=12, color="#F1F5F9")
            ),
            hovermode="x unified"
        )

        return fig_official_nta
        
    if not is_adv:
        # [기본 모드] 중복 제목 없이 3대 지표 + 내 계절 배지만 노출
        st.caption("가벼운 3분 산책: 대한민국 통계청 공식 지표를 통해 내 인생의 사계절 중 어디쯤 와 있는지 확인합니다.")

        if cur_age <= 27: cur_season, s_icon, s_color, s_desc = "봄 (준비기)", "🌱", "#4ADE80", "부모님의 부양으로 배우고 성장하는 계절"
        elif 28 <= cur_age <= 45: cur_season, s_icon, s_color, s_desc = "여름 (성장기)", "☀️", "#F59E0B", "성실하게 일하여 가정을 일구고 최대 흑자를 만드는 계절"
        elif 46 <= cur_age <= 60: cur_season, s_icon, s_color, s_desc = "가을 (결실기)", "🍂", "#FB923C", "자녀 독립과 함께 다가올 겨울을 준비할 골든타임"
        else: cur_season, s_icon, s_color, s_desc = "겨울 (음미기)", "❄️", "#38BDF8", "근로소득이 멈추고 삶의 열매를 누리는 계절"

        st.markdown(f"""
<div style="background: rgba(30, 41, 59, 0.55); border: 2px solid {s_color}; border-radius: 14px; padding: 22px 24px; margin: 16px 0 24px 0; text-align: center;">
<div style="font-size: 32px; margin-bottom: 6px;">{s_icon}</div>
<div style="font-size: 21px; font-weight: 850; color: #F8FAFC; margin-bottom: 4px;">나의 현재 계절은 <span style="color:{s_color};">{cur_season}</span> 입니다 (만 {cur_age}세)</div>
<div style="font-size: 14.5px; color: #CBD5E1; line-height: 1.6; word-break: keep-all; margin-top: 6px;">{s_desc}</div>
</div>
""", unsafe_allow_html=True)

        st.markdown("### 국가데이터처 공식 생애 통계 지표 (대한민국 평균 기준)")
        c_m1, c_m2, c_m3 = st.columns(3)
        c_m1.metric("한국인 평균 흑자 진입", "28세", help="노동소득이 소비를 추월하는 연령")
        c_m2.metric("최대 흑자 정점", "45세", "연 1,932만 원")
        c_m3.metric("평균 적자 재전환", "61세", help="은퇴 후 소비가 노동소득을 다시 초과")

        fig_official_nta = build_official_nta_chart()
        st.plotly_chart(fig_official_nta, use_container_width=True, config={"displayModeBar": False, "scrollZoom": False, "doubleClick": False, "showAxisDragHandles": False})

        _, next_col = st.columns([5, 1])
        with next_col:
            if st.button("다음 →", key="basic_seasons_next", use_container_width=True, type="primary"):
                st.session_state["_pending_nav"] = "AI 시선"
                st.rerun()

    else:
        # [고급 모드] 모든 마이크로 모듈(6.03.01 ~ 6.03.07) 완전 탑재
        # 6.03.01 | 가족 구성원 나이 입력 폼 (3대 직계 가족 슬림화)
        # 6.03.02 | (형제자매 기능 전면 폐기 ➜ 직계 부양가족 집중 완료)
        st.markdown("### 1. 가족 구성원과 은퇴 시점의 나이")
        child_options = ["입력 안 함", "없음", "1명", "2명", "3명", "4명 이상"]
        prev_c_count = st.session_state.get("child_count", "입력 안 함")
        if prev_c_count not in child_options: prev_c_count = "입력 안 함"

        child_count = st.selectbox("자녀 수", child_options, index=child_options.index(prev_c_count), key="child_count_select_direct")

        with st.form("family_form"):
            spouse_age = st.number_input("배우자 나이 (없거나 미입력 시 0)", min_value=0, max_value=120, value=int(st.session_state.get("spouse_age", 0)), step=1)
            child_age1, child_age2, child_age3, child_age4 = 0, 0, 0, 0
            if child_count in ["1명", "2명", "3명", "4명 이상"]:
                c1_col, c2_col = st.columns(2)
                with c1_col: child_age1 = st.number_input("첫째 자녀 나이", min_value=0, max_value=100, value=int(st.session_state.get("child_age", 0)), step=1)
                with c2_col:
                    if child_count in ["2명", "3명", "4명 이상"]: child_age2 = st.number_input("둘째 자녀 나이", min_value=0, max_value=100, value=int(st.session_state.get("child_age2", 0)), step=1)
                    else: st.write("")

            if child_count in ["3명", "4명 이상"]:
                c3_col, c4_col = st.columns(2)
                with c3_col: child_age3 = st.number_input("셋째 자녀 나이", min_value=0, max_value=100, value=int(st.session_state.get("child_age3", 0)), step=1)
                with c4_col:
                    if child_count == "4명 이상": child_age4 = st.number_input("넷째 자녀 나이", min_value=0, max_value=100, value=int(st.session_state.get("child_age4", 0)), step=1)
                    else: st.write("")

            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            f_col, m_col = st.columns(2)
            with f_col: father_age = st.number_input("아버지 나이 (선택, 모르면 0)", min_value=0, max_value=120, value=int(st.session_state.get("father_age", 0)), step=1)
            with m_col: mother_age = st.number_input("어머니 나이 (선택, 모르면 0)", min_value=0, max_value=120, value=int(st.session_state.get("mother_age", 0)), step=1)

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            st.markdown("#### 앞으로의 가족 계획 (선택)")
            p_c1, p_c2, p_c3 = st.columns(3)
            with p_c1:
                marriage_options = ["미정", "계획 없음", "1~3년 내 결혼 생각 있음", "3년 이후 결혼 생각 있음", "결혼 예정/준비 중"]
                marriage_plan = st.selectbox("결혼 계획", marriage_options, index=marriage_options.index(st.session_state.get("marriage_plan", "미정")) if st.session_state.get("marriage_plan", "미정") in marriage_options else 0)
            with p_c2:
                child_plan_options = ["미정", "계획 없음", "자녀 계획 있음", "출산 예정/준비 중", "추가 자녀 계획 있음"]
                child_plan = st.selectbox("출산·자녀 계획", child_plan_options, index=child_plan_options.index(st.session_state.get("child_plan", "미정")) if st.session_state.get("child_plan", "미정") in child_plan_options else 0)
            with p_c3:
                housing_options = ["미정", "현재 주거 유지", "전세·월세 이동 고려", "주택 구입 고려", "주거 계획 확정"]
                housing_plan = st.selectbox("주거 계획", housing_options, index=housing_options.index(st.session_state.get("housing_plan", "미정")) if st.session_state.get("housing_plan", "미정") in housing_options else 0)

            save_family = st.form_submit_button("가족 정보 반영하기", use_container_width=True, type="primary")

        if save_family:
            st.session_state.spouse_age = spouse_age
            st.session_state.child_count = child_count
            st.session_state.child_age = child_age1
            st.session_state.child_age2 = child_age2
            st.session_state.child_age3 = child_age3
            st.session_state.child_age4 = child_age4
            st.session_state.father_age = father_age
            st.session_state.mother_age = mother_age
            st.session_state.marriage_plan = marriage_plan
            st.session_state.child_plan = child_plan
            st.session_state.housing_plan = housing_plan
            st.session_state.pop("sibling_items", None)
            st.rerun()

        # 6.03.03 | 은퇴 시점 가족 미래 나이 2열 슬림 카드 (직계 3대 집중)
        people = [(st.session_state.get("person_name", "나"), cur_age)]
        if getv("spouse_age", 0) > 0: people.append(("배우자", int(getv("spouse_age"))))
        if getv("child_age", 0) > 0: people.append(("첫째 자녀", int(getv("child_age"))))
        if getv("child_age2", 0) > 0: people.append(("둘째 자녀", int(getv("child_age2"))))
        if getv("child_age3", 0) > 0: people.append(("셋째 자녀", int(getv("child_age3"))))
        if getv("child_age4", 0) > 0: people.append(("넷째 자녀", int(getv("child_age4"))))
        if getv("father_age", 0) > 0: people.append(("아버지", int(getv("father_age"))))
        if getv("mother_age", 0) > 0: people.append(("어머니", int(getv("mother_age"))))

        st.markdown(f"""
<div style="background: rgba(30, 41, 59, 0.4); border: 1px solid #334155; border-radius: 10px; padding: 12px 18px; margin: 18px 0 10px 0; display:flex; justify-content:space-between; align-items:center;">
<span style="font-size: 15.5px; font-weight: 800; color: #F8FAFC;">📌 내가 은퇴하는 시점(만 {retire_age}세, {years_left}년 후)의 우리 가족 나이</span>
<span style="font-size: 13px; color: #94A3B8;">현재 나이 ➔ 은퇴 시 나이</span>
</div>
""", unsafe_allow_html=True)

        f_cols = st.columns(2)
        for idx, (name, current) in enumerate(people):
            c = f_cols[idx % 2]
            future = current + years_left
            with c:
                st.markdown(f"""
<div class='soft-card' style='display:flex; align-items:center; justify-content:space-between; padding:12px 18px; margin:5px 0;'>
<b style='font-size:16px; color:#F8FAFC;'>{name}</b>
<div style='display:flex; align-items:center; gap:12px;'>
<span style='font-size:17px; color:#94A3B8;'>{current}세</span>
<span style='font-size:16px; color:#EA580C;'>➔</span>
<span style='font-size:19px; font-weight:800; color:#F59E0B;'>{future}세</span>
</div>
</div>
""", unsafe_allow_html=True)

        # 6.03.04 | 가족 생애 지출 피크(성인/미성년 자녀) 안내 카드
        c_age1 = int(getv("child_age", 0))
        if 0 < c_age1 < 20:
            college_my_age = cur_age + (20 - c_age1)
            st.markdown(f"""
<div style="background: rgba(234, 88, 12, 0.12); border-left: 4px solid #EA580C; border-radius: 6px; padding: 14px 18px; margin: 12px 0 20px 0;">
<div style="font-size: 15px; font-weight: 750; color: #F8FAFC; line-height: 1.6;">
🎯 <b>생애 지출 피크 자각 포인트</b>: 첫째 자녀가 대학에 입학하는 만 20세가 되면, 나의 나이는 <b>만 {college_my_age}세</b>가 됩니다.<br>
<span style="font-size: 13.5px; color: #CBD5E1;">통계청 국민이전계정 상 소득 정점(45세)은 지나가면서, 자녀 학자금과 독립 비용으로 <b>인생에서 가장 큰 지출이 집중되는 결정적 시기</b>입니다.</span>
</div></div>
""", unsafe_allow_html=True)
        elif c_age1 >= 20:
            st.markdown(f"""
<div style="background: rgba(30, 41, 59, 0.5); border-left: 4px solid #38BDF8; border-radius: 6px; padding: 14px 18px; margin: 12px 0 20px 0;">
<div style="font-size: 15px; font-weight: 750; color: #F8FAFC; line-height: 1.6;">
🌱 <b>가족 성장 단계</b>: 첫째 자녀(만 {c_age1}세)가 이미 성년기에 도달하여, 학자금 집중 지출기를 거쳐 독립과 사회 진출의 계절을 맞이하고 있습니다.
</div></div>
""", unsafe_allow_html=True)

        # 6.03.05 | 나만의 생애주기 곡선 & 흑자/적자 2단 연동 차트
        from plotly.subplots import make_subplots

        st.markdown("### 2. 나만의 생애주기 곡선")
        st.caption("※ 통계청 국민이전계정(NTA) 통계 기반으로, 나의 실제 가족·소득·지출을 개략적으로 맞춘 곡선입니다. (단위: 연간 만 원)")
        s = current_financial_summary()
        cur_annual_income = s["annual_total_income"]
        cur_annual_expense = s["annual_total_expenses"]
        ret_annual_pension = float(getv("income_pension", 0) or 0) * 12.0
        ret_annual_expense = float(getv("retirement_monthly_expenses", 200) or 0) * 12.0
        career_st = st.session_state.get("career_stage", "🌱 3년 이하 (초년생)")
        m_plan = st.session_state.get("marriage_plan", "미정")
        c_plan = st.session_state.get("child_plan", "미정")
        h_plan = st.session_state.get("housing_plan", "미정")
        user_gender = st.session_state.get("gender", "🙋‍♂️ 남성")
        is_female = ("여성" in user_gender)

        # 1) 유효한 자녀 나이 수집
        existing_child_ages = [int(getv(k, 0)) for k in ["child_age", "child_age2", "child_age3", "child_age4"] if int(getv(k, 0)) > 0]

        # 2) 👶 출산·육아 집중기 구간 산정 (과거·현재·미래 전 생애 기준 역산)
        childcare_windows = []
        if existing_child_ages:
            for ca in existing_child_ages:
                birth_p_age = cur_age - ca
                childcare_windows.append((max(20, birth_p_age), min(85, birth_p_age + 6)))
        elif c_plan in ["자녀 계획 있음", "출산 예정/준비 중", "추가 자녀 계획 있음"]:
            future_birth = max(cur_age + 1, 33 if is_female else 35)
            childcare_windows.append((future_birth, future_birth + 5))

        childcare_start = min([w[0] for w in childcare_windows]) if childcare_windows else None
        childcare_end = max([w[1] for w in childcare_windows]) if childcare_windows else None

        # 3) 🎓 자녀 대학교 학자금 피크 구간 (과거·현재·미래 전 생애 19~24세 기준 역산)
        college_windows = []
        if existing_child_ages:
            for ca in existing_child_ages:
                c_start = cur_age + (19 - ca)
                c_end = cur_age + (24 - ca)
                college_windows.append((max(20, c_start), min(85, c_end)))
        elif c_plan in ["자녀 계획 있음", "출산 예정/준비 중"]:
            future_birth = max(cur_age + 1, 33 if is_female else 35)
            college_windows.append((future_birth + 19, future_birth + 24))

        college_band_start = min([w[0] for w in college_windows]) if college_windows else None
        college_band_end = max([w[1] for w in college_windows]) if college_windows else None

        # 4) 시뮬레이션 연령 구간 (20세 ~ 85세)
        ages_sim = list(range(20, 86))
        my_income_curve = []
        my_expense_curve = []

        # 은퇴자(D사례 등) 과거 전성기 소득 보정
        is_already_retired = (cur_age >= retire_age) or (cur_annual_income < 1200 and cur_age >= 60)
        if is_already_retired:
            base_career_income = max(cur_annual_income, ret_annual_pension * 1.8, cur_annual_expense * 1.5, 5200.0)
        else:
            base_career_income = cur_annual_income

        for a in ages_sim:
            # --- [소득 곡선 계산] ---
            if a < retire_age:
                growth_rate = 0.022 if "초년생" in career_st else 0.015
                if a <= 46:
                    dist_46 = 46 - a
                    w = 1.0 - (growth_rate * dist_46)
                else:
                    w = 1.0 - (0.012 * (a - 46))
                w = max(0.30, w)

                if childcare_start and childcare_end and (childcare_start <= a <= childcare_end):
                    mid_c = (childcare_start + childcare_end) / 2.0
                    dist = abs(a - mid_c)
                    dip_factor = 0.70 + (0.035 * (dist ** 2))
                    w *= min(0.95, dip_factor)

                inc_val = base_career_income * w
            else:
                inc_val = ret_annual_pension if ret_annual_pension > 0 else (cur_annual_income if is_already_retired else 0)
            my_income_curve.append(inc_val)

            # --- [지출 곡선 계산] ---
            if a < retire_age:
                exp_factor = 1.0
                if childcare_start and childcare_end and (childcare_start <= a <= childcare_end):
                    exp_factor *= 1.18
                if m_plan in ["1~3년 내 결혼 생각 있음", "결혼 예정/준비 중"] and (cur_age <= a <= cur_age + 2):
                    exp_factor *= 1.12
                if h_plan in ["주택 구입 고려", "주거 계획 확정"]:
                    exp_factor *= 1.08

                if a < 30 and cur_age >= 30:
                    exp_factor *= 0.75

                base_exp = (cur_annual_expense if not is_already_retired else (ret_annual_expense * 1.25)) * exp_factor
                college_kids_count = sum(1 for (cs, ce) in college_windows if cs <= a <= ce)
                extra_college_exp = college_kids_count * 1500.0

                exp_val = base_exp + extra_college_exp
            else:
                exp_val = ret_annual_expense
            my_expense_curve.append(exp_val)

        # 5) 연간 순수지 (소득 - 지출): 흑자(+) vs 적자(-)
        net_flow = [i - e for i, e in zip(my_income_curve, my_expense_curve)]

        # 0 교차점 보간으로 흑자(녹색)와 적자(붉은색) 음영 완벽 분리
        ages_fine = []
        flow_fine = []
        for idx in range(len(ages_sim) - 1):
            a1, a2 = ages_sim[idx], ages_sim[idx+1]
            v1, v2 = net_flow[idx], net_flow[idx+1]
            ages_fine.append(a1)
            flow_fine.append(v1)
            if (v1 > 0 and v2 < 0) or (v1 < 0 and v2 > 0):
                t = abs(v1) / (abs(v1) + abs(v2))
                a_zero = a1 + t * (a2 - a1)
                ages_fine.append(a_zero)
                flow_fine.append(0.0)
        ages_fine.append(ages_sim[-1])
        flow_fine.append(net_flow[-1])

        surplus_fine = [max(0.0, v) for v in flow_fine]
        deficit_fine = [min(0.0, v) for v in flow_fine]

# 6) 상단 차트 고도 레벨 산정
        y_max = max(max(my_income_curve), max(my_expense_curve)) if my_income_curve else 6000
        y_top = y_max * 1.16
        alt_level_2 = y_top * 0.32
        alt_level_1 = y_top * 0.10
        alt_level_5 = y_top * 0.85  # 타이틀 뱃지 높이

        # [배경 띠 1] 👶 출산·육아 집중기 (안전장치 적용)
        if childcare_start and childcare_end:
            # 과거 구간은 자르고 현재~끝 구간으로 설정하되, 범위가 꼬이지 않게 처리
            c_band_x0 = max(20, min(childcare_start, 85))
            c_band_x1 = max(20, min(childcare_end, 85))
            if c_band_x1 > c_band_x0:
                fig_my_nta.add_vrect(
                    x0=c_band_x0, x1=c_band_x1,
                    fillcolor="rgba(249, 115, 22, 0.28)", layer="below", line_width=0,
                    row=1, col=1
                )
                fig_my_nta.add_annotation(
                    x=(c_band_x0 + c_band_x1) / 2.0, y=alt_level_5,
                    text="👶 출산·육아", showarrow=False,
                    font=dict(size=11, color="#FDBA74", weight="bold"),
                    bgcolor="rgba(15, 23, 42, 0.8)", bordercolor="#F97316", borderpad=2,
                    row=1, col=1
                )

        # [배경 띠 2] 🎓 자녀 대학교 학자금 집중기 (안전장치 적용)
        if college_band_start and college_band_end:
            k_band_x0 = max(20, min(college_band_start, 85))
            k_band_x1 = max(20, min(college_band_end, 85))
            if k_band_x1 > k_band_x0:
                fig_my_nta.add_vrect(
                    x0=k_band_x0, x1=k_band_x1,
                    fillcolor="rgba(168, 85, 247, 0.28)", layer="below", line_width=0,
                    row=1, col=1
                )
                fig_my_nta.add_annotation(
                    x=(k_band_x0 + k_band_x1) / 2.0, y=alt_level_5,
                    text="🎓 자녀 대학 피크", showarrow=False,
                    font=dict(size=11, color="#E9D5FF", weight="bold"),
                    bgcolor="rgba(15, 23, 42, 0.8)", bordercolor="#A855F7", borderpad=2,
                    row=1, col=1
                )

        # [배경 띠 3] ❄️ 은퇴 후 겨울
        if retire_age < 85:
            r_band_x0 = max(20, min(retire_age, 85))
            r_band_x1 = 85
            if r_band_x1 > r_band_x0:
                fig_my_nta.add_vrect(
                    x0=r_band_x0, x1=r_band_x1,
                    fillcolor="rgba(56, 189, 248, 0.22)", layer="below", line_width=0,
                    row=1, col=1
                )
                fig_my_nta.add_annotation(
                    x=(r_band_x0 + r_band_x1) / 2.0, y=alt_level_5,
                    text="❄️ 은퇴 후 겨울", showarrow=False,
                    font=dict(size=11, color="#BAE6FD", weight="bold"),
                    bgcolor="rgba(15, 23, 42, 0.8)", bordercolor="#38BDF8", borderpad=2,
                    row=1, col=1
                )

        # [Row 1] 소득 & 지출 (3대 심플 범례)
        fig_my_nta.add_trace(go.Scatter(
            x=ages_sim, y=my_income_curve, mode="lines",
            line=dict(color="#10B981", width=3.2, shape='spline', smoothing=0.8),
            name="소득",
            hovertemplate="나이: %{x}세<br>연 소득: <b>%{y:,.0f}만 원</b><extra></extra>"
        ), row=1, col=1)

        fig_my_nta.add_trace(go.Scatter(
            x=ages_sim, y=my_expense_curve, mode="lines",
            line=dict(color="#F97316", width=2.8, dash="dash", shape='spline', smoothing=0.8),
            name="지출",
            hovertemplate="나이: %{x}세<br>연 지출: <b>%{y:,.0f}만 원</b><extra></extra>"
        ), row=1, col=1)

        # [Row 1] 현재 나이 기준선
        fig_my_nta.add_vline(x=cur_age, line_dash="solid", line_color="#38BDF8", line_width=2.0)
        fig_my_nta.add_annotation(
            x=cur_age, y=alt_level_1,
            text=f"현재 ({cur_age}세)",
            showarrow=True, arrowhead=2, arrowcolor="#38BDF8",
            font=dict(size=11, color="#BAE6FD", weight="bold"), ay=-20,
            bgcolor="rgba(15, 23, 42, 0.9)", bordercolor="#38BDF8", borderpad=3,
            row=1, col=1
        )

        # [Row 1] 은퇴 기준선 (화이트 점선)
        retire_line_color = "#F8FAFC"
        fig_my_nta.add_vline(x=retire_age, line_dash="dot", line_color=retire_line_color, line_width=2.2)
        fig_my_nta.add_annotation(
            x=retire_age, y=alt_level_2,
            text=f"은퇴 ({retire_age}세)",
            showarrow=True, arrowhead=2, arrowcolor=retire_line_color,
            font=dict(size=11, color="#F8FAFC", weight="bold"), ay=-20,
            bgcolor="rgba(15, 23, 42, 0.9)", bordercolor=retire_line_color, borderpad=3,
            row=1, col=1
        )

        # [Row 2] 0선 기준선
        fig_my_nta.add_hline(y=0, line_dash="solid", line_color="#94A3B8", line_width=1.5, row=2, col=1)

        # [Row 2] 흑자 영역 (녹색, 범례 숨김)
        fig_my_nta.add_trace(go.Scatter(
            x=ages_fine, y=surplus_fine, mode="lines",
            line=dict(width=0, color="rgba(0,0,0,0)"),
            fill='tozeroy', fillcolor='rgba(16, 185, 129, 0.28)',
            showlegend=False,
            hoverinfo="skip"
        ), row=2, col=1)

        # [Row 2] 적자 영역 (붉은색, 범례 숨김)
        fig_my_nta.add_trace(go.Scatter(
            x=ages_fine, y=deficit_fine, mode="lines",
            line=dict(width=0, color="rgba(0,0,0,0)"),
            fill='tozeroy', fillcolor='rgba(239, 68, 68, 0.28)',
            showlegend=False,
            hoverinfo="skip"
        ), row=2, col=1)

        # [Row 2] 연간 순수지 (범례: '소득-지출')
        fig_my_nta.add_trace(go.Scatter(
            x=ages_sim, y=net_flow, mode="lines",
            line=dict(color="#CBD5E1", width=2.4, shape='spline', smoothing=0.8),
            name="소득-지출",
            hovertemplate="나이: %{x}세<br>순수지: <b>%{y:,.0f}만 원</b><extra></extra>"
        ), row=2, col=1)

        # Row 2 중심축(y=0)에 착 붙인 흑자/적자 뱃지
        fig_my_nta.add_annotation(
            x=38, y=0,
            text="▲ 흑자 (소득 > 지출)", showarrow=False,
            yshift=14,
            font=dict(size=10.5, color="#86EFAC", weight="bold"),
            bgcolor="rgba(15, 23, 42, 0.8)", bordercolor="rgba(34, 197, 94, 0.5)", borderpad=2,
            row=2, col=1
        )
        fig_my_nta.add_annotation(
            x=68, y=0,
            text="▼ 적자 (지출 > 소득)", showarrow=False,
            yshift=-14,
            font=dict(size=10.5, color="#FCA5A5", weight="bold"),
            bgcolor="rgba(15, 23, 42, 0.8)", bordercolor="rgba(239, 68, 68, 0.5)", borderpad=2,
            row=2, col=1
        )

        # 전체 레이아웃 (모바일 3대 심플 범례)
        fig_my_nta.update_layout(
            height=490,
            margin=dict(l=10, r=10, t=25, b=25),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E2E8F0", size=12),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.03,
                xanchor="center",
                x=0.5,
                font=dict(size=11, color="#F1F5F9")
            ),
            hovermode="x unified"
        )

        # X축: 10세 단위 수평 고정
        fig_my_nta.update_xaxes(
            tickmode="linear", tick0=20, dtick=10,
            tickangle=0,
            tickfont=dict(size=12, color="#94A3B8"),
            gridcolor="rgba(100, 116, 139, 0.18)",
            fixedrange=True
        )
        fig_my_nta.update_xaxes(title=dict(text="연령 (세)", font=dict(size=12, color="#94A3B8")), row=2, col=1)

        # Y축
        fig_my_nta.update_yaxes(
            title=None,
            tickfont=dict(size=11, color="#94A3B8"),
            tickformat=",.0f",
            gridcolor="rgba(100, 116, 139, 0.18)",
            fixedrange=True
        )
        fig_my_nta.update_yaxes(range=[0, y_top], row=1, col=1)

        st.plotly_chart(fig_my_nta, use_container_width=True, config={"displayModeBar": False, "scrollZoom": False, "doubleClick": False, "showAxisDragHandles": False})

        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

        # 6.03.06 | 국가데이터처 통계
        st.markdown("### 3. 국가데이터처 통계")
        st.caption("※ 통계청 국민이전계정(NTA) 공식 발표 자료 기준")
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("한국인 평균 흑자 진입", "28세", help="노동소득이 소비를 추월하는 연령")
        col_m2.metric("최대 흑자 정점", "45세", "연 1,932만 원")
        col_m3.metric("평균 적자 재전환", "61세", help="은퇴 후 소비가 노동소득을 다시 초과")

        st.markdown("""
<div style="background: rgba(30, 41, 59, 0.55); border-left: 4px solid #F59E0B; border-radius: 6px; padding: 12px 18px; margin: 12px 0 16px 0;">
<div style="font-size: 15px; font-weight: 800; color: #FDE68A; margin-bottom: 6px;">👩‍👧 여성 출산·육아 경력단절의 현실 지표 (여성가족부·국가데이터처 조사)</div>
<div style="font-size: 13.5px; color: #CBD5E1; line-height: 1.6;">
• <b>재취업까지 소요 기간</b>: 평균 <b>7.5년</b> (단기 공백이 아닌 장기화)<br>
• <b>복귀 후 실질 임금</b>: 단절 이전의 약 <b>80% 수준</b>으로 하락
</div></div>
""", unsafe_allow_html=True)

        fig_official_nta = build_official_nta_chart()
        st.plotly_chart(fig_official_nta, use_container_width=True, config={"displayModeBar": False, "scrollZoom": False, "doubleClick": False, "showAxisDragHandles": False})
        
        st.markdown(f"""
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 14px;">
<a href="{OFFICIAL_PDF_URL}" target="_blank" style="background:#1E293B; border:1px solid #475569; border-radius:8px; padding:12px 14px; text-align:center; text-decoration:none; color:#38BDF8 !important; font-size:15px; font-weight:700; display:flex; align-items:center; justify-content:center; gap:8px;">
<span style="font-size:18px;">📄</span><span style="color:#38BDF8 !important;">2024년 국가데이터처 통계 보도자료</span>
</a>
<a href="{OFFICIAL_RELEASE_URL}" target="_blank" style="background:#1E293B; border:1px solid #475569; border-radius:8px; padding:12px 14px; text-align:center; text-decoration:none; color:#38BDF8 !important; font-size:15px; font-weight:700; display:flex; align-items:center; justify-content:center; gap:8px;">
<span style="font-size:18px;">🌐</span><span style="color:#38BDF8 !important;">국가데이터처 공식 발표 페이지</span>
</a></div>
""", unsafe_allow_html=True)
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

        # 6.03.07 | [위치 이동] 인생의 사계절과 맞이할 겨울의 시간 (사계절 카드)
        st.markdown("### 4. 인생의 사계절과 맞이할 겨울의 시간")
        if cur_age <= 27: cur_season = "spring"
        elif 28 <= cur_age <= 45: cur_season = "summer"
        elif 46 <= cur_age < retire_age: cur_season = "autumn"
        else: cur_season = "winter"

        def get_season_card_ui(season_key, icon, title, age_range, desc):
            is_current = (cur_season == season_key)
            card_border = "border: 2px solid #EA580C; background: rgba(234, 88, 12, 0.14);" if is_current else "border: 1px solid #334155; background: rgba(21, 30, 47, 0.7);"
            badge_html = "<div style='min-height:22px; margin-bottom:4px;'><span style='background:#EA580C; color:#FFFFFF; font-size:11.5px; font-weight:800; padding:2px 7px; border-radius:4px;'>📍 지금 나의 계절</span></div>" if is_current else "<div style='min-height:22px; margin-bottom:4px;'></div>"
            return f'<div class="soft-card" style="text-align:center; min-height:205px; {card_border} padding:14px 10px; margin:0;">{badge_html}<div style="font-size:28px;">{icon}</div><div style="font-size:16.5px; font-weight:800; color:#F8FAFC; margin:4px 0;">{title}</div><div style="font-size:13px; color:#94A3B8;">{age_range}</div><div style="font-size:13px; color:#CBD5E1; margin-top:8px; line-height:1.4;">{desc}</div></div>'

        card_spring = get_season_card_ui("spring", "🌱", "봄 (준비기)", "0세 ~ 27세", "부모님의 부양으로 배우고 성장하는 적자 구간")
        card_summer = get_season_card_ui("summer", "☀️", "여름 (성장기)", "28세 ~ 45세", "성실하게 일하여 가정을 일구고 최대 흑자를 만드는 시기")
        card_autumn = get_season_card_ui("autumn", "🍂", "가을 (결실기)", f"46세 ~ {retire_age}세", "자녀 독립 & 똘똘이의 파이프라인을 다질 골든타임")
        card_winter = get_season_card_ui("winter", "❄️", "겨울 (음미기)", f"{retire_age}세 ~ {life_expectancy}세", f"근로소득 중단 (통계청 {user_gender.split()[1]} {life_expectancy}세 수명)<br><b style='color:#38BDF8;'>약 {winter_years}년 ({winter_months}개월)</b>")

        s_col1, s_col2, s_col3, s_col4 = st.columns(4)
        with s_col1: st.markdown(card_spring, unsafe_allow_html=True)
        with s_col2: st.markdown(card_summer, unsafe_allow_html=True)
        with s_col3: st.markdown(card_autumn, unsafe_allow_html=True)
        with s_col4: st.markdown(card_winter, unsafe_allow_html=True)

        st.markdown(f"""
<div style="background: rgba(30, 41, 59, 0.6); border: 1px solid #334155; border-radius: 12px; padding: 18px 20px; margin: 16px 0 24px 0;">
<div style="font-size: 15px; color: #F8FAFC; line-height: 1.6; word-break: keep-all;">
💡 <b>산책로의 질문</b>: 은퇴 후 우리가 맞이할 겨울의 시간은 <b>약 {winter_years}년 ({winter_months:,}개월)</b>입니다. (통계청 {user_gender.split()[1]} 기대수명 {life_expectancy}세 기준)<br>
<span style="color: #94A3B8;">이 긴 겨울 동안 매달 무거운 물통을 지고 눈길을 걸을 것인가, 방 안에서 따뜻하게 흘러나오는 파이프라인을 맞이할 것인가는 <b>지금 '가을'의 준비</b>에 달려 있습니다.</span>
</div></div>
""", unsafe_allow_html=True)

        _, next_col = st.columns([5, 1])
        with next_col:
            if st.button("다음 →", key="seasons_next", use_container_width=True, type="primary"):
                st.session_state["_pending_nav"] = "AI 시선"
                st.rerun()


# ==============================================================================
# 6.04.00 | Tab 4 — AI 시선
# ==============================================================================
else:
    is_adv = st.session_state.get("advanced_mode", False)
    summary = current_financial_summary()
    person_name = st.session_state.get("person_name", "나")
    person_age = st.session_state.get("person_age", 35)

    if not is_adv:
        # [기본 모드] AI 1문단 자동 성찰 & 초대장 카드 + 심플한 [고급버튼]
        st.caption("AI는 평가자가 아닌, 내가 작성한 삶과 숫자를 객관적인 거울처럼 비춰주는 성찰 파트너입니다.")
        inc_val = float(getv("income_self", 0) or 0)
        exp_val = float(getv("expense_living", 0) or 0)
        surplus_val = inc_val - exp_val

        # 1문단 자동 생성
        if "basic_ai_comment" not in st.session_state or st.session_state.get("basic_ai_last_input") != (inc_val, exp_val):
            prompt_basic = f"""[역할 정의] 가계 재무를 객관적인 거울처럼 정직하고 따뜻하게 짚어주는 성찰 파트너.
인터뷰이: {person_name}님 (만 {person_age}세), 월 실수령 소득 {inc_val:,.0f}만 원, 월 기본 생활비 {exp_val:,.0f}만 원, 월 저축여력 {surplus_val:,.0f}만 원.
[요청 사항]
- 자기소개나 인사말 없이 '{person_name}님,'으로 시작하여 딱 1~2문장(120~180자 내외)으로 담백하고 다정하게 작성하세요.
- 현재 일상 수지의 플러스/마이너스 팩트를 정직하게 짚고, 노동을 멈추었을 때의 지속 가능성을 편안하게 성찰할 수 있는 화두를 던지세요."""
            with st.spinner("AI가 일상의 수지 밸런스를 성찰 중입니다..."):
                comment, _ = call_gemini_text(prompt_basic)
                st.session_state.basic_ai_comment = comment.strip() if comment else "일상의 소중한 현금흐름을 성찰 중입니다."
                st.session_state.basic_ai_last_input = (inc_val, exp_val)

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        st.markdown("### AI 성찰 리포트")
        st.markdown(f"""
<div class='soft-card' style='white-space: pre-wrap; line-height: 1.7; word-break: keep-all; font-size: 16px;'>
{st.session_state.get("basic_ai_comment", "")}
</div>
""", unsafe_allow_html=True)

        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

        # 6.04.02 | [기본 모드] 고급모드 초대장 카드 & 심플한 [고급버튼] (수정 멘트 반영)
        st.markdown("""
<div style="background: radial-gradient(circle at top, #1e293b 0%, #0b1120 100%); border: 1.5px solid #F59E0B; border-radius: 16px; padding: 24px 22px; text-align: center; box-shadow: 0 4px 18px rgba(245, 158, 11, 0.2); margin: 16px 0;">
<div style="font-size: 34px; margin-bottom: 6px;">📜</div>
<div style="font-size: 19px; font-weight: 850; color: #FDE68A; margin-bottom: 8px;">이게 다 일까요?</div>
<div style="font-size: 14.5px; color: #E2E8F0; line-height: 1.7; word-break: keep-all; max-width: 650px; margin: 0 auto 18px auto;">
만약 우리 집의 <b>진짜 순자산 궤적</b>과 <b>자녀 학자금·은퇴 타임라인</b>,<br>
그리고 숨겨진 <b>파이프라인의 가능성</b>까지 시뮬레이션해보고 싶다면..., 아래 <b>'고급버튼'</b>을 눌러보세요.
</div>
</div>
""", unsafe_allow_html=True)

        if st.button("고급버튼", type="primary", use_container_width=True, key="btn_unlock_advanced"):
            st.session_state["advanced_mode"] = True
            st.session_state["_pending_nav"] = "우리집 가계부"
            st.rerun()

    else:
        # [고급 모드] 모든 마이크로 모듈(6.04.01 ~ 6.04.07) 완전 탑재
        st.caption("AI는 평가자가 아닌, 내가 작성한 삶과 숫자를 객관적인 거울처럼 비춰주는 성찰 파트너입니다.")
        
        sib_names = [f"{it['label']}({it.get('age',0)}세)" for it in st.session_state.get("sibling_items", []) if it.get("age", 0) > 0]
        retire_age = st.session_state.get("retirement_age", 60)
        user_gender = st.session_state.get("gender", "🙋‍♂️ 남성")
        is_female = ("여성" in user_gender)
        life_expectancy = 87 if is_female else 81
        winter_years = max(0, life_expectancy - int(retire_age))
        child_count_str = st.session_state.get("child_count", "입력 안 함")

        q_self = active_quadrant(st.session_state.get("job_form", "직장인"))
        q_spouse = active_quadrant(st.session_state.get("job_spouse_form", ""))
        career_st = st.session_state.get("career_stage", "🌱 3년 이하 (초년생)")
        has_pipeline = (q_self in ["B", "I"]) or (q_spouse in ["B", "I"])

        family_desc = {}
        if getv("spouse_age", 0) > 0: family_desc["배우자"] = f"{int(getv('spouse_age'))}세"
        children_list = []
        if child_count_str in ["1명", "2명", "3명", "4명 이상"] and getv("child_age", 0) > 0: children_list.append(f"첫째 {int(getv('child_age'))}세")
        if child_count_str in ["2명", "3명", "4명 이상"] and getv("child_age2", 0) > 0: children_list.append(f"둘째 {int(getv('child_age2'))}세")
        if child_count_str in ["3명", "4명 이상"] and getv("child_age3", 0) > 0: children_list.append(f"셋째 {int(getv('child_age3'))}세")
        if child_count_str == "4명 이상" and getv("child_age4", 0) > 0: children_list.append(f"넷째 {int(getv('child_age4'))}세")
        if children_list: family_desc["자녀"] = f"총 {len(children_list)}명 ({', '.join(children_list)})"
        elif child_count_str == "없음": family_desc["자녀"] = "자녀 없음"
        if getv("father_age", 0) > 0: family_desc["아버지"] = f"{int(getv('father_age'))}세"
        if getv("mother_age", 0) > 0: family_desc["어머니"] = f"{int(getv('mother_age'))}세"

        details = {
            "이름/별칭": person_name, "나이": person_age, "성별": user_gender,
            "나의 소득 형태": f"{st.session_state.get('job_form','직장인')}({q_self})",
            "현업 경력 연차": career_st,
            "배우자 소득 형태": f"{st.session_state.get('job_spouse_form','해당 없음')}({q_spouse})",
            "파이프라인 보유 여부": "보유함 (사업가 B 또는 투자자 I 포함)" if has_pipeline else "미보유 (순수 근로/자영업 E·S)",
            "월수입(정기)": f"{summary['regular_income']:,.0f}만 원", "연간 상여금(비정기)": f"{summary['annual_bonus']:,.0f}만 원",
            "연간 총소득": f"{summary['annual_total_income']:,.0f}만 원", "월평균 지출": f"{summary['expenses']:,.0f}만 원",
            "연간 순저축 여력": f"{summary['annual_net_surplus']:,.0f}만 원 (월환산 {summary['monthly_effective_surplus']:,.0f}만 원)",
            "순자산": f"{summary['net_worth']/10000:,.2f}억 원 (자산 {summary['assets']:,.0f}만 원 - 부채 {summary['debts']:,.0f}만 원)",
            "은퇴 후 예상 월연금": f"{getv('income_pension', 0):,.0f}만 원", "은퇴 후 월 생활비": f"{getv('retirement_monthly_expenses', 200):,.0f}만 원",
            "희망 은퇴 나이": f"{retire_age}세 (은퇴 후 겨울 약 {winter_years}년, {user_gender.split()[1]} {life_expectancy}세 수명 기준)",
            "가족 구성": family_desc if family_desc else "기본 정보만 등록됨",
            "가족 계획": {"결혼": st.session_state.get("marriage_plan", "미정"), "출산/자녀": st.session_state.get("child_plan", "미정"), "주거": st.session_state.get("housing_plan", "미정")}
        }

        if q_self in ["B", "I"]:
            income_instruction = f"""[소득 개선 방향 - B/I 파이프라인 보유형 지침]
인터뷰이는 현재 사분면상 '{q_self}'(사업가/투자자)로서 이미 시스템과 자산에서 발생하는 파이프라인과 상당한 자산 기반({summary['net_worth']/10000:,.1f}억 원)을 확보하고 계십니다.
절대 억지로 노동 의존형 물통이라고 규정하지 마시고, 구축하신 파이프라인과 자산의 성취를 있는 그대로 존중하세요.
배우자의 노동 소득이 결합되어 있다면 가계 전체의 현금흐름 다변화 및 사업 시스템의 영속성을 점검하는 관점을 객관적으로 비춰주세요."""
        else:
            income_instruction = f"""[소득 개선 방향 - E/S 근로/자영업 지침]
현재 부부의 소득은 일손을 멈추면 수입이 중단되는 노동 의존형(E/S) 성격임을 정중하게 짚으세요.
본업을 충실히 유지하면서, 시간과 노동력에만 매이지 않고 시스템과 자산에서 흘러나오는 '파이프라인'을 장기적으로 준비해야 하는 이유를 객관적인 관점에서 정중히 제안하세요."""

        current_taste_val = st.session_state.get("pills_ai_taste", "🧭 보통맛 (정직한 거울)")
        short_taste_tag = "☕ 순한맛" if "순한맛" in current_taste_val else ("🌶️ 매운맛" if "매운맛" in current_taste_val else "🧭 보통맛")
        expander_title = f"⚙️ AI 프롬프트 설정 [{short_taste_tag}]"

        with st.expander(expander_title, expanded=False):
            st.markdown("<div style='font-size:16px; font-weight:800; color:#F8FAFC; margin-bottom:6px;'>1. 분석 강도(맛) 선택</div>", unsafe_allow_html=True)
            taste_mode = st.pills("분석 강도 선택", ["☕ 순한맛 (위로/은유)", "🧭 보통맛 (정직한 거울)", "🌶️ 매운맛 (뼈아픈 직언)"], default="🧭 보통맛 (정직한 거울)", key="pills_ai_taste", label_visibility="collapsed")
            st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:16px; font-weight:800; color:#F8FAFC; margin-bottom:6px;'>2. AI 핵심 원칙 (선택 및 제외)</div>", unsafe_allow_html=True)
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                chk_1 = st.checkbox("평가/가르침 배제, '객관적 거울' 유지", value=True, key="chk_r1")
                chk_2 = st.checkbox("훈계, 잔소리, 공포 유발, 결론 강요 금지", value=True, key="chk_r2")
                chk_3 = st.checkbox("데이터에 없는 사실(결혼/주거 등) 임의 추정 금지", value=True, key="chk_r3")
            with col_r2:
                chk_4 = st.checkbox("계산된 예상값과 실현된 사실 엄격 구분", value=True, key="chk_r4")
                chk_5 = st.checkbox("순자산 0원이나 초년생 단계를 실패로 규정 금지", value=True, key="chk_r5")
                chk_6 = st.checkbox("사분면/경력만으로 소득 성격이나 안정성 단정 금지", value=True, key="chk_r6")
            st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:16px; font-weight:800; color:#F8FAFC; margin-bottom:6px;'>3. ✍️ 내가 직접 추가할 요청 사항 (선택)</div>", unsafe_allow_html=True)
            user_custom_instruction = st.text_area("추가 요청사항", placeholder="예: 30대 초반 주거 독립과 차량 유지비 관점도 함께 짚어줘", height=70, key="inp_user_custom_prompt", label_visibility="collapsed")

        if "순한맛" in taste_mode:
            taste_directive = """[분석 톤앤매너: ☕ 순한맛]
- 직접적이거나 뼈아픈 표현을 지양하고, 은유적이고 다정하며 온기 있는 어조를 유지하세요.
- 조상의 지혜인 "산 입에 거미줄 치랴"의 넉넉한 여유를 담고, 불안감을 자극하지 마세요.
- 지금까지 성실하게 삶을 꾸려온 노고에 대한 깊은 인정과 위로를 중심으로 부드럽게 서술하세요."""
        elif "매운맛" in taste_mode:
            taste_directive = """[분석 톤앤매너: 🌶️ 매운맛]
- 겉치레 립서비스와 안일한 위로를 일체 배제하고, 냉정하고 서늘할 정도로 팩트를 직설적으로 서술하세요.
- 숫자가 가리키는 결손과 한계를 에둘러 말하지 말고 명확히 짚어, 환상을 깨고 현실을 직시할 수 있도록 뼈아프게 직언하세요."""
        else:
            taste_directive = """[분석 톤앤매너: 🧭 보통맛]
- 힘을 빼고, 정직하되, 전문가답고, 정중한 태도를 견지하세요.
- 과도한 낙관론과 과장된 위협을 모두 배제하고, 숫자를 있는 그대로 차분히 비춰주는 객관적 거울의 태도를 유지하세요."""

        active_principles = []
        if chk_1: active_principles.append("당신은 인터뷰이를 평가하거나 가르치지 않는 '정직하고 따뜻한 객관적 거울'입니다.")
        if chk_2: active_principles.append("훈계, 잔소리, 공포를 유발하는 표현, 특정 행동이나 결론의 강요를 금지합니다.")
        active_principles.append("자기소개, 인사말, 마크다운 가로선(---)을 쓰지 마세요.")
        active_principles.append(f"[호칭 규칙]: [소득 개선 방향] 첫머리에서만 '{person_name}님,'을 사용할 수 있습니다. [은퇴 안정성]에서는 이름을 다시 부르지 마세요.")
        active_principles.append(f"경력 단계({career_st}), 순자산 및 가족 생애 정보는 입력 데이터가 실제로 뒷받침하는 범위에서만 활용하세요.")
        if chk_4: active_principles.append("입력된 사실, 수치로 계산할 수 있는 결과, 아직 확인되지 않은 가능성을 구분하세요. 계산된 예상값을 실제로 실현된 사실처럼 표현하지 마세요.")
        if chk_3: active_principles.append("데이터에 없거나 '미정', '미등록', 공란으로 표시된 정보는 임의로 추정하지 마세요. 결혼, 출산, 주택 구입, 부모 지원 등의 계획을 예정된 사실처럼 서술하지 마세요.")
        if chk_6: active_principles.append("사분면이나 경력 단계만으로 실제 소득의 성격, 파이프라인 보유 여부 또는 재무적 안정성을 단정하지 마세요.")
        if chk_5: active_principles.append("순자산이 적거나 0에 가깝더라도 이를 실패로 규정하지 마세요. 소득, 지출, 저축 여력 등 다른 지표와 함께 해석하세요.")
        active_principles.append("입력된 자료만으로 판단할 수 없는 사항은 단정하지 말고, 필요한 경우 확인이 필요하다고 짧게 밝혀주세요.")

        principles_text = "\n".join([f"{i+1}. {p}" for i, p in enumerate(active_principles)])
        custom_section = f"\n[사용자 맞춤 추가 요청사항]\n{user_custom_instruction.strip()}" if user_custom_instruction.strip() else ""

        full_prompt_text = f"""[절대 엄수 원칙]
{principles_text}
{taste_directive}
{custom_section}

[인터뷰이 재무 및 생애 데이터]
{json.dumps(details, ensure_ascii=False, indent=2)}

[요청 사항]
아래 두 제목을 지정된 순서와 표기 그대로 사용하세요.
각 제목 다음 줄부터 본문을 작성하세요. 각 본문은 250~350자 내외로 하되, 분량을 채우기 위해 근거 없는 설명을 추가하지 마세요.

[소득 개선 방향]
{income_instruction}
현재 소득 구조와 재무 데이터에서 실제로 의미 있는 특징을 중심으로 서술하세요. 경력 단계, 저축 여력, 소득 성장 가능성, 가구의 소득 구성 중 근거가 있는 항목을 선택하세요. 파이프라인이나 자산소득은 필요성과 여건이 확인되는 경우에만 선택지로 제시하세요. 정중하고 담백한 존댓말을 사용하세요.

[은퇴 안정성]
반드시 '은퇴 안정성 측면에서는'으로 시작하고 이름을 부르지 마세요.
은퇴 후 월 희망 생활비와 예상 월연금의 차이를 설명하되, 입력된 값의 성격과 산출 근거가 불분명하면 안정성이 확보되었다고 단정하지 마세요. 두 금액의 단순 차액과 실제 은퇴 안정성은 구분하세요.
은퇴 후 약 {winter_years}년은 통계청 {user_gender.split()[1]} 기대수명({life_expectancy}세)에 기초한 계산상 가정으로 취급하세요. 현재 경력 단계와 순자산을 연결해 설명하되, 실제 현금 보유액이나 유동성 자료가 없다면 유동성 준비 상태를 평가하지 마세요. 결혼, 자녀, 주거 계획 등 확인되지 않은 미래 사건을 전제로 삼지 말고, 정중하고 담백하게 서술하세요."""

        if st.button("⚡ AI 리포트 생성", type="primary", use_container_width=True):
            st.session_state.ai_summary = summary
            st.session_state.ai_comment = None
            with st.spinner(f"AI가 {taste_mode.split()[0]} 모드로 지표를 분석 중입니다 (약 15~20초 소요)..."):
                comment, error = call_gemini_text(full_prompt_text)
                st.session_state.ai_comment = comment if comment else error
            st.rerun()

        if st.session_state.get("ai_summary") and st.session_state.get("ai_comment"):
            s = st.session_state.ai_summary
            st.markdown("### 재무제표 요약")
            cols = st.columns(4)
            cols[0].metric("월 정기수입", money(s["regular_income"]))
            cols[1].metric("월 현금지출", money(s["expenses"]))
            cols[2].metric("연간 순저축", money(s["annual_net_surplus"]), f"월환산 {money(s['monthly_effective_surplus'])}")
            cols[3].metric("순자산", fmt_eok(s["net_worth"]))

            st.markdown("### AI (Gemini) 리포트")
            comment_text = str(st.session_state.get("ai_comment", ""))
            cleaned_text = re.sub(r'-{3,}', '', comment_text)
            cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text.strip())
            normalized = cleaned_text.replace("\r\n", "\n").replace("\r", "\n")
            match_retire = re.search(r"(?im)^\s*(?:#{1,6}\s*)?(?:\*\*|__)?\s*(?:\[\s*)?은퇴\s*안정성\s*(?:\])?\s*(?:\*\*|__)?\s*:?\s*$", normalized)
            if match_retire:
                income_comment = normalized[:match_retire.start()]
                retirement_comment = normalized[match_retire.end():]
            else:
                income_comment, retirement_comment = normalized, ""

            income_comment = re.sub(r"(?i)\[\s*소득\s*개선\s*방향\s*\]", "", income_comment).strip()
            retirement_comment = re.sub(r"(?i)\[\s*은퇴\s*안정성\s*\]", "", retirement_comment).strip()
            noise_pattern = r"(?i)^.*?살펴보겠습니다[\.\!\?\s\n]*"
            income_comment = re.sub(noise_pattern, "", income_comment).strip()
            retirement_comment = re.sub(noise_pattern, "", retirement_comment).strip()
            retirement_comment = re.sub(r"^(?:.*?님[\,\s]*)+", "", retirement_comment).strip()

            def format_readable_paragraph(txt):
                sentences = re.split(r'(?<=[.!?])\s+', txt.strip())
                if len(sentences) <= 2: return txt.strip()
                grouped = [" ".join(sentences[i:i+2]) for i in range(0, len(sentences), 2)]
                return "\n\n".join(grouped)

            formatted_income = format_readable_paragraph(income_comment)
            formatted_retire = format_readable_paragraph(retirement_comment)

            st.markdown("#### 소득 개선 관점 (파이프라인)")
            st.markdown(f"""
<div class='soft-card' style='white-space: pre-wrap; line-height: 1.7; word-break: keep-all;'>
{formatted_income or '분석 결과를 정리 중입니다. 다시 시도해 주세요.'}
</div>
""", unsafe_allow_html=True)

            st.markdown("#### 은퇴 안정성 관점")
            st.markdown(f"""
<div class='soft-card' style='white-space: pre-wrap; line-height: 1.7; word-break: keep-all;'>
{formatted_retire}
</div>
""", unsafe_allow_html=True)

            st.caption("※ AI의 코멘트는 참고용 거울이며, 삶의 가장 중요한 결정은 온전히 당신의 것입니다.")

            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
            sync_code = export_diagnosis_code()
            kakao_clean_report = f"""[나침반 🧭 현실점검 & 재무 진단 리포트]
• 진단자: {person_name} ({person_age}세, {career_st})
• 소득 형태: {st.session_state.get('job_form','직장인')} (배우자: {st.session_state.get('job_spouse_form','해당 없음')})
• 분석 모드: {taste_mode}
• 재무 요약:
  - 월 정기수입: {money(s['regular_income'])}
  - 월 현금지출: {money(s['expenses'])}
  - 연간 순저축: {money(s['annual_net_surplus'])} (월평균 {money(s['monthly_effective_surplus'])})
  - 순자산: {fmt_eok(s['net_worth'])}
  - 희망 은퇴나이: {retire_age}세 (맞이할 겨울: 약 {winter_years}년, {user_gender.split()[1]} {life_expectancy}세 수명 기준)

[소득 개선 & 파이프라인]
{formatted_income}

[은퇴 안정성 성찰]
{formatted_retire}"""
            st.markdown("### 💬 카카오톡 전송용 리포트")
            st.caption("※ 아래 리포트를 복사하여 카카오톡 대화방에 바로 붙여넣기(Ctrl+V)하세요.")
            st.code(kakao_clean_report, language="markdown")

            st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
            copy_btn_html = f"""
<!DOCTYPE html><html><head><meta charset="utf-8"><style>body {{ margin: 0; padding: 0; background: transparent; overflow: hidden; }} #copyBtn {{ background: #1E293B; border: 1.5px solid #38BDF8; color: #38BDF8; padding: 10px 18px; border-radius: 8px; font-weight: 800; font-size: 15px; cursor: pointer; display: inline-flex; align-items: center; gap: 8px; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; transition: background 0.15s ease; }} #copyBtn:hover {{ background: #334155; color: #FFFFFF; }}</style></head>
<body><button id="copyBtn"><span>🔑</span><span>동기화 복원코드 복사</span></button><script>document.getElementById('copyBtn').addEventListener('click', function() {{ var code = '{sync_code}'; var ta = document.createElement('textarea'); ta.value = code; ta.style.position = 'fixed'; ta.style.left = '-999999px'; ta.style.top = '-999999px'; document.body.appendChild(ta); ta.focus(); ta.select(); var success = false; try {{ success = document.execCommand('copy'); }} catch (e) {{ success = false; }} document.body.removeChild(ta); if (!success && navigator.clipboard && window.isSecureContext) {{ navigator.clipboard.writeText(code).then(function() {{ alert('동기화 복원코드가 복사되었습니다!\\n인터뷰어에게 카톡으로 붙여넣기(Ctrl+V)해 주세요.'); }}).catch(function() {{ prompt('복원코드를 직접 복사(Ctrl+C)하세요:', code); }}); }} else if (success) {{ alert('동기화 복원코드가 복사되었습니다!\\n인터뷰어에게 카톡으로 붙여넣기(Ctrl+V)해 주세요.'); }} else {{ prompt('복원코드를 직접 복사(Ctrl+C)하세요:', code); }} }});</script></body></html>
"""
            st.components.v1.html(copy_btn_html, height=54)

        else:
            st.info("‘AI 리포트 생성’ 버튼을 누르면 Gemini 초고속 엔진이 삶과 재무의 성찰 리포트를 생성합니다.")

        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        # 6.04.07 | 📋 AI 질의용 재무제표 expander
        with st.expander("📋 AI 질의용 재무제표"):
            st.markdown("<div style='font-size: 13.5px; color: #94A3B8; margin-bottom: 8px;'>프롬프트 지시문 없이, 내가 입력한 재무제표와 가족 생애 통계만 정리된 텍스트입니다. ChatGPT 등에 복사해서 자유롭게 추가 상담을 진행할 수 있습니다.</div>", unsafe_allow_html=True)
            raw_summary_report = f"""### 나침반 재무제표 및 생애주기 요약 데이터
- 성명(별칭): {person_name} (만 {person_age}세, {user_gender}, {career_st})
- 가구 소득 형태: 나({st.session_state.get('job_form','직장인')}) + 배우자({st.session_state.get('job_spouse_form','해당 없음')})
- 월 정기 수입: {summary['regular_income']:,.0f}만 원
- 연간 비정기 상여금: {summary['annual_bonus']:,.0f}만 원
- 연간 총소득: {summary['annual_total_income']:,.0f}만 원
- 월평균 생활비 및 지출: {summary['expenses']:,.0f}만 원
- 연간 실질 순저축: {summary['annual_net_surplus']:,.0f}만 원 (월환산 {summary['monthly_effective_surplus']:,.0f}만 원)
- 자산 합계: {summary['assets']:,.0f}만 원
- 부채 잔액: {summary['debts']:,.0f}만 원
- 현재 순자산: {summary['net_worth']/10000:,.2f}억 원
- 은퇴 예정 나이: {retire_age}세 (은퇴 후 맞이할 겨울 약 {winter_years}년, {user_gender.split()[1]} {life_expectancy}세 수명 기준)
- 은퇴 후 예상 월연금: {getv('income_pension', 0):,.0f}만 원
- 은퇴 후 월 희망 생활비: {getv('retirement_monthly_expenses', 200):,.0f}만 원
- 가족 구성: {', '.join([f'{k}: {v}' for k, v in family_desc.items()]) if family_desc else '미등록'}"""
            st.code(raw_summary_report, language="markdown")

        # [위치 이동] 상단에서 화면 맨 아래로 정갈하게 내려온 기본 모드 전환 버튼
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        _, adv_btm_col = st.columns([4, 1])
        with adv_btm_col:
            if st.button("🌿 기본 모드로 전환", key="btn_lock_basic_bottom", use_container_width=True):
                st.session_state["advanced_mode"] = False
                st.session_state["_pending_nav"] = "우리집 가계부"
                st.rerun()
