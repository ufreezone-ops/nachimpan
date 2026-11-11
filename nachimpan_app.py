#########################################################
# -------------------------------------------------------
# 1.00 | 시스템 환경 및 전역 테마 엔진
# -------------------------------------------------------
#########################################################

#########################################################
# 1.01 | 라이브러리 로드 및 기본 페이지 설정
#########################################################

#--------------------------------------------------------
# 1.01.01 | 필수 및 서드파티 라이브러리 임포트
#--------------------------------------------------------
import os
from pathlib import Path
import random
import json
import base64
import requests
import re
from datetime import date
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

#--------------------------------------------------------
# 1.01.02 | Streamlit 기본 페이지 및 레이아웃 설정
#--------------------------------------------------------
st.set_page_config(
    page_title="나침반 — 나의 삶을 바라보는 산책로",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

#########################################################
# 1.02 | 전역 통합 테마 디자인 시스템 CSS
#########################################################

#--------------------------------------------------------
# 1.02.01 | 전역 스크롤 안정화 및 상단 헤더 다크 일체화
#--------------------------------------------------------
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

/* 본문 텍스트 배치를 유지하고, 옆의 문자형 출처 표식만 클릭 가능하게 표시 */
.st-key-source_retirement_expense,
.st-key-source_nta_basic,
.st-key-source_nta_generational {
    width: auto !important;
    min-width: 0 !important;
    max-width: max-content !important;
    flex: 0 0 auto !important;
    margin-left: 0.1rem !important;
}
.st-key-source_retirement_expense [data-testid="stButton"] button,
.st-key-source_nta_basic [data-testid="stButton"] button,
.st-key-source_nta_generational [data-testid="stButton"] button,
.st-key-expense-panel [data-testid="stPopoverButton"],
.st-key-expense-panel [data-testid="stPopover"] button {
    width: auto !important;
    min-width: 0 !important;
    max-width: max-content !important;
    height: auto !important;
    min-height: 0 !important;
    padding: 0 0.12rem !important;
    margin: 0 !important;
    border: 0 !important;
    background: transparent !important;
    background-color: transparent !important;
    background-image: none !important;
    box-shadow: none !important;
    border-radius: 0 !important;
    color: #38BDF8 !important;
    -webkit-text-fill-color: #38BDF8 !important;
    font-size: 0.9rem !important;
    line-height: 1 !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    flex: 0 0 auto !important;
}
.st-key-source_retirement_expense [data-testid="stButton"] button:hover,
.st-key-source_nta_basic [data-testid="stButton"] button:hover,
.st-key-source_nta_generational [data-testid="stButton"] button:hover,
.st-key-expense-panel [data-testid="stPopoverButton"]:hover,
.st-key-expense-panel [data-testid="stPopover"] button:hover {
    background: transparent !important;
    background-color: transparent !important;
    background-image: none !important;
    border: 0 !important;
    box-shadow: none !important;
    color: #7DD3FC !important;
    -webkit-text-fill-color: #7DD3FC !important;
    text-decoration: underline !important;
}
.st-key-source_retirement_expense [data-testid="stButton"] button p,
.st-key-source_nta_basic [data-testid="stButton"] button p,
.st-key-source_nta_generational [data-testid="stButton"] button p,
.st-key-expense-panel [data-testid="stPopoverButton"] p,
.st-key-expense-panel [data-testid="stPopover"] button p {
    font-size: inherit !important;
    line-height: 1 !important;
    margin: 0 !important;
}
/* 대출 팝오버는 기존 입력 라벨 크기와 정렬을 유지 */
.st-key-expense-panel [data-testid="stPopoverButton"],
.st-key-expense-panel [data-testid="stPopover"] button {
    font-size: inherit !important;
    font-weight: 400 !important;
    line-height: inherit !important;
    justify-content: flex-start !important;
}
.st-key-loan_payment_source_link {
    display: none !important;
}
/* 탭1: 제목 앵커 표시는 숨기고 제목 영역을 글자 너비만 사용 */
.st-key-retirement-title-row [data-testid="stElementContainer"]:has(h3) {
    flex: 0 0 auto !important;
    width: max-content !important;
    min-width: 0 !important;
}
.st-key-retirement-title-row h3 {
    white-space: nowrap !important;
}
/* Streamlit이 제목에 자동으로 붙이는 내부 앵커 링크 아이콘 숨김 */
.st-key-retirement-title-row [data-testid="stHeaderActionElements"],
.st-key-retirement-title-row h3 a[aria-label="Link to heading"] {
    display: none !important;
}
/* 제목과 나침반을 같은 기준선에 배치 */
.st-key-retirement-title-row [data-testid="stHorizontalBlock"] {
    align-items: baseline !important;
    column-gap: 0.15rem !important;
}
.st-key-source_retirement_expense {
    width: auto !important;
    min-width: 0 !important;
    max-width: max-content !important;
    flex: 0 0 auto !important;
    margin: 0 0 0 0.1rem !important;
    transform: translateY(0.08rem) !important;
}
/* PC: 제목과 아이콘 사이 간격을 현재의 절반으로 */
@media (min-width: 769px) {
    .st-key-retirement-title-row [data-testid="stHorizontalBlock"] {
        column-gap: 0.075rem !important;
    }
    .st-key-source_retirement_expense {
        margin-left: 0.05rem !important;
    }
}
/* 모바일 공통: 실제 아이콘 요소의 왼쪽 여백으로 제목과 간격 확보 */
@media (max-width: 1024px) and (pointer: coarse) {
    .st-key-retirement-title-row [data-testid="stHorizontalBlock"] {
        column-gap: 0 !important;
    }
    div.st-key-source_retirement_expense {
        width: auto !important;
        min-width: 0 !important;
        max-width: max-content !important;
        flex: 0 0 auto !important;
        margin: 0 !important;
    }
    /* 버튼 안에 얇은 공백을 넣어 제목과 나침반 사이를 시각적으로 분리 */
    .st-key-source_retirement_expense [data-testid="stButton"] button p::before {
        content: " ";
        white-space: pre;
    }
}
/* 모바일 세로보기: 제목 중심에 맞춰 아이콘을 아래로 미세 조정 */
@media (max-width: 600px) and (orientation: portrait) and (pointer: coarse) {
    .st-key-source_retirement_expense {
        transform: translateY(0.3rem) !important;
    }
}
/* 모바일 가로보기: 세로보기보다 덜 내려 기준선에 맞춤 */
@media (orientation: landscape) and (max-height: 500px) and (pointer: coarse) {
    .st-key-source_retirement_expense {
        transform: translateY(0.08rem) !important;
    }
}
.st-key-source_retirement_expense [data-testid="stButton"] button,
.st-key-source_retirement_expense [data-testid="stButton"] button:hover,
.st-key-source_retirement_expense [data-testid="stButton"] button:focus,
.st-key-source_retirement_expense [data-testid="stButton"] button:focus-visible,
.st-key-source_retirement_expense [data-testid="stButton"] button:active {
    width: auto !important;
    min-width: 0 !important;
    min-height: 0 !important;
    height: auto !important;
    padding: 0 !important;
    margin: 0 !important;
    border: 0 !important;
    outline: 0 !important;
    background: transparent !important;
    background-color: transparent !important;
    box-shadow: none !important;
    color: #38BDF8 !important;
    -webkit-text-fill-color: #38BDF8 !important;
    font-size: 1.3rem !important;
    line-height: 1 !important;
    text-decoration: none !important;
    justify-content: center !important;
}
.st-key-source_retirement_expense [data-testid="stButton"] button p {
    margin: 0 !important;
    font-size: 1.3rem !important;
    line-height: 1 !important;
    text-decoration: none !important;
}

/* 통계 자료실의 산출 방법 팝오버 버튼: primary 색상과 명시적 배경 지정 */
.st-key-retirement-source-details [data-testid="stPopoverButton"],
.st-key-retirement-source-details [data-testid="stPopover"] button,
div.st-key-retirement-source-details button {
    width: auto !important;
    min-width: 0 !important;
    padding: 0.38rem 0.75rem !important;
    background: #0284C7 !important;
    background-color: #0284C7 !important;
    background-image: none !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    border: 1px solid #38BDF8 !important;
    border-radius: 999px !important;
    font-weight: 700 !important;
    box-shadow: 0 1px 5px rgba(2, 132, 199, 0.24) !important;
}
.st-key-retirement-source-details [data-testid="stPopoverButton"]:hover,
.st-key-retirement-source-details [data-testid="stPopover"] button:hover,
div.st-key-retirement-source-details button:hover {
    background: #0369A1 !important;
    background-color: #0369A1 !important;
    background-image: none !important;
    border-color: #7DD3FC !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}
/* 대표사례의 자동 계산 대출 상환액도 일반 입력창과 같은 명도·글자색으로 표시 */
.st-key-expense_loan_case_45_female_45 [data-testid="stNumberInput"] input:disabled {
    opacity: 1 !important;
    background-color: var(--nc-card-bg) !important;
    color: var(--nc-text) !important;
    -webkit-text-fill-color: var(--nc-text) !important;
    border-color: var(--nc-border) !important;
}
</style>
""", unsafe_allow_html=True)

#--------------------------------------------------------
# 1.02.02 | 전역 색상 디자인 토큰 및 가독성 폰트 설정
#--------------------------------------------------------
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

#--------------------------------------------------------
# 1.02.03 | 패널 및 위젯 스타일링
#--------------------------------------------------------
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

#--------------------------------------------------------
# 1.02.04 | 특수 컴포넌트(카카오 옐로우 & expander) 스타일링
#--------------------------------------------------------
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


#########################################################
# 1.03 | 공식 통계 벤치마크 및 전역 상수
#########################################################
#--------------------------------------------------------
# 1.03.01 | 국민이전계정(NTA) 데이터셋 및 공식 URL
#--------------------------------------------------------
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



#########################################################
# -------------------------------------------------------
# 2.00 | 상태 관리 및 재무 유틸리티 엔진
# -------------------------------------------------------
#########################################################
#########################################################
# 2.01 | 세션 상태 및 진단 데이터 관리 엔진
#########################################################
#--------------------------------------------------------
# 2.01.01 | 세션 키 초기화 및 안전 조회 헬퍼
#--------------------------------------------------------
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
    
#--------------------------------------------------------
# 2.01.02 | 테스트 사례 저장용 데이터 키 목록
#--------------------------------------------------------
CASE_DATA_KEYS = [
    "anonymous_id", "person_name", "person_age", "gender", "job_form", "job_spouse_form", "career_stage",
    "income_self", "income_spouse", "income_other", "income_bonus", "income_pension",
    "other_pension_self_enabled", "other_pension_self_amount", "other_pension_self_age",
    "other_pension_spouse_enabled", "other_pension_spouse_amount", "other_pension_spouse_age",
    "expense_living", "expense_loan", "expense_other", "expense_scale_reference_annual", "retirement_monthly_expenses",
    "asset_cash", "asset_financial", "asset_home", "asset_deposit", "asset_other",
    "debt_home", "debt_other", "retirement_age", "spouse_age", "child_count",
    "child_age", "child_age2", "child_age3", "child_age4", "father_age", "mother_age",
    "marriage_plan", "child_plan", "housing_plan", "sibling_items", "advanced_mode"
]

#--------------------------------------------------------
# 2.01.03 | 대표 체험 사례 및 저장/불러오기
#--------------------------------------------------------
from datetime import datetime

# [인터뷰어 전용 체험 사례 2종] - 위젯 키 완벽 바인딩
INTERVIEWER_CASES = {
    "case_32_female": {
        "person_name": "32세 여성 (미혼, 4년차)",
        "person_age": 32,
        "gender": "🙋‍♀️ 여성",
        "job_form": "직장인",
        "job_spouse_form": "해당 없음",
        "career_stage": "🌿 4~9년 (성장기)",
        "income_self": 275, "income_spouse": 0, "income_other": 0,
        "income_bonus": 0, "income_pension": 120,  # 2024 여성 30~34세 중위 세전 305.6 × 90% ≈ 실수령 275; 보너스 중복 방지
        "expense_living": 225, "expense_loan": 0, "expense_other": 300,  # 통계 비교 월환산: 225 + 300/12 = 250만 원(30~34세·1인 가구 중위 251.77만 원 근사)
        "retirement_monthly_expenses": 270,
        "asset_cash": 800, "asset_financial": 700, "asset_home": 0, "asset_deposit": 0, "asset_other": 0,
        "debt_home": 0, "debt_other": 0,
        "retirement_age": 60, "spouse_age": 0,
        "child_count": "없음",
        "child_count_select_direct": "없음",  # 위젯에 직격 주입
        "child_age": 0, "child_age2": 0, "child_age3": 0, "child_age4": 0,
        "father_age": 63, "mother_age": 60,
        "marriage_plan": "1~3년 내 결혼 생각 있음",
        "child_plan": "자녀 계획 있음",
        "housing_plan": "주택 구입 고려",
        "target_housing_age": 39,  # 2024 주거실태조사 가중 중앙값
        "housing_region": "부산",
        "housing_region_select": "부산",    # 위젯에 직격 주입
        "housing_ltv": 35.0,
        "income_pension_self": 60,
        "income_pension_spouse": 60,
        "pension_start_age": 65
    },
    "case_45_female": {
        "person_name": "45세 여성 (기혼, 재취업)",
        "person_age": 45,
        "gender": "🙋‍♀️ 여성",
        "job_form": "직장인",
        "job_spouse_form": "직장인",
        "career_stage": "🌿 4~9년 (성장기)",
        "income_self": 240, "income_spouse": 430, "income_other": 0,
        "income_bonus": 0,  # 월평균 보수 통계와 상여 중복 방지
        "income_pension": 120,  # 본인 45~49세 여성 중위 266.2 × 90%; 배우자 45~49세 남성 중위 478.8 × 90%
        "expense_living": 420, "expense_loan": 67, "expense_other": 500,  # 월 원리금 약 66.84만 원(화면 67); 통계 비교에는 73회차 이자 약 41.21만 원만 포함
        "retirement_monthly_expenses": 270,
        "asset_cash": 1500, "asset_financial": 2500, "asset_home": 40000, "asset_deposit": 0, "asset_other": 0,
        "debt_home": 12000, "debt_other": 0,  # 계산 잔액 12,362만 원을 인터뷰 입력값 기준으로 천만 원 단위 반올림
        "retirement_age": 60, "spouse_age": 47,
        "child_count": "1명",
        "child_count_select_direct": "1명",   # 위젯에 직격 주입
        "child_age": 15, "child_age2": 0, "child_age3": 0, "child_age4": 0,
        "father_age": 75, "mother_age": 72,
        "marriage_plan": "결혼함",
        "child_plan": "계획 없음",
        "housing_plan": "현재 주거 유지",
        "target_housing_age": 39,  # 2024 주거실태조사 가중 중앙값
        "housing_region": "부산",
        "housing_region_select": "부산",    # 위젯에 직격 주입
        "housing_ltv": 35.0,
        "income_pension_self": 60,
        "income_pension_spouse": 60,
        "pension_start_age": 65
    }
}
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
        "expense_living": 150, "expense_loan": 0, "expense_other": 360,
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
        "expense_living": 280, "expense_loan": 130, "expense_other": 960,
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
        "expense_living": 300, "expense_loan": 50, "expense_other": 1200,
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
        for key in CASE_DATA_KEYS
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


#########################################################
# 2.02 | 재무 포맷팅 및 집계 로직
#########################################################
#--------------------------------------------------------
# 2.02.01 | 금액 및 억 단위 표시 포맷터
#--------------------------------------------------------
def money(value):
    return f"{value:,.0f}만 원"

def fmt_eok(value):
    if abs(value) >= 10000:
        return f"{value / 10000:,.2f}억 원"
    return money(value)

#--------------------------------------------------------
# 2.02.02 | 직업-ESBI 사분면 매핑 함수
#--------------------------------------------------------
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

#--------------------------------------------------------
# 2.02.03 | 가계 종합 재무 집계 엔진
#--------------------------------------------------------
# [주택대출 표준 가정] 대표사례 내부 상환모형 (금액 단위: 만 원)
REPRESENTATIVE_HOME_PRICE_MAN = 40000.0
REPRESENTATIVE_MORTGAGE_LTV = 0.35
REPRESENTATIVE_MORTGAGE_PRINCIPAL_MAN = REPRESENTATIVE_HOME_PRICE_MAN * REPRESENTATIVE_MORTGAGE_LTV
REPRESENTATIVE_MORTGAGE_PURCHASE_AGE = 39
REPRESENTATIVE_MORTGAGE_TERM_YEARS = 30
REPRESENTATIVE_MORTGAGE_ANNUAL_RATE = 0.04

def mortgage_monthly_split(principal_man, annual_rate, term_years, payment_number):
    """원리금 균등상환의 특정 회차 원금·이자 분리."""
    monthly_rate = annual_rate / 12.0
    total_months = int(term_years * 12)
    if principal_man <= 0 or total_months <= 0 or not 1 <= payment_number <= total_months:
        return 0.0, 0.0, 0.0
    payment = (
        principal_man / total_months if monthly_rate == 0
        else principal_man * monthly_rate / (1.0 - (1.0 + monthly_rate) ** (-total_months))
    )
    balance = principal_man
    for _ in range(1, payment_number):
        balance -= payment - balance * monthly_rate
    interest = balance * monthly_rate
    principal_payment = min(balance, payment - interest)
    return payment, principal_payment, interest

def mortgage_balance_after_payments(principal_man, annual_rate, term_years, payments_made):
    """일정 회차 납부 후 남은 원금(금액 단위: 만 원)."""
    monthly_rate = annual_rate / 12.0
    total_months = int(term_years * 12)
    payments_made = max(0, min(int(payments_made), total_months))
    if payments_made == 0:
        return float(principal_man)
    if payments_made >= total_months:
        return 0.0
    if monthly_rate == 0:
        return principal_man * (1.0 - payments_made / total_months)
    payment = principal_man * monthly_rate / (1.0 - (1.0 + monthly_rate) ** (-total_months))
    return (
        principal_man * (1.0 + monthly_rate) ** payments_made
        - payment * (((1.0 + monthly_rate) ** payments_made - 1.0) / monthly_rate)
    )

def representative_mortgage_monthly_payment(age):
    """대표사례의 현재 나이에 해당하는 월 원리금 상환액(만원)."""
    payment_number = (int(age) - REPRESENTATIVE_MORTGAGE_PURCHASE_AGE) * 12 + 1
    payment, _, _ = mortgage_monthly_split(
        REPRESENTATIVE_MORTGAGE_PRINCIPAL_MAN,
        REPRESENTATIVE_MORTGAGE_ANNUAL_RATE,
        REPRESENTATIVE_MORTGAGE_TERM_YEARS,
        payment_number,
    )
    return payment

def current_financial_summary():
    # 1) 들어오는 돈 집계
    regular_income = sum(float(getv(k, 0)) for k in ["income_self", "income_spouse", "income_other"])
    annual_bonus = float(getv("income_bonus", 0))
    annual_total_income = (regular_income * 12.0) + annual_bonus
    monthly_effective_income = annual_total_income / 12.0
    
    # 2) 나가는 돈 집계 (기본 생활비·대출은 월간, 기타 지출은 연간 비정기 지출로 처리)
    representative_case_id = st.session_state.get("_representative_case_id")
    if representative_case_id in {"case_32_female", "case_45_female"}:
        current_age = int(getv("person_age", 35) or 35)
        monthly_loan_payment = representative_mortgage_monthly_payment(current_age)
    else:
        monthly_loan_payment = float(getv("expense_loan", 0) or 0)
    monthly_regular_expenses = float(getv("expense_living", 0) or 0) + monthly_loan_payment
    annual_other_expense = float(getv("expense_other", 0))
    annual_total_expenses = (monthly_regular_expenses * 12.0) + annual_other_expense
    monthly_effective_expenses = annual_total_expenses / 12.0
    
    # 3) 잉여/저축여력 집계
    annual_net_surplus = annual_total_income - annual_total_expenses
    monthly_effective_surplus = annual_net_surplus / 12.0
    
    # 4) 자산 및 부채 집계
    assets = sum(float(getv(k, 0)) for k in ["asset_cash", "asset_financial", "asset_home", "asset_deposit", "asset_other"])
    debts = sum(float(getv(k, 0)) for k in ["debt_home", "debt_other"])
    net_worth = assets - debts
    
    return {
        "regular_income": regular_income,
        "annual_bonus": annual_bonus,
        "annual_total_income": annual_total_income,
        "monthly_effective_income": monthly_effective_income,
        "income": regular_income,
        "expenses": monthly_effective_expenses, # 월평균 실질 지출
        "annual_total_expenses": annual_total_expenses,
        "annual_other_expense": annual_other_expense,
        "surplus": monthly_effective_surplus,
        "monthly_regular_surplus": regular_income - monthly_regular_expenses,
        "annual_net_surplus": annual_net_surplus,
        "monthly_effective_surplus": monthly_effective_surplus,
        "assets": assets,
        "debts": debts,
        "net_worth": net_worth
    }


#########################################################
# -------------------------------------------------------
# 3.00 | 외부 AI 연동 서비스 (Gemini API Pipeline)
# -------------------------------------------------------
#########################################################
#########################################################
# 3.01 | Gemini 초고속 자율 매칭 엔진
#########################################################
#--------------------------------------------------------
# 3.01.01 | API 키 정제 및 텍스트 생성 파이프라인
#--------------------------------------------------------
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


#########################################################
# -------------------------------------------------------
# 4.00 | 사이드바 및 진입 표지
# -------------------------------------------------------
#########################################################
#########################################################
# 4.01 | 사이드바 프로필 요약 및 복원
#########################################################
#--------------------------------------------------------
# 4.01.01 | 사이드바 렌더링 및 대표사례 원클릭 버튼
#--------------------------------------------------------
with st.sidebar:
    st.markdown(f"""
<div style="background: rgba(30, 41, 59, 0.4); border: 1px solid #334155; border-radius: 10px; padding: 12px 14px; text-align: center; margin: 8px 0 6px 0;">
<div style="font-size: 11.5px; color: #94a3b8; font-weight: 600; letter-spacing: 0.04em;">익명 진단 고유번호</div>
<div style="font-size: 20px; font-weight: 750; color: #cbd5e1; letter-spacing: 1px; margin-top: 3px;">{st.session_state.anonymous_id}</div>
</div>
""", unsafe_allow_html=True)

    # 고유번호 바로 아래에 일회성 세션 안내 문구 배치
    st.caption("※ 일회성 안전 세션입니다.")
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # 인터뷰어 체험용 2대 대표 사례 버튼 (상단 인터뷰어 영역)
    st.markdown("<div style='font-size: 13.5px; font-weight: 700; color: #94A3B8; margin-bottom: 6px;'>체험용 대표 사례</div>", unsafe_allow_html=True)
    c_btn1, c_btn2 = st.columns(2)
    
    def apply_case_payload(case_dict, case_id=None):
        # 1. 보존해야 할 시스템 핵심 키 목록
        SYSTEM_KEEP_KEYS = {"anonymous_id", "started", "advanced_mode"}

        # 2. 시스템 키를 제외한 세션 내 모든 잔여 위젯/데이터 완벽 초기화 (Flush)
        #    pills_* 전체, 주거 선택 위젯, 가족 확인 상태, AI 연금/가족 검토 임시 상태도 함께 제거
        keys_to_clear = [k for k in list(st.session_state.keys()) if k not in SYSTEM_KEEP_KEYS]
        for k in keys_to_clear:
            st.session_state.pop(k, None)

        # 3. 새로운 대표 사례 데이터 주입
        for k, v in case_dict.items():
            st.session_state[k] = v
        st.session_state["_representative_case_id"] = case_id

        # 4. Streamlit Pills 및 Selectbox 위젯 키 명시적 강제 바인딩
        if "gender" in case_dict: st.session_state["pills_gender"] = case_dict["gender"]
        if "job_form" in case_dict: st.session_state["pills_job_self"] = case_dict["job_form"]
        if "career_stage" in case_dict: st.session_state["pills_career_stage"] = case_dict["career_stage"]
        if "job_spouse_form" in case_dict: st.session_state["pills_job_spouse"] = case_dict["job_spouse_form"]
        if "child_count" in case_dict: st.session_state["child_count_select_direct"] = case_dict["child_count"]
        if "housing_region" in case_dict:
            st.session_state["housing_region_select"] = case_dict["housing_region"]

        # 가족 계획 데이터가 모두 포함된 사례만 입력 완료 상태로 시작
        st.session_state["family_info_checked"] = all(
            key in case_dict for key in ("marriage_plan", "child_plan", "housing_plan")
        )

        st.session_state["started"] = True
        st.session_state["answers"] = {}
        st.session_state["advanced_mode"] = True
        st.session_state["_pending_nav"] = "우리집 가계부"

    with c_btn1:
        if st.button("32세 여성", key="btn_case_32", use_container_width=True, help="미혼 / 직장 4년차 / 결혼·출산 준비"):
            apply_case_payload(INTERVIEWER_CASES["case_32_female"], "case_32_female")
            st.rerun()
    with c_btn2:
        if st.button("45세 여성", key="btn_case_45", use_container_width=True, help="기혼 / 경단 후 재취업 / 자녀 15세"):
            apply_case_payload(INTERVIEWER_CASES["case_45_female"], "case_45_female")
            st.rerun()

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

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

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    
    # [사이드바 모드 전환 버튼]
    is_currently_adv = st.session_state.get("advanced_mode", False)
    mode_btn_label = "🌿 기본 모드로 전환" if is_currently_adv else "🧭 고급 모드로 전환"
    if st.button(mode_btn_label, key="sidebar_mode_toggle_btn", use_container_width=True):
        st.session_state.advanced_mode = not is_currently_adv
        st.rerun()

    # 모드 전환 버튼 바로 아래로 이동한 '화면 새로고침' 버튼
    if st.button("↻ 화면 새로고침", key="sidebar_screen_refresh", use_container_width=True):
        st.rerun()

#--------------------------------------------------------
# 4.01.02 | 개발용 테스트 메뉴 (사례 저장/불러오기)
#--------------------------------------------------------
_dev_enabled = st.secrets.get("DEV_MODE", False)

if _dev_enabled:
    with st.sidebar:
        st.divider()
        st.markdown("### 🧪 개발자 영역")


        _cases = get_test_cases()
        _all_names = list(_cases.keys())

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

            # 인터뷰어 대표 사례와 동일한 전체 초기화·위젯 재주입 경로 사용
            apply_case_payload(_data)

            st.session_state["started"] = True
            st.session_state["answers"] = {}
            st.session_state["anonymous_id"] = f"#DEV-{random.randint(100, 999)}"
            st.session_state["active_navigation_default"] = "우리집 가계부"
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


########################################################## 4.02 | 첫 진입 표지 및 인라인 시작 바##########################################################--------------------------------------------------------
# 4.02.01 | 커버 이미지 렌더링 및 인라인 시작 폼
#--------------------------------------------------------
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



#########################################################
# -------------------------------------------------------
# 5.00 | 메인 네비게이션 헤더
# -------------------------------------------------------
#########################################################

#########################################################
# 5.01 | 상단 5개 메뉴 네비게이션 바
#########################################################

#--------------------------------------------------------
# 5.01.01 | 기본 버튼 기반 메인 네비게이션 렌더링
#--------------------------------------------------------
_pending_nav = st.session_state.pop("_pending_nav", None)

nav_options = [
    "우리집 가계부",
    "삶과 생계수단",
    "인생의 사계절",
    "AI 시선",
    "통계"
]

# 이전 두 줄 메뉴 상태가 남아 있는 세션도 새 한 줄 메뉴로 변환
_legacy_nav_labels = {
    "우리집\n가계부": "우리집 가계부",
    "삶과\n생계수단": "삶과 생계수단",
    "인생의\n사계절": "인생의 사계절",
    "AI\n시선": "AI 시선",
}

_active_nav = _legacy_nav_labels.get(
    st.session_state.get("active_navigation_default"),
    st.session_state.get("active_navigation_default", nav_options[0]),
)
if _active_nav not in nav_options:
    _active_nav = nav_options[0]
if _pending_nav in nav_options:
    _active_nav = _pending_nav
st.session_state["active_navigation_default"] = _active_nav

def _set_active_navigation(page):
    st.session_state["active_navigation_default"] = page

# segmented_control 대신 실제 선택 상태를 파이썬에서 직접 관리하는 버튼 메뉴
st.markdown("""
<style>
/* 바깥 shell: 녹색 프레임과 화살표를 고정 */
.st-key-main_navigation_shell {
    position: relative !important;
    box-sizing: border-box !important;
    width: 100% !important;
    overflow: hidden !important;
    margin-bottom: 14px !important;
    background: #556B2F !important;
    border: 1px solid #788B4A !important;
    border-radius: 14px !important;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.12) !important;
}

/* 실제 탭만 스크롤되는 안쪽 영역 */
.st-key-main_navigation {
    box-sizing: border-box !important;
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: center !important;
    width: 100% !important;
    min-width: 0 !important;
    gap: 4px !important;
    column-gap: 4px !important;
    overflow-x: auto !important;
    overflow-y: hidden !important;
    -webkit-overflow-scrolling: touch !important;
    padding: 8px 32px !important;
    margin: 0 !important;
    background: transparent !important;
    border: 0 !important;
    border-radius: 0 !important;
}

/* 내부 버튼 줄: PC는 가운데, 모바일은 왼쪽부터 스크롤 */
.st-key-main_navigation [data-testid="stHorizontalBlock"] {
    box-sizing: border-box !important;
    width: 100% !important;
    min-width: 100% !important;
    gap: 4px !important;
    column-gap: 4px !important;
    justify-content: center !important;
    flex-wrap: nowrap !important;
}

@media (max-width: 768px) {
    .st-key-main_navigation_shell::before,
    .st-key-main_navigation_shell::after {
        position: absolute;
        top: 0;
        bottom: 0;
        z-index: 20;
        display: none;
        align-items: center;
        justify-content: center;
        width: 32px;
        color: #FFFFFF;
        font-size: 27px;
        font-weight: 800;
        line-height: 1;
        pointer-events: none;
    }
    .st-key-main_navigation_shell.nav-has-left::before {
        content: "‹";
        display: flex;
        left: 0;
        background: linear-gradient(90deg, #556B2F 42%, rgba(85, 107, 47, 0));
    }
    .st-key-main_navigation_shell.nav-has-right::after {
        content: "›";
        display: flex;
        right: 0;
        background: linear-gradient(270deg, #556B2F 42%, rgba(85, 107, 47, 0));
    }
    .st-key-main_navigation [data-testid="stHorizontalBlock"] {
        width: max-content !important;
        min-width: 100% !important;
        justify-content: flex-start !important;
    }
}

/* PC에서는 실제 메뉴 컨테이너 자체에서 탭 묶음을 중앙 정렬 */
@media (min-width: 769px) {
    .st-key-main_navigation {
        justify-content: center !important;
        align-items: center !important;
    }
    .st-key-main_navigation > .stElementContainer {
        flex: 0 0 auto !important;
    }
}

/* PC에서는 스크롤 바를 얇게 복원 */
@media (min-width: 769px) {
    .st-key-main_navigation {
        scrollbar-width: thin !important;
        scrollbar-color: #A3B18A rgba(255, 255, 255, 0.12) !important;
    }
    .st-key-main_navigation::-webkit-scrollbar {
        height: 4px !important;
    }
    .st-key-main_navigation::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.12) !important;
        border-radius: 4px !important;
    }
    .st-key-main_navigation::-webkit-scrollbar-thumb {
        background: #A3B18A !important;
        border-radius: 4px !important;
    }
}
/* 비선택 메뉴 */
.st-key-main_navigation button {
    box-sizing: border-box !important;
    width: auto !important;
    min-width: max-content !important;
    height: 46px !important;
    min-height: 46px !important;
    padding: 7px 10px !important;
    border: 1px solid #475569 !important;
    border-radius: 8px !important;
    background: #334155 !important;
    color: #F1F5F9 !important;
    font-size: 13px !important;
    font-weight: 650 !important;
    white-space: nowrap !important;
    box-shadow: none !important;
}
/* 터치 후 포커스가 남은 비선택 메뉴도 회색 유지 */
.st-key-main_navigation button[kind="secondary"]:focus,
.st-key-main_navigation button[kind="secondary"]:active,
.st-key-main_navigation button[kind="secondary"]:hover {
    background: #334155 !important;
    border-color: #475569 !important;
    color: #F1F5F9 !important;
    box-shadow: none !important;
}
/* 선택된 메뉴는 파이썬 상태에 따라 primary로 지정된 버튼 하나뿐 */
.st-key-main_navigation button[kind="primary"],
.st-key-main_navigation button[kind="primary"]:focus,
.st-key-main_navigation button[kind="primary"]:active,
.st-key-main_navigation button[kind="primary"]:hover {
    background: #0F766E !important;
    border-color: #5EEAD4 !important;
    color: #FFFFFF !important;
    font-weight: 800 !important;
    box-shadow: 0 0 0 1px #5EEAD4 !important;
}
</style>
""", unsafe_allow_html=True)

#--------------------------------------------------------
# 1.02.05 | 탭1 텍스트형 클릭 요소 — 기존 글자 스타일 보존
#--------------------------------------------------------
st.markdown("""
<style>
/* 은퇴 제목: 기존 제목 크기·굵기를 유지하고 버튼 외형은 완전히 제거 */
div.st-key-source_retirement_expense {
    width: 100% !important;
    flex: 1 1 auto !important;
    margin: 0 !important;
}
div.st-key-source_retirement_expense [data-testid="stButton"] button,
div.st-key-source_retirement_expense [data-testid="stButton"] button:hover,
div.st-key-source_retirement_expense [data-testid="stButton"] button:focus,
div.st-key-source_retirement_expense [data-testid="stButton"] button:focus-visible,
div.st-key-source_retirement_expense [data-testid="stButton"] button:active {
    width: auto !important;
    min-width: 0 !important;
    min-height: 0 !important;
    height: auto !important;
    padding: 0 !important;
    margin: 0 !important;
    border: 0 !important;
    outline: 0 !important;
    background: transparent !important;
    background-color: transparent !important;
    background-image: none !important;
    box-shadow: none !important;
    border-radius: 0 !important;
    color: #38BDF8 !important;
    -webkit-text-fill-color: #38BDF8 !important;
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    line-height: 1.25 !important;
    justify-content: flex-start !important;
    text-decoration: none !important;
}
div.st-key-source_retirement_expense [data-testid="stButton"] button p {
    margin: 0 !important;
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    line-height: 1.25 !important;
    color: #38BDF8 !important;
    -webkit-text-fill-color: #38BDF8 !important;
}
div.st-key-source_retirement_expense [data-testid="stButton"] button:hover p {
    color: #38BDF8 !important;
    -webkit-text-fill-color: #38BDF8 !important;
    text-decoration: none !important;
}

/* 대출 설명: 기존 입력 라벨 크기의 청색 텍스트만 남기고 버튼 외형 제거 */
div.st-key-expense-panel [data-testid="stPopoverButton"],
div.st-key-expense-panel [data-testid="stPopoverButton"]:hover,
div.st-key-expense-panel [data-testid="stPopoverButton"]:focus,
div.st-key-expense-panel [data-testid="stPopoverButton"]:focus-visible,
div.st-key-expense-panel [data-testid="stPopoverButton"]:active {
    width: auto !important;
    min-width: 0 !important;
    min-height: 0 !important;
    height: auto !important;
    padding: 0 !important;
    margin: 0 !important;
    border: 0 !important;
    outline: 0 !important;
    background: transparent !important;
    background-color: transparent !important;
    background-image: none !important;
    box-shadow: none !important;
    border-radius: 0 !important;
    color: #38BDF8 !important;
    -webkit-text-fill-color: #38BDF8 !important;
    font-size: inherit !important;
    font-weight: 400 !important;
    line-height: inherit !important;
    justify-content: flex-start !important;
    text-decoration: none !important;
}
div.st-key-expense-panel [data-testid="stPopoverButton"] p {
    margin: 0 !important;
    font-size: inherit !important;
    font-weight: 400 !important;
    line-height: inherit !important;
    color: #38BDF8 !important;
    -webkit-text-fill-color: #38BDF8 !important;
}
div.st-key-expense-panel [data-testid="stPopoverButton"]:hover p {
    color: #7DD3FC !important;
    -webkit-text-fill-color: #7DD3FC !important;
    text-decoration: underline !important;
}
</style>
""", unsafe_allow_html=True)

with st.container(key="main_navigation_shell"):
    with st.container(key="main_navigation", horizontal=True, wrap=False, gap=None):
        for _i, _page in enumerate(nav_options):
            st.button(
                _page,
                key=f"main_nav_button_{_i}",
                type="primary" if _page == _active_nav else "secondary",
                on_click=_set_active_navigation,
                args=(_page,),
            )

selected_page = st.session_state["active_navigation_default"]

# 메뉴의 실제 스크롤 위치를 읽고, 고정 shell에 좌우 화살표 상태 반영
st.components.v1.html(
    """
    <script>
    (() => {
        try {
            const doc = window.parent.document;
            const shell = doc.querySelector(".st-key-main_navigation_shell");
            const nav = doc.querySelector(".st-key-main_navigation");
            if (!shell || !nav) return;

            const updateNavState = () => {
                const maxScroll = Math.max(0, nav.scrollWidth - nav.clientWidth);
                shell.classList.toggle("nav-has-left", nav.scrollLeft > 2);
                shell.classList.toggle("nav-has-right", nav.scrollLeft < maxScroll - 2);
            };

            if (!nav.dataset.navScrollStateBound) {
                nav.addEventListener("scroll", updateNavState, { passive: true });
                if (window.parent.ResizeObserver) {
                    const observer = new window.parent.ResizeObserver(updateNavState);
                    observer.observe(nav);
                    observer.observe(shell);
                }
                window.parent.addEventListener("resize", updateNavState, { passive: true });
                nav.dataset.navScrollStateBound = "true";
            }
            updateNavState();
        } catch (e) {}
    })();
    </script>
    """,
    height=0,
)


#--------------------------------------------------------
# 5.01.02 | 출처 자료실 이동 및 복귀 상태 관리
#--------------------------------------------------------
def _open_source_reference(source_id, origin_page, origin_anchor):
    st.session_state["_active_source_id"] = source_id
    st.session_state["_source_return_context"] = {
        "page": origin_page,
        "anchor": origin_anchor,
    }
    if source_id == "6050600-01":
        st.session_state["_source_open_anchor"] = "stats-anchor-retirement-expense"
    elif source_id == "6050700-01":
        st.session_state["_source_open_anchor"] = "stats-anchor-loan-payment"
    st.session_state["_pending_nav"] = "통계"
    st.rerun()


# 통계 자료실에서 다른 메뉴로 이동한 경우 이전 복귀 경로 폐기
# 단, 복귀 버튼으로 원래 화면을 복원하는 중에는 유지한다.
if (
    selected_page != "통계"
    and not st.session_state.get("_source_restore_anchor")
):
    st.session_state.pop("_active_source_id", None)
    st.session_state.pop("_source_return_context", None)
    st.session_state.pop("_source_open_anchor", None)


#########################################################
# -------------------------------------------------------
# 6.00 | 메인 뷰 페이지 (Main View Tabs)
# -------------------------------------------------------
#########################################################

#########################################################
# 6.01 | Tab 1 — 우리집 가계부
#########################################################

if selected_page == "우리집 가계부":
    is_adv = st.session_state.get("advanced_mode", False)

#--------------------------------------------------------
# 6.01.01 | 기본 모드 — 일상 수지 밸런스 패널
#--------------------------------------------------------
    if not is_adv:
        # [기본 모드] 중복 제목 없이 바로 본론으로 진입하는 3분 일상 수지 산책
        st.caption("가벼운 3분 산책: 가장 핵심적인 우리 집의 한 달 현금흐름 밸런스만 살펴봅니다.")
        
        with st.container():
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
            save_basic = st.button(
                "입력 내용 AI 점검",
                use_container_width=True,
                type="primary"
            )

        # 입력값은 버튼을 누르지 않아도 매 실행마다 공통 세션에 반영
        st.session_state["income_self"] = basic_income
        st.session_state["expense_living"] = basic_expense

        if save_basic:
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
        
        # [고급 모드] 실시간 AI 연금 추정 및 점검 탑재
        with st.container():
            
            
#--------------------------------------------------------
# 6.01.02 | 고급 모드 — ⓪ 우리집 소득 성격 입력 패널
#--------------------------------------------------------       
            with st.container(border=True, key="job-panel"):
                st.markdown("### ⓪ 우리집 소득 성격")
                gender_options = ["🙋‍♂️ 남성", "🙋‍♀️ 여성"]
                prev_gender = st.session_state.get("gender", "🙋‍♂️ 남성")
                if prev_gender not in gender_options: prev_gender = "🙋‍♂️ 남성"
                    
                st.markdown("<div style='font-size: 17px; font-weight: 700; color: #F8FAFC; margin-bottom: 6px;'>나의 성별은?</div>", unsafe_allow_html=True)
                gender_selected = st.pills("나의 성별은?", gender_options, default=prev_gender, key="pills_gender", label_visibility="collapsed")
                st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

                job_options = ["직장인", "공무원", "자영업", "전문직", "사업가", "투자자", "임대소득자", "전업주부", "그외"]
                job_spouse_options = ["해당 없음", "직장인", "공무원", "자영업", "전문직", "사업가", "투자자", "임대소득자", "전업주부", "그외"]
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

#--------------------------------------------------------
# 6.01.03 | 고급 모드 — ① 들어오는 돈 vs ② 나가는 돈 입력 패널
#--------------------------------------------------------
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
                    st.markdown("### ② 나가는 돈 (만원)")
                    expense_living = st.number_input("기본 월 생활비 (식비·관리비·통신비 등)", min_value=0, value=st.session_state.get("expense_living"), step=10, placeholder="월 생활 유지비")
                    representative_case_id_for_loan = st.session_state.get("_representative_case_id")
                    is_representative_case_for_loan = representative_case_id_for_loan in {"case_32_female", "case_45_female"}
                    current_person_age_for_loan = int(st.session_state.get("person_age", 35) or 35)
                    loan_payment_input = (
                        round(representative_mortgage_monthly_payment(current_person_age_for_loan))
                        if is_representative_case_for_loan
                        else st.session_state.get("expense_loan")
                    )
                    loan_widget_key = (
                        f"expense_loan_{representative_case_id_for_loan}_{current_person_age_for_loan}"
                        if is_representative_case_for_loan
                        else "expense_loan_user"
                    )
                    if is_representative_case_for_loan:
                        if st.button(
                            "대출 원리금 월상환액(원금+이자) [주석]",
                            key="loan_payment_source_link",
                        ):
                            _open_source_reference(
                                "6050700-01",
                                "우리집 가계부",
                                "loan-payment-label-origin",
                            )
                        expense_loan = st.number_input(
                            "대출 원리금 월상환액(원금+이자) [주석]",
                            min_value=0,
                            value=loan_payment_input,
                            step=10,
                            placeholder="은행 납입 합계",
                            disabled=True,
                            key=loan_widget_key,
                        )
                        st.components.v1.html(
                            """
                            <script>
                            (() => {
                                try {
                                    const doc = window.parent.document;
                                    const labels = Array.from(
                                        doc.querySelectorAll('[data-testid="stWidgetLabel"]')
                                    );
                                    const label = labels.find(
                                        el => el.innerText.trim() === "대출 원리금 월상환액(원금+이자) [주석]"
                                    );
                                    const hiddenButton = doc.querySelector(
                                        ".st-key-loan_payment_source_link button"
                                    );
                                    if (label && hiddenButton && !label.dataset.sourceLinkBound) {
                                        label.dataset.sourceLinkBound = "true";
                                        label.addEventListener("click", () => hiddenButton.click());
                                        label.style.cursor = "pointer";
                                    }
                                } catch (e) {}
                            })();
                            </script>
                            """,
                            height=0,
                        )
                    else:
                        expense_loan = st.number_input(
                            "대출 원리금 월 상환액 (원금+이자 합계)",
                            min_value=0,
                            value=loan_payment_input,
                            step=10,
                            placeholder="은행 납입 합계",
                            key=loan_widget_key,
                        )
                    expense_other = st.number_input("그 밖의 연간 비정기 지출 (여행·경조사·세금)", min_value=0, value=st.session_state.get("expense_other"), step=10, placeholder="연간 비정기 지출 합계")

#--------------------------------------------------------
# 6.01.04 | 고급 모드 — ③ 가지고 있는 것 vs ④ 갚아야 할 돈 패널
#--------------------------------------------------------
            asset_col, debt_col = st.columns(2)
            with asset_col:
                with st.container(border=True, key="asset-panel"):
                    st.markdown("### ③ 가지고 있는 것 (만원)")
                    asset_cash = st.number_input("현금·예적금", min_value=0, value=st.session_state.get("asset_cash"), step=100, placeholder="금액")
                    asset_financial = st.number_input("주식·채권 등", min_value=0, value=st.session_state.get("asset_financial"), step=100, placeholder="금액")
                    asset_home = st.number_input("부동산 시세", min_value=0, value=st.session_state.get("asset_home"), step=100, placeholder="금액")
                    asset_deposit = st.number_input("전세보증금", min_value=0, value=st.session_state.get("asset_deposit"), step=100, placeholder="금액")
                    asset_other = st.number_input("그외 자산 (사업체·지분 등)", min_value=0, value=st.session_state.get("asset_other"), step=100, placeholder="금액")
            with debt_col:
                with st.container(border=True, key="debt-panel"):
                    st.markdown("### ④ 갚아야 할 돈 (만원)")
                    debt_home = st.number_input("주택·전세 대출잔액", min_value=0, value=st.session_state.get("debt_home"), step=100, placeholder="금액")
                    debt_other = st.number_input("그외 부채 (신용·마이너스통장)", min_value=0, value=st.session_state.get("debt_other"), step=100, placeholder="금액")

#--------------------------------------------------------
# 6.01.05 | 고급 모드 — 은퇴 후 가정 입력 패널
#--------------------------------------------------------
            with st.container(border=True, key="retirement-panel"):
                with st.container(horizontal=True, vertical_alignment="bottom", gap=None, key="retirement-title-row"):
                    st.markdown("### 은퇴 후에는? (만원)")
                    if st.button(
                        "🧭",
                        key="source_retirement_expense",
                        help="은퇴 후 연령대별 생활비 통계와 적용 방식 보기",
                        type="tertiary",
                    ):
                        _open_source_reference(
                            "6050600-01",
                            "우리집 가계부",
                            "source-anchor-retirement-expense",
                        )
                st.markdown(
                    '<div id="source-anchor-retirement-expense"></div>',
                    unsafe_allow_html=True,
                )

                pension_col, retirement_expense_col = st.columns(2)

                with pension_col:
                    income_pension = st.number_input(
                        "은퇴 후 받을 월 국민연금 (모르면 빈칸)",
                        min_value=0,
                        value=st.session_state.get("income_pension"),
                        step=10,
                        placeholder="싱글 1명 / 부부 2명 합산"
                    )

                with retirement_expense_col:
                    retirement_monthly_expenses = st.number_input(
                        "은퇴 후 월 생활비",
                        min_value=0,
                        value=int(st.session_state.get(
                            "retirement_monthly_expenses", 270
                        ) or 0),
                        step=10,
                    )

            save_finance_trigger = st.button(
                "입력 내용 AI 점검",
                use_container_width=True,
                type="primary"
            )

        # ----------------------------------------------------------------------
        # 일반 재무 입력값을 매 실행마다 공통 세션에 즉시 반영
        # ----------------------------------------------------------------------
        final_gender = gender_selected if gender_selected else "🙋‍♂️ 남성"
        final_job = job_selected if job_selected else "직장인"
        final_career = career_selected if career_selected else "🌱 3년 이하 (초년생)"
        final_spouse_job = (
            ""
            if (not job_spouse_selected or job_spouse_selected == "해당 없음")
            else job_spouse_selected
        )

        st.session_state["gender"] = final_gender
        st.session_state["job_form"] = final_job
        st.session_state["career_stage"] = final_career
        st.session_state["job_spouse_form"] = final_spouse_job

        finance_values = {
            "income_self": income_self,
            "income_spouse": income_spouse,
            "income_other": income_other,
            "income_bonus": income_bonus,
            "income_pension": income_pension,
            "expense_living": expense_living,
            "expense_loan": expense_loan,
            "expense_other": expense_other,
            "retirement_monthly_expenses": retirement_monthly_expenses,
            "asset_cash": asset_cash,
            "asset_financial": asset_financial,
            "asset_home": asset_home,
            "asset_deposit": asset_deposit,
            "asset_other": asset_other,
            "debt_home": debt_home,
            "debt_other": debt_other,
        }

        for key, value in finance_values.items():
            st.session_state[key] = value

        # AI 검토 화면에서도 항상 최신 입력값을 참조하도록 갱신
        st.session_state["_pending_finance_draft"] = {
            "gender": final_gender,
            "job_form": final_job,
            "career_stage": final_career,
            "job_spouse_form": final_spouse_job,
            **finance_values,
        }
        
        # ----------------------------------------------------------------------
        # [실제 Gemini AI 호출을 통한 지능형 연금 추정 및 가계부 점검]
        # ----------------------------------------------------------------------

#--------------------------------------------------------
# 6.01.06 | 고급 모드 — AI 은퇴연금 추정 엔진 및 확인 카드
#--------------------------------------------------------
        if save_finance_trigger:

            cur_p_age = int(st.session_state.get("person_age", 35))
            has_spouse = (final_spouse_job != "")

            ai_pension_prompt = f"""[역할: 대한민국 국민연금 및 직역연금 통계 전문가]
인터뷰이 정보:
- 본인: {final_gender}, 만 {cur_p_age}세, 직종 {final_job}, 경력 {final_career}, 월 실수령 {income_self or 0}만 원
- 배우자: {final_spouse_job if has_spouse else '없음'}, 월 실수령 {income_spouse or 0}만 원
- 현재 직접 입력된 은퇴 후 예상연금: {income_pension or '미입력(0)'}만 원

[통계적 팩트 기준]
1. 2025년 국민연금 평균: 남성 약 70만 원, 여성 약 36만 원, 20년 이상 장기가입자 평균 약 113만 원.
2. 직종이 '공무원'인 경우 공무원연금 특성(퇴직 후 월 200~250만 원 안팎 수령 가능성)을 고려할 것.
3. 맞벌이 부부인 경우 두 사람의 합산 국민연금 예상액을 현실적으로 산출할 것 (예: 맞벌이 20년 이상 시 합산 200~230만 원 수준).

[출력 형식 가이드]
반드시 아래 JSON 포맷으로만 정확히 응답하세요 (순수 JSON만 출력):
{{
  "suggested_pension": 권장월연금숫자(만원 단위 정수만, 예: 210),
  "analysis_comment": "2~3문장으로 담백하게 설명. 본문에서 언급하는 추천 금액(예: 210만 원)과 suggested_pension 숫자가 반드시 100% 일치해야 함."
}}"""

            with st.spinner("AI가 입력 내용을 토대로 우리집 가계부와 예상 연금을 점검하는 중입니다..."):
                raw_ai_res, ai_err = call_gemini_text(ai_pension_prompt)

                suggested_val = 210 if has_spouse else 110
                analysis_msg = (
                    "국가데이터처 통계를 기준으로 65세 이후 수령 가능한 기본 연금액을 제안합니다."
                )

                if raw_ai_res:
                    try:
                        clean_json = re.search(r"\{.*\}", raw_ai_res, re.DOTALL)
                        if clean_json:
                            parsed = json.loads(clean_json.group(0))
                            suggested_val = int(
                                parsed.get("suggested_pension", suggested_val)
                            )
                            analysis_msg = str(
                                parsed.get("analysis_comment", analysis_msg)
                            )
                    except Exception:
                        pass

                # 사용자가 0이 아닌 값을 명시적으로 입력하지 않았다면 AI 추천값 적용
                if income_pension and int(income_pension) > 0 and int(income_pension) != 120:
                    final_suggested_pension = int(income_pension)
                else:
                    final_suggested_pension = suggested_val

                st.session_state["_ai_pension_result"] = {
                    "suggested_val": final_suggested_pension,
                    "comment": analysis_msg
                }

                st.session_state["input_adjusted_pension"] = final_suggested_pension
                st.session_state["show_ai_finance_review"] = True

        # ----------------------------------------------------------------------
        # [AI 제안 및 은퇴 후 연금 최종 반영: 통합 영역]
        # ----------------------------------------------------------------------
        if (
            st.session_state.get("show_ai_finance_review", False)
            and "_pending_finance_draft" in st.session_state
        ):
            draft = st.session_state["_pending_finance_draft"]
            ai_data = st.session_state.get(
                "_ai_pension_result",
                {"suggested_val": 120, "comment": ""}
            )

            user_retire_age = int(
                st.session_state.get("retirement_age") or 60
            )
            pension_gap_years = max(0, 65 - user_retire_age)

            review_spouse_job = str(
                draft.get("job_spouse_form", "") or ""
            )
            review_has_spouse = (
                review_spouse_job not in ("", "해당 없음")
            )

            # 싱글 사례에서는 배우자 연금 입력값 초기화
            if not review_has_spouse:
                st.session_state["other_pension_spouse_enabled"] = False
                st.session_state["other_pension_spouse_amount"] = 0
                st.session_state["other_pension_spouse_age"] = 65

            # AI 제안과 추가 연금 입력을 하나의 영역으로 통합
            with st.container(border=True):

                st.markdown("### 🤖 AI 가계부 점검 & 은퇴 연금액 제안")

                st.markdown(
                    ai_data.get("comment", "")
                )

                st.markdown(
                    f"**⚠️ 소득 공백 참고:** 희망 은퇴 나이(만 "
                    f"{user_retire_age}세)부터 노령연금 개시(만 65세)까지 "
                    f"약 **{pension_gap_years}년간** 소득 공백이 발생합니다."
                )

                st.divider()

                adjusted_pension = st.number_input(
                    "은퇴 후 최종 반영할 월 국민연금액 (만원)",
                    min_value=0,
                    max_value=2000,
                    value=int(st.session_state.get(
                        "input_adjusted_pension",
                        ai_data.get("suggested_val", 120)
                    )),
                    step=10,
                    key="input_adjusted_pension"
                )

                st.divider()

                st.markdown("#### 국민연금 외 다른 연금")

                st.markdown(
                    "**당신에게 국민연금 외 다른 연금이 있다면 아래에 입력하세요.**"
                )

                self_pension_col1, self_pension_col2 = st.columns(2)

                with self_pension_col1:
                    self_pension_amount = st.number_input(
                        "나의 월 예상 수령액 (만원)",
                        min_value=0,
                        value=int(st.session_state.get(
                            "other_pension_self_amount", 0
                        ) or 0),
                        step=5,
                        key="other_pension_self_amount"
                    )

                with self_pension_col2:
                    st.number_input(
                        "나의 수령 시작 나이",
                        min_value=40,
                        max_value=100,
                        value=int(st.session_state.get(
                            "other_pension_self_age", 65
                        ) or 65),
                        step=1,
                        key="other_pension_self_age"
                    )

                # 입력한 연금액이 0보다 클 때만 그래프에 반영
                st.session_state["other_pension_self_enabled"] = (
                    self_pension_amount > 0
                )

                if review_has_spouse:
                    st.divider()

                    st.markdown(
                        "**배우자에게 국민연금 외 다른 연금이 있다면 아래에 입력하세요.**"
                    )

                    spouse_pension_col1, spouse_pension_col2 = st.columns(2)

                    with spouse_pension_col1:
                        spouse_pension_amount = st.number_input(
                            "배우자의 월 예상 수령액 (만원)",
                            min_value=0,
                            value=int(st.session_state.get(
                                "other_pension_spouse_amount", 0
                            ) or 0),
                            step=5,
                            key="other_pension_spouse_amount"
                        )

                    with spouse_pension_col2:
                        st.number_input(
                            "배우자의 수령 시작 나이",
                            min_value=40,
                            max_value=100,
                            value=int(st.session_state.get(
                                "other_pension_spouse_age", 65
                            ) or 65),
                            step=1,
                            key="other_pension_spouse_age"
                        )

                    st.session_state["other_pension_spouse_enabled"] = (
                        spouse_pension_amount > 0
                    )

                st.divider()

                st.markdown(
                    "위 내용을 확인한 뒤 가계부에 반영해 주세요."
                )

                btn_confirm = st.button(
                    "✅ 이 금액으로 가계부 확정",
                    type="primary",
                    use_container_width=True,
                    key="btn_confirm_ai_final"
                )

            if btn_confirm:
                draft["income_pension"] = adjusted_pension

                # 이미 생성된 위젯의 key는 재대입하지 않음
                widget_keys = {
                    "other_pension_self_enabled",
                    "other_pension_self_amount",
                    "other_pension_self_age",
                    "other_pension_spouse_enabled",
                    "other_pension_spouse_amount",
                    "other_pension_spouse_age",
                }

                for k, v in draft.items():
                    if k not in widget_keys:
                        st.session_state[k] = v

                # 최종 확정 후에도 AI 제안 및 연금 입력 영역 유지
                st.session_state["finance_saved_notice"] = True
                st.rerun()

#--------------------------------------------------------
# 6.01.07 | 고급 모드 — 우리집 재무 현황 2x2 ESBI 매트릭스 카드
#--------------------------------------------------------
        q_self = active_quadrant(st.session_state.get("job_form", "직장인"))
        q_spouse = active_quadrant(st.session_state.get("job_spouse_form", ""))
        st.markdown("### 우리집 재무 현황")
        st.markdown("<div id='selected-esbi'></div>", unsafe_allow_html=True)
        if st.session_state.pop("finance_saved_notice", False):
            st.success("입력 및 AI 점검이 완료된 재무 정보가 완벽히 반영되었습니다.")
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

#--------------------------------------------------------
# 6.01.08 | 고급 모드 — 현재 재무 요약 메트릭
#--------------------------------------------------------
        s = current_financial_summary()
        st.markdown("### 현재 재무 요약")
        cols = st.columns(4)
        cols[0].metric("월 수입", money(s["regular_income"]))
        cols[1].metric("월 지출", money(s["expenses"]))
        bonus_help = f"연간 상여금 {money(s['annual_bonus'])} 및 연간 비정기 지출 {money(s['annual_other_expense'])} 반영"
        cols[2].metric("연간 잉여자금", money(s["annual_net_surplus"]), delta=f"월평균 {money(s['monthly_effective_surplus'])}", help=bonus_help)
        cols[3].metric("현재 파악된 금융자산", fmt_eok(s["net_worth"]))


#--------------------------------------------------------
# 6.01.09 | 고급 모드 — 우리 가정 생애 소득(예상) 차트
#--------------------------------------------------------
        st.markdown("### 우리 가정 생애 소득(예상)")

        st.caption(
            "내 직업과 배우자의 직업에 따라 각각 하나의 기준곡선을 적용합니다. "
            "배우자의 현재 소득이 입력되지 않았다면 직업군 기준곡선을 사용합니다. "
            "연금은 각자의 수령 시작 시점부터 가구 합산 소득에 반영합니다. "
            "그래프는 내 나이를 기준으로 표시합니다."
        )

        st.caption(
            "보라색 점선은 2024년 임금근로일자리의 연령·성별 월평균 보수를 1인 기준으로 표시한 통계 비교선입니다. "
            "개인의 은퇴 희망 연령과 무관하며, 연령대별 평균 보수(세전)를 연환산해 참고 표시합니다. "
            "가구 합산 소득과는 기준 인원이 다르며, 70세 이상 값은 해당 연령집단의 평균이지 실제 노동 종료 연령이 아닙니다."
        )
        st.markdown(
            "[통계 출처·산출 기준](https://github.com/ufreezone-ops/nachimpan/blob/dev/data/기준데이터/국가데이터처_2024_연령별_임금근로일자리_평균보수_README.md)"
        )

        cur_age = int(st.session_state.get("person_age", 35) or 35)
        # 기대수명은 생애주기 탭보다 먼저 사용하는 소득 그래프에서 선행 정의
        user_gender = st.session_state.get("gender", "🙋‍♂️ 남성")
        life_expectancy = 87 if "여성" in user_gender else 81
        spouse_age_input = int(st.session_state.get("spouse_age", 0) or 0)

        current_monthly_income = float(
            st.session_state.get("income_self", 0) or 0
        )
        spouse_monthly_income = float(
            st.session_state.get("income_spouse", 0) or 0
        )

        self_job = str(st.session_state.get("job_form", "직장인") or "직장인")
        spouse_job = str(st.session_state.get("job_spouse_form", "") or "")

        # 배우자 직업을 선택하면 배우자가 있는 가구로 판단
        has_spouse = spouse_job not in ("", "해당 없음")

        # 배우자 나이가 없으면 본인과 같은 나이로 임시 가정
        spouse_age_assumed = has_spouse and spouse_age_input <= 0
        spouse_age = (
            spouse_age_input if spouse_age_input > 0 else cur_age
        ) if has_spouse else 0

        age_gap = spouse_age - cur_age if has_spouse else 0

        retire_age = int(
            st.session_state.get("retirement_age", 60) or 60
        )

        # 확정된 국민연금: 싱글은 전액, 부부는 50:50
        monthly_pension = float(
            st.session_state.get("income_pension", 0) or 0
        )
        annual_pension = monthly_pension * 12

        # 국민연금 개시 연령: 현재 설계 가정 65세
        national_pension_start_age = 65

        # 국민연금 외 추가 연금
        other_self_enabled = bool(
            st.session_state.get("other_pension_self_enabled", False)
        )
        other_self_annual = (
            float(st.session_state.get("other_pension_self_amount", 0) or 0) * 12
            if other_self_enabled else 0
        )
        other_self_start_age = int(
            st.session_state.get("other_pension_self_age", 65) or 65
        )

        other_spouse_enabled = bool(
            st.session_state.get("other_pension_spouse_enabled", False)
        )
        other_spouse_annual = (
            float(st.session_state.get("other_pension_spouse_amount", 0) or 0) * 12
            if other_spouse_enabled else 0
        )
        other_spouse_start_age = int(
            st.session_state.get("other_pension_spouse_age", 65) or 65
        )

        # 20~75세 기준 추정곡선 (월평균 소득, 만원)
        ages_base = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75]

        employee_base = [
            180, 270, 350, 420, 460, 469,
            445, 360, 280, 210, 160, 120
        ]

        self_employed_base = [
            130, 210, 290, 350, 390, 410,
            420, 400, 350, 290, 230, 170
        ]

        # 직업군을 E / SBI 기준곡선으로 매핑
        def select_income_base(job):
            if job in ("전업주부",):
                return None

            if job in ("직장인", "공무원"):
                return employee_base

            return self_employed_base

        self_base = select_income_base(self_job)
        spouse_base = select_income_base(spouse_job) if has_spouse else None

        # 기준곡선의 연령별 소득 보간
        def interpolate_income(age, values):
            if age <= ages_base[0]:
                return values[0]

            if age >= ages_base[-1]:
                return values[-1]

            for i in range(len(ages_base) - 1):
                if ages_base[i] <= age <= ages_base[i + 1]:
                    ratio = (
                        (age - ages_base[i])
                        / (ages_base[i + 1] - ages_base[i])
                    )
                    return (
                        values[i]
                        + (values[i + 1] - values[i]) * ratio
                    )

            return 0

        # 75세 이후 감소 추세를 100세까지 연장
        def extended_base_income(age, values):
            if age <= 75:
                return interpolate_income(age, values)

            slope = (values[-1] - values[-2]) / 5
            return max(0, values[-1] + slope * (age - 75))

        # 현재 소득을 기준으로 개인별 독립 보정
        def get_scale(current_age, current_income, base_values):
            if base_values is None:
                return 0

            base_income = extended_base_income(
                current_age, base_values
            )

            return (
                current_income / base_income
                if base_income > 0 else 0
            )

        self_scale = get_scale(
            cur_age, current_monthly_income, self_base
        )

        
        spouse_scale = (
            get_scale(
                spouse_age,
                spouse_monthly_income,
                spouse_base
            )
            if has_spouse and spouse_base is not None
            and spouse_monthly_income > 0
            else (
                1.0
                if has_spouse and spouse_base is not None
                else 0
            )
        )


        # 그래프 연령 범위: 생애주기 계산과 동일하게 기대수명 직전까지
        ages = list(range(20, life_expectancy))

        self_income_curve = []
        spouse_income_curve = []
        household_income_curve = []

        for age in ages:

            # 본인 소득
            self_income = (
                extended_base_income(age, self_base) * self_scale * 12
                if self_base is not None else 0
            )

            # 배우자 나이를 인터뷰이 나이축으로 환산
            spouse_current_age = age + age_gap

            spouse_income = (
                extended_base_income(
                    spouse_current_age, spouse_base
                ) * spouse_scale * 12
                if has_spouse and spouse_base is not None else 0
            )

            # 각자 자신의 은퇴 연령에 도달하면 근로·사업소득 종료
            if age >= retire_age:
                self_income = 0

            if has_spouse and spouse_current_age >= retire_age:
                spouse_income = 0

            # 가구 합산 소득: 본인 + 배우자
            household_income = self_income + spouse_income

            # 국민연금: 부부는 50:50, 싱글은 전액 본인에게 반영
            if has_spouse:
                if age >= national_pension_start_age:
                    household_income += annual_pension / 2

                if spouse_current_age >= national_pension_start_age:
                    household_income += annual_pension / 2
            else:
                if age >= national_pension_start_age:
                    self_income += annual_pension
                    household_income += annual_pension

            # 국민연금 외 본인 연금
            if other_self_enabled and age >= other_self_start_age:
                self_income += other_self_annual
                household_income += other_self_annual

            # 국민연금 외 배우자 연금
            if (
                has_spouse
                and other_spouse_enabled
                and spouse_current_age >= other_spouse_start_age
            ):
                household_income += other_spouse_annual

            # 그래프에 표시할 연령별 소득 데이터 저장
            self_income_curve.append(self_income)
            spouse_income_curve.append(spouse_income)
            household_income_curve.append(household_income)

        # 그래프: 배우자 유무에 따라 곡선 표시
        fig_income = go.Figure()

        # ① 가구 소득: 실선
        fig_income.add_trace(go.Scatter(
            x=ages,
            y=household_income_curve,
            mode="lines",
            name="가구 소득",
            line=dict(width=3.5, color="#FFFFFF"),
            hovertemplate=(
                "가구 연간 소득: %{y:,.0f}만 원<extra></extra>"
            )
        ))

        # ② 내 소득: 점선
        fig_income.add_trace(go.Scatter(
            x=ages,
            y=self_income_curve,
            mode="lines",
            name="내 소득",
            line=dict(width=2.5, dash="dash", color="#EF553B"),
            hovertemplate=(
                "내 연간 소득: %{y:,.0f}만 원<extra></extra>"
            )
        ))

        # ③ 배우자 소득: 점선 (배우자가 있는 경우에만 표시)
        if has_spouse:
            fig_income.add_trace(go.Scatter(
                x=ages,
                y=spouse_income_curve,
                mode="lines",
                name="배우자 소득",
                line=dict(width=2.5, dash="dash", color="#00CC96"),
                hovertemplate=(
                    "배우자 연간 소득: %{y:,.0f}만 원<extra></extra>"
                )
            ))
        # 2024년 국가데이터처 연령·성별 임금근로일자리 평균보수 비교선
        # 개인의 은퇴 희망 연령과 무관하게 표시하는 1인 기준 통계 참고선
        try:
            wage_stats_path = (
                Path(__file__).resolve().parent
                / "data"
                / "기준데이터"
                / "국가데이터처_2024_연령별_임금근로일자리_평균보수.csv"
            )
            wage_stats = pd.read_csv(wage_stats_path)
            wage_value_col = (
                "여성_월평균보수_만원"
                if "여성" in user_gender
                else "남성_월평균보수_만원"
            )
            wage_ages = wage_stats["대표연령"].astype(int).tolist()
            wage_age_groups = wage_stats["연령구간"].astype(str).tolist()
            wage_monthly = wage_stats[wage_value_col].astype(float).tolist()
            wage_monthly_net_estimated = [value * 0.9 for value in wage_monthly]
            wage_annualized = [value * 12 for value in wage_monthly_net_estimated]

            fig_income.add_trace(go.Scatter(
                x=wage_ages,
                y=wage_annualized,
                customdata=list(zip(wage_age_groups, wage_monthly_net_estimated)),
                mode="lines+markers",
                name="동연령 근로자 평균 실수령액(추정)",
                line=dict(width=3.5, dash="dot", color="#A78BFA"),
                marker=dict(size=7, symbol="diamond"),
                hovertemplate=(
                    "통계 연령구간: %{customdata[0]}<br>"
                    "월평균 실수령액(추정): %{customdata[1]:,.0f}만 원<br>"
                    "연환산 실수령액(추정): %{y:,.0f}만 원"
                    "<extra></extra>"
                )
            ))
        except Exception as e:
            st.warning(f"연령별 임금근로소득 통계 비교선을 불러오지 못했습니다. ({e})")

        # 인터뷰이 현재 나이
        fig_income.add_vline(
            x=cur_age,
            line_dash="dot",
            line_color="#F8FAFC",
            line_width=1.8
        )

        fig_income.add_annotation(
            x=cur_age,
            y=current_monthly_income * 12,
            text="나",
            showarrow=True,
            arrowhead=2,
            ay=-35,
            font=dict(color="#EF553B"),
            arrowcolor="#EF553B"
        )

        # 인터뷰이 은퇴 시점만 작은 점 형태의 수직 점선으로 표시
        fig_income.add_vline(
            x=retire_age,
            line_dash="dot",
            line_color="#3B82F6",
            line_width=1.5,
            annotation_text=f"내 은퇴 ({retire_age}세)",
            annotation_position="bottom right",
            annotation_font_color="#3B82F6"
        )

        fig_income.update_layout(
            height=520,
            margin=dict(l=20, r=20, t=65, b=35),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E2E8F0", size=12),
            xaxis=dict(
                title="내 나이(세)",
                unifiedhovertitle=dict(
                    text="내 나이: %{x}세"
                ),
                range=[20, life_expectancy],
                tickmode="linear",
                tick0=20,
                dtick=5,
                gridcolor="rgba(100, 116, 139, 0.2)",
                fixedrange=True
            ),
            yaxis=dict(
                title="연간 소득 (만원)",
                rangemode="tozero",
                tickformat=",",
                gridcolor="rgba(100, 116, 139, 0.2)",
                fixedrange=True
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
            ),
            hovermode="x unified"
        )

        st.plotly_chart(
            fig_income,
            use_container_width=True,
            config={
                "displayModeBar": False,
                "scrollZoom": False,
                "doubleClick": False,
                "showAxisDragHandles": False
            }
        )

        # 기존 다음 버튼 유지
        _, next_col = st.columns([5, 1])
        with next_col:
            if st.button("다음 →", key="finance_next", use_container_width=True, type="primary"):
                st.session_state["_pending_nav"] = "삶과 생계수단"
                st.rerun()


#########################################################
# 6.02 | Tab 2 — 삶과 생계수단
#########################################################
elif selected_page == "삶과 생계수단":
    is_adv = st.session_state.get("advanced_mode", False)

#--------------------------------------------------------
# 6.02.01 | 공통 — 돌쇠와 똘똘이 우화 카드 렌더러
#--------------------------------------------------------
    def render_dolssoe_story_card():
        """기본 모드와 고급 모드에서 공통으로 사용하는 우화 카드"""
        st.markdown("""
<div style="background: rgba(45, 35, 20, 0.55); border: 1.5px solid #6d4a1a; border-radius: 14px; padding: 24px 26px; margin: 16px 0 24px 0;">
<div style="font-size: 21px; font-weight: 850; color: #FDE68A; margin-bottom: 12px;">🌾 지혜로운 산책: 돌쇠와 똘똘이</div>
<div style="font-size: 14.5px; color: #E2E8F0; margin-bottom: 16px;">옛날 어느 마을, 머슴을 구하는 대감댁에 두 젊은이가 찾아왔습니다.</div>

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
<div style="background: rgba(15, 23, 42, 0.75); border: 1px solid #78350f; border-radius: 10px; padding: 16px 18px;">
<div style="font-size: 17.5px; font-weight: 800; color: #F59E0B; margin-bottom: 6px;">돌쇠의 선택 (물통)</div>
<div style="font-size: 14px; color: #CBD5E1; line-height: 1.6; word-break: keep-all;">
"대감마님, 저는 매달 <b>쌀 한 가마(80kg)</b>씩을 주십시오."<br>
돌쇠는 첫 달부터 쌀 한 가마를 받아 가족을 부양했습니다. 하지만 늙어 힘이 빠질 때까지 지게를 내려놓지 못했습니다.
</div>
</div>

<div style="background: rgba(15, 23, 42, 0.75); border: 1px solid #0369a1; border-radius: 10px; padding: 16px 18px;">
<div style="font-size: 17.5px; font-weight: 800; color: #38BDF8; margin-bottom: 6px;">똘똘이의 선택 (파이프라인)</div>
<div style="font-size: 14px; color: #CBD5E1; line-height: 1.6; word-break: keep-all;">
"저는 첫 달에 <b>쌀 한 되(1kg)</b>만 주시고, 매달 곱절로 주십시오."<br>
똘똘이는 <b>'복리'(파이프라인의 속성)</b>로 훗날을 기약했습니다. <br><b>하지만 당장 첫 달 받은 쌀 한 되로는 가족들을 부양할 수 없었습니다.</b>
</div>
</div>
</div>

<div style="background: rgba(234, 88, 12, 0.14); border-left: 4px solid #EA580C; border-radius: 4px; padding: 14px 18px;">
<div style="font-size: 15px; font-weight: 750; color: #F8FAFC; line-height: 1.6; word-break: keep-all;">
<b>나침반의 성찰:</b><br>이 우화는 누구의 선택을 두둔하는 얘기가 아닙니다. 둘 다 우리가 원하는 결과가 아니기 때문입니다.<br>
돌쇠처럼 성실하게 당장의 가족 생계를 책임지면서도, 똘똘이가 구상한 파이프라인을 덧붙일 수 있는 길은 없을까요?<br>바로 그 <b>'현명한 플랜 B'</b>를 생각하게 하는 얘기입니다.
</div>
</div>
</div>
""", unsafe_allow_html=True)
    
    if not is_adv:
        
        # [기본 모드] 중복 제목 없이 '돌쇠와 똘똘이' 우화 단독 노출
        st.caption("가벼운 3분 산책: 소득의 크기보다 중요한 '소득의 성격'을 한 편의 지혜로운 이야기로 마주합니다.")

        # 기본모드 — 돌쇠와 똘똘이 우화 카드 호출
        render_dolssoe_story_card()

        _, next_col = st.columns([5, 1])
        with next_col:
            if st.button("다음 →", key="basic_livelihood_next", use_container_width=True, type="primary"):
                st.session_state["_pending_nav"] = "인생의 사계절"
                st.rerun()

    else:
        # [고급 모드] 소득 구조와 은퇴 성찰 상세 기능
        
#--------------------------------------------------------
# 6.02.02 | 고급 모드 — 2x2 사분면 (물통과 파이프라인)
#--------------------------------------------------------
        st.markdown("""
<div style="background: rgba(30, 41, 59, 0.45); border: 1.5px solid #334155; border-radius: 14px; padding: 18px 22px; margin-bottom: 22px;">
<div style="font-size: 20px; font-weight: 850; color: #F8FAFC; margin-bottom: 14px;">물통  &  파이프라인</div>
""", unsafe_allow_html=True)
        
        q_self = active_quadrant(st.session_state.get("job_form", "직장인"))
        q_spouse = active_quadrant(st.session_state.get("job_spouse_form", ""))
        
        def get_quad_badge(target_code):
            badges = []
            if q_self == target_code: badges.append("<span style='background:#EA580C; color:#FFFFFF; font-size:12px; font-weight:800; padding:2px 8px; border-radius:4px;'>나</span>")
            if q_spouse == target_code: badges.append("<span style='background:#0284C7; color:#FFFFFF; font-size:12px; font-weight:800; padding:2px 8px; border-radius:4px;'>배우자</span>")
            return f"<div style='min-height:22px; margin-bottom:4px; display:flex; justify-content:center; gap:6px;'>{' '.join(badges)}</div>" if badges else "<div style='min-height:22px; margin-bottom:4px;'></div>"



        @st.cache_data
        def make_livelihood_icon(filename, width=88):
            """assets 폴더의 PNG를 사분면 카드용 HTML 이미지로 변환"""
            image_path = Path(__file__).resolve().parent / "assets" / filename

            with open(image_path, "rb") as image_file:
                encoded = base64.b64encode(image_file.read()).decode("ascii")

            return (
                f'<img src="data:image/png;base64,{encoded}" '
                f'width="{width}" alt="" '
                f'style="display:block; object-fit:contain; '
                f'max-width:100%; height:auto; margin:0 auto;">'
            )


        
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
            return f'<div style="{border_style} border-radius: 12px; padding: 14px 10px; text-align: center; display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100%; min-height: 195px; box-sizing: border-box; width: 100%;">{badge_html}<div style="height: 100px; display: flex; align-items: center; justify-content: center; margin-bottom: 4px;">{icon_html}</div><div style="font-size: 17.5px; font-weight: 850; color: #F8FAFC; line-height: 1.2;">{title}</div><div style="font-size: 13px; font-weight: 700; color: {accent_color}; margin: 3px 0 5px 0; line-height: 1.3;">{sub_title}</div><div style="font-size: 12.5px; color: #CBD5E1; line-height: 1.4; word-break: keep-all; text-align: center;">{desc}</div></div>'


        card_e = render_livelihood_quad("E", make_livelihood_icon("E_small_buckets.png", 88), "작은 물통 (E)", "나의 시간과 돈을 1:1 맞교환", "직접 일한 시간만큼 소득 창출<br><span style='color:#F59E0B; font-weight:600;'>(노동을 멈추면 수입도 멈춤)</span>", is_right=False)

        card_s = render_livelihood_quad("S", make_livelihood_icon("S_large_bucket.png", 112), "큰 물통 (S)", "전문성과 몸값으로 키운 물통", "한 번에 담는 물통의 양을 키운 모습<br><span style='color:#F59E0B; font-weight:600;'>(큰 물통이지만 여전히 지고 다님)</span>", is_right=False)

        card_b = render_livelihood_quad("B", make_livelihood_icon("B_pipeline_build.png", 112), "파이프라인<br>구축 (B)", "시스템 소유", "스스로 굴러가는 비즈니스 소유<br><span style='color:#38BDF8; font-weight:600;'>(내가 멈추어도 시스템이 일함)</span>", is_right=True)

        card_i = render_livelihood_quad("I", make_livelihood_icon("I_pipeline_connect.png", 112), "파이프라인<br>접속 (I)", "플랫폼·자본 접속", "이미 구축된 플랫폼에 접속 레버리지<br><span style='color:#38BDF8; font-weight:600;'>(자산과 네트워크가 소득을 만듦)</span>", is_right=True)

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

        # 고급모드 — 돌쇠와 똘똘이 우화 카드 호출
        render_dolssoe_story_card()

#--------------------------------------------------------
# 6.02.03 | 고급 모드 — 더 생각해보기 4대 질문
#--------------------------------------------------------
        st.markdown("""
<div style="margin: 28px 0 26px 0; padding: 4px 2px;">
<div style="font-size: 21px; font-weight: 850; color: #F8FAFC; margin-bottom: 6px;">더 생각해보기</div>
<div style="font-size: 14px; color: #94A3B8; margin-bottom: 18px; line-height: 1.6;">우리가 당연하게 여겨온 것들을 잠시 멈추어 생각해 봅니다.</div>
<div style="display: flex; flex-direction: column; gap: 14px;">
<div style="background: rgba(30, 41, 59, 0.35); border-left: 3.5px solid #64748B; border-radius: 4px; padding: 12px 16px; display: flex; align-items: baseline; gap: 12px;"><span style="font-size: 14px; font-weight: 800; color: #94A3B8; min-width: 24px;">01</span><span style="font-size: 18.5px; font-weight: 800; color: #F8FAFC; line-height: 1.5; word-break: keep-all;">'일을 하고 있는 것'과 '생계를 위해 반드시 일해야 하는 것'은 같은가?</span></div>
<div style="background: rgba(30, 41, 59, 0.35); border-left: 3.5px solid #64748B; border-radius: 4px; padding: 12px 16px; display: flex; align-items: baseline; gap: 12px;"><span style="font-size: 14px; font-weight: 800; color: #94A3B8; min-width: 24px;">02</span><span style="font-size: 18.5px; font-weight: 800; color: #F8FAFC; line-height: 1.5; word-break: keep-all;">'소득이 발생하는 것'과 '내가 직접 일해야 소득이 발생하는 것'은 같은가?</span></div>
<div style="background: rgba(30, 41, 59, 0.35); border-left: 3.5px solid #64748B; border-radius: 4px; padding: 12px 16px; display: flex; align-items: baseline; gap: 12px;"><span style="font-size: 14px; font-weight: 800; color: #94A3B8; min-width: 24px;">03</span><span style="font-size: 18.5px; font-weight: 800; color: #F8FAFC; line-height: 1.5; word-break: keep-all;">'직장을 그만두는 것'과 '은퇴'는 같은가?</span></div>
<div style="background: rgba(30, 41, 59, 0.35); border-left: 3.5px solid #64748B; border-radius: 4px; padding: 12px 16px; display: flex; align-items: baseline; gap: 12px;"><span style="font-size: 14px; font-weight: 800; color: #94A3B8; min-width: 24px;">04</span><span style="font-size: 18.5px; font-weight: 800; color: #F8FAFC; line-height: 1.5; word-break: keep-all;">'은퇴'란 무엇이며, '나'는 은퇴를 어떻게 바라보고 있나?</span></div>
</div></div>
""", unsafe_allow_html=True)

#--------------------------------------------------------
# 6.02.04 | 고급 모드 — 내가 생각하는 은퇴 예상 나이 및 벤치마크
#--------------------------------------------------------
        st.markdown("""
<div style="background: rgba(24, 32, 47, 0.65); border: 1.5px solid #3b4b66; border-radius: 14px; padding: 20px 22px; margin-bottom: 22px;">
<div style="font-size: 17px; font-weight: 750; color: #FDE68A; line-height: 1.6; word-break: keep-all; margin-bottom: 6px;">나는 언제부터 생계를 위해 반드시 일해야 하는 삶에서 벗어날 수 있을까?</div>
<div style="font-size: 20px; font-weight: 850; color: #F8FAFC; margin-bottom: 12px;">내가 생각하는 은퇴 예상 나이</div>
""", unsafe_allow_html=True)

        cur_user_age = int(st.session_state.person_age)
        default_retire = int(st.session_state.get("retirement_age") or 60)
        if default_retire < cur_user_age:
            default_retire = cur_user_age

        with st.container():
            r_col1, r_col2 = st.columns([3.2, 1.0])
            with r_col1:
                retirement_input = st.number_input(
                    "지금 하는 현업을 졸업(은퇴)하고 싶은 나이",
                    min_value=cur_user_age,
                    max_value=100,
                    value=default_retire,
                    step=1,
                    label_visibility="collapsed"
                )
            with r_col2:
                retirement_saved = st.button(
                    "은퇴 나이 확인",
                    use_container_width=True,
                    type="primary"
                )
        # 은퇴 예상 나이는 입력 즉시 공통 세션에 반영
        st.session_state["retirement_age"] = int(retirement_input)

        if retirement_saved:
            st.session_state["retire_age_saved_notice"] = True

        # 은퇴 나이 확인 버튼을 눌렀거나, 이미 은퇴 나이가 설정되어 있는 경우 노출
        if st.session_state.get("retire_age_saved_notice", False) or "retirement_age" in st.session_state:
            st.success(f"은퇴 예상 나이({st.session_state.get('retirement_age', retirement_input)}세)가 반영되었습니다.")

            st.markdown("""
<div style="background: rgba(15, 23, 42, 0.85); border: 1px solid #475569; border-radius: 10px; padding: 16px 18px; margin-top: 12px;">
<div style="font-size: 15px; font-weight: 800; color: #38BDF8; margin-bottom: 10px;">📊 국가데이터처 통계로 본 대한민국 3대 은퇴 분기점</div>
<div style="display: flex; flex-direction: column; gap: 8px; font-size: 14.5px; color: #E2E8F0; line-height: 1.6;">
  <div>• <b>"근로소득의 정점 및 본업 졸업"</b> 관점이라면 ➔ <span style="color: #F59E0B; font-weight: 800;">55~60세 전후</span> <span style="font-size: 13px; color: #94A3B8;">(주된 일자리 퇴직 평균 53세)</span></div>
  <div>• <b>"국가 통계적 흑자·적자 수지 균형"</b> 관점이라면 ➔ <span style="color: #F59E0B; font-weight: 800;">61세</span> <span style="font-size: 13px; color: #94A3B8;">(국민이전계정 NTA 공식 적자 재전환 연령)</span></div>
  <div>• <b>"완전히 노동을 손에서 놓는 시점"</b> 관점이라면 ➔ <span style="color: #F59E0B; font-weight: 800;">72~73세</span> <span style="font-size: 13px; color: #94A3B8;">(OECD 실질 은퇴 연령 및 2·3차 일자리 종료)</span></div>
</div>
</div>
""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)


#########################################################
# 6.03 | Tab 3 — 인생의 사계절
#########################################################
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

#--------------------------------------------------------
# 6.03.01 | 공통 — 공식 NTA 차트 빌더 함수
#--------------------------------------------------------
    def build_official_nta_chart():
        fig_official_nta = go.Figure()
        official_ages = [0, 5, 10, 14, 17, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 61, 65, 70, 75, 80, 85]
        official_income = [0, 0, 0, 0, 0, 3, 10, 18, 28, 27, 28, 38, 35, 39, 36, 26, 21, 14, 7, 2, 0.5, 0]
        official_expense = [4, 5, 18, 20, 22, 15, 19, 18, 22, 20, 19, 23, 20, 24, 26, 23, 23, 25, 16, 11, 7, 5]
        official_deficit = [e - i for e, i in zip(official_expense, official_income)]
        
        fig_official_nta.add_trace(go.Scatter(
            x=official_ages, y=official_deficit, mode="lines",
            line=dict(color="rgba(147, 197, 253, 0.0)", width=0),
            fill='tozeroy', fillcolor='rgba(147, 197, 253, 0.45)',
            name="생애주기 적자/흑자 (소비 - 노동소득)",
            hovertemplate="나이: %{x}세<br>적자/흑자 차액: <b>%{y:.1f}조 원</b><extra></extra>"
        ))
        fig_official_nta.add_trace(go.Scatter(
            x=official_ages, y=official_expense, mode="lines",
            line=dict(color="#65A30D", width=3, dash="dash"),
            name="소비",
            hovertemplate="나이: %{x}세<br>소비: <b>%{y:.1f}조 원</b><extra></extra>"
        ))
        fig_official_nta.add_trace(go.Scatter(
            x=official_ages, y=official_income, mode="lines",
            line=dict(color="#2563EB", width=3.5),
            name="노동소득",
            hovertemplate="나이: %{x}세<br>노동소득: <b>%{y:.1f}조 원</b><extra></extra>"
        ))
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
            title=dict(text="&lt; 생애주기 소득과 소비 &gt;", x=0.5, xanchor="center", font=dict(size=16, color="#F8FAFC")),
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
                range=[0, 85],
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

#--------------------------------------------------------
# 6.03.02 | 기본 모드 — 인생의 사계절 안내
#--------------------------------------------------------
    if not is_adv:
        # [기본 모드] 중복 제목 없이 3대 지표 + 내 계절 배지만 노출
        # [출처 ID: 6030200-01]
        st.markdown(
            '<div id="source-anchor-nta-basic"></div>',
            unsafe_allow_html=True
        )

        with st.container(horizontal=True, vertical_alignment="center", gap=None):
            st.caption(
                "가벼운 3분 산책: 국가데이터처 「2024년 국민이전계정」의 "
                "공식 지표를 통해 내 인생의 사계절 중 어디쯤 와 있는지 확인합니다."
            )
            if st.button(
                "☞",
                key="source_nta_basic",
                help="국가데이터처 2024년 국민이전계정 출처 보기",
                type="tertiary",
            ):
                _open_source_reference(
                    "6030200-01",
                    "인생의 사계절",
                    "source-anchor-nta-basic",
                )

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

        st.markdown("### 국가데이터처 공식 생애 통계 지표 (2024년 국민이전계정 · 대한민국 1인당 평균 기준)")
        c_m1, c_m2, c_m3 = st.columns(3)
        c_m1.metric("한국인 평균 흑자 진입", "28세", help="노동소득이 소비를 추월하는 연령")
        c_m2.metric("최대 흑자 정점", "45세", "연 1,932만 원")
        c_m3.metric("평균 적자 재전환", "61세", help="은퇴 후 소비가 노동소득을 다시 초과")

        fig_official_nta = build_official_nta_chart()
        st.plotly_chart(fig_official_nta, use_container_width=True, config={"displayModeBar": False, "scrollZoom": False, "doubleClick": False, "showAxisDragHandles": False})
        st.caption("출처: 국가데이터처 「2024년 국민이전계정」(2026. 9. 17. 발표). 28세 흑자 진입, 45세 최대 흑자(연 1,932만 원), 61세 적자 재진입 지표를 기준으로 표시합니다.")
        st.markdown(f"[📄 국가데이터처 2024년 국민이전계정 보도자료]({OFFICIAL_RELEASE_URL}) · [PDF 원문]({OFFICIAL_PDF_URL})")

        _, next_col = st.columns([5, 1])
        with next_col:
            if st.button("다음 →", key="basic_seasons_next", use_container_width=True, type="primary"):
                st.session_state["_pending_nav"] = "AI 시선"
                st.rerun()

    else:

#--------------------------------------------------------
# 6.03.03 | 고급 모드 — 1. 가족 구성원 나이 및 주택가격 기준 통계
#--------------------------------------------------------
        HOUSING_PRICE_SOURCE = {
            "기관": "한국부동산원",
            "서비스": "R-ONE 부동산통계정보",
            "조사명": "전국주택가격동향조사",
            "기준시점": "2025년 12월",
            "단위": "천원",
            "통계표": {
                "주택종합_평균": "A_2024_00025",
                "주택종합_중위": "A_2024_00027",
                "아파트_평균": "A_2024_00060",
                "아파트_중위": "A_2024_00062",
            },
            "유의사항": "평균·중위가격은 지역 간 가격 수준 비교용이며 시계열 가격 변동률 산출에는 적합하지 않음."
        }

        HOUSING_PRICE_DATA = {
            "서울": (971553.80, 730985.52, 1289425.52, 958000.00),
            "부산": (318320.03, 248908.43, 366711.09, 282000.00),
            "대구": (317554.67, 246429.82, 321226.18, 253500.00),
            "인천": (313505.90, 270821.95, 383246.94, 333500.00),
            "광주": (263456.13, 208528.23, 273138.10, 222000.00),
            "대전": (312666.25, 271365.61, 333865.33, 296500.00),
            "울산": (299595.23, 258011.48, 303239.79, 259000.00),
            "세종": (519184.01, 504995.09, 531779.84, 533000.00),
            "경기": (487418.21, 388431.39, 554567.89, 454000.00),
            "강원": (173667.76, 139350.97, 188085.45, 159000.00),
            "충북": (190726.72, 147059.38, 206815.65, 167000.00),
            "충남": (192370.35, 149066.06, 200927.89, 177000.00),
            "전북": (162832.90, 116139.19, 193999.22, 148000.00),
            "전남": (138772.70, 106559.48, 174020.68, 143000.00),
            "경북": (151964.16, 116928.27, 167634.81, 140000.00),
            "경남": (208788.94, 154977.99, 221808.54, 175000.00),
            "제주": (265384.89, 222651.58, 291781.39, 245000.00),
        }

        # 2024 주거실태조사 LTV1: 금융기관 대출 이용 가구의 구입가격 대비 대출 비율
        # 수도권·광역시 등 34.3%, 도지역 41.8%. 부산은 광역시 등에 포함.
        REGIONAL_LTV1 = {
            "서울": 34.3, "경기": 34.3, "인천": 34.3,
            "부산": 34.3, "대구": 34.3, "광주": 34.3,
            "대전": 34.3, "울산": 34.3, "세종": 34.3,
            "강원": 41.8, "충북": 41.8, "충남": 41.8,
            "전북": 41.8, "전남": 41.8, "경북": 41.8,
            "경남": 41.8, "제주": 41.8,
        }

        RETIREMENT_EXPENSE_SOURCE = {
            "기관": "국민연금공단 국민연금연구원",
            "조사명": "국민노후보장패널조사(KReIS)",
            "승인통계번호": "제322001호",
            "기준단위": "월 만 원",
            "산출기준": "건강한 노년을 전제로 응답자가 인식하는 주관적 노후 필요 생활비",
            "최소생활비_정의": "최저 생활을 유지하는 데 필요한 비용",
            "적정생활비_정의": "표준적인 생활을 하는 데 흡족한 비용",
            "유의사항": "실제 고령가구의 소비지출액이나 보장되는 연금액이 아닌 조사 응답자의 주관적 필요 생활비임.",
            "공식자료": {
                "2024년 부가조사_보도자료": "https://m.nps.or.kr/pnsgdnc/nscvrgdata/getOHAE0002M1.do?hmpgBbsCd=BS20240145&hmpgCd=01&menuId=MN24000898&pageIndex=1&pstId=ZZ202500000000001624&sortSe=FR",
                "2024년 부가조사_보고서": "https://institute.nps.or.kr/rschpblcn/whol/getOHBD0002M0.do?menuId=MN24001508&pblcnRptpSn=1670",
                "2023년 본조사_보고서": "https://institute.nps.or.kr/rschpblcn/whol/getOHBD0002M0.do?pblcnRptpSn=1603",
            }
        }

        RETIREMENT_EXPENSE_DATA = {
            "2023년_제10차_본조사": {
                "조사연도": 2023, "발표연도": 2024,
                "개인기준": {"최소생활비": 136.1, "적정생활비": 192.1},
                "부부기준": {"최소생활비": 217.1, "적정생활비": 296.9},
                "출처": "국민연금연구원 조사보고서 2024-01",
            },
            "2024년_제10차_부가조사": {
                "조사연도": 2024, "발표연도": 2025,
                "개인기준": {"최소생활비": 139.2, "적정생활비": 197.6},
                "부부기준": {"최소생활비": 216.6, "적정생활비": 298.1},
                "출처": "국민연금연구원 조사보고서 2025-01",
            },
        }

        RETIREMENT_EXPENSE_DEFAULT_SURVEY = "2024년_제10차_부가조사"
        RETIREMENT_INFLATION_RATE = None

        st.markdown("### 1. 우리 가족과 나의 은퇴 나이")
        child_options = ["입력 안 함", "없음", "1명", "2명", "3명", "4명 이상"]
        prev_c_count = st.session_state.get("child_count", "입력 안 함")
        if prev_c_count not in child_options:
            prev_c_count = "입력 안 함"

        child_count = st.selectbox(
            "자녀 수",
            child_options,
            index=child_options.index(prev_c_count),
            key="child_count_select_direct"
        )

        with st.container():
            spouse_age = st.number_input(
                "배우자 나이 (없거나 미입력 시 0)",
                min_value=0, max_value=120,
                value=int(st.session_state.get("spouse_age", 0)),
                step=1
            )

            child_age1, child_age2, child_age3, child_age4 = 0, 0, 0, 0

            if child_count in ["1명", "2명", "3명", "4명 이상"]:
                c1_col, c2_col = st.columns(2)
                with c1_col:
                    child_age1 = st.number_input(
                        "첫째 자녀 나이",
                        min_value=0, max_value=100,
                        value=int(st.session_state.get("child_age", 0)),
                        step=1
                    )
                with c2_col:
                    if child_count in ["2명", "3명", "4명 이상"]:
                        child_age2 = st.number_input(
                            "둘째 자녀 나이",
                            min_value=0, max_value=100,
                            value=int(st.session_state.get("child_age2", 0)),
                            step=1
                        )
                    else:
                        st.write("")

            if child_count in ["3명", "4명 이상"]:
                c3_col, c4_col = st.columns(2)
                with c3_col:
                    child_age3 = st.number_input(
                        "셋째 자녀 나이",
                        min_value=0, max_value=100,
                        value=int(st.session_state.get("child_age3", 0)),
                        step=1
                    )
                with c4_col:
                    if child_count == "4명 이상":
                        child_age4 = st.number_input(
                            "넷째 자녀 나이",
                            min_value=0, max_value=100,
                            value=int(st.session_state.get("child_age4", 0)),
                            step=1
                        )
                    else:
                        st.write("")

            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            f_col, m_col = st.columns(2)

            with f_col:
                father_age = st.number_input(
                    "아버지 나이 (선택, 모르면 0)",
                    min_value=0, max_value=120,
                    value=int(st.session_state.get("father_age", 0)),
                    step=1
                )

            with m_col:
                mother_age = st.number_input(
                    "어머니 나이 (선택, 모르면 0)",
                    min_value=0, max_value=120,
                    value=int(st.session_state.get("mother_age", 0)),
                    step=1
                )

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            st.markdown("#### 앞으로의 가족 계획 (선택)")

            p_c1, p_c2, p_c3 = st.columns(3)

            with p_c1:
                marriage_options = [
                    "미정", "계획 없음", "결혼 예정", "결혼함",
                    "1~3년 내 결혼 생각 있음",
                    "3년 이후 결혼 생각 있음"
                ]
                marriage_plan = st.selectbox(
                    "결혼 계획",
                    marriage_options,
                    index=marriage_options.index(
                        st.session_state.get("marriage_plan", "미정")
                    ) if st.session_state.get("marriage_plan", "미정") in marriage_options else 0
                )

                actual_marriage_age = int(
                    st.session_state.get("actual_marriage_age", 0) or 0
                )

                if marriage_plan == "결혼함":
                    actual_marriage_age = st.number_input(
                        "실제 결혼 나이 (선택, 0이면 자동 추정)",
                        min_value=0,
                        max_value=max(0, int(cur_age)),
                        value=min(
                            max(0, actual_marriage_age),
                            max(0, int(cur_age))
                        ),
                        step=1,
                        help="실제 결혼 나이를 알고 있다면 입력하세요. 입력하지 않으면 통계와 가족 정보를 바탕으로 추정합니다."
                    )

            with p_c2:
                child_plan_options = [
                    "미정", "계획 없음", "자녀 계획 있음",
                    "출산 예정", "추가 자녀 계획 있음", "추가 자녀 계획 없음"
                ]
                child_plan = st.selectbox(
                    "출산·자녀 계획",
                    child_plan_options,
                    index=child_plan_options.index(
                        st.session_state.get("child_plan", "미정")
                    ) if st.session_state.get("child_plan", "미정") in child_plan_options else 0
                )

            with p_c3:
                housing_options = [
                    "미정", "주택 구입 고려", "현재 주거 유지",
                    "전세·월세 이동 고려", "주거 계획 확정"
                ]
                housing_plan = st.selectbox(
                    "주거 계획",
                    housing_options,
                    index=housing_options.index(
                        st.session_state.get("housing_plan", "미정")
                    ) if st.session_state.get("housing_plan", "미정") in housing_options else 0
                )

            save_family_trigger = st.button(
                "입력 정보 AI 점검",
                use_container_width=True,
                type="primary"
            )

        st.session_state["child_count"] = child_count
        st.session_state["spouse_age"] = int(spouse_age or 0)
        st.session_state["child_age"] = int(child_age1 or 0)
        st.session_state["child_age2"] = int(child_age2 or 0)
        st.session_state["child_age3"] = int(child_age3 or 0)
        st.session_state["child_age4"] = int(child_age4 or 0)
        st.session_state["father_age"] = int(father_age or 0)
        st.session_state["mother_age"] = int(mother_age or 0)
        st.session_state["marriage_plan"] = marriage_plan
        st.session_state["child_plan"] = child_plan
        st.session_state["housing_plan"] = housing_plan
        st.session_state["family_info_checked"] = True

        housing_info_needed = (
            st.session_state.get("family_info_checked", False)
            and st.session_state.get("housing_plan", "미정")
            not in ["현재 주거 유지", "주거 계획 확정"]
        )

        if housing_info_needed:
            st.markdown("#### 주택가격 산정 기준")
            is_representative_case = st.session_state.get("_representative_case_id") in {
                "case_32_female", "case_45_female"
            }
            housing_region_options = (
                ["부산"] if is_representative_case
                else ["지역 선택"] + list(HOUSING_PRICE_DATA.keys())
            )
            prev_housing_region = st.session_state.get("housing_region", "부산" if is_representative_case else "지역 선택")
            if prev_housing_region not in housing_region_options:
                prev_housing_region = "부산" if is_representative_case else "지역 선택"

            housing_region = st.selectbox(
                "주택 구입 예정 지역",
                housing_region_options,
                index=housing_region_options.index(prev_housing_region),
                key="housing_region_select"
            )

            statistical_ltv = REGIONAL_LTV1.get(housing_region, 34.3)
            housing_ltv = REPRESENTATIVE_MORTGAGE_LTV * 100.0 if is_representative_case else statistical_ltv
            st.session_state["housing_region"] = housing_region
            st.session_state["housing_ltv"] = housing_ltv

            if housing_region != "지역 선택":
                if is_representative_case:
                    st.caption(
                        f"대표사례 기준: 주택가격 4억 원 · LTV {REPRESENTATIVE_MORTGAGE_LTV * 100:.0f}% "
                        f"→ 최초 대출 1억 4천만 원 · 자기자금 2억 6천만 원"
                    )
                else:
                    apartment_median_won = HOUSING_PRICE_DATA[housing_region][3] * 1000
                    housing_equity_won = apartment_median_won * (1 - housing_ltv / 100)
                    st.caption(
                        f"선택 지역: {housing_region} · "
                        f"아파트 중위가격: {apartment_median_won / 100000000:.2f}억 원 · "
                        f"통계 LTV1: {housing_ltv:.1f}% · "
                        f"자기자금 기준: {housing_equity_won / 100000000:.2f}억 원"
                    )

            st.caption("주택가격 자료: 한국부동산원 R-ONE · 전국주택가격동향조사 · 2025년 12월 아파트 중위가격")

#--------------------------------------------------------
# 6.03.04 | 고급 모드 — 은퇴 시점 가족 미래 나이 카드
#--------------------------------------------------------
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
<span style="font-size: 15.5px; font-weight: 800; color: #F8FAFC;">내 은퇴 시점의 우리 가족</span>
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

        c_age1 = int(getv("child_age", 0))
        if 0 < c_age1 < 20:
            college_my_age = cur_age + (20 - c_age1)
            st.markdown(f"""
<div style="background: rgba(234, 88, 12, 0.12); border-left: 4px solid #EA580C; border-radius: 6px; padding: 14px 18px; margin: 12px 0 20px 0;">
<div style="font-size: 15px; font-weight: 750; color: #F8FAFC; line-height: 1.6;">
<b>생애 주요지출</b><br>: '첫째가 대학에 입학하는 만 20세가 되면, 나의 나이는 <b>만 {college_my_age}세</b>가 되는구나...,'<br>
<span style="font-size: 13.5px; color: #CBD5E1;">국가데이터처 통계상 소득 정점(45세)은 지나가면서, 자녀 학자금과 독립 비용으로 <b>인생에서 가장 큰 지출이 집중되는 결정적 시기</b>입니다.</span>
</div></div>
""", unsafe_allow_html=True)
        elif c_age1 >= 20:
            st.markdown(f"""
<div style="background: rgba(30, 41, 59, 0.5); border-left: 4px solid #38BDF8; border-radius: 6px; padding: 14px 18px; margin: 12px 0 20px 0;">
<div style="font-size: 15px; font-weight: 750; color: #F8FAFC; line-height: 1.6;">
🌱 <b>가족 성장 단계</b>: 첫째 자녀(만 {c_age1}세)가 이미 성년기에 도달하여, 학자금 집중 지출기를 거쳐 독립과 사회 진출의 계절을 맞이하고 있습니다.
</div></div>
""", unsafe_allow_html=True)

#--------------------------------------------------------
# 6.03.05 | 고급 모드 — 2. 우리 가정 생애주기 재정곡선
#--------------------------------------------------------
        
#############    6.03.05.01 | 헤더 타이틀 및 기준 지역 안내 카드
        from plotly.subplots import make_subplots

        st.markdown("### 2. 우리 가정 생애주기 재정곡선")

        # 기본 기준 지역을 '부산'으로 지정하고 현재 선택된 지역 정보 추출
        selected_region = st.session_state.get("housing_region")
        if not selected_region or selected_region == "지역 선택":
            selected_region = "부산"
            st.session_state["housing_region"] = "부산"

        representative_case_id = st.session_state.get("_representative_case_id")
        is_representative_case = representative_case_id in {"case_32_female", "case_45_female"}
        selected_ltv = REPRESENTATIVE_MORTGAGE_LTV * 100.0 if is_representative_case else float(REGIONAL_LTV1.get(selected_region, 34.3))
        region_apt_price = (
            REPRESENTATIVE_HOME_PRICE_MAN if is_representative_case
            else HOUSING_PRICE_DATA.get(selected_region, HOUSING_PRICE_DATA["부산"])[3] / 10.0
        )
        home_equity_display = (
            region_apt_price - REPRESENTATIVE_MORTGAGE_PRINCIPAL_MAN
            if is_representative_case
            else region_apt_price * (1.0 - selected_ltv / 100.0)
        )

#############    6.03.05.02 | 기본 재무·연금 파라미터 수집 및 정제
        cur_age = int(st.session_state.get("person_age", 35) or 35)
        user_gender = st.session_state.get("gender", "🙋‍♂️ 남성")
        is_female = ("여성" in user_gender)
        career_st = st.session_state.get("career_stage", "🌱 3년 이하 (초년생)")
        
        self_job = str(st.session_state.get("job_form", "직장인") or "직장인")
        spouse_job_raw = str(st.session_state.get("job_spouse_form", "") or "")
        
        monthly_income_self = float(getv("income_self", 0) or 0)
        monthly_income_spouse = float(getv("income_spouse", 0) or 0)
        annual_bonus = float(getv("income_bonus", 0) or 0)
        annual_other_income = float(getv("income_other", 0) or 0) * 12.0
        
        representative_case_id = st.session_state.get("_representative_case_id")
        current_loan_interest_monthly = float(getv("expense_loan", 0) or 0)
        if representative_case_id == "case_45_female":
            current_payment_number = (cur_age - REPRESENTATIVE_MORTGAGE_PURCHASE_AGE) * 12 + 1
            _, _, current_loan_interest_monthly = mortgage_monthly_split(
                REPRESENTATIVE_MORTGAGE_PRINCIPAL_MAN,
                REPRESENTATIVE_MORTGAGE_ANNUAL_RATE,
                REPRESENTATIVE_MORTGAGE_TERM_YEARS,
                current_payment_number,
            )
        elif representative_case_id == "case_32_female":
            current_loan_interest_monthly = 0.0

        # 통계 비교용 소비지출에는 이자만 포함하고 원금은 제외한다.
        cur_annual_expense = (
            float(getv("expense_living", 0) or 0) * 12.0
            + current_loan_interest_monthly * 12.0
            + float(getv("expense_other", 0) or 0)
        )
        # 화면의 월 생활비는 대표값·통계 미탑재 시 대체값이며,
        # 은퇴 후 기본 지출 계산에는 아래 MDIS 연령대별 통계값을 직접 적용한다.
        ret_annual_expense = float(getv("retirement_monthly_expenses", 270) or 0) * 12.0

        # 2024 MDIS 가구주 연령대·가구원 수별 지출 통계표
        household_expense_stats = pd.DataFrame()
        try:
            stats_path = Path(__file__).resolve().parent / "data" / "기준데이터" / "국가데이터처_2024_가계동향조사_가구주연령대별가구원수별가계지출_가중중위값.csv"
            household_expense_stats = pd.read_csv(stats_path, dtype={"가구원수": str})
        except Exception as e:
            st.warning(f"가구 지출 통계표를 불러오지 못했습니다. 기존 입력 지출을 사용합니다. ({e})")

        monthly_pension = float(getv("income_pension", 0) or 0)
        annual_pension = monthly_pension * 12.0
        national_pension_start_age = 65

        other_self_enabled = bool(st.session_state.get("other_pension_self_enabled", False))
        other_self_annual = float(st.session_state.get("other_pension_self_amount", 0) or 0) * 12.0 if other_self_enabled else 0.0
        other_self_start_age = int(st.session_state.get("other_pension_self_age", 65) or 65)

        other_spouse_enabled = bool(st.session_state.get("other_pension_spouse_enabled", False))
        other_spouse_annual = float(st.session_state.get("other_pension_spouse_amount", 0) or 0) * 12.0 if other_spouse_enabled else 0.0
        other_spouse_start_age = int(st.session_state.get("other_pension_spouse_age", 65) or 65)

        m_plan = st.session_state.get("marriage_plan", "미정")
        c_plan = st.session_state.get("child_plan", "미정")
        h_plan = st.session_state.get("housing_plan", "미정")

#############    6.03.05.03 | 가족 타임라인 결정 엔진
        marriage_start = None
        if m_plan == "계획 없음":
            marriage_start = None
        elif m_plan == "결혼함":
            manual_marriage_age = int(st.session_state.get("actual_marriage_age", 0) or 0)
            conf_m = int(st.session_state.get("target_marriage_age", 0) or 0)
            if 20 <= manual_marriage_age <= cur_age:
                marriage_start = manual_marriage_age
            elif 20 <= conf_m <= cur_age:
                marriage_start = conf_m
            elif int(getv("child_age", 0) or 0) > 0:
                inferred_age = cur_age - int(getv("child_age", 0)) - 2
                marriage_start = max(20, min(cur_age, inferred_age))
            else:
                marriage_start = max(20, min(cur_age, 28 if is_female else 30))
        elif m_plan in ["결혼 예정", "1~3년 내 결혼 생각 있음"]:
            conf_m = int(st.session_state.get("target_marriage_age", 0) or 0)
            marriage_start = conf_m if conf_m > cur_age else cur_age + 2
        elif m_plan == "3년 이후 결혼 생각 있음":
            conf_m = int(st.session_state.get("target_marriage_age", 0) or 0)
            marriage_start = conf_m if conf_m > cur_age else cur_age + 4
        elif m_plan == "미정":
            conf_m = int(st.session_state.get("target_marriage_age", 0) or 0)
            if conf_m > cur_age:
                marriage_start = conf_m
            else:
                sim_marry_age = 32 if is_female else 34
                marriage_start = max(cur_age + 2, sim_marry_age)

#############    6.03.05.04 | 배우자 프로필 및 직업군 기준곡선 매핑
        has_future_or_current_spouse = (m_plan == "결혼함") or (marriage_start is not None)
        if spouse_job_raw and spouse_job_raw != "해당 없음":
            spouse_job = spouse_job_raw
        else:
            spouse_job = "직장인" if self_job == "전업주부" else self_job

        spouse_age_input = int(getv("spouse_age", 0) or 0)
        spouse_age_diff = (spouse_age_input - cur_age) if spouse_age_input > 0 else 0
        retire_age = int(st.session_state.get("retirement_age", 60) or 60)

#############    6.03.05.05 | 5대 생애 이벤트 총비용 및 기간 산출
        raw_c_count = st.session_state.get("child_count", "입력 안 함")
        existing_child_ages = []
        if raw_c_count == "1명":
            if int(getv("child_age", 0)) > 0: existing_child_ages.append(int(getv("child_age", 0)))
        elif raw_c_count == "2명":
            for k in ["child_age", "child_age2"]:
                if int(getv(k, 0)) > 0: existing_child_ages.append(int(getv(k, 0)))
        elif raw_c_count == "3명":
            for k in ["child_age", "child_age2", "child_age3"]:
                if int(getv(k, 0)) > 0: existing_child_ages.append(int(getv(k, 0)))
        elif raw_c_count == "4명 이상":
            for k in ["child_age", "child_age2", "child_age3", "child_age4"]:
                if int(getv(k, 0)) > 0: existing_child_ages.append(int(getv(k, 0)))

        childcare_windows = []
        college_windows = []
        wedding_windows = []

        for ca in existing_child_ages:
            birth_p_age = cur_age - ca
            childcare_windows.append((birth_p_age, birth_p_age + 6))
            c_start = cur_age + (19 - ca)
            college_windows.append((c_start, c_start + 4))
            w_start = cur_age + (30 - ca)
            wedding_windows.append((w_start, w_start + 5))

        future_birth_age = None
        if (
            has_future_or_current_spouse
            and c_plan in ["자녀 계획 있음", "출산 예정", "추가 자녀 계획 있음"]
        ):
            conf_b = int(st.session_state.get("target_birth_age", 0) or 0)
            if conf_b > cur_age:
                future_birth_age = conf_b
            else:
                base_m_age = cur_age if m_plan == "결혼함" else marriage_start
                future_birth_age = base_m_age + 2

        if future_birth_age is not None and future_birth_age <= 85:
            childcare_windows.append((future_birth_age, future_birth_age + 6))
            college_windows.append((future_birth_age + 19, future_birth_age + 19 + 4))
            wedding_windows.append((future_birth_age + 30, future_birth_age + 30 + 5))

        # 5) 주택구입 기간 (4년 구간)
        housing_start, housing_end = None, None
        conf_h = int(st.session_state.get("target_housing_age", 0) or 0)
        if conf_h > 0:
            housing_start = conf_h
            housing_end = housing_start + 4
        elif h_plan in ["주택 구입 고려", "주거 계획 확정"]:
            housing_start = max(cur_age + 5, 20)
            housing_end = housing_start + 4

        # 6) 사건별 총비용 산출 (기본 부산 기준)
        apartment_price_man = region_apt_price
        home_equity_man = home_equity_display
        half_home_equity_man = home_equity_man * 0.5

        marriage_cost_man = half_home_equity_man + 6298.0
        marriage_overlap_deduction_man = 2615.0  # 2024 가연 결혼비용 중 혼수: 가구 내구재 지출과 중복 의심
        childcare_cost_man = 8064.0
        childcare_overlap_deduction_man = 111.6 * 72.0  # 2024년 조사 월평균 양육비 × 72개월; 총지출에 포함된 부분만 차감
        housing_cost_man = home_equity_man
        # 자녀 대학 비용: 등록금과 생활비를 분리해 산출 (단위: 만 원)
        # 등록금: 2026학년도 비수도권 4년제 일반·교육대학 평균 연 661.96만 원 × 4년
        college_tuition_annual_man = 661.96
        college_tuition_total_man = college_tuition_annual_man * 4.0
        # 생활비: 2022년 대학생 학기 중 월평균 83만 원을 방학 포함 48개월에 적용한 모델 가정
        college_living_monthly_man = 83.0
        college_living_total_man = college_living_monthly_man * 48.0
        # 합계 약 6,631.84만 원 (기존 6,632만 원과 사실상 동일)
        college_cost_man = college_tuition_total_man + college_living_total_man
        college_overlap_deduction_man = college_cost_man  # 등록금·생활비 모두 MDIS 교육·일반생활 지출과 중복 의심
        # 자녀 결혼 지원 추정액 — 성별 입력 없이 양측 부모 지원 통계의 평균 적용
        # 가연 2024: 신혼집 24,176만 원, 신혼집 외 6,298만 원
        # 한국보건사회연구원 2020 표 3-2: 주거자금 중 부모 지원 7,616 / 전체 19,292
        # 양가 부모 지원을 절반씩 나눈 한쪽 부모의 평균 지원 비율을 적용
        child_housing_support_man = 24176.0 * (7616.0 / 19292.0) / 2.0
        # 한국보건사회연구원 2020 표 3-10: 평균 부모 지원 1,745 / 평균 측별 비용 3,611
        # 가연의 신혼집 외 비용은 양측 합산 총액이므로 절반을 한쪽 비용으로 보고 부모 지원 비율 적용
        child_other_wedding_support_man = 6298.0 * (1745.0 / 3611.0) / 2.0
        child_wedding_cost_man = child_housing_support_man + child_other_wedding_support_man
        # 신혼집 외 부모지원은 가구간 이전지출과 중복 의심. 주거자금 지원은 자산이전 성격으로 차감하지 않음.
        child_wedding_overlap_deduction_man = child_other_wedding_support_man

        event_costs = []

        # [수정 1] 본인 결혼:
        # - 미래 결혼: 신혼집 부담분 + 신혼집 외 비용을 2년에 걸쳐 분산 반영
        # - 과거 결혼: 신혼집 외 총비용 6,298만 원에서 혼수 중복분 2,615만 원을 차감한 금액을 반영
        #   (신혼집 부담분은 과거 실제 부담액을 확인할 수 없어 이번 계산에서는 제외)
        if marriage_start is not None and 20 <= marriage_start <= 85 and m_plan != "계획 없음":
            is_past_marriage = (m_plan == "결혼함")
            past_marriage_cost_man = 6298.0
            applied_marriage_cost_man = past_marriage_cost_man if is_past_marriage else marriage_cost_man
            applied_marriage_deduction_man = min(marriage_overlap_deduction_man, applied_marriage_cost_man)
            event_costs.append({
                "name": "나의 결혼",
                "start": marriage_start,
                "end": marriage_start + (1 if is_past_marriage else 2),
                "center": marriage_start,
                "total": applied_marriage_cost_man - applied_marriage_deduction_man,
                "display_total": applied_marriage_cost_man,
                "deducted_total": applied_marriage_deduction_man,
                "duration": 1 if is_past_marriage else 2,
                "color": "#3B82F6",
                "is_past": is_past_marriage
            })

        for start, end in childcare_windows:
            event_costs.append({
                "name": "출산·육아",
                "start": start,
                "end": end,
                "total": childcare_cost_man - childcare_overlap_deduction_man,
                "display_total": childcare_cost_man,
                "deducted_total": childcare_overlap_deduction_man,
                "duration": 6,
                "color": "#F97316",
                "is_past": (end <= cur_age)
            })
        if housing_start is not None and housing_end is not None:
            event_costs.append({
                "name": "주택구입",                "start": housing_start,
                "end": housing_end,
                "total": housing_cost_man,
                "display_total": housing_cost_man,
                "deducted_total": 0.0,
                "duration": 4,
                "color": "#14B8A6",
                "is_past": False
            })

        for start, end in college_windows:
            event_costs.append({
                "name": "자녀 대학",
                "start": start,
                "end": end,
                "total": college_cost_man - college_overlap_deduction_man,
                "display_total": college_cost_man,
                "deducted_total": college_overlap_deduction_man,
                "duration": 4,
                "color": "#A855F7",
                "is_past": (end <= cur_age)
            })

        for start, end in wedding_windows:
            event_costs.append({
                "name": "자녀 결혼",
                "start": start,
                "end": end,
                "total": child_wedding_cost_man - child_wedding_overlap_deduction_man,
                "display_total": child_wedding_cost_man,
                "deducted_total": child_wedding_overlap_deduction_man,
                "duration": 5,
                "color": "#F43F5E",
                "is_past": False
            })

        # 이벤트의 total은 중복 차감 후 가구 지출곡선에 추가할 금액.
        # display_total은 예보원 면적을 결정하는 차감 전 총비용.
        # 총비용과 차감액은 아래 시뮬레이션에서 동일한 연령별 CPI 상대계수를 적용받음.
        event_expense_by_age = {a: 0.0 for a in range(0, life_expectancy)}
        for event in event_costs:
            if event["total"] > 0:
                annual_addition = event["total"] / float(event["duration"])
                for a in range(max(20, event["start"]), min(life_expectancy, event["end"])):
                    event_expense_by_age[a] += annual_addition

#############    6.03.05.06 | 기준곡선 보간(Interpolation) 및 감쇄 엔진
        ages_base = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75]
        employee_base = [180, 270, 350, 420, 460, 469, 445, 360, 280, 210, 160, 120]
        self_employed_base = [130, 210, 290, 350, 390, 410, 420, 400, 350, 290, 230, 170]

        def get_job_base(job):
            if job == "전업주부": return None
            if job in ("직장인", "공무원"): return employee_base
            return self_employed_base

        def interpolate_income(age, values):
            if age <= ages_base[0]: return values[0]
            if age >= ages_base[-1]: return values[-1]
            for i in range(len(ages_base) - 1):
                if ages_base[i] <= age <= ages_base[i + 1]:
                    ratio = (age - ages_base[i]) / float(ages_base[i + 1] - ages_base[i])
                    return values[i] + (values[i + 1] - values[i]) * ratio
            return 0.0

        def extended_base_income(age, values):
            if values is None: return 0.0
            if age <= 75: return interpolate_income(age, values)
            slope = (values[-1] - values[-2]) / 5.0
            return max(0.0, values[-1] + slope * (age - 75))

        self_base = get_job_base(self_job)
        spouse_base = get_job_base(spouse_job) if has_future_or_current_spouse else None

        self_base_at_cur = extended_base_income(cur_age, self_base)

        # 현재 입력소득은 경력단절 후 실제소득일 수 있으므로,
        # 현재 연령에 적용되는 경력복귀 80% 감액을 기준곡선 배율 산정 전에 복원한다.
        current_is_in_childcare = any(
            c_start <= cur_age < c_end for c_start, c_end in childcare_windows
        )
        current_has_completed_childcare = any(
            cur_age >= c_end for c_start, c_end in childcare_windows
        )
        current_career_recovery_ratio = (
            0.80
            if is_female and current_has_completed_childcare and not current_is_in_childcare
            else 1.0
        )
        normalized_monthly_income_self = monthly_income_self / current_career_recovery_ratio
        normalized_annual_bonus = annual_bonus / current_career_recovery_ratio

        self_scale = (
            normalized_monthly_income_self / self_base_at_cur
            if (self_base_at_cur > 0 and monthly_income_self > 0)
            else (1.0 if self_base else 0.0)
        )

        cur_spouse_age = cur_age + spouse_age_diff
        sp_base_at_cur = extended_base_income(cur_spouse_age, spouse_base)
        
        # 동질혼 반영: 배우자 소득 미입력 시 본인 소득 비율(self_scale) 연동
        if monthly_income_spouse > 0 and sp_base_at_cur > 0:
            spouse_scale = monthly_income_spouse / sp_base_at_cur
        else:
            spouse_scale = self_scale if (spouse_base is not None) else 0.0

#############    6.03.05.06.01 | MDIS 가구 지출 통계 매핑 및 현재 지출 보정
        def household_age_band(age):
            if age >= 80:
                return "80세 이상"
            lower = (int(age) // 5) * 5
            return f"{lower}~{lower + 4}세"

        def household_size_at_age(age):
            # 은퇴 시점에는 자녀가 독립한 것으로 보고, 부부 2인(비혼은 1인) 가구로 전환
            if age >= retire_age:
                return 2 if marriage_start is not None else 1

            size = 1
            if marriage_start is not None and age >= marriage_start:
                size += 1
            for child_age_value in existing_child_ages:
                birth_age = cur_age - child_age_value
                if age >= birth_age:
                    size += 1
            if future_birth_age is not None and age >= future_birth_age:
                size += 1
            return min(size, 5)

        def lookup_household_expense(age, household_size):
            if household_expense_stats.empty:
                return None

            age_band = household_age_band(age)
            size_label = str(household_size) if household_size <= 4 else "5인 이상"
            amount_col = "월중위_가계지출_만원"

            rows = household_expense_stats[
                (household_expense_stats["가구주_연령대"] == age_band)
                & (household_expense_stats["가구원수"] == size_label)
            ]
            rows = rows[rows[amount_col].notna()]

            fallback = False
            if rows.empty:
                # 해당 연령대·가구원 수 셀이 비어 있으면 같은 연령대의 가장 가까운 가구원 수를 참고
                same_age = household_expense_stats[
                    (household_expense_stats["가구주_연령대"] == age_band)
                    & (household_expense_stats[amount_col].notna())
                ].copy()
                if not same_age.empty:
                    def size_rank(value):
                        return 5 if value == "5인 이상" else int(value)
                    same_age["_size_distance"] = same_age["가구원수"].map(
                        lambda value: abs(size_rank(value) - household_size)
                    )
                    rows = same_age.sort_values("_size_distance").head(1)
                else:
                    # 연령대 셀 자체가 없을 때는 같은 가구원 수의 가장 가까운 연령대를 참고
                    same_size = household_expense_stats[
                        (household_expense_stats["가구원수"] == size_label)
                        & (household_expense_stats[amount_col].notna())
                    ].copy()
                    if same_size.empty:
                        return None
                    same_size["_age_distance"] = same_size["가구주_연령대"].map(
                        lambda value: abs(
                            (80 if value == "80세 이상" else int(value.split("~")[0]) + 2)
                            - age
                        )
                    )
                    rows = same_size.sort_values("_age_distance").head(1)
                fallback = True

            row = rows.iloc[0]
            used_size = row["가구원수"]
            used_age_band = row["가구주_연령대"]
            sample_n = int(row["표본수"])
            return {
                "monthly": float(row[amount_col]),
                "sample_n": sample_n,
                "age_band": used_age_band,
                "household_size": used_size,
                "fallback": fallback or used_size != size_label or used_age_band != age_band,
                "small_sample": sample_n < 30,
            }

        # 2024년 MDIS 기준곡선을 연령별 해당 연도의 명목가치로 옮기기 위한 거시지수
        macro_index_stats = pd.DataFrame()
        try:
            macro_path = Path(__file__).resolve().parent / "data" / "기준데이터" / "국가데이터처_소비자물가지수_및_고용노동부_임금지수_1965-2025.csv"
            macro_index_stats = pd.read_csv(macro_path)
        except Exception as e:
            st.warning(f"통시성 보정 지수표를 불러오지 못했습니다. ({e})")

        current_calendar_year = date.today().year
        cpi_reference_year = 2024
        cpi_reference_index = None
        if not macro_index_stats.empty:
            cpi_reference_rows = macro_index_stats[macro_index_stats["year"] == cpi_reference_year]
            if not cpi_reference_rows.empty and pd.notna(cpi_reference_rows.iloc[0]["cpi_index_2020_100"]):
                cpi_reference_index = float(cpi_reference_rows.iloc[0]["cpi_index_2020_100"])

        def macro_index_at_or_before(year, column):
            if macro_index_stats.empty:
                return None
            valid = macro_index_stats[
                (macro_index_stats["year"] <= year) & macro_index_stats[column].notna()
            ].sort_values("year")
            if valid.empty:
                return None
            return float(valid.iloc[-1][column])

        def historical_cagr(column, start_year, end_year):
            """실제 관측된 시작·종료 지수로 연평균 복합상승률을 계산한다."""
            if macro_index_stats.empty:
                return 0.0
            start_rows = macro_index_stats[
                (macro_index_stats["year"] == start_year) & macro_index_stats[column].notna()
            ]
            end_rows = macro_index_stats[
                (macro_index_stats["year"] == end_year) & macro_index_stats[column].notna()
            ]
            if start_rows.empty or end_rows.empty or end_year <= start_year:
                return 0.0
            start_value = float(start_rows.iloc[0][column])
            end_value = float(end_rows.iloc[0][column])
            if start_value <= 0 or end_value <= 0:
                return 0.0
            return (end_value / start_value) ** (1.0 / (end_year - start_year)) - 1.0

        # 2011~2025년 실제 관측 임금·물가 지수의 CAGR을 미래 시뮬레이션 가정으로 사용
        wage_forecast_rate = historical_cagr(
            "moel_wage_index_2024_100", 2011, 2025
        )
        cpi_forecast_rate = historical_cagr(
            "cpi_index_2020_100", 2011, 2025
        )

        def macro_index_for_model_year(year, column, forecast_rate):
            """실제 연도는 관측값, 미래 연도는 최신 실적 수준에서 CAGR로 연장한다."""
            if year <= current_calendar_year:
                return macro_index_at_or_before(year, column)
            latest_observed = macro_index_at_or_before(current_calendar_year, column)
            if latest_observed is None:
                return None
            return latest_observed * ((1.0 + forecast_rate) ** (year - current_calendar_year))

        latest_cpi_index = macro_index_at_or_before(current_calendar_year, "cpi_index_2020_100")
        latest_wage_index = macro_index_at_or_before(current_calendar_year, "moel_wage_index_2024_100")
        cpi_current_factor = (
            latest_cpi_index / cpi_reference_index
            if latest_cpi_index is not None and cpi_reference_index
            else 1.0
        )

        current_household_size = household_size_at_age(cur_age)
        current_expense_reference = lookup_household_expense(cur_age, current_household_size)
        # 대표사례는 통계 기준선을 100%로 적용한다. 개인 사례만 현재 입력 지출과 가중중위값의 비율을 반영한다.
        if is_representative_case:
            expense_scale_ratio = 1.0
        elif current_expense_reference and current_expense_reference["monthly"] > 0 and cur_annual_expense > 0:
            expense_scale_ratio = cur_annual_expense / (
                current_expense_reference["monthly"] * 12.0 * cpi_current_factor
            )
        else:
            expense_scale_ratio = 1.0

        #############    6.03.05.07 | 연령별 소득·지출 흐름 시뮬레이션 루프
        ages_sim = list(range(20, life_expectancy))
        my_income_curve = []
        household_income_curve = []
        household_expense_curve = []
        mortgage_principal_curve = []
        mortgage_interest_curve = []
        mortgage_balance_curve = []
        expense_debug_rows = []  # 임시 진단: 연령별 기본 지출·생애사건 지출 분리 확인

        for a in ages_sim:
            # 연령 a가 실제로 해당하는 달력연도. 실행 시점의 현재 나이를 기준으로 과거·미래를 연결한다.
            calendar_year = current_calendar_year + (a - cur_age)
            year_cpi_index = macro_index_for_model_year(
                calendar_year, "cpi_index_2020_100", cpi_forecast_rate
            )
            year_wage_index = macro_index_for_model_year(
                calendar_year, "moel_wage_index_2024_100", wage_forecast_rate
            )
            cpi_year_factor = (
                year_cpi_index / cpi_reference_index
                if year_cpi_index is not None and cpi_reference_index
                else 1.0
            )
            cpi_relative_to_current = (
                year_cpi_index / latest_cpi_index
                if year_cpi_index is not None and latest_cpi_index
                else 1.0
            )
            # 임금지수는 2011년부터 제공된다. 그 이전은 임의 보간하지 않고 원래 기준값을 유지한다.
            wage_year_factor = (
                year_wage_index / latest_wage_index
                if year_wage_index is not None and latest_wage_index
                else 1.0
            )

            # --- [A. 본인 단독 근로소득] ---
            if a < retire_age:
                self_inc = extended_base_income(a, self_base) * self_scale * 12.0
                self_inc += normalized_annual_bonus

                # 여성 출산·육아기 경력단절 및 80% 하향 복귀 모델링
                if is_female and childcare_windows:
                    is_in_childcare = False
                    has_completed_childcare = False

                    for c_start, c_end in childcare_windows:
                        if c_start <= a < c_end:
                            is_in_childcare = True
                            years_in = a - c_start
                            drop_ratio = 0.35 if years_in <= 1 else 0.50
                            self_inc *= drop_ratio
                            break
                        elif a >= c_end:
                            has_completed_childcare = True

                    if not is_in_childcare and has_completed_childcare:
                        self_inc *= 0.80
            else:
                self_inc = 0.0

            # 근로소득·상여금에 해당 연도의 임금지수 적용
            self_inc *= wage_year_factor
            my_income_curve.append(self_inc)

            # --- [B. 배우자 근로소득] ---
            spouse_inc = 0.0
            sp_a = a + spouse_age_diff

            if has_future_or_current_spouse and (marriage_start is not None) and (a >= marriage_start):
                if sp_a < retire_age:
                    spouse_inc = extended_base_income(sp_a, spouse_base) * spouse_scale * 12.0
                    spouse_inc *= wage_year_factor

            # --- [C. 가구 합산 소득] ---
            total_hh_inc = self_inc + spouse_inc + annual_other_income

            if has_future_or_current_spouse:
                if a >= national_pension_start_age:
                    total_hh_inc += (annual_pension / 2.0)
                if sp_a >= national_pension_start_age:
                    total_hh_inc += (annual_pension / 2.0)
            else:
                if a >= national_pension_start_age:
                    total_hh_inc += annual_pension

            if other_self_enabled and a >= other_self_start_age:
                total_hh_inc += other_self_annual
            if has_future_or_current_spouse and other_spouse_enabled and sp_a >= other_spouse_start_age:
                total_hh_inc += other_spouse_annual

            household_income_curve.append(total_hh_inc)

            # --- [D. 주택대출 원리금 분리] ---
            annual_mortgage_principal = 0.0
            annual_mortgage_interest = 0.0
            if is_representative_case:
                first_payment = (a - REPRESENTATIVE_MORTGAGE_PURCHASE_AGE) * 12 + 1
                for payment_number in range(first_payment, first_payment + 12):
                    _, principal_part, interest_part = mortgage_monthly_split(
                        REPRESENTATIVE_MORTGAGE_PRINCIPAL_MAN,
                        REPRESENTATIVE_MORTGAGE_ANNUAL_RATE,
                        REPRESENTATIVE_MORTGAGE_TERM_YEARS,
                        payment_number,
                    )
                    annual_mortgage_principal += principal_part
                    annual_mortgage_interest += interest_part
            mortgage_principal_curve.append(annual_mortgage_principal)
            mortgage_interest_curve.append(annual_mortgage_interest)
            mortgage_balance_at_age_start = (
                mortgage_balance_after_payments(
                    REPRESENTATIVE_MORTGAGE_PRINCIPAL_MAN,
                    REPRESENTATIVE_MORTGAGE_ANNUAL_RATE,
                    REPRESENTATIVE_MORTGAGE_TERM_YEARS,
                    (a - REPRESENTATIVE_MORTGAGE_PURCHASE_AGE) * 12,
                )
                if is_representative_case and a >= REPRESENTATIVE_MORTGAGE_PURCHASE_AGE
                else 0.0
            )
            mortgage_balance_curve.append(mortgage_balance_at_age_start)

            # --- [E. 가구 지출 곡선] ---
            household_size = household_size_at_age(a)
            expense_reference = lookup_household_expense(a, household_size)

            if a < retire_age:
                # 은퇴 전: 연령대·가구원 수별 MDIS 가중중위값에 개인별 지출 수준 보정계수를 적용
                if expense_reference:
                    base_exp = (
                        expense_reference["monthly"] * 12.0
                        * expense_scale_ratio * cpi_year_factor
                    )
                else:
                    base_exp = cur_annual_expense * cpi_relative_to_current
            else:
                # 은퇴 후: 자녀 독립 후 가구원 수(부부 2인)를 기준으로
                # 해당 연령대 MDIS 가중중위값을 적용하고 2024년 기준에서 해당 연도로 통시성 보정
                if expense_reference:
                    base_exp = expense_reference["monthly"] * 12.0 * cpi_year_factor
                else:
                    # 통계표를 읽지 못한 경우에만 화면 입력값을 대체 기준으로 사용
                    base_exp = ret_annual_expense * cpi_relative_to_current

            # 결혼·출산·교육 등 생애사건 비용도 발생 연도의 물가 기준으로 환산
            event_expense = event_expense_by_age.get(a, 0.0) * cpi_relative_to_current
            total_hh_exp = base_exp + event_expense
            household_expense_curve.append(total_hh_exp)
            if 30 <= a <= 45 or a >= retire_age:
                expense_debug_rows.append({
                    "나이": a,
                    "가구원 수": household_size,
                    "통계 기준 월지출(만원)": expense_reference["monthly"] if expense_reference else None,
                    "적용 연령대": expense_reference["age_band"] if expense_reference else "",
                    "표본 수": expense_reference["sample_n"] if expense_reference else None,
                    "표본 주의": "30 미만" if expense_reference and expense_reference["small_sample"] else "",
                    "통계 대체 적용": bool(expense_reference and expense_reference["fallback"]),
                    "기본 지출(만원/년)": base_exp,
                    "주택대출 연초 잔액(만원)": mortgage_balance_at_age_start,
                    "주택대출 원금상환(만원/년)": annual_mortgage_principal,
                    "주택대출 이자(만원/년)": annual_mortgage_interest,
                    "생애사건 추가 지출(만원/년)": event_expense,
                    "최종 가구 지출(만원/년)": total_hh_exp,
                })

        st.caption(
            "통시성 보정 적용: 근로소득은 2011~2025년 실제 임금지수, 지출은 실제 CPI를 사용합니다. "
            "2026년은 최신 실적연도(2025년) 수준을 기준점으로 두고, 2027년 이후에는 2011~2025년 연평균 복합상승률 "
            f"(임금 {wage_forecast_rate * 100:.2f}%, 물가 {cpi_forecast_rate * 100:.2f}%)을 미래 가정으로 적용합니다. "
            "2011년 이전 임금지수는 자료가 없어 임의 추정하지 않습니다."
        )

        # 임시 진단 패널: 계산식과 그래프에는 영향을 주지 않음
        with st.expander("🔎 임시 진단 — 연령별 가구 지출 계산", expanded=True):
            st.write({
                "현재 나이": cur_age,
                "결혼 상태(m_plan)": m_plan,
                "결혼 시작 나이(marriage_start)": marriage_start,
                "현재 가구원 수": current_household_size,
                "현재 연령·가구원 수 통계 월지출(만원)": current_expense_reference["monthly"] if current_expense_reference else None,
                "현재 통계 표본 수": current_expense_reference["sample_n"] if current_expense_reference else None,
                "현재 가구 연간 기본 지출(만원)": cur_annual_expense,
                "현재 지출 보정계수": round(expense_scale_ratio, 4),
                "실제 결혼 나이 입력값": st.session_state.get("actual_marriage_age", 0),
                "목표 결혼 나이 입력값": st.session_state.get("target_marriage_age", 0),
            })
            st.dataframe(pd.DataFrame(expense_debug_rows), use_container_width=True, hide_index=True)

#############    6.03.05.08 | 가구 순수지 분리 및 Y축 자동 스케일링
        # MDIS 가계지출에는 이자 등 비소비지출이 포함되므로 이자를 별도 가산하지 않는다.
        # 원금은 소비지출에서 제외하되 실제 현금 유출이므로 순현금흐름에서 별도 차감한다.
        net_flow = [
            i - e - p
            for i, e, p in zip(household_income_curve, household_expense_curve, mortgage_principal_curve)
        ]

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

        # [버그 수정] [20:] 슬라이싱을 제거하고 20세~기대수명 전체 구간에서 최대치 산출
        max_exp_val = max(household_expense_curve) if household_expense_curve else 5000.0
        max_income_val = max(household_income_curve) if household_income_curve else 6000.0

        y_max = max(max_income_val, max_exp_val)
        y_top = max(10000.0, y_max * 1.15)  # 최소 10,000(1억) 확보
        alt_level_2 = y_top * 0.35
        alt_level_1 = y_top * 0.12

        fig_my_nta = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.26,
            row_heights=[0.55, 0.45]
        )

#############    6.03.05.09 | 이벤트 버블 마커 Trace 생성
        max_event_total = max((event.get("display_total", event["total"]) for event in event_costs), default=1.0)

        for event in event_costs:
            event_mid_age = event.get("center", (event["start"] + event["end"] - 1) / 2.0)
            if not 20 <= event_mid_age <= life_expectancy: continue

            event_age_index = min(range(len(ages_sim)), key=lambda i: abs(ages_sim[i] - event_mid_age))
            event_y = household_expense_curve[event_age_index]

            disp_tot = event.get("display_total", event["total"])
            marker_size = 65 * ((disp_tot / max_event_total) ** 0.5)

            deducted_tot = event.get("deducted_total", 0.0)
            cashflow_tot = event.get("total", 0.0)
            if event.get("is_past") and event.get("name") != "나의 결혼":
                hover_cost_str = "과거 완료된 생애 사건"
            else:
                hover_cost_str = (
                    f"이벤트 총비용: {disp_tot:,.0f}만 원<br>"
                    f"중복 의심 차감: {deducted_tot:,.0f}만 원<br>"
                    f"가구지출 추가분: {cashflow_tot:,.0f}만 원"
                )

            fig_my_nta.add_trace(go.Scatter(
                x=[event_mid_age],
                y=[event_y],
                mode="markers",
                marker=dict(size=marker_size, color=event["color"], opacity=0.35, line=dict(color=event["color"], width=1.5)),
                name=event["name"],
                showlegend=False,
                hovertemplate=(
                    f"<b>{event['name']}</b><br>"
                    f"연령: {event['start']}~{event['end'] - 1}세<br>"
                    f"{hover_cost_str}"
                    "<extra></extra>"
                )
            ), row=1, col=1)

            # 이벤트 타이틀: 버블 중심에서 반지름의 절반만큼 안쪽으로 배치
            title_shift = marker_size * 0.25
            title_on_right = event_mid_age < (min(ages_sim) + max(ages_sim)) / 2
            fig_my_nta.add_annotation(
                x=event_mid_age,
                y=event_y,
                xref="x",
                yref="y",
                xshift=title_shift if title_on_right else -title_shift,
                text=event["name"],
                showarrow=False,
                xanchor="left" if title_on_right else "right",
                font=dict(size=11, color=event["color"], weight="bold")
            )

        # [Row 1] 가구 소득, 본인 단독소득 보조 점선, 가구 지출 (20세~기대수명)
        fig_my_nta.add_trace(go.Scatter(
            x=ages_sim, y=household_income_curve, mode="lines",
            line=dict(color="#10B981", width=3.4, shape='spline', smoothing=0.8),
            name="가구 소득",
            hovertemplate="나이: %{x}세<br>연간 가구소득: <b>%{y:,.0f}만 원</b><extra></extra>"
        ), row=1, col=1)

        if has_future_or_current_spouse and marriage_start is not None and marriage_start < retire_age:
            fig_my_nta.add_trace(go.Scatter(
                x=ages_sim, y=my_income_curve, mode="lines",
                line=dict(color="rgba(16, 185, 129, 0.40)", width=1.8, dash="dot", shape='spline'),
                name="본인 단독소득",
                hovertemplate="나이: %{x}세<br>본인 단독소득: <b>%{y:,.0f}만 원</b><extra></extra>"
            ), row=1, col=1)

        fig_my_nta.add_trace(go.Scatter(
            x=ages_sim, y=household_expense_curve, mode="lines",
            line=dict(color="#F97316", width=3.2, dash="dot", shape='linear'),
            name="가구 지출",
            hovertemplate="나이: %{x}세<br>연간 가구지출: <b>%{y:,.0f}만 원</b><extra></extra>"
        ), row=1, col=1)

        # 기준선 렌더링: 두 차트 사이 여백에 화살표 없는 라벨 표시
        current_line_color = "#38BDF8"
        fig_my_nta.add_vline(x=cur_age, line_dash="solid", line_color=current_line_color, line_width=2.0)
        fig_my_nta.add_annotation(
            x=cur_age, y=0.533,
            xref="x", yref="paper",
            text=f"현재 ({cur_age}세)",
            showarrow=False,
            font=dict(size=11, color="#BAE6FD", weight="bold"),
            bgcolor="rgba(15, 23, 42, 0.9)",
            bordercolor=current_line_color, borderwidth=1.2, borderpad=3
        )

        retire_line_color = "#F8FAFC"
        fig_my_nta.add_vline(x=retire_age, line_dash="dot", line_color=retire_line_color, line_width=2.2)
        fig_my_nta.add_annotation(
            x=retire_age, y=0.533,
            xref="x", yref="paper",
            text=f"은퇴 ({retire_age}세)",
            showarrow=False,
            font=dict(size=11, color=retire_line_color, weight="bold"),
            bgcolor="rgba(15, 23, 42, 0.9)",
            bordercolor=retire_line_color, borderwidth=1.2, borderpad=3
        )

        # [Row 2] 0선 기준선 및 가구 순수지 영역 (20세~기대수명)
        fig_my_nta.add_hline(y=0, line_dash="solid", line_color="#94A3B8", line_width=1.5, row=2, col=1)

        fig_my_nta.add_trace(go.Scatter(
            x=ages_fine, y=surplus_fine, mode="lines",
            line=dict(width=0, color="rgba(0,0,0,0)"),
            fill='tozeroy', fillcolor='rgba(16, 185, 129, 0.28)',
            showlegend=False,
            hoverinfo="skip"
        ), row=2, col=1)

        fig_my_nta.add_trace(go.Scatter(
            x=ages_fine, y=deficit_fine, mode="lines",
            line=dict(width=0, color="rgba(0,0,0,0)"),
            fill='tozeroy', fillcolor='rgba(239, 68, 68, 0.28)',
            showlegend=False,
            hoverinfo="skip"
        ), row=2, col=1)

        fig_my_nta.add_trace(go.Scatter(
            x=ages_sim, y=net_flow, mode="lines",
            line=dict(color="#CBD5E1", width=2.4, shape='spline', smoothing=0.8),
            name="가구 순현금흐름 (소득-지출-원금상환)",
            hovertemplate="나이: %{x}세<br>가구 순현금흐름: <b>%{y:,.0f}만 원</b><extra></extra>"
        ), row=2, col=1)

        fig_my_nta.add_annotation(
            x=45, y=0.15,
            xref="x", yref="y2 domain",
            yanchor="bottom",
            text="▲ 가구 흑자 (소득 > 지출)", showarrow=False,
            font=dict(size=10.5, color="#86EFAC", weight="bold"),
            bgcolor="rgba(15, 23, 42, 0.8)", bordercolor="rgba(34, 197, 94, 0.5)", borderpad=2
        )
        fig_my_nta.add_annotation(
            x=68, y=0.55,
            xref="x", yref="y2 domain",
            yanchor="top",
            text="▼ 가구 적자 (지출 > 소득)", showarrow=False,
            font=dict(size=10.5, color="#FCA5A5", weight="bold"),
            bgcolor="rgba(15, 23, 42, 0.8)", bordercolor="rgba(239, 68, 68, 0.5)", borderpad=2
        )

#############    6.03.05.10 | 2단 서브플롯 조립 및 Plotly 렌더링
        fig_my_nta.update_layout(
            height=630,
            # 가로보기에서 범례가 플롯 영역과 겹치지 않도록 상단 여백 확보
            margin=dict(l=10, r=10, t=70, b=25),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E2E8F0", size=12),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.10,
                xanchor="center",
                x=0.5,
                font=dict(size=11, color="#F1F5F9")
            ),
            hovermode="x unified"
        )

        # X축: 20세부터 성별 기대수명까지 10년 단위 정렬
        fig_my_nta.update_xaxes(
            tickmode="linear", tick0=20, dtick=10,
            range=[20, life_expectancy],
            tickangle=0,
            tickfont=dict(size=12, color="#94A3B8"),
            gridcolor="rgba(100, 116, 139, 0.18)",
            showline=True, linecolor="#334155", linewidth=1.5, mirror=True,
            fixedrange=True
        )
        fig_my_nta.update_xaxes(title=dict(text="연령 (세)", font=dict(size=12, color="#94A3B8")), row=2, col=1)

        # Y축 상한선 일괄 적용
        fig_my_nta.update_yaxes(
            title=None,
            tickfont=dict(size=11, color="#94A3B8"),
            tickformat=",.0f",
            gridcolor="rgba(100, 116, 139, 0.18)",
            showline=True, linecolor="#334155", linewidth=1.5, mirror=True,
            fixedrange=True
        )
        fig_my_nta.update_yaxes(range=[0, y_top], row=1, col=1)

        st.plotly_chart(fig_my_nta, use_container_width=True, config={"displayModeBar": False, "scrollZoom": False, "doubleClick": False, "showAxisDragHandles": False})

        # 생애주기 누적 총액: 20세부터 성별 기대수명까지 연령별 연간 금액을 합산
        lifetime_income_total = float(sum(household_income_curve))
        lifetime_expense_total = float(sum(household_expense_curve))
        lifetime_net_total = lifetime_income_total - lifetime_expense_total

        st.markdown("#### 생애주기 누적 총액 (20세~기대수명)")
        total_cols = st.columns(3)
        total_cols[0].metric("누적 가구소득", f"{lifetime_income_total:,.0f}만 원")
        total_cols[1].metric("누적 가구지출", f"{lifetime_expense_total:,.0f}만 원")
        total_cols[2].metric(
            "누적 소득 − 지출",
            f"{lifetime_net_total:+,.0f}만 원",
            "누적 흑자" if lifetime_net_total > 0 else ("누적 적자" if lifetime_net_total < 0 else "균형")
        )
        st.caption(
            f"20세부터 기대수명 연령({life_expectancy}세)에 도달하기 전까지의 연간 가구소득·가구지출을 합산한 모델값입니다. "
            "은퇴 후 생활비는 입력한 월 금액을 연간 금액으로 환산한 뒤 물가를 반영합니다. "
            "현재 자산·부채의 잔액이나 자산 매각·상속 등은 이 누적 현금흐름 합계에 포함하지 않습니다."
        )

#############    6.03.05.10.01 | 과거 소득·지출의 시간 기준 환산 안내
        # 2024년 MDIS 기준곡선을 공식 임금·물가지수로 과거 연도와 비교한다.
        if cur_age > 20 and self_base is not None:
            historical_compare_age = max(20, cur_age - 13)
            years_back = cur_age - historical_compare_age
            historical_year = date.today().year - years_back
            macro_index_stats = pd.DataFrame()
            try:
                macro_path = Path(__file__).resolve().parent / "data" / "기준데이터" / "국가데이터처_소비자물가지수_및_고용노동부_임금지수_1965-2025.csv"
                macro_index_stats = pd.read_csv(macro_path)
            except Exception as e:
                st.warning(f"시간축 보정 지수표를 불러오지 못했습니다. ({e})")

            def get_macro_value(year, column):
                if macro_index_stats.empty:
                    return None
                matched = macro_index_stats[macro_index_stats["year"] == year]
                if matched.empty or pd.isna(matched.iloc[0][column]):
                    return None
                return float(matched.iloc[0][column])

            wage_base_index = get_macro_value(2025, "moel_wage_index_2024_100")
            historical_wage_index = get_macro_value(historical_year, "moel_wage_index_2024_100")
            cpi_base_index = get_macro_value(2024, "cpi_index_2020_100")
            historical_cpi_index = get_macro_value(historical_year, "cpi_index_2020_100")

            historical_current_value_monthly = (
                extended_base_income(historical_compare_age, self_base) * self_scale
            )

            if (
                wage_base_index is not None
                and historical_wage_index is not None
                and historical_wage_index > 0
            ):
                historical_wage_factor = wage_base_index / historical_wage_index
                historical_nominal_monthly = (
                    historical_current_value_monthly / historical_wage_factor
                )
            else:
                historical_wage_factor = None
                historical_nominal_monthly = None

            # 월 기본급끼리 비교하도록 연간 상여금은 제외하고,
            # 해당 연령의 육아·경력 회복 계수만 기존 소득곡선과 동일하게 적용한다.
            historical_career_factor = 1.0
            historical_is_in_childcare = False
            historical_has_completed_childcare = False
            for c_start, c_end in childcare_windows:
                if c_start <= historical_compare_age < c_end:
                    years_in = historical_compare_age - c_start
                    historical_career_factor = 0.35 if years_in <= 1 else 0.50
                    historical_is_in_childcare = True
                    break
                elif historical_compare_age >= c_end:
                    historical_has_completed_childcare = True

            if (
                not historical_is_in_childcare
                and historical_has_completed_childcare
            ):
                historical_career_factor = 0.80

            historical_model_monthly = (
                historical_nominal_monthly * historical_career_factor
                if historical_nominal_monthly is not None else None
            )

            historical_expense_reference = lookup_household_expense(
                historical_compare_age,
                household_size_at_age(historical_compare_age)
            )
            if (
                historical_expense_reference
                and cpi_base_index is not None
                and historical_cpi_index is not None
                and historical_cpi_index > 0
            ):
                historical_cpi_factor = cpi_base_index / historical_cpi_index
                historical_expense_2024 = (
                    historical_expense_reference["monthly"] * 12.0 * expense_scale_ratio
                )
                historical_expense_nominal = historical_expense_2024 / historical_cpi_factor
            else:
                historical_cpi_factor = None
                historical_expense_2024 = None
                historical_expense_nominal = None

            st.markdown("#### 시간을 맞춰 소득과 지출 비교하기")
            st.caption(
                f"{historical_year}년 소득은 2025년 임금통계 기준으로, 지출은 2024년 MDIS 기준으로 환산합니다. "
                "소득은 임금지수, 지출은 소비자물가지수를 각각 적용합니다."
            )
            time_value_col1, time_value_col2 = st.columns(2)
            if historical_nominal_monthly is not None:
                time_value_col1.metric(
                    f"{historical_year}년 소득 추정",
                    f"{historical_nominal_monthly:,.0f}만 원/월",
                    help="2025년 임금지수 기준 소득을 실제 임금지수의 연도 간 비율로 역산한 추정치입니다."
                )
                time_value_col2.metric(
                    "2025년 임금통계 기준 소득",
                    f"{historical_current_value_monthly:,.0f}만 원/월",
                    help="가장 최근 연간 임금통계인 2025년을 기준으로 본 소득 추정치입니다."
                )
                st.caption(
                    f"임금지수 환산 배율: {historical_wage_factor:.3f}배. "
                    f"육아·경력 영향을 반영한 {historical_compare_age}세 당시의 모델 소득은 "
                    f"월 {historical_model_monthly:,.0f}만 원입니다."
                )
            else:
                st.info(
                    f"{historical_year}년 임금지수는 현재 자료표에서 확인되지 않아 "
                    "소득의 시간 환산을 생략했습니다."
                )

            if historical_expense_nominal is not None:
                st.caption(
                    f"같은 연령·가구원 수의 2024년 MDIS 지출 기준은 연 "
                    f"{historical_expense_2024:,.0f}만 원이며, "
                    f"{historical_year}년 물가로 환산한 추정치는 연 "
                    f"{historical_expense_nominal:,.0f}만 원입니다. "
                    f"물가 환산 배율은 {historical_cpi_factor:.3f}배입니다."
                )
            else:
                st.caption(
                    f"{historical_year}년 소비자물가지수 또는 해당 연령·가구원 수 지출 기준을 "
                    "확인할 수 없어 지출의 시간 환산을 생략했습니다."
                )
            st.caption(
                "주의: 2024년 MDIS 연령별 지출 가중중위값은 횡단면 통계이며, 과거 지출값은 실제 관측치가 아닌 "
                "2024년 기준곡선에 물가지수를 적용한 비교용 추정치입니다. "
                "임금 통계는 2011년 이전과 시계열이 단절되어 있습니다."
            )

#############    6.03.05.10.02 | [개발 메모] 시간축 보정 원칙 — 과거와 미래
        # >>> 개발 중 계속 눈에 띄게 확인할 것: 돈의 액수만 비교하지 말고, 시간의 기준을 맞춘다. <<<
        #
        # [과거의 시간] 과거 소득을 현재 소득과 비교할 때는 당시 명목금액만 나란히 놓지 않는다.
        # 임금상승률을 적용해 현재 가치로 환산한 값도 함께 살펴본다.
        # 예: 2013년 추정 소득은 2011~2025년 고용노동부 임금총액 지수로 2025년 기준 환산한다.
        # 같은 시점의 지출은 2024년 MDIS 기준곡선에 소비자물가지수를 별도로 적용한다.
        # 과거 지출·소득 환산값은 해당 개인·가구의 실제 과거 관측치가 아니라 비교용 추정치다.
        #
        # [현재의 시간] 현재 입력소득과 통계 기준소득을 비교할 때도 기준 시점을 분명히 한다.
        # 경력단절·육아 등에 따른 실제 소득 감소와, 시간 경과에 따른 임금수준 변화는 섞지 않는다.
        #
        # [미래의 시간] 시간축 보정은 과거 비교만으로 완성되지 않는다. 이것은 절반이다.
        # 앞으로 받을 연금과 은퇴 후 생활비도 수령·지출 시점의 가치로 함께 바라봐야 한다.
        # 미래 연금의 증가·물가 반영, 은퇴 후 생활비의 구매력 변화는 별도의 시간축 문제로 이어서 검토한다.
        #
        # 임금상승률과 물가상승률은 장기적으로 비슷하게 움직일 수 있어도 같은 지표로 취급하지 않는다.
        # 이 메모는 일반 사용자 화면에 노출하기 위한 설명문이 아니라, 개발·검토 과정에서
        # 이 시간의 문제를 잊지 않도록 코드 안에 붙여 두는 작업 메모다.
        
        if current_expense_reference:
            st.caption(
                f"기준: 2024년 현재 {cur_age}세·{current_household_size}인 가구의 월 가중중위값 "
                f"{current_expense_reference['monthly']:,.1f}만 원을 연간 지출 곡선에 적용했습니다. "
                f"개인 지출 보정률: {expense_scale_ratio:.1%}."
            )
        else:
            st.caption("MDIS 지출 통계표를 읽지 못해 현재 입력한 연간 지출을 기준으로 표시하고 있습니다.")
        st.caption("표본 수 30 미만인 구간(특히 일부 3·4인 가구)은 변동 가능성이 커 참고값으로 해석해 주세요.")
        st.markdown(
            '[지출 통계 출처 및 산출방법](https://github.com/ufreezone-ops/nachimpan/blob/dev/data/기준데이터/국가데이터처_2024_가계동향조사_가구주연령대별가구원수별가계지출_가중중위값_README.md) · '
            '[MDIS 자료 이용 안내](https://mdis.mods.go.kr/mobile/pageLink.do?link=mdisService)',
            unsafe_allow_html=True
        )

        # 기준 지역 안내 카드
        housing_price_label = "대표사례 적용 주택가격" if is_representative_case else "아파트 중위가격"
        st.markdown(f"""
<div style="background: rgba(30, 41, 59, 0.5); border: 1px solid #0284C7; border-radius: 8px; padding: 10px 14px; margin: 6px 0 12px 0; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
    <div style="font-size: 14.5px; color: #F8FAFC;">
        🏠 <b>부동산 산정 기준 지역: <span style="color: #38BDF8; font-size: 16px;">{selected_region}</span></b>
        <span style="font-size: 13px; color: #94A3B8; margin-left: 8px;">({housing_price_label}: <b>{region_apt_price/10000:.2f}억 원</b> · 대출 LTV {selected_ltv:.0f}% 적용 자기자금: <b>{home_equity_display/10000:.2f}억 원</b>)</span>
    </div>
    <div style="font-size: 12px; color: #CBD5E1; background: rgba(15, 23, 42, 0.6); padding: 3px 8px; border-radius: 4px;">
        ※ 지역에 따라 결혼 주거지원비와 내 집 마련 규모가 크게 변동됩니다.
    </div>
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div style="background: rgba(30, 41, 59, 0.45); border: 1px solid #475569; border-radius: 8px; padding: 12px 15px; margin: 8px 0 12px 0; font-size: 13.5px; line-height: 1.7; color: #CBD5E1;">
<b style="color:#F8FAFC;">소득 기준곡선의 출처와 산정 방식</b><br>
• <b>직장인 기준곡선:</b> 국가데이터처 「2023년 국민이전계정」의 연령별 1인당 임금소득 흐름을 참고해 나침반에서 월소득 기준으로 재구성한 자체 기준곡선입니다. NTA의 1인당 금액은 해당 연령의 전체 인구를 기준으로 계산한 값이므로, 취업자 개인의 실제 평균임금과 같지 않으며 원자료 수치를 그대로 옮긴 곡선도 아닙니다.<br>
• <b>자영업자 기준곡선:</b> NTA의 자영자 노동소득은 사업소득 전체가 아니라 노동소득으로 분류된 일부이며, 전체 인구 기준 1인당 값이므로 자영업자 개인의 실제 사업소득 곡선으로 직접 사용하지 않았습니다. 대신 국가데이터처 「2024년 가계금융복지조사」(2023년 소득 자료)의 가구주 종사상지위별 통계를 참고했습니다. 자영업자 가구의 평균 가구소득은 7,769만 원, 그중 사업소득은 4,680만 원, 재산소득은 634만 원입니다. 이 수치는 가구 단위 평균이며 연령별 개인 소득곡선이 아니므로, 나침반의 자영업자 연령별 기준곡선은 이 자료를 참고하되 코로나 시기 왜곡을 정상화한다는 별도 가정을 반영해 구성한 자체 시뮬레이션입니다.<br>
• 각 기준곡선은 현재 입력한 소득을 기준으로 조정되며, 연령 사이 값은 보간합니다. 75세 이후는 추정 연장값입니다. 배우자의 미래 소득도 직업군 기준곡선을 적용한 가정이며 실제 미래 소득을 보장하거나 예측하지 않습니다.<br>
자료: <a href="https://mods.go.kr/board.es?act=view&amp;bid=11898&amp;list_no=438783&amp;mid=a10301130100" target="_blank" style="color:#38BDF8;">국가데이터처, 2023년 국민이전계정</a> · <a href="https://mods.go.kr/boardDownload.es?bid=215&amp;list_no=434107&amp;seq=4" target="_blank" style="color:#38BDF8;">국가데이터처·한국은행·금융감독원, 2024년 가계금융복지조사</a>
</div>
""", unsafe_allow_html=True)


        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

#--------------------------------------------------------
# 6.03.06 | 고급 모드 — 3. 세대 계승 생애주기 재정곡선
#--------------------------------------------------------
        st.markdown("### 3. 세대 계승 생애주기 재정곡선")

        # [출처 ID 재사용: 6030200-01]
        st.markdown(
            '<div id="source-anchor-nta-generational"></div>',
            unsafe_allow_html=True
        )

        with st.container(horizontal=True, vertical_alignment="center", gap=None):
            st.caption(
                "※ 국가데이터처 「2024년 국민이전계정」"
                "(2026. 9. 17. 발표) 기준 · 전 국민 1인당 평균 지표"
            )
            if st.button(
                "☞",
                key="source_nta_generational",
                help="국가데이터처 2024년 국민이전계정 출처 보기",
                type="tertiary",
            ):
                _open_source_reference(
                    "6030200-01",
                    "인생의 사계절",
                    "source-anchor-nta-generational",
                )
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("한국인 평균 흑자 진입", "28세", help="노동소득이 소비를 추월하는 연령")
        col_m2.metric("최대 흑자 정점", "45세", "연 1,932만 원")
        col_m3.metric("평균 적자 재전환", "61세", help="은퇴 후 소비가 노동소득을 다시 초과")

        st.markdown("""
<div style="background: rgba(30, 41, 59, 0.55); border-left: 4px solid #F59E0B; border-radius: 6px; padding: 12px 18px; margin: 12px 0 16px 0;">
<div style="font-size: 15px; font-weight: 800; color: #FDE68A; margin-bottom: 6px;">👩‍👧 여성 출산·육아 경력단절의 현실(여성가족부·국가데이터처)</div>
<div style="font-size: 13.5px; color: #CBD5E1; line-height: 1.6;">
• <b>재취업까지 소요 기간</b>: 평균 <b>7.5년</b> (단기 공백이 아닌 장기화)<br>
• <b>복귀 후 실질 임금</b>: 단절 이전의 약 <b>80% 수준</b>으로 하락
</div></div>
""", unsafe_allow_html=True)

        fig_official_nta = build_official_nta_chart()
        st.plotly_chart(fig_official_nta, use_container_width=True, config={"displayModeBar": False, "scrollZoom": False, "doubleClick": False, "showAxisDragHandles": False})
        
        st.markdown(f"""
<div style="display: flex; justify-content: center; margin-top: 14px;">
  <a href="{OFFICIAL_PDF_URL}" target="_blank" style="background:#1E293B; border:1px solid #475569; border-radius:8px; padding:12px 20px; text-decoration:none; color:#38BDF8 !important; font-size:15px; font-weight:700; display:inline-flex; align-items:center; justify-content:center; gap:8px; white-space: nowrap;">
    <span style="font-size:18px;">📄</span>
    <span style="color:#38BDF8 !important; white-space: nowrap;">2024년 국민이전계정 보도자료</span>
  </a>
</div>
""", unsafe_allow_html=True)
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

#--------------------------------------------------------
# 6.03.07 | 고급 모드 — 4. 인생의 사계절 카드
#--------------------------------------------------------
        st.markdown("### 4. 인생의 사계절")
        if cur_age <= 27: cur_season = "spring"
        elif 28 <= cur_age <= 45: cur_season = "summer"
        elif 46 <= cur_age < retire_age: cur_season = "autumn"
        else: cur_season = "winter"

        def get_season_card_ui(season_key, icon, title, age_range, desc):
            is_current = (cur_season == season_key)
            card_border = "border: 2px solid #EA580C; background: rgba(234, 88, 12, 0.14);" if is_current else "border: 1px solid #334155; background: rgba(21, 30, 47, 0.7);"
            badge_html = "<div style='min-height:22px; margin-bottom:4px;'><span style='background:#EA580C; color:#FFFFFF; font-size:11.5px; font-weight:800; padding:2px 7px; border-radius:4px;'>지금 나의 계절</span></div>" if is_current else "<div style='min-height:22px; margin-bottom:4px;'></div>"
            return f'<div class="soft-card" style="text-align:center; min-height:205px; {card_border} padding:14px 10px; margin:0;">{badge_html}<div style="font-size:28px;">{icon}</div><div style="font-size:16.5px; font-weight:800; color:#F8FAFC; margin:4px 0;">{title}</div><div style="font-size:13px; color:#94A3B8;">{age_range}</div><div style="font-size:13px; color:#CBD5E1; margin-top:8px; line-height:1.4;">{desc}</div></div>'

        card_spring = get_season_card_ui("spring", "🌱", "봄 (준비기)", "0세 ~ 27세", "부모님의 부양으로 배우고 성장하는 계절")
        card_summer = get_season_card_ui("summer", "☀️", "여름 (성장기)", "28세 ~ 45세", "성실하게 일하여 가정을 일구고 최대 흑자를 만드는 계절")
        card_autumn = get_season_card_ui("autumn", "🍂", "가을 (결실기)", f"46세 ~ {retire_age}세", "자녀 독립과 함께 다가올 겨울을 준비할 골든타임")
        card_winter = get_season_card_ui("winter", "❄️", "겨울 (음미기)", f"{retire_age}세 ~ {life_expectancy}세", f"근로소득이 멈추고 삶의 열매를 누리는 계절")

        s_col1, s_col2, s_col3, s_col4 = st.columns(4)
        with s_col1: st.markdown(card_spring, unsafe_allow_html=True)
        with s_col2: st.markdown(card_summer, unsafe_allow_html=True)
        with s_col3: st.markdown(card_autumn, unsafe_allow_html=True)
        with s_col4: st.markdown(card_winter, unsafe_allow_html=True)

        st.markdown(f"""
<div style="background: rgba(30, 41, 59, 0.6); border: 1px solid #334155; border-radius: 12px; padding: 18px 20px; margin: 16px 0 24px 0;">
<div style="font-size: 15px; color: #F8FAFC; line-height: 1.6; word-break: keep-all;">
💡 <b>산책로의 질문</b><br>은퇴 후 내가 맞이할 겨울은 <b>약 {winter_years}년 </b>입니다. (국가데이터처 {user_gender.split()[1]} 기대수명 {life_expectancy}세 기준)<br>
<span style="color: #94A3B8;">이 긴 겨울 동안 매달 무거운 물통을 지고 눈길을 걸을 것인가, 방 안에서 따뜻하게 흘러나오는 파이프라인을 맞이할 것인가는 <b>운명이 아니라 선택입니다.</span>
</div></div>
""", unsafe_allow_html=True)

        _, next_col = st.columns([5, 1])
        with next_col:
            if st.button("다음 →", key="seasons_next", use_container_width=True, type="primary"):
                st.session_state["_pending_nav"] = "AI 시선"
                st.rerun()


#########################################################
# 6.04 | Tab 4 — AI 시선
#########################################################
elif selected_page == "AI 시선":
    is_adv = st.session_state.get("advanced_mode", False)
    summary = current_financial_summary()
    person_name = st.session_state.get("person_name", "나")
    person_age = st.session_state.get("person_age", 35)

#--------------------------------------------------------
# 6.04.01 | 기본 모드 — AI 자동 성찰문 생성 및 표시
#--------------------------------------------------------
    if not is_adv:
    
        st.caption("AI는 평가자가 아닌, 내가 작성한 삶의 숫자를 객관적인 거울처럼 비춰주는 성찰 파트너입니다.")
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

#--------------------------------------------------------
# 6.04.02 | 기본 모드 — 고급 모드 초대장 카드
#--------------------------------------------------------
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
        st.caption("AI는 평가자가 아닌, 내가 작성한 삶의 숫자를 객관적인 거울처럼 비춰주는 성찰 파트너입니다.")

#--------------------------------------------------------
# 6.04.03 | 고급 모드 — 재무 및 가족 생애 데이터 프롬프트 구성
#--------------------------------------------------------
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
            "연간 잉여자금": f"{summary['annual_net_surplus']:,.0f}만 원 (월환산 {summary['monthly_effective_surplus']:,.0f}만 원)",
            "현재 파악된 금융자산": f"{summary['net_worth']/10000:,.2f}억 원 (자산 {summary['assets']:,.0f}만 원 - 부채 {summary['debts']:,.0f}만 원)",
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

#--------------------------------------------------------
# 6.04.04 | 고급 모드 — AI 분석 원칙·톤(맛) 설정 패널
#--------------------------------------------------------
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
은퇴 후 약 {winter_years}년은 국가데이터처 {user_gender.split()[1]} 기대수명({life_expectancy}세)에 기초한 계산상 가정으로 취급하세요. 현재 경력 단계와 순자산을 연결해 설명하되, 실제 현금 보유액이나 유동성 자료가 없다면 유동성 준비 상태를 평가하지 마세요. 결혼, 자녀, 주거 계획 등 확인되지 않은 미래 사건을 전제로 삼지 말고, 정중하고 담백하게 서술하세요."""

#--------------------------------------------------------
# 6.04.05 | 고급 모드 — Gemini AI 리포트 생성 버튼
#--------------------------------------------------------
        if st.button("⚡ AI 리포트 생성", type="primary", use_container_width=True):
            st.session_state.ai_summary = summary
            st.session_state.ai_comment = None
            with st.spinner(f"AI가 {taste_mode.split()[0]} 모드로 지표를 분석 중입니다 (약 15~20초 소요)..."):
                comment, error = call_gemini_text(full_prompt_text)
                st.session_state.ai_comment = comment if comment else error
            st.rerun()

#--------------------------------------------------------
# 6.04.06 | 고급 모드 — AI 리포트 표시 및 카카오톡 전송용 리포트
#--------------------------------------------------------
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

        else:
            st.info("‘AI 리포트 생성’ 버튼을 누르면 Gemini 초고속 엔진이 삶과 재무의 성찰 리포트를 생성합니다.")

        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

#--------------------------------------------------------
# 6.04.07 | 고급 모드 — 📋 AI 질의용 재무제표 expander
#--------------------------------------------------------
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




#########################################################
# 6.05 | Tab 5 — 통계 자료실
#########################################################
elif selected_page == "통계":
    #--------------------------------------------------------
    # 6.05.01.00 | 출처 자료 표시 및 원위치 복귀
    #--------------------------------------------------------
    st.markdown("""
    <style>
    div.st-key-source-return-bar {
        position: fixed !important;
        top: 7rem !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: max-content !important;
        max-width: calc(100vw - 1.5rem) !important;
        box-sizing: border-box !important;
        z-index: 9999 !important;
        background: transparent !important;
        padding: 0 !important;
        border: 0 !important;
        box-shadow: none !important;
    }
    div.st-key-source-return-bar [data-testid="stButton"] button {
        width: auto !important;
        min-width: max-content !important;
        padding: 0.42rem 0.85rem !important;
        border-radius: 999px !important;
        border: 1px solid #38BDF8 !important;
        background: #0284C7 !important;
        background-color: #0284C7 !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-weight: 700 !important;
        box-shadow: 0 2px 8px rgba(2, 132, 199, 0.25) !important;
        white-space: nowrap !important;
        flex: 0 0 auto !important;
    }
    div.st-key-source-return-bar [data-testid="stButton"] button:hover {
        background: #0369A1 !important;
        background-color: #0369A1 !important;
        border-color: #7DD3FC !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }
    </style>
    """, unsafe_allow_html=True)

    _active_source_id = st.session_state.get("_active_source_id")

    _source_labels = {
        "6030200-01": "국가데이터처 「2024년 국민이전계정」",
        "6050600-01": "국가데이터처 「2024년 가계동향조사」 은퇴 후 연령대별 가계지출",
        "6050700-01": "국토교통부 「2024년도 주거실태조사 결과」 및 나침반의 표준 대출 상환 가정",
    }
    if _active_source_id in _source_labels:
        with st.container(key="source-return-bar"):
            if st.button(
                "← 이전 위치로 돌아가기",
                key="source_return_button",
                use_container_width=False,
            ):
                _return_context = st.session_state.get(
                    "_source_return_context"
                )
                if _return_context:
                    st.session_state["_source_restore_anchor"] = (
                        _return_context["anchor"]
                    )
                    st.session_state["_pending_nav"] = (
                        _return_context["page"]
                    )
                    st.rerun()

        st.markdown("<div style='height: 42px;'></div>", unsafe_allow_html=True)
        st.caption(f"선택한 출처: {_source_labels[_active_source_id]}")

    st.markdown("## 통계로 읽는 인생")
    st.caption("내 삶의 숫자를 사회 전체의 흐름과 나란히 놓고 살펴보는 자료실입니다. 통계는 정답이 아니라, 내 생각의 경계를 넓히는 참고선입니다.")

    #--------------------------------------------------------
    # 6.05.02.00 | 1. 소득과 소비의 생애주기
    #--------------------------------------------------------
    with st.expander("1. 소득과 소비의 생애주기", expanded=True):
        st.markdown("""
**국민이전계정(NTA)이 보여주는 생애주기**

- 평균적으로 노동소득이 소비를 넘어서는 흑자 진입 연령: **28세**
- 평균 흑자 정점: **45세** (연간 1,932만 원)
- 노동소득보다 소비가 다시 커지는 적자 재전환 연령: **61세**

이 지표는 대한민국 전체 인구의 1인당 평균 흐름입니다. 개인이나 특정 가구의 실제 소득·지출과 같다는 뜻은 아닙니다. 내 가구의 생애주기 곡선과 사회 전체의 평균 곡선을 비교해 보는 기준선으로 활용합니다.

자료: [국가데이터처 「2024년 국민이전계정」 보도자료](https://mods.go.kr/board.es?act=view&bid=11898&list_no=447028&mid=a10301130100)
""")
        st.markdown("""
**생애주기 흑자·적자를 누적해서 보면**

연령별 노동소득에서 소비를 뺀 금액을 매년 더하면, 한 해의 흑자·적자와는 다른 흐름이 보입니다. 아래 그래프는 같은 2024년 1인당 자료를 사용해, 20세부터 누적한 값은 실선으로, 출생부터 누적한 값은 점선으로 함께 보여줍니다.
""")

        nta_cumulative_path = os.path.join(
            "data", "기준데이터",
            "국가데이터처_2024_국민이전계정_연령별_누적노동잉여.csv"
        )
        if os.path.exists(nta_cumulative_path):
            nta_cumulative_df = pd.read_csv(nta_cumulative_path)
            nta_cumulative_df["age"] = pd.to_numeric(
                nta_cumulative_df["age"], errors="coerce"
            )
            nta_cumulative_df["cumulative_from_0_eok"] = (
                nta_cumulative_df["cumulative_from_0_thousand_won"] / 100000
            )
            nta_cumulative_df["cumulative_from_20_eok"] = (
                nta_cumulative_df["cumulative_from_20_thousand_won"] / 100000
            )

            fig_nta_cumulative = go.Figure()

            # 20세부터 누적한 값: 실선
            nta_adult_df = nta_cumulative_df[
                nta_cumulative_df["age"] >= 20
            ].copy()
            fig_nta_cumulative.add_trace(go.Scatter(
                x=nta_adult_df["age"],
                y=nta_adult_df["cumulative_from_20_eok"],
                customdata=nta_adult_df["age_label"],
                mode="lines",
                name="20세부터 누적",
                line=dict(color="#F59E0B", width=3, dash="solid"),
                hovertemplate=(
                    "연령: %{customdata}<br>"
                    "20세부터 누적: <b>%{y:,.2f}억 원</b>"
                    "<extra></extra>"
                ),
            ))

            # 0세부터 누적한 값: 점선
            fig_nta_cumulative.add_trace(go.Scatter(
                x=nta_cumulative_df["age"],
                y=nta_cumulative_df["cumulative_from_0_eok"],
                customdata=nta_cumulative_df["age_label"],
                mode="lines",
                name="0세부터 누적",
                line=dict(color="#38BDF8", width=3, dash="dot"),
                hovertemplate=(
                    "연령: %{customdata}<br>"
                    "0세부터 누적: <b>%{y:,.2f}억 원</b>"
                    "<extra></extra>"
                ),
            ))

            fig_nta_cumulative.add_hline(
                y=0, line_color="#CBD5E1", line_width=1.4,
                line_dash="solid"
            )
            fig_nta_cumulative.update_layout(
                height=390,
                margin=dict(l=12, r=12, t=28, b=48),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#E2E8F0", size=12),
                xaxis=dict(
                    title="연령",
                    range=[0, 85],
                    tickmode="linear",
                    tick0=0,
                    dtick=10,
                    gridcolor="rgba(100, 116, 139, 0.18)",
                    fixedrange=True,
                ),
                yaxis=dict(
                    title="누적액 (억 원)",
                    range=[-9, 4],
                    dtick=2,
                    gridcolor="rgba(100, 116, 139, 0.18)",
                    zeroline=False,
                    fixedrange=True,
                ),
                hovermode="x",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="left",
                    x=0,
                ),
            )
            st.plotly_chart(
                fig_nta_cumulative,
                use_container_width=True,
                config={"displayModeBar": False, "scrollZoom": False},
            )

            st.markdown("""
- **0세 기준:** 출생부터 85세 이상까지 누적 노동잉여는 계속 마이너스이며, 마지막 85세 이상 구간에서는 약 **-8억 588만 원**입니다. 노동소득이 없는 유년기의 소비가 생애 초기에 큰 누적 적자로 쌓이기 때문입니다.
- **20세 기준:** 20세부터 누적하면 39세까지는 마이너스지만 **40세에 처음 플러스로 전환**합니다. 60세에 약 **2억 9,695만 원**으로 가장 높아집니다.
- **연간 수지와 누적 수지는 다릅니다.** 연간 노동소득이 소비보다 작아지는 시점은 61세입니다. 그러나 20세부터 쌓인 누적 노동잉여는 79세에도 약 **934만 원** 남아 있고, 80세에 약 **-1,504만 원**으로 다시 마이너스가 됩니다.
- 85세 이상 구간의 20세 기준 누적값은 약 **-1억 4,533만 원**입니다.

**이 그래프가 말해주는 것**

한 해의 소득이 줄어드는 것과 곧바로 생계가 어려워지는 것은 같은 일이 아닙니다. 일하는 시기에 소비보다 더 많이 벌어 쌓은 잉여가 이후의 연간 적자를 일정 기간 메워줄 수 있기 때문입니다. 그래서 연간 수지뿐 아니라 생애 전체의 누적 흐름도 함께 볼 필요가 있습니다.

> **해석할 때 주의할 점:** 이 누적 노동잉여는 실제 개인의 예금·투자자산 잔액이나 순자산이 아닙니다. 연령별 1인당 평균 노동소득과 소비의 차이를 가상의 생애 경로로 합산한 값입니다. 공적·사적 이전, 자산소득, 투자수익, 주택 등 자산의 취득·처분은 포함하지 않습니다. 따라서 플러스 금액을 실제 보유자산으로 해석해서는 안 됩니다.

자료: 국가데이터처 「2024년 국민이전계정」 연령별 1인 규모 원자료. 단위는 1인당 연간 천 원이며, 85세 이상은 집단 구간입니다. [원자료 CSV](https://github.com/ufreezone-ops/nachimpan/blob/dev/data/원자료/생애주기적자계정_1인규모__20261110084848.csv) · [가공 데이터 및 산출방법](https://github.com/ufreezone-ops/nachimpan/blob/dev/data/기준데이터/국가데이터처_2024_국민이전계정_연령별_누적노동잉여_README.md)
""")
        else:
            st.info("국민이전계정 누적 노동잉여 기준데이터 파일을 찾지 못했습니다. data/기준데이터 파일을 확인해 주세요.")

    #--------------------------------------------------------
    # 6.05.03.00 | 2. 취업과 소득의 변화
    #--------------------------------------------------------
    with st.expander("2. 취업과 소득의 변화"):
        st.markdown("""
연령에 따라 임금소득과 노동소득이 어떻게 달라지는지 살펴보는 영역입니다.

- 연령대별 임금·노동소득의 흐름
- 직장인과 자영업자의 소득 구조 차이
- 경력의 축적, 소득 정점, 노동시간과 소득의 관계

평균값은 개인의 실제 경력이나 소득을 그대로 설명하지 않으므로, 자료의 조사 대상과 단위를 함께 확인합니다.
""")
    #--------------------------------------------------------
    # 6.05.04.00 | 3. 결혼과 주거
    #--------------------------------------------------------
    with st.expander("3. 결혼과 주거"):
        st.markdown("""
삶의 큰 전환기에 필요한 주거비와 자금 흐름을 살펴보는 영역입니다.

- 결혼과 독립에 필요한 초기 자금
- 전세·월세·주택 구입 비용과 가계 부담
- 지역별 주택가격 차이와 내 집 마련 기간

지역, 가구 형태, 대출 조건에 따라 결과가 달라지므로 전국 평균과 내가 선택한 지역의 수치를 구분해 읽습니다.

---

**청년의 주거 형태: 부모 동거와 독립생활**

2024년 청년의 삶 실태조사에서 만 19~34세 청년의 주거 형태는 다음과 같이 나타났습니다.

| 구분 | 비율 |
|---|---:|
| 부모와 동거하는 청년 | **54.4%** |
| 부모와 따로 살며 독립생활하는 청년 | **45.6%** |

청년 10명 중 약 5.4명은 부모와 함께 살고, 약 4.6명은 독립생활을 하고 있습니다. 청년의 생활비와 자립 과정을 살펴볼 때, 모든 청년이 동일한 주거비를 부담한다고 가정해서는 안 된다는 점을 보여주는 자료입니다.

참고로 부모와 동거하는 청년 가운데 **38.0%는 구체적인 독립계획이 있다**고 응답했습니다.

- 조사 대상: 전국 만 19~34세 청년
- 조사명: 국무조정실 「2024년 청년의 삶 실태조사」
- 발표일: 2025년 3월 11일
- 통계 성격: 청년 개인의 주거 형태 비율
- 해석 시 유의: 부모 동거 여부는 주거 형태를 나타내는 지표이며, 부모 동거 청년의 개인 생활비나 부모의 실제 비용 부담액을 직접 보여주는 통계는 아닙니다.

자료: [국무조정실 「2024년 청년의 삶 실태조사 결과 발표」](https://www.opm.go.kr/opm/news/press-release.do?articleNo=158583&mode=view)
""")
    #--------------------------------------------------------
    # 6.05.05.00 | 4. 출산과 양육
    #--------------------------------------------------------
    with st.expander("4. 출산과 양육"):
        st.markdown("""
자녀의 성장 단계에 따라 달라지는 가계 지출과 부모의 경제활동을 살펴보는 영역입니다.

- 출산·양육 과정의 지출 변화
- 자녀 교육비와 대학 진학 시기의 비용
- 출산·육아에 따른 경력 공백과 재취업

통계의 평균 비용이 모든 가정의 지출 기준은 아닙니다. 우리 집의 가족 계획과 실제 지출을 비교하는 참고자료로 봅니다.
""")
    #--------------------------------------------------------
    # 6.05.06.00 | 5. 노후와 은퇴
    #--------------------------------------------------------
    st.markdown(
        '<div id="stats-anchor-retirement-expense" style="scroll-margin-top: 150px;"></div>',
        unsafe_allow_html=True,
    )
    with st.expander(
        "5. 노후와 은퇴",
        expanded=_active_source_id == "6050600-01",
    ):
        st.markdown("""
**은퇴 후 생활비는 한 가지 금액으로 고정되지 않습니다.**

나침반은 은퇴 후 자녀가 독립한 가구를 가정하고, 가구주 연령대와 가구원 수에 해당하는 2024년 가계동향조사의 월 가계지출 가중중위값을 기준으로 사용합니다. 부부 가구는 2인, 1인 가구는 1인 기준을 적용하며, 이후 연도의 금액은 소비자물가지수로 환산합니다.

**2024년 연령대별 월 가계지출 가중중위값**

| 가구주 연령 | 1인 가구 | 2인 가구 |
|---|---:|---:|
| 60~64세 | 161.83만 원 | 324.27만 원 |
| 65~69세 | 159.16만 원 | 262.55만 원 |
| 70~74세 | 124.42만 원 | 221.71만 원 |
| 75~79세 | 112.79만 원 | 195.72만 원 |
| 80세 이상 | 101.82만 원 | 161.91만 원 |

**화면의 ‘은퇴 후 월 생활비’ 입력값은 어떻게 쓰이나요?**

화면에 기본 표시되는 270만 원은 은퇴 후 생활비를 생각해 보기 위한 참고 입력값입니다. 실제 생애주기 재정곡선에서는 이 금액을 모든 은퇴 연령에 일괄 적용하지 않습니다. 위 표처럼 해당 연령대와 가구원 수에 맞는 통계값을 연령별로 적용합니다. 통계 파일을 읽지 못하는 경우에만 입력값을 대체 기준으로 사용합니다.

이 값은 특정 개인의 미래 지출 예측이 아닙니다. 2024년 가구 표본의 가중중위값이며, 개인의 주거 형태·건강·돌봄·지역·생활 방식에 따라 실제 지출은 달라질 수 있습니다.

자료: 국가데이터처 「가계동향조사(2019~2024년 구분류)」 2024년 연간자료, MDIS 제공 공공용 마이크로데이터.
""")
        with st.container(key="retirement-source-details"):
            with st.popover("산출 방법과 원자료 변수 보기", type="primary"):
                _retirement_readme_path = (
                    Path(__file__).resolve().parent
                    / "data"
                    / "기준데이터"
                    / "국가데이터처_2024_가계동향조사_가구주연령대별가구원수별가계지출_가중중위값_README.md"
                )
                if _retirement_readme_path.exists():
                    st.markdown(
                        _retirement_readme_path.read_text(encoding="utf-8")
                    )
                else:
                    st.info("산출 방법 파일을 현재 앱에서 찾을 수 없습니다.")

    #--------------------------------------------------------
    # 6.05.07.00 | 6. 주택대출과 원리금 분리
    #--------------------------------------------------------
    st.markdown(
        '<div id="stats-anchor-loan-payment" style="scroll-margin-top: 150px;"></div>',
        unsafe_allow_html=True,
    )
    with st.expander(
        "6. 주택대출과 원리금 분리",
        expanded=_active_source_id == "6050700-01",
    ):
        st.markdown("""
**주택 구입자금과 대출 상환의 기준**

- **LTV1:** 금융기관 대출액 ÷ 주택 구입가격. 2024년 주거실태조사에서 대출 이용 가구 기준 전국 37.2%, 수도권 34.3%, 광역시 등 34.3%, 도지역 41.8%입니다.
- 부산은 '광역시 등'에 해당하므로 대표사례의 기본 LTV1은 34.3%입니다. 4억 원 주택이면 약 1억 3,720만 원이며, 대표사례에서는 천만 원 단위로 반올림해 1억 4천만 원(적용 LTV 약 35%)으로 단순화합니다.
- 이 비율은 대출 이용 가구의 조사상 평균이며, 특정 연도 신규 구입자의 대출 실행비율이나 모든 가구의 평균과는 다릅니다.

**나침반의 표준 상환 가정**

- 상환 방식: 원리금 균등상환
- 대출 기간: 30년
- 연 이자율: 4% (대표 시뮬레이션 가정)
- 1억 4천만 원 대출의 월 상환액: 약 66.8만 원(화면 표시는 약 67만 원)

**원리금은 서로 다른 흐름으로 처리합니다.**

- 이자: 가계지출에 포함되는 비용. MDIS 가계지출 기준에도 이자 등 비소비지출이 포함되므로 통계 기준곡선에 별도로 더하지 않습니다.
- 원금: 소비지출이 아니라 부채 감소입니다. 가계지출 곡선에서는 제외하되, 실제 현금 유출이므로 가구 순현금흐름 계산에서 별도로 차감합니다.
- 대표사례의 45세 여성은 39세에 대출을 시작해 6년간 상환한 것으로 가정합니다. 현재 추정 잔액은 약 1억 2,362만 원이며, 다음 회차 기준 월 이자는 약 41.2만 원, 원금은 약 25.6만 원입니다.
- 32세 여성은 현재 주택·대출이 없는 상태로 두고, 39세 주택 구입 시점부터 같은 대출모형을 적용합니다.

주의: 실제 대출계약의 금리·만기·상환방식과 다를 수 있는 교육용 표준 가정입니다. LTV1 또한 조사 평균이므로 개별 가구의 실제 대출을 뜻하지 않습니다.

자료: [국토교통부 「2024년도 주거실태조사 결과」(2025.11.17.)](https://www.molit.go.kr/USR/NEWS/dtl.jsp?id=95091415&lcmspage=2)
""")
    #--------------------------------------------------------
    # 6.05.08.00 | 7. 동시성과 통시성
    #--------------------------------------------------------
    with st.expander("7. 동시성과 통시성", expanded=True):
        st.markdown("""
**왜 시간의 기준을 맞춰야 하는가**

2024년 MDIS 가계동향조사처럼 한 해에 서로 다른 연령대와 가구를 관찰한 자료는 **동시성(共時性) 자료**입니다. 반면 한 사람의 과거·현재·미래를 시간의 흐름에 따라 비교하거나, 서로 다른 출생세대의 같은 나이를 비교하려면 **통시성(通時性) 보정**이 필요합니다.

나침반은 관측된 연령별 통계의 모양과 시간에 따른 금액 변화를 구분합니다. 연령에 따른 차이는 연령별 기준곡선으로, 연도에 따른 명목금액 변화는 임금·물가 지수로 각각 다룹니다.

**소득과 지출은 서로 다른 지수로 보정합니다**

- **근로소득:** 고용노동부 사업체노동력조사의 전체근로자 월평균 임금총액으로 만든 연도별 임금지수를 사용합니다.
- **가계지출:** 국가데이터처 소비자물가지수(CPI)를 사용합니다.
- **주택가격:** 일반 소비자물가와 별개로 한국부동산원의 주택매매가격지수를 참고합니다. 주택가격은 지역·주택유형에 따라 차이가 커서 CPI로 대체하지 않습니다.

**실제 관측자료의 기준**

현재 기준데이터 파일에는 CPI가 1965~2025년, 임금지수가 2011~2025년까지 들어 있습니다. 임금지수는 2024년을 100으로 재기준화한 값이며, 임금 자료가 없는 1965~2010년은 빈칸으로 보존합니다. 임금 통계는 2011년 조사통합·추정법 변경으로 이전 자료와 시계열 단절이 있다는 공식 주석이 있어, 그 이전을 임의로 이어 붙이지 않습니다.

2024년 MDIS 지출 기준값을 다른 연도의 명목가치로 옮길 때는 해당 연도의 CPI를 적용합니다. 임금 기준값은 연도별 임금지수로 환산합니다. 기준연도가 다르므로 화면과 보고서에서 각각의 기준연도를 구분합니다.

| 항목 | 기준연도 | 실제 자료 범위 |
|---|---:|---:|
| MDIS 가계지출 기준곡선 | 2024년 | 2024년 조사자료 |
| 소비자물가지수 | 2020=100 | 1965~2025년 |
| 임금지수 | 2024=100 | 2011~2025년 |

**미래 연도는 실제 통계가 아니라 평균상승률을 이용한 추정입니다**

2025년까지는 실제 관측 지수를 사용하고, 그 이후에는 2011~2025년의 연평균 복합상승률(CAGR)을 미래 가정으로 사용합니다. 현재 모델의 달력연도 2026년은 최신 실적연도인 2025년 지수 수준을 기준점으로 두며, 2027년부터 미래 상승률을 한 해씩 누적합니다.

| 미래 보정 가정 | 실제 관측기간 | 연평균 복합상승률 |
|---|---:|---:|
| 명목 임금 | 2011~2025년 | 약 3.47% |
| 소비자물가 | 2011~2025년 | 약 1.87% |
| 전국 주택매매가격 | 2012~2025년 | 약 1.22% |

임금과 물가의 평균상승률은 각각의 지수 시작값과 끝값으로 계산한 연평균 복합상승률입니다. 해마다 실제 상승률이 일정했다는 뜻은 아닙니다. 미래에는 이 평균값을 적용하되, 실제 관측치가 갱신되면 기준자료와 평균값을 다시 계산해야 합니다.

**미래 보정식**

- 미래 임금지수 = 2025년 임금지수 × (1 + 3.47%)을 미래 경과연수만큼 거듭제곱
- 미래 소비자물가지수 = 2025년 CPI × (1 + 1.87%)을 미래 경과연수만큼 거듭제곱
- 미래 주택가격은 CPI와 분리해 주택매매가격지수를 사용하며, 실제 적용 시에는 지역·주택유형을 맞춘 지수를 우선합니다.

**주택가격지수는 별도 관리합니다**

한국부동산원의 전국주택가격동향조사는 주택 매매·전세·월세 가격의 변화를 지수로 측정합니다. 2012~2025년 전국 연말 지수의 연평균 복합상승률은 약 1.22%지만, 이는 전국 단일 참고값입니다. 부산 등 특정 지역의 주택구입 비용이나 미래 주택가치를 보정할 때 전국 평균을 그대로 적용하지 않고, 해당 지역과 주택유형에 맞는 시계열을 확인해야 합니다. 주택가격지수는 우선 통계자료실의 별도 참고지표로 관리하며, 적용 범위가 정해진 뒤 주택구입 이벤트와 자산가치 계산에 연결합니다.

**나침반 적용 원칙**

1. 국가데이터처의 세대계승 재정곡선은 공식 통계 기준을 그대로 유지합니다.
2. 우리 가정 생애주기 재정곡선은 실제 관측기간에는 실제 임금·물가 지수를 적용하고, 미래기간에는 위 평균상승률을 적용합니다.
3. 임금지수는 연령별 임금곡선 자체를 만드는 자료가 아니라, 연도별 명목 임금수준을 맞추는 거시 보정지수입니다.
4. 미래 보정값은 예측 결과가 아니라 평균상승률을 전제로 한 시뮬레이션 가정입니다. 실제 미래 임금·물가·주택가격을 보장하지 않습니다.

**해석상의 한계**

2024년 연령별 지출자료에 CPI를 적용한 값은 과거·미래 가구를 직접 추적한 패널자료가 아니라, 2024년의 동시성 구조를 다른 시점의 명목금액으로 환산한 통시적 비교 추정치입니다. 임금지수 역시 전체근로자 평균이므로 개인별 임금상승률이나 연령별 임금격차를 그대로 나타내지 않습니다.

자료:
- [국가데이터처 소비자물가 총지수](https://www.index.go.kr/unity/potal/eNara/sub/showStblGams3.do?freq=Y&idx_cd=4226&period=1965%3A2025&stts_cd=422601)
- [고용노동부 사업체노동력조사 임금총액](https://www.index.go.kr/unity/potal/eNara/sub/showStblGams3.do?freq=Y&idx_cd=1485&period=2011%3A2025&stts_cd=148505)
- [한국부동산원 전국주택가격동향조사](https://www.reb.or.kr/reb/cm/cntnts/cntntsView.do?cntntsId=1033&mi=10333&statId=S234820263)
- 기준데이터: `국가데이터처_소비자물가지수_및_고용노동부_임금지수_1965-2025.csv`
""")

    #--------------------------------------------------------
    # 6.05.09.00 | 8. 소득 통계
    #--------------------------------------------------------
    with st.expander("8. 소득 통계: 연령별 임금과 연도별 임금지수", expanded=True):
        st.markdown("""
**1. 연령별 임금 통계 — 같은 해, 서로 다른 연령대의 소득 수준**

국가데이터처 「2024년 임금근로일자리 소득(보수) 결과」는 2024년 12월 임금근로일자리에서 하루 이상 일한 근로자의 월평균 보수를 연령대·성별로 제공합니다. 금액은 세전 월평균 보수이며, 취업하지 않은 사람의 소득을 0원으로 포함한 전체 인구 평균이 아닙니다.

| 연령대 | 전체 평균 | 남성 | 여성 |
|---|---:|---:|---:|
| 20대 | 271만 원 | 286만 원 | 255만 원 |
| 30대 | 397만 원 | 428만 원 | 354만 원 |
| 40대 | 469만 원 | 544만 원 | 363만 원 |
| 50대 | 445만 원 | 548만 원 | 306만 원 |
| 60대 | 293만 원 | 362만 원 | 200만 원 |
| 70세 이상 | 165만 원 | 234만 원 | 95만 원 |

이 통계의 연령구간은 20대·30대처럼 **10세 단위**입니다. 나침반의 20·25·30·35세 등 5세 간격 소득 기준점은 이 표의 5세 단위 원자료가 아닙니다. 앱의 생애 소득 기준곡선에 사용하기 위해 설정한 모델 기준값이며, 연령대 사이의 값은 보간합니다.

**2. 연도별 임금지수 — 같은 임금 수준을 서로 다른 연도 사이에서 환산**

연령별 임금 통계와 별도로, 고용노동부 「사업체노동력조사」의 전체근로자 월평균 임금총액을 사용합니다. 2011년 260만 7천 원에서 2025년 420만 5천 원으로 변화했으며, 이를 2024년=100으로 환산한 임금지수는 2025년 103.089입니다.

- 연령별 임금 통계: 2024년 한 시점의 연령대별 임금 차이를 보여줍니다.
- 연도별 임금지수: 전체근로자의 평균 임금수준이 연도에 따라 어떻게 달라졌는지 보여줍니다.
- 임금지수의 연도별 변화율: 전년 대비 임금상승률을 계산할 수 있습니다.

따라서 임금지수는 5세 단위 연령별 임금표가 아니며, 특정 개인의 임금이 매년 정확히 그 비율만큼 올랐다는 뜻도 아닙니다.

**3. 나침반 소득곡선에 적용하는 방식**

- 연령별 기준곡선은 직장인·자영업자별로 5세 간격의 모델 기준값을 두고, 현재 입력소득에 맞춰 개인별 배율을 적용합니다.
- 탭 3의 우리 가정 생애주기 재정곡선은 각 연령이 해당하는 달력연도를 계산하고, 2011~2025년은 실제 임금지수로 과거·현재의 명목 임금수준을 환산합니다.
- 2027년 이후는 2011~2025년 임금지수의 연평균 복합상승률 약 3.47%를 미래 가정으로 적용합니다. 2026년은 최신 실적연도 2025년 수준을 기준점으로 둡니다.
- 출산·육아 경력단절 및 복귀계수는 임금의 시간 보정과 별개의 생애사건 가정으로 적용합니다.

**4. 연간 상여금의 처리**

탭 3은 가계부의 `income_bonus`에 입력한 본인의 연간 상여금을 본인 근로소득에 더합니다. 현재 연간 상여금은 근로기간 동안 반복되는 연간 금액으로 모델링하고, 해당 연도의 임금지수와 출산·육아 경력계수를 함께 적용합니다. 따라서 미래 상여금도 임금지수에 따라 함께 보정됩니다.

배우자의 상여금을 별도로 입력하는 항목은 현재 구현되어 있지 않습니다. 배우자 소득곡선에는 월소득 기준곡선과 임금지수는 적용되지만 별도 상여금은 더해지지 않습니다.

국민연금과 추가연금, 기타 연간소득은 현재 입력한 명목금액을 고정해 더하며, 임금지수나 CPI로 자동 인상하지 않습니다. 따라서 연금의 물가연동이나 기타소득의 성장률은 별도 모델링 과제로 남아 있습니다.

탭 1의 소득곡선은 연간 상여금을 곡선에 더하지 않습니다. 다만 탭 1의 현재 재무 요약에서는 연간 상여금을 연간 총소득과 잉여자금 계산에 포함합니다. 즉, **현재 연간 재무 요약에 반영되는 것과 미래 생애 소득곡선에 반영되는 것은 서로 다른 기능**입니다.

**5. 자료 해석의 주의점**

임금근로일자리 평균보수는 사업체노동력조사의 임금총액과 조사대상·산출방식이 다릅니다. 두 통계를 하나의 연속된 임금계열처럼 합치지 않습니다. 연령별 통계는 연령별 소득 수준을 설명하고, 연도별 임금지수는 시간에 따른 명목 임금수준을 보정하는 용도로 구분합니다.

출처:
- [국가데이터처 「2024년 임금근로일자리 소득(보수) 결과」](https://www.mods.go.kr/board.es?act=view&bid=11113&list_no=443648&mid=a10301010000)
- [고용노동부 「사업체노동력조사」 임금총액 통계](https://www.index.go.kr/unity/potal/eNara/sub/showStblGams3.do?freq=Y&idx_cd=1485&period=2011%3A2025&stts_cd=148505)
- 기준데이터: `국가데이터처_2024_연령별_임금근로일자리_평균보수.csv`
""")

    #--------------------------------------------------------
    # 6.05.10.00 | 9. 결혼비용 통계
    #--------------------------------------------------------
    with st.expander("9. 결혼비용 통계: 신혼집은 신랑 측 77%, 그 외 비용은 비슷하게 나눠서", expanded=True):
        st.markdown("""
**결혼비용은 어디에서, 누구의 자금으로 마련될까?**

한국보건사회연구원은 2019년 조사 원자료를 분석해 신혼부부의 주거자금과 주거 이외 결혼비용을 구분하고, 신랑·신부 본인과 양측 부모의 부담을 살펴봤습니다. 두 항목은 조사표와 금액 기준이 다르므로 서로 더해 하나의 결혼비용 총액으로 해석하지 않습니다.

### ① 신혼집 마련 — 부모 지원과 대출을 포함한 주거자금

전체 평균 주거자금은 **1억 9,292만 원(2015년 가격 기준)**입니다.

| 자금 원천 | 금액 | 전체 주거자금 중 비중 |
|---|---:|---:|
| 부부 자기자금 | 6,716만 원 | 34.8% |
| 양가 부모 지원 | 7,616만 원 | 39.5% |
| 대출 | 4,960만 원 | 25.7% |
| **전체** | **1억 9,292만 원** | **100.0%** |

**네 가족 주체의 부담액**

| 부담 주체 | 금액 | 전체 주거자금 대비 | 네 주체 비대출 자금 내 비중 |
|---|---:|---:|---:|
| 신랑 본인 | 4,850만 원 | 25.1% | 33.8% |
| 신랑 부모 | 6,198만 원 | 32.1% | 43.2% |
| 신부 본인 | 1,866만 원 | 9.7% | 13.0% |
| 신부 부모 | 1,418만 원 | 7.3% | 9.9% |

네 주체의 비대출 자금 합계는 1억 4,332만 원입니다. 이 금액 안에서 신랑 본인과 신랑 부모의 몫은 **77.1%**, 신부 본인과 신부 부모의 몫은 **22.9%**입니다. 전체 주거자금에는 대출 4,960만 원(25.7%)도 별도로 포함됩니다.

**자금 원천별 신랑 측·신부 측 구성비**

| 자금 원천 | 신랑 측 | 신부 측 |
|---|---:|---:|
| 본인 자기자금 | 72.2% | 27.8% |
| 부모 지원 | 81.4% | 18.6% |
| 대출 | 87.2% | 12.8% |
| 전체 주거자금 | 79.7% | 20.3% |

보고서가 제시한 신랑 측 전체 조달액 79.7%와 신부 측 20.3%에는 각 측의 대출까지 포함되어 있습니다. 따라서 이 79.7%를 신랑 본인과 신랑 부모만의 부담률로 읽어서는 안 됩니다.

### ② 신혼집 외 결혼비용 — 신랑 측과 신부 측의 부담은 비교적 비슷함

여기에는 혼수 등 내구소비재, 신혼여행, 결혼식 비용 등이 포함됩니다. 표 3-10의 신랑 측·신부 측 금액과 각 측 내부의 부담 구성을 함께 봅니다.

| 부담 주체 | 신랑 측 금액 | 신랑 측 내 비중 | 신부 측 금액 | 신부 측 내 비중 |
|---|---:|---:|---:|---:|
| 본인 | 1,848만 원 | 49.5% | 1,884만 원 | 54.0% |
| 부모 | 1,884만 원 | 50.5% | 1,605만 원 | 46.0% |
| **측별 합계** | **3,732만 원** | **100.0%** | **3,489만 원** | **100.0%** |

보고서의 평균 열은 본인 부담 1,866만 원(51.7%), 부모 지원 1,745만 원(48.3%), 합계 3,611만 원입니다. 이 3,611만 원은 신랑 측과 신부 측 금액의 평균이지 두 측의 금액을 합산한 값이 아닙니다.

**읽을 때 기억할 점**

- 신혼집은 주거자금 조달에서 신랑 측 기여가 더 크게 나타났습니다. 대출을 제외한 네 주체 자금 중 신랑 측 비중은 77.1%입니다.
- 신혼집 외 비용은 신랑 측 3,732만 원, 신부 측 3,489만 원으로 큰 차이가 나타나지 않았습니다. 각 측 내부에서는 본인과 부모가 대체로 절반씩 부담했습니다.
- 이는 조사에 참여한 신혼부부의 평균적 경향입니다. 모든 가정이 같은 비율로 부담하거나 부모 지원을 받는다는 뜻은 아닙니다.

**나침반 적용 원칙 — 자녀 성별을 묻지 않는 평균 지원액**

나침반은 입력을 최소화하기 위해 자녀의 성별을 별도로 묻지 않습니다. 대신 신랑 측·신부 측 부모 지원 통계의 평균을 적용해, 한쪽 부모인 우리 가정의 지원 추정액을 계산합니다.

- 신혼집: 가연 2024년 신혼집 비용 2억 4,176만 원 × (한국보건사회연구원 표 3-2의 부모 지원 7,616만 원 ÷ 전체 주거자금 1억 9,292만 원) ÷ 2
- 신혼집 외: 가연 2024년 비용 6,298만 원 × (한국보건사회연구원 표 3-10의 평균 부모 지원 1,745만 원 ÷ 평균 측별 비용 3,611만 원) ÷ 2
- 한 자녀당 부모 지원 추정액은 약 **6,294만 원**입니다. 생애주기 곡선에서는 기존처럼 5년에 나누어 반영하고, 발생 연도의 소비자물가 기준으로 환산합니다.

이 값은 서로 다른 조사자료의 평균 구조를 결합한 모델 추정치이며, 개별 가정의 실제 지원액을 뜻하지 않습니다.

**자료와 산출 기준**

- 기관·보고서: 한국보건사회연구원, 최선영·오신휘·박종서, 「신혼부부의 주거자금 조달방식과 부모 지원의 젠더-계층적 성격」, 연구보고서(수시) 2020-08, 2020년 11월
- 조사: 2019년 「청년세대의 결혼 및 출산 동향에 관한 조사」 원자료 분석
- 표 3-2·3-9: 신혼집 주거자금 원천별 금액. 2015년 가격 기준
- 표 3-10: 신랑 측·신부 측 주거 이외 결혼비용 규모. 보고서 수록 금액
- CSV 백데이터: `data/기준데이터/한국보건사회연구원_2020_신혼부부_결혼비용_자금원천.csv`
- 산출 정의와 분모별 비율: 같은 폴더의 README 참고

원문: [한국보건사회연구원 연구보고서 PDF](https://repository.kihasa.re.kr/bitstream/201002/37080/2/%EC%97%B0%EA%B5%AC%EB%B3%B4%EA%B3%A0%EC%84%9C%28%EC%88%98%EC%8B%9C%29%202020-08.pdf)
""")

        # 가연 「2024 결혼비용 리포트」의 전체 평균: 신혼집과 신혼집 외 비용 비교
        fig_total_wedding = go.Figure(data=[go.Pie(
            labels=["신혼집", "신혼집 외"],
            values=[24176, 6298],
            hole=0.38,
            textinfo="label+percent",
            textposition="inside",
            insidetextorientation="horizontal",
            textfont_size=14,
            hovertemplate="%{label}<br>%{value:,.0f}만 원<extra></extra>",
            sort=False
        )])
        fig_total_wedding.update_layout(
            title="신혼집과 신혼집 외 결혼비용 — 가연 2024",
            showlegend=False,
            margin=dict(t=52, b=8, l=8, r=8),
            height=340,
            annotations=[dict(
                text="3억 474만 원",
                x=0.5, y=0.5,
                xref="paper", yref="paper",
                showarrow=False,
                font=dict(size=17, color="#FFFFFF"),
                bgcolor="#334155",
                bordercolor="#334155",
                borderpad=4.25
            )]
        )
        st.plotly_chart(fig_total_wedding, use_container_width=True, config={"displayModeBar": False})
        st.caption("※ 가연 「2024 결혼비용 리포트」 기준: 총 3억 474만 원 중 신혼집 2억 4,176만 원, 신혼집 외 비용 6,298만 원입니다. ‘신혼집 외 비용’에는 혼수뿐 아니라 예식·신혼여행 등도 포함되므로 혼수만의 금액을 뜻하지 않습니다.")

        col_house, col_nonhouse = st.columns(2)
        with col_house:
            fig_house_share = go.Figure(data=[go.Pie(
                labels=["신랑 측", "신부 측"],
                values=[11048, 3284],
                hole=0.38,
                textinfo="label+percent",
                textposition="inside",
                insidetextorientation="horizontal",
                hovertemplate="%{label}<br>%{value:,.0f}만 원<extra></extra>",
                sort=False
            )])
            fig_house_share.update_layout(title="신혼집 비대출 자금 분담", showlegend=False, margin=dict(t=48, b=8, l=8, r=8), height=300)
            st.plotly_chart(fig_house_share, use_container_width=True, config={"displayModeBar": False})
        with col_nonhouse:
            fig_nonhouse_share = go.Figure(data=[go.Pie(
                labels=["신랑 측", "신부 측"],
                values=[3732, 3489],
                hole=0.38,
                textinfo="label+percent",
                textposition="inside",
                insidetextorientation="horizontal",
                hovertemplate="%{label}<br>%{value:,.0f}만 원<extra></extra>",
                sort=False
            )])
            fig_nonhouse_share.update_layout(title="신혼집 외 비용의 양측 비중", showlegend=False, margin=dict(t=48, b=8, l=8, r=8), height=300)
            st.plotly_chart(fig_nonhouse_share, use_container_width=True, config={"displayModeBar": False})
        st.caption("※ 신혼집은 대출을 제외한 네 주체의 자금(1억 4,332만 원) 중 양측 비중입니다. 신혼집 외는 표 3-10의 신랑 측 평균액 3,732만 원과 신부 측 평균액 3,489만 원을 비교한 상대 비중이며, 두 금액을 공식 평균 총액으로 합산한 값은 아닙니다.")


    #--------------------------------------------------------
    # 6.05.11.00 | 10. 빅5 우리집 이벤트
    #--------------------------------------------------------
    with st.expander("10. 빅5 우리집 이벤트", expanded=True):
        st.markdown("""
**우리 집의 생애주기에서 큰 비용이 발생하는 다섯 가지 사건을 살펴봅니다.**

이 자료는 미래 비용을 정답처럼 예측하기 위한 것이 아니라, 각 사건의 비용이 어떤 통계와 가정에서 나오는지 확인하기 위한 자료실입니다. 확인된 통계와 아직 검증이 필요한 모델 가정을 구분합니다.

| 이벤트 | 현재 모델 금액·기간 | 근거와 현재 상태 |
|---|---:|---|
| ① 나의 결혼 | 미래 결혼: 주택 자기자금 추정액의 1/2 + 6,298만 원. 2년 분산 | 가연 2024 결혼비용 중 신혼집 외 비용 6,298만 원. 신혼집 비용은 별도 주택 마련 모델과 중복 여부 확인 필요 |
| ② 출산·육아 | 8,064만 원 / 6년 (연 1,344만 원) | 2024년 전국보육실태조사 월평균 111.6만 원을 72개월 환산하면 8,035.2만 원. 기존 값과 약 0.36% 차이 |
| ③ 주택구입 | 지역 아파트 가격 × (1-LTV). 4년 분산 | 주거실태조사 자금 구성 분석 완료. 연령·지역·주택유형별 통계 기본값을 설계 중이며 아직 계산식에 연결하지 않음 |
| ④ 자녀 대학 | 등록금 2,648만 원 + 생활비 3,984만 원 = 약 6,632만 원 / 4년 | 2026학년도 비수도권 4년제 평균 등록금과 2022년 대학생 학기 중 생활비 조사. 생활비 48개월 적용은 모델 가정 |
| ⑤ 자녀 결혼 | 약 6,294만 원 / 5년 (연 약 1,259만 원) | 가연 2024 결혼비용과 한국보건사회연구원 2020년 부모 지원 비율을 결합한 모델 추정치 |

### 가구지출과 생애사건 비용의 중복 조정

예보원의 크기는 **중복 차감 전 이벤트 총비용**을 기준으로 유지합니다. 반면 가구 재정곡선에는 MDIS 가계지출에 이미 포함되었을 가능성이 있는 항목을 차감한 금액만 추가합니다.

| 이벤트 | 예보원 기준 총비용 | 차감액 | 차감률* | 재정곡선 추가분 |
|---|---:|---:|---:|---:|
| ① 나의 결혼 | 6,298만 원 + 신혼집 부담분 | 혼수 2,615만 원 | 41.5% | 3,683만 원 + 신혼집 부담분 |
| ② 출산·육아 | 8,064만 원 | 8,035.2만 원 | 99.6% | 28.8만 원 |
| ③ 주택구입 | 주택 자기자금 H | 0원 | 0% | H |
| ④ 자녀 대학 | 등록금 2,647.84만 원 + 생활비 3,984만 원 | 6,631.84만 원 | 100% | 0원 |
| ⑤ 자녀 결혼 | 약 6,293.8만 원 | 신혼집 외 부모지원 약 1,521.7만 원 | 24.2% | 신혼집 주거자금 지원 약 4,772만 원 |

* 차감률은 각 이벤트의 차감 대상 총액 기준입니다. 나의 결혼은 신혼집 외 비용 6,298만 원, 자녀 결혼은 부모지원 추정액 전체를 분모로 계산합니다.

- **나의 결혼:** 혼수는 가구의 가전·가구 등 내구재 지출과 겹칠 가능성이 높아 차감합니다. 예식·여행 등 세부 중복액을 분리할 근거가 부족한 나머지 비용은 그대로 둡니다.
- **출산·육아:** 2024년 보육실태조사의 월평균 양육비 111.6만 원은 같은 조사에서 측정한 가구 총지출의 29.4%입니다. 72개월 환산액 8,035.2만 원만 차감하고, 모델 총액 8,064만 원과의 차이 28.8만 원은 남깁니다.
- **주택구입:** 주택 자기자금은 일반 소비·가계지출과 구분되는 자산 취득 성격이므로 차감하지 않습니다.
- **자녀 대학:** 등록금과 생활비는 각각 교육비 및 일반 생활비와 중복될 가능성이 있어 전액 차감합니다.
- **자녀 결혼:** 신혼집 외 부모지원은 가구간 이전지출과 겹칠 가능성이 있어 차감하되, 주거자금 지원은 자산이전 성격으로 보아 추가분에 남깁니다.

차감 전 총비용과 차감액은 이벤트 발생 연령에 적용하는 **동일한 CPI 상대계수**로 함께 환산합니다. 국가데이터처 가계동향조사에서 가구간 이전지출은 비소비지출에 포함되고, 부동산 구입·자산이전 등 자산변동 지출은 별도 항목으로 구분됩니다([조사항목별 기입 방법](https://mods.go.kr/boardDownload.es?bid=12030&list_no=428759&seq=2)). 구분할 수 없는 비용은 임의로 차감하지 않고 재정곡선에 남깁니다. 이 조정은 중복 가능성을 반영한 모델 가정이며, 실제 가구별 중복액을 직접 측정한 통계는 아닙니다.

### ① 나의 결혼과 ⑤ 자녀 결혼 — 근거 확보

가연 「2024 결혼비용 리포트」의 평균 결혼비용은 3억 474만 원이며, 신혼집 2억 4,176만 원과 신혼집 외 비용 6,298만 원으로 구분합니다.

한국보건사회연구원 2020년 연구보고서(2019년 조사 분석)에서는 신혼집 주거자금 중 부모 지원 비중이 39.5%, 주거 이외 결혼비용에서 부모 지원 비중이 약 48.3%로 나타났습니다.

자녀 한 명의 결혼 지원 추정액은 다음과 같이 계산합니다.

- 신혼집 지원: 24,176만 원 × (7,616 ÷ 19,292) ÷ 2 = 약 4,772만 원
- 신혼집 외 지원: 6,298만 원 × (1,745 ÷ 3,611) ÷ 2 = 약 1,522만 원
- 합계: 약 **6,294만 원**. 생애주기 곡선에서는 5년에 나누어 반영합니다.

서로 다른 조사자료의 비용 수준과 부모 지원 비율을 결합한 모델 추정치이며, 개별 가정의 실제 지원액이나 공식 예측값은 아닙니다.

### ② 출산·육아 — 추가 근거 확인 필요

교육부 「2024년 전국보육실태조사 - 가구조사 보고」에서 실제 양육비 표를 확인했습니다. 조사대상은 0~6세 미만 자녀가 있는 가구이며, 표본은 2,494가구입니다. 월평균 양육비는 영아 가구 109.1만 원, 유아 가구 116.5만 원, 영유아 가구 전체 111.6만 원입니다.

전체 평균 111.6만 원을 72개월로 단순 환산하면 8,035.2만 원입니다. 현재 모델의 8,064만 원과 약 0.36% 차이로 매우 가깝습니다. 다만 동일한 월평균을 6년 내내 적용한 환산치이지, 동일 아동을 6년간 추적한 누적 지출액은 아닙니다. 영아·유아 구분별 비용을 이용해 단계별 비용 곡선을 만들 수 있는지 추가 검토합니다.

원문 보고서: [육아정책연구소 「2024년 보육실태조사: 가구조사 보고」](https://repo.kicce.re.kr/bitstream/2019.oak/5843/11/CR2412_re3.pdf) · 참고 분석: [국회예산정책처 자료](https://nabo.go.kr/board/file/down.do?fid=33318651)

### ③ 주택구입 — 2024년 주거실태조사 분석 결과

이번 MDIS 추출본은 61,341가구, 41개 변수입니다. 문13의 네 가지 자금 출처를 모두 확인하고 최종가중치를 적용해 집계했습니다.

현재 주택이 생애최초 주택이고 아파트인 가구 10,607가구의 자금 구성은 다음과 같습니다.

| 생애최초 아파트 취득 연령 | 표본수 | 자기자금 | 금융기관 융자 | 부모·친지 지원 |
|---|---:|---:|---:|---:|
| 25~29세 | 556 | 54.28% | 30.01% | 15.15% |
| 30~34세 | 1,868 | 59.91% | 31.13% | 8.43% |
| 35~39세 | 2,261 | 65.29% | 28.54% | 5.79% |
| 40~44세 | 1,813 | 71.07% | 24.86% | 3.91% |
| 45~49세 | 1,273 | 75.15% | 22.26% | 2.44% |

금융기관 융자 비율은 해당 가구의 문13 네 가지 자금 출처 합계 중 금융기관 융자액이 차지하는 비중입니다. 주택담보대출만을 분리한 규제상 LTV가 아닙니다. 따라서 앱에서는 '통계적 금융기관 융자 비율'로 표시하고, LTV와 구분해야 합니다.

예상 구매 연령·지역·주택유형에 맞는 통계값을 기본 참고값으로 제시하는 방향을 검토합니다. 표본이 적은 조합은 전국 또는 상위 지역 집단으로 대체하고, 표본 수를 함께 표시합니다.

- [가공 CSV — 생애최초 주택 구입자금 구성](https://github.com/ufreezone-ops/nachimpan/blob/dev/data/기준데이터/국토교통부_2024_주거실태조사_생애최초주택_구입자금구성.csv)
- [분석 README — 변수·가중치·필터·해석 기준](https://github.com/ufreezone-ops/nachimpan/blob/dev/data/기준데이터/국토교통부_2024_주거실태조사_생애최초주택_구입자금구성_README.md)
- [국토교통부 2024년 주거실태조사 조사표·요약보고서](https://mods.go.kr/boardDownload.es?bid=11477&list_no=442458&seq=4)

기존 '생애최초 주택 마련 연령' CSV는 취득 연령 분포와 중앙값을 보여주는 자료이고, 이번 CSV는 자금 조달 구성을 보여주는 자료입니다. 분석 목적이 다르므로 두 파일은 삭제·통합하지 않고 함께 보존합니다.

### ④ 자녀 대학 — 등록금과 생활비를 분리한 기준

기존 4년 총액 약 **6,632만 원**을 등록금과 생활비로 나누어 근거를 정리했습니다. 두 통계의 기준연도와 성격이 다르므로, 각각 별도 항목으로 유지합니다.

**① 등록금 — 약 2,648만 원 / 4년**

교육부·한국대학교육협의회 「2026년 4월 대학정보공시 분석 결과」에 따르면 4년제 일반대학·교육대학 192개교의 2026학년도 연간 평균 등록금은 전국 727만 300원, 수도권 827만 원, 비수도권 661만 9,600원입니다.

나침반의 기본 예시는 비수도권 평균을 사용합니다.

- 연간 등록금: **661만 9,600원**
- 4년 환산: 661만 9,600원 × 4년 = **2,647만 8,400원**
- 평균 산출: 학과별·학년별 등록금에 해당 입학정원을 곱한 값의 합을 전체 입학정원의 합으로 나눈 값
- 장학금 차감 전 금액이며, 실제 부담액은 대학·전공·장학금에 따라 달라집니다.

자료: [교육부 「2026년 4월 대학정보공시 분석 결과」(2026.4.29.)](https://www.moe.go.kr/boardCnts/viewRenew.do?boardID=294&boardSeq=106020&lev=0&m=020402&s=moe)

**② 생활비 — 약 3,984만 원 / 4년**

학원복음화협의회 「2022 한국 대학생의 의식과 생활에 대한 조사」에서 학기 중 한 달 평균 생활비는 **83만 원**으로 조사됐습니다. 해당 조사 결과를 목회데이터연구소 「넘버즈 179호」(2023.2.14.)가 소개했습니다.

- 조사 대상: 국내 대학 재학생 중 2~4년제 학부생 및 석·박사
- 조사 지역·방법: 전국 온라인 패널 조사
- 유효 표본: 1,000명
- 조사 기간: 2022년 8월 17일~31일
- 표본 설계: 지역별 대학생 수 비례 할당 후 무작위 추출
- 조사 결과: 학기 중 월평균 생활비 83만 원
- 모델 환산: 83만 원 × 48개월 = **3,984만 원**

**중요한 가정:** 조사값은 연중 월평균이 아니라 학기 중 월평균입니다. 이를 방학 기간까지 포함한 48개월에 적용한 것은 나침반의 단순 모델 가정이며, 조사에서 직접 측정한 4년 누적액이 아닙니다. 요약자료만으로 생활비의 세부 항목(주거비·교통비 등) 포함 범위도 확인되지 않으므로, 포함 여부를 단정하지 않습니다.

자료: 학원복음화협의회 「2022 한국 대학생의 의식과 생활에 대한 조사」 결과를 소개한 [목회데이터연구소 「넘버즈 179호」(2023.2.14.)](https://mhdata.or.kr/mailing/Numbers179_230214_Full_Report.pdf)

**③ 기존 4년 총액의 구성**

| 항목 | 기준 | 4년 환산액 |
|---|---:|---:|
| 등록금 | 연 661만 9,600원 × 4년 | 2,647만 8,400원 |
| 생활비 | 월 83만 원 × 48개월 | 3,984만 원 |
| **합계** | | **6,631만 8,400원 ≈ 6,632만 원** |

등록금은 2026학년도, 생활비는 2022년 조사 기준으로 서로 다릅니다. 따라서 6,632만 원은 동일 기준연도로 물가 조정한 합계가 아니라, 현재 확보한 두 통계를 결합한 참고 추정치입니다. 통시성 보정에서는 등록금과 생활비를 분리해 각각의 기준연도와 지수로 환산해야 합니다.

- [가공 CSV — 등록금·생활비 분리 기준](https://github.com/ufreezone-ops/nachimpan/blob/dev/data/기준데이터/교육부_2026_대학등록금_및_대학생생활비_기준.csv)
- [README — 출처·조사 범위·환산 가정](https://github.com/ufreezone-ops/nachimpan/blob/dev/data/기준데이터/교육부_2026_대학등록금_및_대학생생활비_기준_README.md)

기존 모델의 6,632만 원은 잠정 기준값으로 유지하되, 등록금과 생활비를 별도 항목으로 관리합니다. 특히 생활비 48개월 적용은 통계값 자체가 아니라 모델 가정임을 표시합니다.

### 아직 확정해야 할 모델 쟁점

1. **결혼과 주택구입의 중복:** 미래 결혼 이벤트에는 주택 자기자금 추정액의 1/2이 들어가고, 별도 주택구입 이벤트에는 주택 자기자금 추정액 전체가 들어갑니다. 같은 신혼집을 뜻한다면 중복 계산일 수 있으므로, 두 이벤트가 서로 다른 주택 마련인지 먼저 정해야 합니다.
2. **주택자금 기본값:** 기존 LTV 입력값과 이번 조사에서 산출한 금융기관 융자 비율은 다른 개념입니다. 통계값을 연령·지역·주택유형별 기본 참고값으로 제시하는 설계를 확정한 뒤 연결합니다.
3. **시간 보정:** 현재 빅5 이벤트 금액은 코드에서 연도별 물가·주택가격 지수로 자동 환산되지 않는 고정 기준값입니다. 일반 비용은 CPI, 주택 관련 비용은 지역·유형별 주택가격지수를 적용하는 방식으로 분리해야 합니다. 다년간 분산 비용은 각 연도 몫을 해당 연도 기준으로 환산해야 합니다.

### 다음에 확보·검증할 자료

- 출산·육아: 원문 보고서와 주요 양육비 표를 확인했습니다. 다음 단계는 영아·유아 연령 구분, 지출 항목, 정부 지원금 차감 여부를 확인하고 단계별 CSV로 정리하는 것입니다.
- 대학: 등록금·생활비의 기준 자료를 확보했습니다. 다음에는 대학별·계열별 등록금 차이, 장학금 차감 후 실부담액, 최신 대학생 생활비 조사와 방학 지출을 추가 검증합니다.
- 주택: 지역·주택유형별 실제 주택가격 수준 자료. 기존 KB 연간 주택가격지수는 가격 변동률용이며, 기준 주택가격 금액을 대신하지 않음
- 시간 보정: 기존 CPI·임금지수 CSV의 공식 원자료 대조 및 시계열 검증. 현재 파일은 공식 시계열 검증이 끝난 자료로 취급하지 않음

**현재 상태:** 결혼·자녀 결혼은 산출식과 주요 출처를 확보했습니다. 출산·육아는 2024년 보육실태조사 근거를 확인했습니다. 주택구입은 MDIS 원자료 추출과 가중 집계표를 확보했습니다. 자녀 대학은 등록금과 생활비를 분리해 출처 및 환산 가정을 기록했습니다. 빅5 전체의 시간 보정과 결혼·주택구입 중복 여부는 아직 확정 전입니다.
""")



    #--------------------------------------------------------
    # 6.05.12.00 | 11. 고령층 근로연령 통계
    #--------------------------------------------------------
    with st.expander("11. 고령층 근로연령 통계", expanded=True):
        st.markdown("""
**은퇴를 몇 살로 생각하더라도, 실제 사회에서는 그 이후에도 일하는 사람이 적지 않습니다.** 이 자료는 개인의 은퇴 희망 연령과 사회의 고령층 근로 현실을 비교해 보기 위한 참고 자료입니다.

### ① 고령층의 현재 고용 상황 — 2026년 5월

국가데이터처 「2026년 5월 경제활동인구조사 고령층 부가조사 결과」에 따르면, 55~79세 고령층의 고용률은 **59.5%**입니다.

| 지표 | 수치 | 의미 |
|---|---:|---|
| 고령층(55~79세) 인구 | 1,701만 7천 명 | 조사 대상 인구 |
| 경제활동참가율 | 60.9% | 취업자와 실업자를 합친 경제활동인구 비율 |
| 고용률 | **59.5%** | 전체 인구 중 취업자 비율 |
| 장래 근로 희망자 | **69.2%** | 앞으로도 일하기를 희망한다고 답한 비율 |
| 희망 근로 연령 | **73.6세** | 계속 일하기를 희망하는 사람들의 평균 희망 연령 |

고령층 10명 중 약 6명이 현재 취업 상태이고, 약 7명은 앞으로도 일하기를 희망한다고 응답한 셈입니다. 2026년 조사에서 취업자는 1,012만 5천 명, 고용률은 59.5%였습니다.

### ② 몇 살까지 일하고 싶을까?

2026년 조사에서 장래 근로를 희망한 사람들의 평균 희망 연령은 **73.6세**였습니다. 이 값은 실제 은퇴 연령이나 실제 취업 종료 연령이 아닙니다. 일을 계속하고 싶다는 사람들의 희망을 조사한 결과입니다.

따라서 나침반에서는 이 수치를 '73세까지 일해야 한다'는 기준으로 사용하지 않습니다. 개인이 생각하는 은퇴 시점과 사회에서 관찰되는 근로 현실 사이에 차이가 있을 수 있음을 보여주는 참고 지표로만 해석합니다.

### ③ 가장 오래 다닌 일자리와 실제 근로는 다르다

2026년 조사에서 취업 경험자의 가장 오래 근무한 일자리를 살펴보면 다음과 같습니다.

| 지표 | 결과 |
|---|---:|
| 가장 오래 근무한 일자리를 그만둔 사람 | 69.5% |
| 그 일자리를 그만둘 당시 평균 연령 | 53.0세 |
| 가장 오래 근무한 일자리를 현재도 다니는 사람 | 30.5% |
| 현재 그 일자리에 근무하는 사람의 평균 연령 | 62.6세 |

여기서 '가장 오래 근무한 일자리를 그만둔 나이'는 모든 경제활동을 끝낸 나이가 아닙니다. 주된 일자리에서 이탈한 뒤 다른 일자리나 자영업 등으로 근로를 이어갈 수 있습니다. 주된 일자리의 퇴직과 생애 전체의 노동 종료를 구분해야 합니다.

### ④ 연령대별 임금근로일자리 평균보수 — 그래프의 보라색 점선

나침반의 '우리 가정 생애 소득(예상)' 그래프에 표시한 보라색 점선은 국가데이터처 「2024년 임금근로일자리 소득(보수) 결과」의 성별·연령대별 월평균 보수입니다. 그래프에서는 월평균 보수에 12를 곱해 연환산 참고값으로 표시합니다.

| 연령대 | 전체 | 남성 | 여성 |
|---|---:|---:|---:|
| 20대 | 271만 원 | 286만 원 | 255만 원 |
| 30대 | 397만 원 | 428만 원 | 354만 원 |
| 40대 | 469만 원 | 544만 원 | 363만 원 |
| 50대 | 445만 원 | 548만 원 | 306만 원 |
| 60대 | 293만 원 | 362만 원 | 200만 원 |
| 70세 이상 | 165만 원 | 234만 원 | 95만 원 |

단위: 만 원 / 월 / 세전. 기준: 2024년 12월 임금근로일자리.

**이 보수 통계는 해당 연령대에서 임금근로일자리에 종사한 사람들의 평균값입니다.** 취업하지 않은 사람을 0원으로 포함한 인구 전체의 평균소득이 아닙니다. 사업소득자와 특수형태근로종사자 등 일부는 작성 대상에서 제외됩니다.

또한 그래프의 70세 이상 구간을 75세 위치에 표시한 것은 시각화를 위한 대표연령 좌표입니다. 75세가 실제 평균 근로 종료 연령이라는 뜻은 아닙니다.

### ⑤ 나침반에서의 해석 원칙

- 개인·가구의 예상소득 곡선은 사용자가 설정한 은퇴 희망 연령을 반영합니다.
- 보라색 점선은 개인의 은퇴 희망 연령과 무관하게 표시되는 연령대별 임금근로자 평균보수 비교선입니다.
- 고용률은 해당 연령대 인구 중 취업자의 비율이고, 평균보수는 임금근로일자리에서 일하는 사람들의 보수입니다. 서로 분모와 의미가 다른 통계이므로 하나의 수치처럼 합치지 않습니다.
- 이 자료는 은퇴를 늦추도록 권하거나 개인의 미래 소득을 예측하는 자료가 아닙니다. 은퇴 이후에도 노동과 소득활동이 이어질 수 있다는 사회적 현실을 살펴보는 참고 자료입니다.

**자료 출처 및 가공 파일**

- [국가데이터처 — 2026년 5월 경제활동인구조사 고령층 부가조사 결과](https://www.mods.go.kr/board.es?act=view&bid=210&list_no=446335&mid=a10301010000)
- [국가데이터처 — 2024년 임금근로일자리 소득(보수) 결과](https://www.mods.go.kr/board.es?act=view&bid=11113&list_no=443648&mid=a10301010000)
- [가공 CSV — 연령별 임금근로일자리 평균보수](https://github.com/ufreezone-ops/nachimpan/blob/dev/data/기준데이터/국가데이터처_2024_연령별_임금근로일자리_평균보수.csv)
- [README — 출처·자료 범위·해석 기준](https://github.com/ufreezone-ops/nachimpan/blob/dev/data/기준데이터/국가데이터처_2024_연령별_임금근로일자리_평균보수_README.md)
""")

    st.caption("※ 이 자료실은 주제별 통계와 출처를 차근차근 확장하기 위한 첫 구성입니다. 출처와 기준이 확인되지 않은 수치는 제시하지 않습니다.")


#--------------------------------------------------------
# 5.01.03 | 출처 복귀 — 원래 화면 위치 복원
#--------------------------------------------------------
_restore_anchor = st.session_state.get("_source_restore_anchor")
_open_anchor = st.session_state.get("_source_open_anchor")

if _restore_anchor or _open_anchor:
    _scroll_target_id = _open_anchor or _restore_anchor
    _scroll_block = "start" if _open_anchor else "center"
    st.components.v1.html(
        f"""
        <script>
        try {{
            const doc = window.parent.document;
            const target = doc.getElementById("{_scroll_target_id}");

            if (target) {{
                window.parent.setTimeout(() => {{
                    target.scrollIntoView({{
                        behavior: "auto",
                        block: "{_scroll_block}"
                    }});
                }}, 250);
            }}
        }} catch(e) {{}}
        </script>
        """,
        height=0
    )

    st.session_state.pop("_source_restore_anchor", None)
    st.session_state.pop("_source_open_anchor", None)
    if _restore_anchor:
        st.session_state.pop("_source_return_context", None)
        st.session_state.pop("_active_source_id", None)