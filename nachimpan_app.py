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
.st-key-source_nta_generational,
.st-key-source_retirement_milestones,
.st-key-loan_payment_source_link {
    width: auto !important;
    min-width: 0 !important;
    max-width: max-content !important;
    flex: 0 0 auto !important;
    margin-left: 0.1rem !important;
}
.st-key-source_retirement_expense [data-testid="stButton"] button,
.st-key-source_nta_basic [data-testid="stButton"] button,
.st-key-source_nta_generational [data-testid="stButton"] button,
.st-key-source_retirement_milestones [data-testid="stButton"] button,
.st-key-loan_payment_source_link [data-testid="stButton"] button,
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
.st-key-source_retirement_milestones [data-testid="stButton"] button:hover,
.st-key-loan_payment_source_link [data-testid="stButton"] button:hover,
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
.st-key-source_retirement_milestones [data-testid="stButton"] button p,
.st-key-loan_payment_source_link [data-testid="stButton"] button p,
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
/* 대출 라벨과 아이콘을 은퇴 제목 행과 같은 하단 기준선으로 정렬 */
.st-key-loan-payment-label-row [data-testid="stHorizontalBlock"] {
    align-items: flex-end !important;
    column-gap: 0.12rem !important;
}
.st-key-loan-payment-label-row [data-testid="stElementContainer"] {
    flex: 0 0 auto !important;
    width: max-content !important;
    min-width: 0 !important;
}
.loan-payment-label-text {
    display: inline-block;
    margin: 0 !important;
    padding: 0 !important;
    color: var(--text-color) !important;
    font: inherit !important;
    line-height: inherit !important;
    white-space: nowrap !important;
}
.st-key-loan-payment-field [data-testid="stMarkdownContainer"] p {
    margin: 0 !important;
}
/* 행 안의 버튼을 은퇴 제목 옆 나침반과 동일한 무테·무배경 형태로 */
.st-key-loan-payment-label-row [data-testid="stButton"],
.st-key-loan-payment-label-row [data-testid="stButton"] > div {
    width: max-content !important;
    min-width: 0 !important;
    height: auto !important;
    min-height: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
    border: 0 !important;
    background: transparent !important;
    box-shadow: none !important;
}
.st-key-loan-payment-label-row [data-testid="stButton"] button,
.st-key-loan-payment-label-row [data-testid="stButton"] button:hover,
.st-key-loan-payment-label-row [data-testid="stButton"] button:focus,
.st-key-loan-payment-label-row [data-testid="stButton"] button:focus-visible,
.st-key-loan-payment-label-row [data-testid="stButton"] button:active {
    appearance: none !important;
    -webkit-appearance: none !important;
    width: auto !important;
    min-width: 0 !important;
    height: auto !important;
    min-height: 0 !important;
    padding: 0 0.12rem !important;
    margin: 0 !important;
    border: 0 !important;
    outline: none !important;
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
    transform: none !important;
}
.st-key-loan-payment-label-row [data-testid="stButton"] button p {
    margin: 0 !important;
    padding: 0 !important;
    font-size: inherit !important;
    line-height: 1 !important;
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

/* 탭3 가족 입력 expander: 주황색 배경으로 클릭 영역을 명확히 표시 */
.st-key-family-retirement-expander [data-testid="stExpander"] summary {
    background: linear-gradient(135deg, #EA580C 0%, #C2410C 100%) !important;
    background-color: #EA580C !important;
    border: 1px solid #EA580C !important;
    color: #FFFFFF !important;
}
.st-key-family-retirement-expander [data-testid="stExpander"] summary:hover {
    background: #C2410C !important;
    border-color: #C2410C !important;
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

# 첫 화면에서 받는 현재 주거지역 선택지
KOREA_REGION_OPTIONS = [
    "서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종",
    "경기", "강원", "충북", "충남", "전북", "전남", "경북", "경남", "제주",
]



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
    "marriage_plan", "child_plan", "housing_plan", "residence_region",
    "housing_region", "housing_ltv", "sibling_items", "advanced_mode"
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
        "residence_region": "부산",
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
        "residence_region": "부산",
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
        # 구버전 저장 사례에는 현재 주거지역이 없을 수 있으므로 기존 지역값을 우선 승계
        if "residence_region" not in st.session_state:
            st.session_state["residence_region"] = case_dict.get(
                "housing_region", "지역 선택"
            )

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
        st.markdown(f"**지역:** {st.session_state.get('residence_region', '미입력')}")

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
            name_col, age_col = st.columns([2.0, 1.1])

            with name_col:
                st.markdown("<div style='font-size: 18px; font-weight: 800; color: #F8FAFC; margin-bottom: 6px; text-align: center;'>이름(별칭)</div>", unsafe_allow_html=True)
                name = st.text_input("이름(별칭)", placeholder="이름 또는 별칭", key="start_person_name", label_visibility="collapsed")

            with age_col:
                st.markdown("<div style='font-size: 18px; font-weight: 800; color: #F8FAFC; margin-bottom: 6px; text-align: center;'>나이</div>", unsafe_allow_html=True)
                age_text = st.text_input("나이", placeholder="예: 38", key="start_person_age_text", max_chars=3, label_visibility="collapsed")

            region_col, start_col = st.columns([2.0, 1.1])
            with region_col:
                st.markdown("<div style='font-size: 18px; font-weight: 800; color: #F8FAFC; margin-bottom: 6px; text-align: center;'>지역</div>", unsafe_allow_html=True)
                residence_region = st.selectbox(
                    "지역", ["지역 선택"] + KOREA_REGION_OPTIONS,
                    key="start_person_region", label_visibility="collapsed"
                )

            with start_col:
                st.markdown("<div style='font-size: 18px; font-weight: 800; margin-bottom: 6px; text-align: center;'>&nbsp;</div>", unsafe_allow_html=True)
                submitted = st.form_submit_button("시작", use_container_width=True, type="primary")

            try:
                age = int(age_text) if age_text.strip() else None
                if age is not None and not (1 <= age <= 120):
                    age = None
            except ValueError:
                age = None

            if submitted:
                if not name.strip() or age is None or residence_region == "지역 선택":
                    st.warning("이름(별칭), 나이, 지역을 모두 올바르게 입력해 주세요.")
                else:
                    st.session_state.person_name = name.strip()
                    st.session_state.person_age = int(age)
                    st.session_state.residence_region = residence_region
                    st.session_state.started = True
                    st.rerun()
            
    st.stop()



#########################################################
# -------------------------------------------------------
# 5.00 | 메인 네비게이션 헤더
# -------------------------------------------------------
#########################################################

#########################################################
# 5.01 | 상단 6개 메뉴 네비게이션 바
#########################################################

#--------------------------------------------------------
# 5.01.01 | 기본 버튼 기반 메인 네비게이션 렌더링
#--------------------------------------------------------
_pending_nav = st.session_state.pop("_pending_nav", None)

nav_options = [
    "우리집 가계부",
    "삶과 생계수단",
    "인생의 사계절",
    "우리집 재정곡선",
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

/* 여섯 번째 나침반은 탭 버튼이 아닌 독립 아이콘처럼 표시 */
div.st-key-main_nav_button_5 {
    flex: 0 0 42px !important;
    width: 42px !important;
    min-width: 42px !important;
}
div.st-key-main_nav_button_5 button,
div.st-key-main_nav_button_5 button:hover,
div.st-key-main_nav_button_5 button:focus,
div.st-key-main_nav_button_5 button:focus-visible,
div.st-key-main_nav_button_5 button:active,
div.st-key-main_nav_button_5 button[kind="primary"],
div.st-key-main_nav_button_5 button[kind="secondary"] {
    box-sizing: border-box !important;
    width: 42px !important;
    min-width: 42px !important;
    height: 46px !important;
    min-height: 46px !important;
    padding: 0 !important;
    border: 0 !important;
    border-radius: 0 !important;
    outline: 0 !important;
    background: transparent !important;
    background-color: transparent !important;
    box-shadow: none !important;
    color: #FFFFFF !important;
}
div.st-key-main_nav_button_5 button p {
    margin: 0 !important;
    font-size: 27px !important;
    line-height: 1 !important;
    font-weight: 400 !important;
}
div.st-key-main_nav_button_5 button:hover p {
    filter: brightness(1.25);
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
            _nav_label = "🧭" if _page == "통계" else _page
            st.button(
                _nav_label,
                key=f"main_nav_button_{_i}",
                type="primary" if _page == _active_nav else "secondary",
                on_click=_set_active_navigation,
                args=(_page,),
                help="통계 자료실" if _page == "통계" else None,
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
    _source_anchor_map = {
        "6050200-00": "stats-anchor-lifecycle-income",
        "6050300-00": "stats-anchor-marriage-housing",
        "6050400-01": "stats-anchor-retirement-expense",
        "6050500-01": "stats-anchor-loan-payment",
        "6050600-00": "stats-anchor-time-adjustment",
        "6050700-00": "stats-anchor-income-statistics",
        "6050800-00": "stats-anchor-marriage-cost",
        "6050900-00": "stats-anchor-household-events",
        "6051000-00": "stats-anchor-older-work",
        "6051100-00": "stats-anchor-retirement-milestones",
        "6051200-00": "stats-anchor-household-income-after-retirement",
        "6051300-00": "stats-anchor-historical-comparison",
        "6051400-00": "stats-anchor-spending-method",
        "6051500-00": "stats-anchor-housing-method",
        "6051600-00": "stats-anchor-income-curve-method",
        "6051700-00": "stats-anchor-nta-generational",
        "6051800-00": "stats-anchor-career-break",
        "6051900-00": "stats-anchor-retirement-income-stop",
        "6052000-00": "stats-anchor-event-own-marriage",
        "6052100-00": "stats-anchor-event-childcare",
        "6052200-00": "stats-anchor-event-housing",
        "6052300-00": "stats-anchor-event-college",
        "6052400-00": "stats-anchor-event-child-marriage",
    }
    if source_id in _source_anchor_map:
        st.session_state["_source_open_anchor"] = _source_anchor_map[source_id]
    st.session_state["_pending_nav"] = "통계"
    st.rerun()


@st.dialog("통계 비교선", width="large")
def _show_income_wage_stats_dialog():
    st.markdown(
        "**자료**  \n"
        "국가데이터처 「2024년 임금근로일자리 소득(보수) 결과」 "
        "(2026년 2월 발표)"
    )
    st.markdown(
        "**통계 기준**  \n"
        "2024년 12월 임금근로일자리에서 하루 이상 일한 근로자의 "
        "성별·연령대별 월평균 보수입니다. 원자료는 세전 금액입니다."
    )
    st.markdown(
        "**그래프 적용 방식**  \n"
        "월평균 보수에 90%를 적용해 실수령액을 근사하고, "
        "12개월을 곱해 연간 참고값으로 표시합니다. "
        "90%는 세금을 개인별로 계산한 값이 아닌 단순 추정 비율입니다."
    )
    st.markdown(
        "**해석할 때 참고하세요**  \n"
        "- 가구 합산 예상소득과 달리, 통계 비교선은 1인 기준입니다.\n"
        "- 70세 이상은 해당 연령집단의 평균이며, 실제 노동 종료 연령을 뜻하지 않습니다."
    )
    st.markdown(
        "[국가데이터처 원문 보고서](https://www.mods.go.kr/board.es?act=view&bid=11113&list_no=443648&mid=a10301010000) · "
        "[자료 및 산출 기준](https://github.com/ufreezone-ops/nachimpan/blob/dev/data/기준데이터/국가데이터처_2024_연령별_임금근로일자리_평균보수_README.md)"
    )


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
                        with st.container(key="loan-payment-field"):
                            with st.container(
                                horizontal=True,
                                vertical_alignment="bottom",
                                gap=None,
                                key="loan-payment-label-row",
                            ):
                                st.markdown(
                                    '<span class="loan-payment-label-text">대출 원리금 월상환액(원금+이자)</span>',
                                    unsafe_allow_html=True,
                                )
                                if st.button(
                                    "🧭",
                                    key="loan_payment_source_link",
                                    help="대출 원리금 산출 기준과 적용 방식 보기",
                                    type="tertiary",
                                ):
                                    _open_source_reference(
                                        "6050500-01",
                                        "우리집 가계부",
                                        "loan-payment-label-origin",
                                    )
                            st.markdown(
                                '<div id="loan-payment-label-origin"></div>',
                                unsafe_allow_html=True,
                            )
                            expense_loan = st.number_input(
                                "",
                                min_value=0,
                                value=loan_payment_input,
                                step=10,
                                placeholder="은행 납입 합계",
                                disabled=True,
                                key=loan_widget_key,
                                label_visibility="collapsed",
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
                            "6050400-01",
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
# 6.01.07 | 고급 모드 — 우리집 재무 현황
#--------------------------------------------------------
        st.markdown("### 우리집 재무 현황")
        st.markdown("<div id='selected-esbi'></div>", unsafe_allow_html=True)
        if st.session_state.pop("finance_saved_notice", False):
            st.success("입력 및 AI 점검이 완료된 재무 정보가 완벽히 반영되었습니다.")
            st.components.v1.html("<script>try { window.parent.document.getElementById('selected-esbi').scrollIntoView({behavior:'smooth',block:'center'}); } catch(e) {}</script>", height=0)

#--------------------------------------------------------
# 6.01.08 | 고급 모드 — 현재 재무 요약 메트릭
#--------------------------------------------------------
        s = current_financial_summary()
        st.markdown("### 현재 재무 요약")
        cols = st.columns(4)
        cols[0].metric("월 수입", money(s["regular_income"]))
        cols[1].metric("월 지출", money(s["expenses"]))
        bonus_help = f"연간 상여금 {money(s['annual_bonus'])} 및 연간 비정기 지출 {money(s['annual_other_expense'])} 반영"
        with cols[2]:
            with st.container(horizontal=True, vertical_alignment="center", gap="small"):
                st.markdown("연간 잉여자금")
                with st.popover("🧭", help="연간 잉여자금 계산에 반영된 항목 보기"):
                    st.write(bonus_help)
            st.metric("", money(s["annual_net_surplus"]), delta=f"월평균 {money(s['monthly_effective_surplus'])}")
        cols[3].metric("현재 파악된 금융자산", fmt_eok(s["net_worth"]))


#--------------------------------------------------------
# 6.01.09 | 고급 모드 — 우리 가정 생애 소득(예상) 차트
#--------------------------------------------------------
        st.markdown("### 우리 가정 생애 소득(예상)")

        # 그래프 설명은 그래프 아래의 통계 비교선 안내와 인앱 팝업으로 제공
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

        with st.container(
            horizontal=True,
            vertical_alignment="center",
            gap=None,
            key="income-wage-stats-note-row",
        ):
            st.markdown("보라색 점선은 통계 비교선입니다.")
            if st.button(
                "🧭",
                key="income_wage_stats_popup",
                help="통계 비교선의 자료와 산출 기준 보기",
                type="tertiary",
            ):
                _show_income_wage_stats_dialog()

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

<div style="font-size: 24px; font-weight: 850; color: #F8FAFC; line-height: 1.4; margin: 0 0 14px 0; padding: 0;">지혜로운 산책: 돌쇠와 똘똘이</div>
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
<b>나침반의 성찰:</b><br>
<b>누구의 선택을 두둔하는 얘기가 아닙니다.</b><br>
<b>두 경우 모두 우리가 원하는 결과가 아니기 때문입니다.</b><br>
돌쇠처럼 성실하게 당장의 가족 생계를 책임지면서도, 똘똘이가 구상한 파이프라인을 덧붙일 수 있는 길은 없을까요?
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
<div style="background: transparent; border: none; border-radius: 0; padding: 0; margin-bottom: 44px;">
<div style="font-size: 24px; font-weight: 850; color: #F8FAFC; line-height: 1.4; margin: 0 0 14px 0; padding: 0;">물통 &amp; 파이프라인</div>
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


        card_e = render_livelihood_quad("E", make_livelihood_icon("E_small_buckets.png", 88), "작은 물통 (E)", "시간과 돈을 1:1 교환", "일한 시간만큼 소득<br><span style='color:#F59E0B; font-weight:600;'>(NO 노동, NO 수입)</span>", is_right=False)

        card_s = render_livelihood_quad("S", make_livelihood_icon("S_large_bucket.png", 112), "큰 물통 (S)", "전문성과 큰 몸값", "시간당 소득이 큼", is_right=False)

        card_b = render_livelihood_quad("B", make_livelihood_icon("B_pipeline_build.png", 112), "파이프라인<br>구축 (B)", "시스템 소유", "스스로 굴러가는 비즈니스<br><span style='color:#38BDF8; font-weight:600;'>(나 대신 시스템이 일함)</span>", is_right=True)

        card_i = render_livelihood_quad("I", make_livelihood_icon("I_pipeline_connect.png", 112), "파이프라인<br>접속 (I)", "플랫폼·자본 접속", "이미 구축된 플랫폼에 접속<br><span style='color:#38BDF8; font-weight:600;'>(나 대신 시스템이 일함)</span>", is_right=True)

        st.markdown(f"""
<div style="margin: 6px 0 50px 0;">
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
<div style="margin: 50px 0 26px 0; padding: 4px 2px;">
<div style="font-size: 24px; font-weight: 850; color: #F8FAFC; margin-bottom: 6px;">더 생각해보기</div>
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

            st.markdown('<div id="retirement-milestones-origin" style="scroll-margin-top: 150px;"></div>', unsafe_allow_html=True)
            with st.container(border=True, key="retirement-milestones-panel"):
                with st.container(horizontal=True, vertical_alignment="center", gap=None):
                    st.markdown("**10. 통계로 본 대한민국 3대 은퇴 분기점**")
                    if st.button("🧭", key="source_retirement_milestones", help="대한민국 3대 은퇴 분기점 통계 리포트 보기", type="tertiary"):
                        _open_source_reference("6051100-00", "삶과 생계수단", "retirement-milestones-origin")
                with st.container(horizontal=True, vertical_alignment="center", gap=None):
                    st.markdown(
                        '**"근로소득의 정점 및 본업 졸업" 관점이라면**  \n'
                        '➔ **55~60세 전후** <span style="font-size: 0.9em; color: #94A3B8;">(주된 일자리 퇴직 당시 평균 53.0세)</span>',
                        unsafe_allow_html=True,
                    )
                with st.container(horizontal=True, vertical_alignment="center", gap=None):
                    st.markdown(
                        '**"국가 통계적 흑자·적자 수지 균형" 관점이라면**  \n'
                        '➔ **61세** <span style="font-size: 0.9em; color: #94A3B8;">(국민이전계정 NTA 적자 재전환 연령)</span>',
                        unsafe_allow_html=True,
                    )
                with st.container(horizontal=True, vertical_alignment="center", gap=None):
                    st.markdown(
                        '**"노동시장에서 실질적으로 이탈하는 시점" 관점이라면**  \n'
                        '➔ **남성 67.4세 · 여성 69.6세** <span style="font-size: 0.9em; color: #94A3B8;">(OECD 2024년 추정치)</span>',
                        unsafe_allow_html=True,
                    )

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
        official_net_balance = [i - e for e, i in zip(official_expense, official_income)]

        # 적자(양수)와 흑자(음수) 면적을 0선에서 분리하고,
        # 부호가 바뀌는 지점은 두 곡선의 선형 교차점으로 보정합니다.
        def _signed_area_segments(values, positive=True):
            x_out, y_out = [], []
            for idx in range(len(official_ages) - 1):
                x0, x1 = official_ages[idx], official_ages[idx + 1]
                y0, y1 = values[idx], values[idx + 1]
                segment = None

                if positive:
                    if y0 >= 0 and y1 >= 0:
                        segment = ((x0, y0), (x1, y1))
                    elif y0 >= 0 and y1 < 0:
                        cross_x = x0 + (x1 - x0) * y0 / (y0 - y1)
                        segment = ((x0, y0), (cross_x, 0))
                    elif y0 < 0 and y1 >= 0:
                        cross_x = x0 + (x1 - x0) * (-y0) / (y1 - y0)
                        segment = ((cross_x, 0), (x1, y1))
                else:
                    if y0 <= 0 and y1 <= 0:
                        segment = ((x0, y0), (x1, y1))
                    elif y0 <= 0 and y1 > 0:
                        cross_x = x0 + (x1 - x0) * (-y0) / (y1 - y0)
                        segment = ((x0, y0), (cross_x, 0))
                    elif y0 > 0 and y1 <= 0:
                        cross_x = x0 + (x1 - x0) * y0 / (y0 - y1)
                        segment = ((cross_x, 0), (x1, y1))

                if segment is None:
                    continue
                (sx0, sy0), (sx1, sy1) = segment
                if x_out and x_out[-1] is not None and abs(x_out[-1] - sx0) < 1e-9 and y_out[-1] == sy0:
                    x_out.append(sx1)
                    y_out.append(sy1)
                else:
                    if x_out:
                        x_out.append(None)
                        y_out.append(None)
                    x_out.extend([sx0, sx1])
                    y_out.extend([sy0, sy1])
            return x_out, y_out

        surplus_x, surplus_y = _signed_area_segments(official_net_balance, positive=True)
        deficit_x, deficit_y = _signed_area_segments(official_net_balance, positive=False)

        fig_official_nta.add_trace(go.Scatter(
            x=deficit_x, y=deficit_y, mode="lines",
            line=dict(color="rgba(185, 85, 65, 0)", width=0),
            fill="tozeroy", fillcolor="rgba(185, 85, 65, 0.34)",
            name="생애주기 적자", legendrank=3,
            hoverinfo="skip", connectgaps=False,
        ))
        fig_official_nta.add_trace(go.Scatter(
            x=surplus_x, y=surplus_y, mode="lines",
            line=dict(color="rgba(34, 139, 94, 0)", width=0),
            fill="tozeroy", fillcolor="rgba(34, 139, 94, 0.34)",
            name="생애주기 흑자", legendrank=4,
            hoverinfo="skip", connectgaps=False,
        ))
        fig_official_nta.add_trace(go.Scatter(
            x=official_ages, y=official_expense, mode="lines",
            line=dict(color="#C65D4B", width=3, dash="dash"),
            name="지출(소비)", legendrank=2,
            hovertemplate="나이: %{x}세<br>지출(소비): <b>%{y:.1f}조 원</b><extra></extra>"
        ))
        fig_official_nta.add_trace(go.Scatter(
            x=official_ages, y=official_income, mode="lines",
            line=dict(color="#22A06B", width=3.5),
            name="소득(노동소득)", legendrank=1,
            hovertemplate="나이: %{x}세<br>소득(노동소득): <b>%{y:.1f}조 원</b><extra></extra>"
        ))
        fig_official_nta.add_hline(y=0, line_dash="solid", line_color="#475569", line_width=1.5)
        fig_official_nta.add_vline(x=17, line_dash="dash", line_color="#94A3B8", line_width=1.5)
        fig_official_nta.add_vline(x=65, line_dash="dash", line_color="#94A3B8", line_width=1.5)
        fig_official_nta.add_annotation(x=8, y=50, text="유년층", showarrow=False, font=dict(size=12, color="#E2E8F0"), bgcolor="rgba(30, 41, 59, 0.8)", bordercolor="#475569")
        fig_official_nta.add_annotation(x=41, y=50, text="노동연령층", showarrow=False, font=dict(size=12, color="#E2E8F0"), bgcolor="rgba(30, 41, 59, 0.8)", bordercolor="#475569")
        fig_official_nta.add_annotation(x=75, y=50, text="노년층", showarrow=False, font=dict(size=12, color="#E2E8F0"), bgcolor="rgba(30, 41, 59, 0.8)", bordercolor="#475569")
        fig_official_nta.add_annotation(x=12, y=-9.5, text="적자", showarrow=False, font=dict(size=13, color="#D98A78", weight="bold"))
        fig_official_nta.add_annotation(x=45, y=7.8, text="흑자", showarrow=False, font=dict(size=13, color="#62C795", weight="bold"))
        fig_official_nta.add_annotation(x=73, y=-4.5, text="적자", showarrow=False, font=dict(size=13, color="#D98A78", weight="bold"))

        fig_official_nta.update_layout(
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
                font=dict(size=12, color="#F1F5F9"),
                traceorder="normal"
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

        if cur_age <= 27: cur_season, s_icon, s_color, s_desc = "봄 (준비기)", "🌱", "#4ADE80", "배우고 성장하며, 부모와 사회의 지원 속에서 삶의 기반을 준비하는 시기"
        elif 28 <= cur_age <= 49: cur_season, s_icon, s_color, s_desc = "여름 (성장기)", "☀️", "#F59E0B", "경제활동을 통해 스스로의 생계를 책임지고, 가정을 일구며 경제적 기반을 만드는 시기"
        elif 50 <= cur_age <= 69: cur_season, s_icon, s_color, s_desc = "가을 (결실기)", "🍂", "#FB923C", "자녀의 독립과 노후를 준비하고, 노동의 결실을 삶의 여유로 바꾸는 계절"
        else: cur_season, s_icon, s_color, s_desc = "겨울 (음미기)", "❄️", "#38BDF8", "생계를 위한 노동의 비중을 줄이고, 살아온 삶의 열매를 누리는 계절"

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
                st.session_state["_pending_nav"] = "우리집 재정곡선"
                st.rerun()

    else:
        st.caption("내 인생의 사계절과 우리가족  \n대한민국 통계자료로 비춰봅니다")

    #--------------------------------------------------------
# 6.03.03 | 고급 모드 — 2. 세대 계승 생애주기 재정곡선
#--------------------------------------------------------
        st.markdown("### 세대 계승 생애주기 재정곡선")

        fig_official_nta = build_official_nta_chart()
        st.plotly_chart(fig_official_nta, use_container_width=True, config={"displayModeBar": False, "scrollZoom": False, "doubleClick": False, "showAxisDragHandles": False})

        st.caption(
            "※ 국가데이터처 「2024년 국민이전계정」(2026. 9. 17. 발표)"
        )

        if st.button(
            "🧭 16. 세대 계승 생애주기 재정곡선 리포트 보기",
            key="open_nta_generational_report",
            use_container_width=True,
        ):
            _open_source_reference(
                "6051700-00",
                "인생의 사계절",
                "source-anchor-nta-generational",
            )

        # [출처 ID: 6051700-00]
        st.markdown(
            '<div id="source-anchor-nta-generational"></div>',
            unsafe_allow_html=True
        )
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("생애 흑자 진입", "28세")
        col_m2.metric("최대 흑자 정점", "45세", "연 1,932만 원")
        col_m3.metric("생애 적자 재진입", "61세")

        
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

#--------------------------------------------------------
# 6.03.04 | 고급 모드 — 3. 인생의 사계절 카드
#--------------------------------------------------------
        st.markdown("### 인생의 사계절")
        if cur_age <= 27: cur_season = "spring"
        elif 28 <= cur_age <= 49: cur_season = "summer"
        elif 50 <= cur_age <= 69: cur_season = "autumn"
        else: cur_season = "winter"

        def get_season_card_ui(season_key, icon, title, age_range, desc):
            is_current = (cur_season == season_key)
            card_border = "border: 2px solid #EA580C; background: rgba(234, 88, 12, 0.14);" if is_current else "border: 1px solid #334155; background: rgba(21, 30, 47, 0.7);"
            badge_html = "<div style='min-height:22px; margin-bottom:4px;'><span style='background:#EA580C; color:#FFFFFF; font-size:11.5px; font-weight:800; padding:2px 7px; border-radius:4px;'>지금 나의 계절</span></div>" if is_current else "<div style='min-height:22px; margin-bottom:4px;'></div>"
            return f'<div class="soft-card" style="text-align:center; min-height:205px; {card_border} padding:14px 10px; margin:0;">{badge_html}<div style="font-size:28px;">{icon}</div><div style="font-size:16.5px; font-weight:800; color:#F8FAFC; margin:4px 0;">{title}</div><div style="font-size:13px; color:#94A3B8;">{age_range}</div><div style="font-size:13px; color:#CBD5E1; margin-top:8px; line-height:1.4;">{desc}</div></div>'

        card_spring = get_season_card_ui("spring", "🌱", "봄 (준비기)", "0세 ~ 27세", "배우고 성장하며, 부모와 사회의 지원 속에서 삶의 기반을 준비하는 시기")
        card_summer = get_season_card_ui("summer", "☀️", "여름 (성장기)", "28세 ~ 49세", "경제활동을 통해 스스로의 생계를 책임지고, 가정을 일구며 경제적 기반을 만드는 시기")
        card_autumn = get_season_card_ui("autumn", "🍂", "가을 (결실기)", "50세 ~ 69세", "자녀의 독립과 노후를 준비하고, 노동의 결실을 삶의 여유로 바꾸는 계절")
        card_winter = get_season_card_ui("winter", "❄️", "겨울 (음미기)", "70세 이후", "생계를 위한 노동의 비중을 줄이고, 살아온 삶의 열매를 누리는 계절")

        s_col1, s_col2, s_col3, s_col4 = st.columns(4)
        with s_col1: st.markdown(card_spring, unsafe_allow_html=True)
        with s_col2: st.markdown(card_summer, unsafe_allow_html=True)
        with s_col3: st.markdown(card_autumn, unsafe_allow_html=True)
        with s_col4: st.markdown(card_winter, unsafe_allow_html=True)

        st.markdown(f"""
<div style="background: rgba(30, 41, 59, 0.6); border: 1px solid #334155; border-radius: 12px; padding: 18px 20px; margin: 16px 0 24px 0;">
<div style="font-size: 15px; color: #F8FAFC; line-height: 1.6; word-break: keep-all;">
💡 <b>산책로의 질문</b><br>은퇴 후 기대수명까지 약 <b>{winter_years}년</b>이 남아 있습니다. (국가데이터처 {user_gender.split()[1]} 기대수명 {life_expectancy}세 기준)<br>
<span style="color: #94A3B8;">이 긴 시간 동안 매달 무거운 물통을 지고 눈길을 걸을 것인가, 방 안에서 따뜻하게 흘러나오는 파이프라인을 맞이할 것인가는 <b>운명이 아니라 선택입니다.</span>
</div></div>
""", unsafe_allow_html=True)

        _, next_col = st.columns([5, 1])
        with next_col:
            if st.button("다음 →", key="seasons_next", use_container_width=True, type="primary"):
                st.session_state["_pending_nav"] = "우리집 재정곡선"
                st.rerun()


#########################################################
# 6.04 | Tab 4 — 우리집 재정곡선
#########################################################
elif selected_page == "우리집 재정곡선":
    if st.session_state.pop("_scroll_to_top_once", False):
        st.components.v1.html("<script>try { window.parent.scrollTo({top: 0, behavior: 'instant'}); } catch(e) {}</script>", height=0)

    is_adv = st.session_state.get("advanced_mode", False)
    cur_age = int(st.session_state.get("person_age", 35) or 35)
    user_gender = st.session_state.get("gender", "🙋‍♂️ 남성")
    is_female = ("여성" in user_gender)
    life_expectancy = 87 if is_female else 81
    retire_val = st.session_state.get("retirement_age")
    retire_age = int(retire_val) if retire_val is not None else 60
    retire_age = max(cur_age, min(retire_age, 90))
    years_left = max(0, retire_age - cur_age)
    winter_years = max(0, life_expectancy - retire_age)
    winter_months = winter_years * 12

    if not is_adv:
        st.caption("우리집 재정곡선과 가족의 미래를 살펴보려면 고급 모드로 전환해 주세요.")
    else:
        st.markdown("## 우리집 재정곡선")
        st.caption("우리 가족의 현재 조건과 생애 이벤트를 바탕으로 미래의 소득과 지출을 살펴봅니다.")

#--------------------------------------------------------
# 6.04.01 | 고급 모드 — 1. 가족 구성원 나이 및 주택가격 기준 통계
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

        with st.container(key="family-retirement-expander"):
            with st.expander("가족 구성과 계획", expanded=False):
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

                with st.container(gap="small"):
                    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
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

                    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
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
                    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
                    st.markdown("#### 주택가격 산정 기준")
                    is_representative_case = st.session_state.get("_representative_case_id") in {
                        "case_32_female", "case_45_female"
                    }
                    housing_region_options = (
                        ["부산"] if is_representative_case
                        else ["지역 선택"] + list(HOUSING_PRICE_DATA.keys())
                    )
                    default_future_region = st.session_state.get("residence_region", "지역 선택")
                    if default_future_region not in HOUSING_PRICE_DATA:
                        default_future_region = "지역 선택"
                    prev_housing_region = st.session_state.get(
                        "housing_region",
                        "부산" if is_representative_case else default_future_region
                    )
                    if prev_housing_region not in housing_region_options:
                        prev_housing_region = "부산" if is_representative_case else "지역 선택"

                    housing_region = st.selectbox(
                        "주택구입 예정지역",
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
# 6.04.02 | 고급 모드 — 은퇴 시점 가족 미래 나이 카드
#--------------------------------------------------------
        people = [("나", cur_age)]
        if getv("spouse_age", 0) > 0: people.append(("배우자", int(getv("spouse_age"))))
        if getv("child_age", 0) > 0: people.append(("첫째", int(getv("child_age"))))
        if getv("child_age2", 0) > 0: people.append(("둘째", int(getv("child_age2"))))
        if getv("child_age3", 0) > 0: people.append(("셋째", int(getv("child_age3"))))
        if getv("child_age4", 0) > 0: people.append(("넷째", int(getv("child_age4"))))
        if getv("mother_age", 0) > 0: people.append(("어머니", int(getv("mother_age"))))
        if getv("father_age", 0) > 0: people.append(("아버지", int(getv("father_age"))))

        st.markdown("### 내 은퇴 시점의 우리 가족")

        # 한 행씩 두 사람을 배치해 모바일에서도 가족 순서를 유지한다.
        for row_start in range(0, len(people), 2):
            f_cols = st.columns(2)
            for col_idx, (name, current) in enumerate(people[row_start:row_start + 2]):
                future = current + years_left
                with f_cols[col_idx]:
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
<div style="font-size: 15px; font-weight: 400; color: #F8FAFC; line-height: 1.6;">
<span style="font-size: 17px; font-weight: 750;"><b>"첫째가 대학에 입학하는 20세가 되면, 나는 {college_my_age}세가 되는구나!"</b></span><br>
: 국가데이터처 통계상 소득 정점(45세)은 지나가면서, 자녀 학자금과 독립 비용으로 인생에서 가장 큰 지출이 집중되는 시기가 됩니다.
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
# 6.04.03 | 고급 모드 — 2. 우리 가정 생애주기 재정곡선
#--------------------------------------------------------
        
#############    6.04.03.01 | 헤더 타이틀 및 기준 지역 안내 카드
        from plotly.subplots import make_subplots

        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
        with st.container(horizontal=True, vertical_alignment="bottom", gap=None, key="retirement-title-row"):
            st.markdown("### 우리 가정 생애주기 재정곡선")
            if st.button(
                "🧭",
                key="source_retirement_expense",
                help="11. 우리 가정 생애주기 소득곡선의 통계적 보정 방식 보기",
                type="tertiary",
            ):
                _open_source_reference(
                    "6051200-00",
                    "우리집 재정곡선",
                    "statistical-household-income-origin",
                )
        st.markdown(
            '<div id="statistical-household-income-origin"></div>',
            unsafe_allow_html=True,
        )

        # 기존 주거 유지·계획 확정이면 현재 주거지역을 사용하고,
        # 향후 주택구입 정보를 입력한 경우에는 예정지역을 사용한다.
        current_region = st.session_state.get("residence_region", "부산")
        if current_region not in HOUSING_PRICE_DATA:
            current_region = "부산"
        current_housing_plan = st.session_state.get("housing_plan", "미정")
        if current_housing_plan in ["현재 주거 유지", "주거 계획 확정"]:
            selected_region = current_region
        else:
            selected_region = st.session_state.get("housing_region") or current_region
            if selected_region not in HOUSING_PRICE_DATA:
                selected_region = current_region

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

#############    6.04.03.02 | 기본 재무·연금 파라미터 수집 및 정제
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

#############    6.04.03.03 | 가족 타임라인 결정 엔진
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

#############    6.04.03.04 | 배우자 프로필 및 직업군 기준곡선 매핑
        has_future_or_current_spouse = (m_plan == "결혼함") or (marriage_start is not None)
        if spouse_job_raw and spouse_job_raw != "해당 없음":
            spouse_job = spouse_job_raw
        else:
            spouse_job = "직장인" if self_job == "전업주부" else self_job

        spouse_age_input = int(getv("spouse_age", 0) or 0)
        spouse_age_diff = (spouse_age_input - cur_age) if spouse_age_input > 0 else 0
        retire_age = int(st.session_state.get("retirement_age", 60) or 60)

#############    6.04.03.05 | 5대 생애 이벤트 총비용 및 기간 산출
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

        # 6) 사건별 총비용 산출 (현재 주거지역 또는 주택구입 예정지역 기준)
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
        # - 과거·미래 모두 결혼 관련 비용을 2년에 걸쳐 분산 반영
        # - 과거 결혼은 신혼집 외 총비용 6,298만 원에서 혼수 중복분 2,615만 원을 차감
        #   (신혼집 부담분은 과거 실제 부담액을 확인할 수 없어 이번 계산에서는 제외)
        if marriage_start is not None and 20 <= marriage_start <= 85 and m_plan != "계획 없음":
            is_past_marriage = (m_plan == "결혼함")
            past_marriage_cost_man = 6298.0
            applied_marriage_cost_man = past_marriage_cost_man if is_past_marriage else marriage_cost_man
            applied_marriage_deduction_man = min(marriage_overlap_deduction_man, applied_marriage_cost_man)
            event_costs.append({
                "name": "나의 결혼",
                "start": marriage_start,
                "end": marriage_start + 2,
                "center": marriage_start,
                "total": applied_marriage_cost_man - applied_marriage_deduction_man,
                "display_total": applied_marriage_cost_man,
                "deducted_total": applied_marriage_deduction_man,
                "duration": 2,
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
                "end": start + 2,
                "total": child_wedding_cost_man - child_wedding_overlap_deduction_man,
                "display_total": child_wedding_cost_man,
                "deducted_total": child_wedding_overlap_deduction_man,
                "duration": 2,
                "color": "#F43F5E",
                "is_past": False
            })

        # 이벤트의 total은 중복 차감 후 가구 지출곡선에 추가할 금액.
        # display_total은 차트 이벤트 원의 크기를 결정하는 차감 전 총비용.
        # 총비용과 차감액은 아래 시뮬레이션에서 동일한 연령별 CPI 상대계수를 적용받음.
        event_expense_by_age = {a: 0.0 for a in range(0, life_expectancy)}
        for event in event_costs:
            if event["total"] > 0:
                annual_addition = event["total"] / float(event["duration"])
                for a in range(max(20, event["start"]), min(life_expectancy, event["end"])):
                    event_expense_by_age[a] += annual_addition

#############    6.04.03.06 | 기준곡선 보간(Interpolation) 및 감쇄 엔진
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

#############    6.04.03.06.01 | MDIS 가구 지출 통계 매핑 및 현재 지출 보정
        def household_age_band(age):
            if age >= 80:
                return "80세 이상"
            lower = (int(age) // 5) * 5
            return f"{lower}~{lower + 4}세"

        def household_size_at_age(age):
            # 가구원 수는 은퇴 시점이 아니라 실제 가족 형성·자녀 독립 시점을 따라간다.
            size = 1
            if marriage_start is not None and age >= marriage_start:
                size += 1

            # 자녀는 출생 이후 가구원으로 포함하고, 결혼 이벤트가 시작되는 시점부터
            # 독립한 것으로 간주한다. 이미 만 30세 이상인 자녀는 결혼 여부를 알 수 없으므로
            # 별도 정보 없이 자동으로 가구에서 제외하지 않는다.
            for child_age_value in existing_child_ages:
                birth_age = cur_age - child_age_value
                child_wedding_age = birth_age + 30 if child_age_value < 30 else None
                if age >= birth_age and (
                    child_wedding_age is None or age < child_wedding_age
                ):
                    size += 1

            if future_birth_age is not None and age >= future_birth_age:
                future_child_wedding_age = future_birth_age + 30
                if age < future_child_wedding_age:
                    size += 1

            return min(size, 5)

        def lookup_household_expense_band(age_band, household_size):
            """특정 5세 연령 구간의 가중중위값을 조회하고 기존 결측 셀 대체 규칙을 적용한다."""
            if household_expense_stats.empty:
                return None

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
                    # 같은 가구원 수 자료가 있는 가장 가까운 연령 구간을 참고
                    same_size = household_expense_stats[
                        (household_expense_stats["가구원수"] == size_label)
                        & (household_expense_stats[amount_col].notna())
                    ].copy()
                    if same_size.empty:
                        return None
                    same_size["_age_distance"] = same_size["가구주_연령대"].map(
                        lambda value: abs(
                            (80 if value == "80세 이상" else int(value.split("~")[0]) + 2)
                            - (80 if age_band == "80세 이상" else int(age_band.split("~")[0]) + 2)
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

        def lookup_household_expense(age, household_size):
            """5세 단위 MDIS 기준값을 인접 연령구간 사이에서 선형 보간한다."""
            if household_expense_stats.empty:
                return None

            # 각 통계 구간의 대표 연령을 보간 기준점으로 사용한다.
            age_points = []
            for band in household_expense_stats["가구주_연령대"].dropna().unique():
                band = str(band)
                if band == "80세 이상":
                    midpoint = 80.0
                elif "~" in band:
                    lower_text, upper_text = band.replace("세", "").split("~", 1)
                    midpoint = (float(lower_text) + float(upper_text)) / 2.0
                else:
                    continue
                # 시뮬레이션은 20세부터 시작하므로 17~19세 소표본 구간은 보간 기준점에서 제외한다.
                if midpoint < 20:
                    continue
                age_points.append((midpoint, band))

            age_points = sorted(set(age_points), key=lambda item: item[0])
            if not age_points:
                return None

            target_age = float(age)
            if target_age <= age_points[0][0]:
                return lookup_household_expense_band(age_points[0][1], household_size)
            if target_age >= age_points[-1][0]:
                # 80세 이상은 마지막 공개 통계 구간이므로,
                # 75~79세와 80세 이상 기준값 사이의 감소 기울기를 이후에도 연장한다.
                last_point = age_points[-1]
                previous_point = age_points[-2] if len(age_points) >= 2 else None
                last_data = lookup_household_expense_band(last_point[1], household_size)

                if previous_point is None or last_data is None:
                    return last_data

                previous_data = lookup_household_expense_band(
                    previous_point[1], household_size
                )
                if previous_data is None:
                    return last_data

                age_span = last_point[0] - previous_point[0]
                if age_span <= 0:
                    return last_data

                monthly_slope = (
                    last_data["monthly"] - previous_data["monthly"]
                ) / age_span
                extended_monthly = max(
                    0.0,
                    last_data["monthly"]
                    + monthly_slope * (target_age - last_point[0])
                )

                return {
                    "monthly": extended_monthly,
                    "sample_n": min(
                        last_data["sample_n"], previous_data["sample_n"]
                    ),
                    "age_band": f'{previous_point[1]} ↔ {last_point[1]} 감소추세 연장',
                    "household_size": str(household_size),
                    "fallback": last_data["fallback"] or previous_data["fallback"],
                    "small_sample": last_data["small_sample"] or previous_data["small_sample"],
                }

            lower_point = age_points[0]
            upper_point = age_points[-1]
            for idx in range(len(age_points) - 1):
                if age_points[idx][0] <= target_age <= age_points[idx + 1][0]:
                    lower_point = age_points[idx]
                    upper_point = age_points[idx + 1]
                    break

            lower_data = lookup_household_expense_band(lower_point[1], household_size)
            upper_data = lookup_household_expense_band(upper_point[1], household_size)

            if lower_data is None and upper_data is None:
                return None
            if lower_data is None:
                return upper_data
            if upper_data is None:
                return lower_data

            ratio = (
                (target_age - lower_point[0])
                / (upper_point[0] - lower_point[0])
            )
            monthly = (
                lower_data["monthly"]
                + (upper_data["monthly"] - lower_data["monthly"]) * ratio
            )

            return {
                "monthly": monthly,
                "sample_n": min(lower_data["sample_n"], upper_data["sample_n"]),
                "age_band": f'{lower_point[1]} ↔ {upper_point[1]} 보간',
                "household_size": str(household_size),
                "fallback": lower_data["fallback"] or upper_data["fallback"],
                "small_sample": lower_data["small_sample"] or upper_data["small_sample"],
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

        #############    6.04.03.07 | 연령별 소득·지출 흐름 시뮬레이션 루프
        ages_sim = list(range(20, life_expectancy))
        my_income_curve = []
        household_income_curve = []
        # 은퇴 후에도 기존 연령별 근로·사업소득 기준곡선을 연장한 비교용 가구소득
        statistical_adjusted_income_curve = []
        household_expense_curve = []
        mortgage_principal_curve = []
        mortgage_interest_curve = []
        mortgage_balance_curve = []

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

            # --- [C-1. 은퇴 이후 통계적 보정 소득 비교선] ---
            # 기존 가구소득 실선은 유지하고, 은퇴 이후에만 직업군별 연령 기준곡선을 연장한다.
            if a >= retire_age:
                stat_self_inc = (
                    extended_base_income(a, self_base) * self_scale * 12.0
                    + normalized_annual_bonus
                ) if self_base is not None else 0.0

                if is_female and childcare_windows:
                    stat_in_childcare = False
                    stat_completed_childcare = False
                    for c_start, c_end in childcare_windows:
                        if c_start <= a < c_end:
                            stat_in_childcare = True
                            years_in = a - c_start
                            stat_self_inc *= 0.35 if years_in <= 1 else 0.50
                            break
                        elif a >= c_end:
                            stat_completed_childcare = True
                    if not stat_in_childcare and stat_completed_childcare:
                        stat_self_inc *= 0.80

                stat_self_inc *= wage_year_factor
                stat_spouse_inc = 0.0
                if (
                    has_future_or_current_spouse
                    and marriage_start is not None
                    and a >= marriage_start
                    and spouse_base is not None
                ):
                    stat_spouse_inc = (
                        extended_base_income(sp_a, spouse_base)
                        * spouse_scale * 12.0 * wage_year_factor
                    )

                stat_total_hh_inc = stat_self_inc + stat_spouse_inc + annual_other_income

                statistical_adjusted_income_curve.append(stat_total_hh_inc)
            else:
                statistical_adjusted_income_curve.append(None)

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
            # 대출 원금은 소비지출 통계에는 없지만 실제 가계 현금 유출이므로 가구지출에 포함한다.
            # 이자는 MDIS 비소비지출에 포함된 것으로 보고 별도 가산하지 않는다.
            total_hh_exp = base_exp + event_expense + annual_mortgage_principal
            household_expense_curve.append(total_hh_exp)

        # 별도 가구처분가능소득 자료는 사용하지 않는다.
        # 기존 직업군별 연령 기준곡선을 은퇴 이후까지 연장한 비교 시나리오를 사용한다.

#############    6.04.03.08 | 가구 순수지 분리 및 Y축 자동 스케일링
        # 대출 원금상환액은 가구지출에 이미 포함했으므로 여기서 중복 차감하지 않는다.
        net_flow = [
            i - e
            for i, e in zip(household_income_curve, household_expense_curve)
        ]
        statistical_adjusted_net_flow = [
            income - expense if income is not None else None
            for income, expense in zip(
                statistical_adjusted_income_curve,
                household_expense_curve,
            )
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

        max_stat_adjusted_income_val = max(
            (value for value in statistical_adjusted_income_curve if value is not None),
            default=0.0,
        )
        y_max = max(max_income_val, max_exp_val, max_stat_adjusted_income_val)
        y_top = max(10000.0, y_max * 1.15)  # 최소 10,000(1억) 확보
        alt_level_2 = y_top * 0.35
        alt_level_1 = y_top * 0.12

        fig_my_nta = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.26,
            row_heights=[0.55, 0.45]
        )

#############    6.04.03.09 | 이벤트 버블 마커 Trace 생성
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

        # [Row 1] 기존 우리 가정 가구소득 곡선은 전 연령 유지하고, 통계 비교선을 별도 추가
        fig_my_nta.add_trace(go.Scatter(
            x=ages_sim,
            y=household_income_curve,
            mode="lines",
            line=dict(color="#10B981", width=3.4, shape="spline", smoothing=0.8),
            name="가구소득",
            hovertemplate="나이: %{x}세<br>우리 가정 예상 연간소득(연금 포함): <b>%{y:,.0f}만 원</b><extra></extra>"
        ), row=1, col=1)

        # 은퇴 이후 통계적 기준곡선을 연장한 가구소득(연금 포함)
        fig_my_nta.add_trace(go.Scatter(
            x=ages_sim,
            y=statistical_adjusted_income_curve,
            mode="lines",
            line=dict(color="#22C55E", width=3.0, dash="dot", shape="spline", smoothing=0.8),
            name="가구소득(통계보정)",
            connectgaps=False,
            hovertemplate=(
                "나이: %{x}세<br>"
                "통계적 보정 가구소득(연금 제외): "
                "<b>%{y:,.0f}만 원</b><extra></extra>"
            ),
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
            x=cur_age, y=0.508,
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
            x=retire_age, y=0.508,
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
            name="순 현금흐름",
            legend="legend2",
            hovertemplate="나이: %{x}세<br>순 현금흐름: <b>%{y:,.0f}만 원</b><extra></extra>"
        ), row=2, col=1)

        fig_my_nta.add_trace(go.Scatter(
            x=ages_sim,
            y=statistical_adjusted_net_flow,
            mode="lines",
            line=dict(color="#22C55E", width=2.8, dash="dot", shape="spline", smoothing=0.8),
            name="통계적 보정",
            legend="legend2",
            connectgaps=False,
            hovertemplate=(
                "나이: %{x}세<br>"
                "통계적 보정 순현금흐름: <b>%{y:,.0f}만 원</b><extra></extra>"
            ),
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

#############    6.04.03.10 | 2단 서브플롯 조립 및 Plotly 렌더링
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
            legend2=dict(
                orientation="h",
                yanchor="bottom",
                y=0.35,
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
        fig_my_nta.update_xaxes(showticklabels=True, row=1, col=1)
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

        # 생애주기 누적 총액은 그래프 해석의 혼선을 줄이기 위해 표시하지 않는다.

        st.markdown('<div id="household-major-events" style="scroll-margin-top: 120px;"></div>', unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("**가구소득 주요 이벤트**")
            st.caption("출산·육아에 따른 경력 변화와 은퇴 이후의 근로소득 단절을 살펴봅니다.")
            _income_event_reports = [
                ("17. 여성의 출산·육아와 경력단절", "6051800-00"),
                ("18. 은퇴와 수입 단절", "6051900-00"),
            ]
            for _event_title, _event_id in _income_event_reports:
                if st.button(
                    f"🧭 {_event_title}",
                    key=f"household_income_event_{_event_id}",
                    use_container_width=True,
                ):
                    _open_source_reference(
                        _event_id,
                        "우리집 재정곡선",
                        "household-major-events",
                    )

            st.markdown("---")
            st.markdown("**가구지출 주요 이벤트**")
            st.caption("재정곡선에 표시되는 빅5 생애사건과 각각의 비용 산출 근거입니다.")
            _expense_event_reports = [
                ("19. 나의 결혼", "6052000-00"),
                ("20. 출산과 육아", "6052100-00"),
                ("21. 주택구입", "6052200-00"),
                ("22. 자녀 대학", "6052300-00"),
                ("23. 자녀 결혼", "6052400-00"),
            ]
            for _event_title, _event_id in _expense_event_reports:
                if st.button(
                    f"🧭 {_event_title}",
                    key=f"household_expense_event_{_event_id}",
                    use_container_width=True,
                ):
                    _open_source_reference(
                        _event_id,
                        "우리집 재정곡선",
                        "household-major-events",
                    )

        st.markdown('<div id="chart-stat-report-links" style="scroll-margin-top: 120px;"></div>', unsafe_allow_html=True)
        st.markdown("**이 재정곡선의 통계 자료실**")
        st.caption("아래 제목을 누르면 통계탭의 해당 보고서로 이동합니다.")
        _graph_stat_reports = [
            ("1. 소득과 소비의 생애주기", "6050200-00"),
            ("2. 결혼과 주거", "6050300-00"),
            ("3. 노후와 은퇴", "6050400-01"),
            ("5. 동시성과 통시성", "6050600-00"),
            ("6. 소득 통계", "6050700-00"),
            ("7. 결혼비용 통계", "6050800-00"),
            ("8. 빅5 우리집 이벤트", "6050900-00"),
            ("9. 고령층 근로연령 통계", "6051000-00"),
            ("10. 통계로 본 대한민국 3대 은퇴 분기점", "6051100-00"),
            ("11. 우리 가정 생애주기 소득곡선의 통계적 보정", "6051200-00"),
        ]
        st.markdown("""
<style>
/* 통계 자료실 링크는 단일 세로 목록으로 표시해 PC·모바일 순서를 동일하게 유지한다. */
div[class*="st-key-graph_stat_report_"] [data-testid="stButton"] button,
div[class*="st-key-case_stat_detail_"] [data-testid="stButton"] button,
div[class*="st-key-case_housing_stat_"] [data-testid="stButton"] button,
div[class*="st-key-household_income_event_"] [data-testid="stButton"] button,
div[class*="st-key-household_expense_event_"] [data-testid="stButton"] button,
div[class*="st-key-open_nta_generational_report"] [data-testid="stButton"] button {
    width: 100% !important;
    justify-content: flex-start !important;
    text-align: left !important;
}
div[class*="st-key-graph_stat_report_"] [data-testid="stButton"] button > div,
div[class*="st-key-case_stat_detail_"] [data-testid="stButton"] button > div,
div[class*="st-key-case_housing_stat_"] [data-testid="stButton"] button > div,
div[class*="st-key-household_income_event_"] [data-testid="stButton"] button > div,
div[class*="st-key-household_expense_event_"] [data-testid="stButton"] button > div,
div[class*="st-key-open_nta_generational_report"] [data-testid="stButton"] button > div {
    width: 100% !important;
    justify-content: flex-start !important;
    text-align: left !important;
}
</style>
""", unsafe_allow_html=True)
        for _report_title, _report_id in _graph_stat_reports:
            if st.button(
                f"🧭 {_report_title}",
                key=f"graph_stat_report_{_report_id}",
                use_container_width=True,
            ):
                _open_source_reference(
                    _report_id,
                    "우리집 재정곡선",
                    "chart-stat-report-links",
                )

        # 위쪽 보고서와 중복되지 않는 추가 보고서도 번호순으로 표시한다.
        st.markdown('<div id="case-stat-detail-links" style="scroll-margin-top: 120px;"></div>', unsafe_allow_html=True)
        _case_stat_links = [
            ("12. 과거 소득·지출을 현재 기준과 비교하는 방법", "6051300-00"),
            ("13. 지출 통계 출처 및 산출방법", "6051400-00"),
            ("15. 소득 기준곡선의 출처와 산정 방식", "6051600-00"),
        ]
        for _case_stat_title, _case_stat_id in _case_stat_links:
            if st.button(
                f"🧭 {_case_stat_title}",
                key=f"case_stat_detail_{_case_stat_id}",
                use_container_width=True,
            ):
                _open_source_reference(
                    _case_stat_id,
                    "우리집 재정곡선",
                    "case-stat-detail-links",
                )

        # 대표사례의 계산 가정과 지역별 주택가격 통계를 구분해 표시한다.
        _case_is_representative = st.session_state.get("_representative_case_id") in {
            "case_32_female", "case_45_female"
        }
        _case_housing_region = st.session_state.get("housing_region")
        if not _case_housing_region or _case_housing_region == "지역 선택":
            _case_housing_region = st.session_state.get("residence_region", "지역 선택")
        if _case_housing_region in HOUSING_PRICE_DATA:
            <div id="case-housing-statistics" style="scroll-margin-top: 120px;"></div>
            _case_housing_stats = HOUSING_PRICE_DATA[_case_housing_region]
            _case_house_median_eok = _case_housing_stats[1] / 100000
            _case_apt_median_eok = _case_housing_stats[3] / 100000

            @st.dialog("지역별 주택가격 통계", width="large")
            def _show_housing_price_stats_dialog():
                st.markdown(
                    "한국부동산원 R-ONE 「전국주택가격동향조사」의 "
                    "2025년 12월 지역별 중위가격입니다."
                )
                _housing_rows = [
                    {
                        "지역": _region,
                        "주택종합": f"{_values[1] / 100000:.2f}억 원",
                        "아파트": f"{_values[3] / 100000:.2f}억 원",
                    }
                    for _region, _values in HOUSING_PRICE_DATA.items()
                ]
                st.table(_housing_rows)
                st.caption(
                    "단위: 억 원. 지역 간 가격 수준을 비교하기 위한 통계값이며, "
                    "개별 주택의 실제 매매가격이나 미래 가격을 뜻하지 않습니다."
                )
                st.markdown(
                    "[한국부동산원 R-ONE 통계정보]"
                    "(https://www.reb.or.kr/reb/cm/cntnts/cntntsView.do?cntntsId=1033&mi=10333&statId=S234820263)"
                )

            with st.container(border=True):
                st.markdown("**🏠 부동산 적용 기준**")
                if _case_is_representative:
                    st.markdown("**기본사례 예시**")
                    st.markdown(
                        "- 주택가격 4.0억 원\n"
                        "- 대출금 1.4억 원(LTV 35%)\n"
                        "- 자기자금 2.6억 원(65%)"
                    )
                    st.caption("※ 재정곡선을 계산하기 위해 설정한 가정값입니다.")

                st.markdown(f"**{_case_housing_region} 지역의 주택가격 통계 중위값**")
                st.markdown(
                    f"- {_case_house_median_eok:.2f}억 원 (주택)\n"
                    f"- {_case_apt_median_eok:.2f}억 원 (아파트)"
                )
                with st.container(horizontal=True, vertical_alignment="center", gap=None):
                    if st.button(
                        "17개 시·도 주택종합·아파트 중위가격표 보기",
                        key="open_housing_price_stats_table",
                        help="17개 시·도 주택종합·아파트 중위가격 표 보기",
                        type="tertiary",
                    ):
                        _show_housing_price_stats_dialog()
                    st.caption(
                        "※ 한국부동산원 전국주택가격동향조사 · 2025년 12월 기준. 지역별 시장가격"
                    )
                    if st.button(
                        "🧭",
                        key="source_housing_price_stats",
                        help="지역별 주택가격 통계 출처 보기",
                        type="tertiary",
                    ):
                        _open_source_reference(
                            "6051500-00",
                            "우리집 재정곡선",
                            "case-housing-statistics",
                        )
            _housing_report_links = [
                ("4. 주택대출과 원리금 분리", "6050500-01"),
                ("14. 부동산 적용 기준과 지역별 산정방법", "6051500-00"),
            ]
            for _housing_report_title, _housing_report_id in _housing_report_links:
                if st.button(
                    f"🧭 {_housing_report_title}",
                    key=f"case_housing_stat_{_housing_report_id}",
                    use_container_width=True,
                ):
                    _open_source_reference(
                        _housing_report_id,
                        "우리집 재정곡선",
                        "case-stat-detail-links",
                    )






#########################################################
# 6.05 | Tab 5 — AI 시선
#########################################################
elif selected_page == "AI 시선":
    is_adv = st.session_state.get("advanced_mode", False)
    summary = current_financial_summary()
    person_name = st.session_state.get("person_name", "나")
    person_age = st.session_state.get("person_age", 35)

#--------------------------------------------------------
# 6.05.01 | 기본 모드 — AI 자동 성찰문 생성 및 표시
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
# 6.05.02 | 기본 모드 — 고급 모드 초대장 카드
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
        # [고급 모드] 모든 마이크로 모듈(6.05.01 ~ 6.05.07) 완전 탑재
        st.caption("AI는 평가자가 아닌, 내가 작성한 삶의 숫자를 객관적인 거울처럼 비춰주는 성찰 파트너입니다.")

#--------------------------------------------------------
# 6.05.03 | 고급 모드 — 재무 및 가족 생애 데이터 프롬프트 구성
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
# 6.05.04 | 고급 모드 — AI 분석 원칙·톤(맛) 설정 패널
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
# 6.05.05 | 고급 모드 — Gemini AI 리포트 생성 버튼
#--------------------------------------------------------
        if st.button("⚡ AI 리포트 생성", type="primary", use_container_width=True):
            st.session_state.ai_summary = summary
            st.session_state.ai_comment = None
            with st.spinner(f"AI가 {taste_mode.split()[0]} 모드로 지표를 분석 중입니다 (약 15~20초 소요)..."):
                comment, error = call_gemini_text(full_prompt_text)
                st.session_state.ai_comment = comment if comment else error
            st.rerun()

#--------------------------------------------------------
# 6.05.06 | 고급 모드 — AI 리포트 표시 및 카카오톡 전송용 리포트
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
# 6.05.07 | 고급 모드 — 📋 AI 질의용 재무제표 expander
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
# 6.06 | Tab 6 — 통계 자료실
#########################################################
elif selected_page == "통계":
    #--------------------------------------------------------
    # 6.06.01.00 | 출처 자료 표시 및 원위치 복귀
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
        "6050200-00": "1. 소득과 소비의 생애주기",
        "6050300-00": "2. 결혼과 주거",
        "6050400-01": "3. 노후와 은퇴",
        "6050500-01": "4. 주택대출과 원리금 분리",
        "6050600-00": "5. 동시성과 통시성",
        "6050700-00": "6. 소득 통계",
        "6050800-00": "7. 결혼비용 통계",
        "6050900-00": "8. 빅5 우리집 이벤트",
        "6051000-00": "9. 고령층 근로연령 통계",
        "6051100-00": "10. 통계로 본 대한민국 3대 은퇴 분기점",
        "6051200-00": "11. 우리 가정 생애주기 소득곡선의 통계적 보정",
        "6051300-00": "12. 과거 소득·지출을 현재 기준과 비교하는 방법",
        "6051400-00": "13. 지출 통계 출처 및 산출방법",
        "6051500-00": "14. 부동산 적용 기준과 지역별 산정방법",
        "6051600-00": "15. 소득 기준곡선의 출처와 산정 방식",
        "6051700-00": "16. 세대 계승 생애주기 재정곡선",
        "6051800-00": "17. 여성의 출산·육아와 경력단절",
        "6051900-00": "18. 은퇴와 수입 단절",
        "6052000-00": "19. 나의 결혼",
        "6052100-00": "20. 출산과 육아",
        "6052200-00": "21. 주택구입",
        "6052300-00": "22. 자녀 대학",
        "6052400-00": "23. 자녀 결혼",
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
    # 6.06.02.00 | 1. 소득과 소비의 생애주기
    #--------------------------------------------------------
    st.markdown('<div id="stats-anchor-lifecycle-income" style="scroll-margin-top: 150px;"></div>', unsafe_allow_html=True)
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
    # 6.06.03.00 | 2. 결혼과 주거
    #--------------------------------------------------------
    st.markdown('<div id="stats-anchor-marriage-housing" style="scroll-margin-top: 150px;"></div>', unsafe_allow_html=True)
    with st.expander("2. 결혼과 주거", expanded=_active_source_id == "6050300-00"):
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
    # 6.06.04.00 | 3. 노후와 은퇴
    #--------------------------------------------------------
    st.markdown(
        '<div id="stats-anchor-retirement-expense" style="scroll-margin-top: 150px;"></div>',
        unsafe_allow_html=True,
    )
    with st.expander(
        "3. 노후와 은퇴",
        expanded=_active_source_id == "6050400-01",
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
    # 6.06.05.00 | 4. 주택대출과 원리금 분리
    #--------------------------------------------------------
    st.markdown(
        '<div id="stats-anchor-loan-payment" style="scroll-margin-top: 150px;"></div>',
        unsafe_allow_html=True,
    )
    with st.expander(
        "4. 주택대출과 원리금 분리",
        expanded=_active_source_id == "6050500-01",
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
- 원금: 소비지출이 아니라 부채 감소입니다. 다만 실제 현금 유출이므로 나침반의 가구지출 곡선에 원금상환액을 포함하고, 순현금흐름에서는 가구지출에 포함된 금액을 별도로 다시 차감하지 않습니다.
- 대표사례의 45세 여성은 39세에 대출을 시작해 6년간 상환한 것으로 가정합니다. 현재 추정 잔액은 약 1억 2,362만 원이며, 다음 회차 기준 월 이자는 약 41.2만 원, 원금은 약 25.6만 원입니다.
- 32세 여성은 현재 주택·대출이 없는 상태로 두고, 39세 주택 구입 시점부터 같은 대출모형을 적용합니다.

주의: 실제 대출계약의 금리·만기·상환방식과 다를 수 있는 교육용 표준 가정입니다. LTV1 또한 조사 평균이므로 개별 가구의 실제 대출을 뜻하지 않습니다.

자료: [국토교통부 「2024년도 주거실태조사 결과」(2025.11.17.)](https://www.molit.go.kr/USR/NEWS/dtl.jsp?id=95091415&lcmspage=2)
""")
    #--------------------------------------------------------
    # 6.06.06.00 | 5. 동시성과 통시성
    #--------------------------------------------------------
    st.markdown('<div id="stats-anchor-time-adjustment" style="scroll-margin-top: 150px;"></div>', unsafe_allow_html=True)
    with st.expander("5. 동시성과 통시성", expanded=True):
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

### 통시성 보정 검토: 장기 임금·물가 전망과 구매력의 해석

이번 검토의 결론은 **현재 통시성 보정식을 곧바로 수정할 필요는 없으며, 먼저 그 결과를 읽는 관점을 바로잡아야 한다**는 것입니다. 현재의 임금·물가 상승률은 과거 관측자료에서 산출한 가정이고, 공공기관의 장기 거시경제 전망과 비교했을 때 실질임금 상승률 측면에서 상당히 가까운 수준을 보입니다.

**① 과거 관측치와 장기 전망의 비교**

나침반은 2011~2025년 실제 지수의 연평균 복합상승률을 미래 가정으로 사용합니다.

- 나침반의 과거 관측 CAGR: 명목임금 약 3.47%, 소비자물가 약 1.87%
- 두 상승률을 함께 고려한 실질임금 상승률: 약 1.57%

한국보건사회연구원 「사회보장 재정 장기추계 모형 연구」(연구보고서 2024-02)는 제5차 국민연금 재정계산의 거시경제 가정을 활용해 장기 전망을 제시합니다. 이 전망에서 물가상승률은 2025~2070년 2.0%로 유지되고, 명목임금 상승률은 장기적으로 3.9%에서 3.6%로 낮아집니다.

| 연도 | 장기 물가상승률 전망 | 장기 명목임금 상승률 전망 | 환산 실질임금 상승률 |
|---|---:|---:|---:|
| 2025 | 2.0% | 3.9% | 약 1.86% |
| 2040 | 2.0% | 3.9% | 약 1.86% |
| 2050 | 2.0% | 3.8% | 약 1.76% |
| 2060 | 2.0% | 3.7% | 약 1.67% |
| 2070 | 2.0% | 3.6% | 약 1.57% |
| 나침반 과거 CAGR | 1.87% | 3.47% | 약 1.57% |

실질임금 상승률은 단순 차감이 아니라 다음 식으로 환산했습니다.

- 실질임금 상승률 = (1 + 명목임금 상승률) ÷ (1 + 물가상승률) − 1

따라서 나침반의 과거 15년 평균에서 계산한 실질임금 상승률 약 1.57%는 이 장기 전망의 2070년 수준과 거의 같습니다. 다만 2025~2040년의 장기 전망과는 차이가 있으므로, 두 수치가 모든 기간에 동일하다는 뜻은 아닙니다.

자료: 한국보건사회연구원, 「사회보장 재정 장기추계 모형 연구」(연구보고서 2024-02), 제2장 표 2-2 및 거시경제변수 전망 설명. [원문 PDF](https://repository.kihasa.re.kr/bitstream/201002/45625/1/%EC%97%B0%EA%B5%AC%EB%B3%B4%EA%B3%A0%EC%84%9C%202024-02.pdf)

**② 임금이 물가보다 더 오르면 잉여소득은 왜 커지는가**

물가상승은 같은 돈으로 살 수 있는 양을 줄입니다. 그러나 임금이 물가보다 더 빠르게 오른다는 가정에는 물가상승에 따른 화폐가치 하락 외에 **근로소득의 실질 구매력이 장기적으로 개선된다**는 의미도 포함됩니다.

예를 들어 명목임금이 연 3.47%, 물가가 연 1.87% 상승한다면, 임금의 실질 구매력은 연 약 1.57% 증가하는 것으로 계산됩니다. 이 가정이 장기간 누적되면 미래의 근로소득은 현재 구매력으로 환산해도 커집니다.

따라서 나침반에서 미래 소득곡선이 지출곡선보다 빠르게 커지고 잉여소득이 증가하는 것은 단순히 물가 때문에 숫자만 커진 결과가 아닙니다. **임금의 실질 구매력이 장기적으로 개선된다는 가정이 반영된 결과**입니다.

**③ 그렇다면 대한민국 국민은 모두 점점 더 부자가 되는가?**

그렇게 단정할 수는 없습니다. 장기 전망의 실질임금 상승은 거시경제 모형에서 설정한 평균적인 임금 경로이지, 모든 국민과 모든 가구의 소득이 매년 같은 비율로 증가한다는 뜻은 아닙니다.

- 임금근로자의 평균 임금이 상승해도 자영업자·무직자·은퇴자의 소득은 다른 흐름을 보일 수 있습니다.
- 평균 임금 상승이 소득분배 개선이나 모든 계층의 소득 증가를 보장하지 않습니다.
- 고용률, 근로시간, 노동시장 진입·이탈, 세금과 사회보험료, 연금 및 이전소득에 따라 가구의 실제 가처분소득은 달라집니다.
- 가구의 순자산과 부채, 주거비·의료비 등 지출 구조도 부의 변화를 좌우합니다.

그러므로 이 전망이 말해주는 것은 '대한민국 국민 모두가 부자가 된다'가 아니라, **장기 거시경제 가정상 평균 임금근로자의 실질임금이 완만하게 증가할 수 있다**는 것입니다.

**④ 나침반에서의 해석 원칙**

1. 현재의 통시성 보정은 2024년 전후의 동시성 통계를 서로 다른 미래 연도의 명목금액으로 환산하기 위한 절차입니다.
2. 임금 상승률과 물가 상승률을 따로 적용하는 것은 서로 다른 경제적 움직임을 반영하기 위한 것이며, 두 상승률의 차이는 실질임금 구매력 변화로 해석합니다.
3. 미래 잉여소득 증가는 임금의 실질 구매력이 지출보다 빠르게 증가한다는 가정의 결과입니다. 이를 확정적인 개인의 미래 소득이나 부의 증가로 표현하지 않습니다.
4. 현재의 3.47%·1.87%는 과거 관측기간의 CAGR을 미래에 적용한 시뮬레이션 가정입니다. 장기 공공 전망과의 비교는 이 가정의 합리성을 점검하는 참고자료이지, 미래 실적을 보증하는 근거가 아닙니다.
5. 따라서 당장은 계산식을 변경하기보다, 그래프의 미래 금액은 해당 미래 연도의 명목금액이며 잉여소득 증가에는 실질임금 상승 가정이 포함되어 있다는 점을 사용자에게 분명히 설명합니다.

**검토 결론**

현재 나침반의 통시성 보정은 단순한 인플레이션 보정에 그치지 않습니다. 과거 통계에서 관측한 임금과 물가의 장기 상승률을 각각 적용함으로써, 미래의 명목금액 변화와 임금의 실질 구매력 변화를 함께 시뮬레이션합니다. 장기 전망과 비교한 결과, 현재 가정의 실질임금 상승률은 장기 전망의 후반부 수준과 거의 일치합니다.

따라서 현 단계에서는 통시성 보정식을 성급히 바꾸지 않습니다. 대신 미래 명목금액과 현재 구매력의 차이, 실질임금 상승이 잉여소득에 미치는 영향을 명확히 설명하는 것을 우선합니다.
""")

    #--------------------------------------------------------
    # 6.06.07.00 | 6. 소득 통계
    #--------------------------------------------------------
    st.markdown('<div id="stats-anchor-income-statistics" style="scroll-margin-top: 150px;"></div>', unsafe_allow_html=True)
    with st.expander("6. 소득 통계: 연령별 임금과 연도별 임금지수", expanded=True):
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
    # 6.06.08.00 | 7. 결혼비용 통계
    #--------------------------------------------------------
    st.markdown('<div id="stats-anchor-marriage-cost" style="scroll-margin-top: 150px;"></div>', unsafe_allow_html=True)
    with st.expander("7. 결혼비용 통계: 신혼집은 신랑 측 77%, 그 외 비용은 비슷하게 나눠서", expanded=True):
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
- 한 자녀당 부모 지원 추정액은 약 **6,294만 원**입니다. 생애주기 곡선에서는 2년에 나누어 반영하고, 발생 연도의 소비자물가 기준으로 환산합니다.

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
    #--------------------------------------------------------
    # 6.06.09.00 | 8. 빅5 우리집 이벤트 개요
    #--------------------------------------------------------
    st.markdown('<div id="stats-anchor-household-events" style="scroll-margin-top: 150px;"></div>', unsafe_allow_html=True)
    with st.expander("8. 빅5 우리집 이벤트", expanded=_active_source_id == "6050900-00"):
        st.markdown("""
우리 가정의 생애주기 재정곡선에는 다섯 가지 큰 지출 사건이 표시됩니다. 차트에 표시되는 원의 크기는 각 사건의 **중복 차감 전 총비용**을 기준으로 하고, 실제 가구지출 곡선에는 기존 MDIS 가계지출과 겹칠 가능성이 있는 금액을 조정한 뒤 반영합니다.

| 이벤트 | 모델 기준 총비용 | 적용 기간 | 재정곡선에 추가되는 방식 |
|---|---:|---:|---|
| ① 나의 결혼 | 신혼집 자기자금 추정액의 1/2 + 6,298만 원 | 2년 | 혼수 중복 의심액 2,615만 원 차감 |
| ② 출산과 육아 | 8,064만 원 | 6년 | MDIS 지출과 겹치는 8,035.2만 원 차감 |
| ③ 주택구입 | 지역 아파트 중위가격 × (1-LTV) | 4년 | 자산 취득 지출로 별도 반영 |
| ④ 자녀 대학 | 등록금 2,647.8만 원 + 생활비 3,984만 원 | 4년 | 기존 교육·생활 지출과 중복 가능액 전액 차감 |
| ⑤ 자녀 결혼 | 약 6,293.8만 원 | 2년 | 신혼집 외 부모지원 약 1,521.7만 원 차감 |

**읽을 때 유의할 점**

- 차트의 이벤트 원은 생애사건의 총규모를 보여주며, 총비용 전액이 가구지출 곡선에 추가되는 것은 아닙니다.
- 주택구입은 소비가 아니라 자산 취득 성격이므로 일반 생활비와 구분합니다.
- 자녀 대학 비용은 등록금과 생활비의 조사 기준연도가 서로 다르며, 생활비를 48개월 적용한 것은 모델 가정입니다.
- 결혼과 주택구입이 같은 주택 마련을 가리키는 경우 중복될 수 있습니다. 두 사건의 관계는 가정별 계획에 맞춰 해석해야 합니다.

각 사건의 통계 근거, 비용 산식, 중복 조정과 모델 가정은 아래 개별 리포트에서 확인할 수 있습니다.
""")
    # 6.06.10.00 | 9. 고령층 근로연령 통계
    #--------------------------------------------------------
    st.markdown('<div id="stats-anchor-older-work" style="scroll-margin-top: 150px;"></div>', unsafe_allow_html=True)
    with st.expander("9. 고령층 근로연령 통계", expanded=True):
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

    #--------------------------------------------------------
    # 6.06.11.00 | 10. 통계로 본 대한민국 3대 은퇴 분기점
    #--------------------------------------------------------
    st.markdown('<div id="stats-anchor-retirement-milestones" style="scroll-margin-top: 150px;"></div>', unsafe_allow_html=True)
    with st.expander(
        "10. 통계로 본 대한민국 3대 은퇴 분기점",
        expanded=True,
    ):
        st.markdown("""
은퇴는 하나의 나이로 끝나는 사건이 아닙니다. **주된 일자리에서 물러나는 시기**, **사회 전체의 생애주기 수지가 적자로 돌아서는 시기**, **노동시장에서 실질적으로 이탈하는 시기**는 서로 다른 통계가 보여주는 세 가지 장면입니다.

### ① 주된 일자리에서 물러나는 시기

#### 55~60세 전후

국가데이터처의 2026년 5월 고령층 부가조사에서, 가장 오래 근무한 일자리를 그만둔 당시 평균 연령은 **53.0세**였습니다.

**55~60세 전후**는 조사에서 직접 측정한 평균 퇴직 연령이 아니라, 주된 일자리에서 물러난 뒤 경력과 소득 구조를 재편하는 시기를 살펴보기 위한 나침반의 해석 구간입니다. 주된 일자리의 퇴직이 곧 모든 경제활동의 종료를 뜻하지는 않습니다.

### ② 사회 전체의 생애주기 수지가 적자로 돌아서는 시기

#### 61세

국가데이터처 「2024년 국민이전계정」에서 노동소득보다 소비가 다시 커지는 **적자 재전환 연령은 61세**입니다. 국민 전체의 연령별 노동소득과 소비를 1인당 평균으로 살펴본 결과입니다.

이는 개인이 61세에 은퇴한다는 뜻이 아닙니다. 사회 전체의 평균적인 생애주기에서 노동소득만으로 소비를 충당하기 어려워지는 연령을 보여줍니다.

### ③ 노동시장에서 실질적으로 이탈하는 시기

#### 남성 67.4세 · 여성 69.6세

OECD 「Pensions at a Glance 2025: Korea」는 2024년 한국의 실질 노동시장 이탈 연령을 **남성 67.4세, 여성 69.6세**로 제시합니다. 한국의 65~69세 고용률도 **57%**로, OECD 평균 26%보다 높았습니다.

이 지표는 개인이 마지막 일자리를 그만둔 나이를 직접 조사한 값이 아닙니다. OECD가 40세 이상 인구의 노동시장 참여율 변화를 연령집단별로 분석해 추정한 평균 이탈 연령입니다. 따라서 개인의 정년이나 실제 은퇴 시점과 동일하게 해석해서는 안 됩니다.

---

**세 통계가 함께 보여주는 것**

주된 일자리에서 물러나는 시기와 생애주기 수지가 적자로 바뀌는 시기, 노동시장 참여에서 실질적으로 이탈하는 시기는 일치하지 않습니다. 은퇴를 한 번의 퇴직이 아니라 **소득활동과 생계 구조가 단계적으로 바뀌는 과정**으로 바라볼 필요가 있습니다.

**자료 출처**

- [국가데이터처 — 2026년 5월 경제활동인구조사 고령층 부가조사 결과](https://www.mods.go.kr/board.es?act=view&bid=210&list_no=446335&mid=a10301010000)
- [국가데이터처 — 2024년 국민이전계정](https://mods.go.kr/board.es?act=view&bid=11898&list_no=447028&mid=a10301130100)
- [OECD — Pensions at a Glance 2025: Korea](https://www.oecd.org/en/publications/pensions-at-a-glance-2025-country-notes_8a53ef12-en/korea-republic-of_5cd52913-en.html)
- [OECD — Effective age of labour market exit: definition and methodology](https://www.oecd.org/en/publications/pensions-at-a-glance-2025_e40274c1-en/full-report/effective-age-of-labour-market-exit_fd1212b7.html)
""", unsafe_allow_html=True)

    #--------------------------------------------------------
    # 6.06.12.00 | 11. 우리 가정 생애주기 소득곡선의 통계적 보정
    #--------------------------------------------------------
    st.markdown('<div id="stats-anchor-household-income-after-retirement" style="scroll-margin-top: 150px;"></div>', unsafe_allow_html=True)
    with st.expander(
        "11. 우리 가정 생애주기 소득곡선의 통계적 보정",
        expanded=True,
    ):
        st.markdown("""
### 기존 가구소득 곡선은 어떻게 만들어지나요?

우리 가정의 소득곡선은 별도의 연령대별 평균 가구처분가능소득을 덧붙여 만든 것이 아닙니다. 직업군별 연령 기준소득 곡선을 바탕으로, 인터뷰이 또는 대표사례가 입력한 현재 소득이 해당 기준에 비해 어느 수준인지 보정계수로 계산합니다. 그 비율을 전 연령대의 기준곡선에 적용하고, 임금지수에 따른 통시성 보정과 생애 이벤트의 추가 소득을 반영합니다.

### 그래프의 두 소득선

- **가구소득 실선**은 기존 우리 가정의 예상 소득입니다. 은퇴 시점부터 본인·배우자의 근로·사업소득 중단 조건이 적용되는 기존 계산을 그대로 유지합니다. 국민연금과 입력한 기타연금은 각 수령 개시 연령부터 기존 방식대로 반영합니다.
- **통계적 보정 점선**은 은퇴 이후에도 기존 직업군별 연령 기준소득 곡선을 연장한 가상 비교선입니다. 현재 근로·사업소득을 기준으로 한 보정계수, 임금지수, 본인·배우자의 연령 차이와 기존 경력단절 조건은 유지하지만, 인터뷰이가 별도로 입력한 국민연금과 기타연금은 더하지 않습니다.
- 이 점선은 은퇴 후 실제 취업이나 사업소득을 예측하는 값이 아닙니다. 은퇴 시점에서 근로·사업소득을 자동으로 0으로 만드는 가정을 제거했을 때, 기존 통계적 기준곡선이 어떻게 이어지는지 살펴보는 비교 시나리오입니다.

### 아래 그래프의 '통계적 보정' 순현금흐름

아래 그래프에는 기존 '순 현금흐름'과 함께 녹색 점선 '통계적 보정'을 표시합니다. 두 곡선은 **동일한 가구지출(대출 원금상환액 포함)**을 사용하고, 소득 부분만 다르게 계산합니다.

- 기존 순 현금흐름 = 기존 가구소득 실선 − 가구지출
- 통계적 보정 = 은퇴 후 연장한 통계적 기준소득 − 동일한 가구지출

따라서 두 선의 차이는 은퇴 후 소득을 어떤 기준으로 가정하느냐에 따른 차이입니다. 통계적 보정선은 은퇴 연령부터 표시하며, 기존 실선이나 기존 순현금흐름을 대체하지 않습니다.

### 해석할 때 유의할 점

- 직업군별 연령 기준곡선은 앱에 내장된 기준값이며, 현재 소득을 기준으로 한 보정계수를 적용합니다. 개별 인터뷰이의 실제 미래 소득을 보장하거나 예측하는 값은 아닙니다.
- 임금지수 통시성 보정과 연령별 기준곡선은 기존 모델의 계산 방식을 그대로 사용합니다.
- 인터뷰이가 입력한 국민연금과 기타연금은 통계적 보정 점선에서 제외합니다. 개인별 연금 예상액은 기존 가구소득 실선에만 반영합니다.
- 통계적 보정선은 비교 시나리오입니다. 실제 은퇴 후 취업 여부, 근로시간, 사업 지속 여부, 건강 및 노동시장 상황은 개인마다 다릅니다.
- 두 순현금흐름의 비교에서는 지출, 생애 이벤트 비용, 대출 원금상환 가정을 동일하게 유지합니다. 소득 가정 외의 차이를 섞지 않기 위한 설계입니다.

**이 비교가 던지는 질문**

은퇴 시점에 생계를 위한 노동을 줄이거나 그만두더라도 소득활동이 반드시 동시에 끝나는 것은 아닙니다. 기존 가구소득 시나리오와 통계적 기준곡선을 연장한 시나리오를 나란히 보며, 우리 가정의 은퇴 이후 현금흐름을 다시 생각해 볼 수 있습니다.
""", unsafe_allow_html=True)

    #--------------------------------------------------------
    # 6.06.13.00 | 12. 과거 소득·지출을 현재 기준과 비교하는 방법
    #--------------------------------------------------------
    st.markdown('<div id="stats-anchor-historical-comparison" style="scroll-margin-top: 150px;"></div>', unsafe_allow_html=True)
    with st.expander("12. 과거 소득·지출을 현재 기준과 비교하는 방법", expanded=_active_source_id == "6051300-00"):
        st.markdown("""
과거의 소득과 지출을 당시 명목금액만으로 현재 값과 나란히 놓으면 화폐가치의 변화를 놓치게 됩니다. 나침반은 과거 연령의 소득 기준값에 당시 임금지수를 적용해 과거 명목소득을 추정하고, 같은 연도의 지출 기준값에는 소비자물가지수(CPI)를 적용해 과거 명목지출을 추정합니다. 소득에는 임금지수, 지출에는 CPI를 각각 사용하며 서로 바꾸어 적용하지 않습니다.

이 비교는 과거 개인·가구의 실제 소득과 지출을 복원한 값이 아닙니다. 2024년 연령별·가구원 수별 기준곡선을 과거 지수로 환산한 비교용 추정치입니다. 임금지수는 2011년 이전과 시계열이 단절되어 있으므로, 그 이전 소득은 동일한 방식으로 연속 환산할 수 없습니다.

| 항목 | 기준연도 | 실제 자료 범위 |
|---|---:|---:|
| MDIS 가계지출 기준곡선 | 2024년 | 2024년 조사자료 |
| 소비자물가지수 | 2020=100 | 1965~2025년 |
| 임금지수 | 2024=100 | 2011~2025년 |

자료:
- 국가데이터처 소비자물가 총지수
- 고용노동부 사업체노동력조사 임금총액
- 기준데이터: `국가데이터처_소비자물가지수_및_고용노동부_임금지수_1965-2025.csv`
""")

    #--------------------------------------------------------
    # 6.06.14.00 | 13. 지출 통계 출처 및 산출방법
    #--------------------------------------------------------
    st.markdown('<div id="stats-anchor-spending-method" style="scroll-margin-top: 150px;"></div>', unsafe_allow_html=True)
    with st.expander("13. 지출 통계 출처 및 산출방법", expanded=_active_source_id == "6051400-00"):
        st.markdown("""
나침반의 우리 가정 생애주기 지출곡선은 국가데이터처 MDIS의 2024년 가계동향조사 연간자료를 이용합니다. 가구주 연령대와 가구원 수별로 가계지출의 **가중중위값**을 산출해 연령별 기준값으로 사용합니다.

**대표사례의 현재 기준값**

2024년 현재 45세·3인 가구의 월 가계지출 가중중위값은 **504.4만 원**입니다. 이 금액은 대표사례의 기준점이며, 실제 곡선에는 인터뷰이가 입력한 현재 지출과 기준값의 차이를 반영한 개인 지출 보정률이 적용됩니다. 예를 들어 보정률이 100%라면 MDIS 기준값을 그대로 사용한다는 뜻입니다.

연령대·가구원 수 조합에 따라 표본 수가 30 미만인 구간이 있습니다. 특히 일부 3·4인 가구의 가중중위값은 표본 변동 가능성이 있으므로 정밀한 예측값이 아닌 참고 기준으로 해석해야 합니다.

**원자료와 산출방법**
- 조사: 국가데이터처 「가계동향조사(2019~2024년 구분류)」 2024년 연간자료
- 제공 경로: MDIS 공공용 마이크로데이터
- 대상: 전체가구, 1인 이상
- 산출: 가구주 연령대·가구원 수별 가계지출 가중중위값
- 기준데이터: `국가데이터처_2024_가계동향조사_가구주연령대별가구원수별가계지출_가중중위값.csv`
- 변수·가중치·세부 산출 절차: 같은 폴더의 README 참고

이 통계값은 특정 개인의 미래 지출 예측이 아닙니다. 주거 형태·건강·돌봄·지역·생활 방식에 따라 실제 지출은 달라질 수 있습니다.
""")
        with st.container(key="spending-method-source-details"):
            with st.popover("원자료 변수와 산출 절차 보기", type="primary"):
                _spending_readme_path = (
                    Path(__file__).resolve().parent
                    / "data" / "기준데이터"
                    / "국가데이터처_2024_가계동향조사_가구주연령대별가구원수별가계지출_가중중위값_README.md"
                )
                if _spending_readme_path.exists():
                    st.markdown(_spending_readme_path.read_text(encoding="utf-8"))
                else:
                    st.info("산출 방법 파일을 현재 앱에서 찾을 수 없습니다.")

    #--------------------------------------------------------
    # 6.06.15.00 | 14. 부동산 적용 기준과 지역별 산정방법
    #--------------------------------------------------------
    st.markdown('<div id="stats-anchor-housing-method" style="scroll-margin-top: 150px;"></div>', unsafe_allow_html=True)
    with st.expander("14. 부동산 적용 기준과 지역별 산정방법", expanded=_active_source_id == "6051500-00"):
        st.markdown("""
**지역별 대표 주택가격**

나침반은 한국부동산원 R-ONE 「전국주택가격동향조사」의 2025년 12월 지역별 주택가격 통계를 참고합니다. 지역 간 가격 수준을 비교하기 위해 주택종합·아파트의 평균 및 중위가격을 구분해 보유하며, 현재 가구의 주택구입 기준에는 **지역별 아파트 중위가격**을 사용합니다.

| 지역 | 2025년 12월 아파트 중위가격 |
|---|---:|
| 서울 | 9억 5,800만 원 |
| 부산 | 2억 8,200만 원 |
| 대구 | 2억 5,350만 원 |
| 인천 | 3억 3,350만 원 |
| 광주 | 2억 2,200만 원 |
| 대전 | 2억 9,650만 원 |
| 울산 | 2억 5,900만 원 |
| 세종 | 5억 3,300만 원 |
| 경기 | 4억 5,400만 원 |
| 강원 | 1억 5,900만 원 |
| 충북 | 1억 6,700만 원 |
| 충남 | 1억 7,700만 원 |
| 전북 | 1억 4,800만 원 |
| 전남 | 1억 4,300만 원 |
| 경북 | 1억 4,000만 원 |
| 경남 | 1억 7,500만 원 |
| 제주 | 2억 4,500만 원 |

**대출비율(LTV) 기준**

2024년 주거실태조사에서 금융기관 대출 이용 가구의 구입가격 대비 대출 비율은 수도권·광역시 등 34.3%, 도지역 41.8%입니다. 부산은 광역시에 해당하므로 기본값 34.3%를 적용합니다.

**대표사례의 별도 단순화**

대표사례는 지역 통계값을 그대로 쓰지 않고 주택가격 4억 원을 가정합니다. LTV는 약 35%로 단순화해 대출 1억 4천만 원, 자기자금 2억 6천만 원으로 표시합니다. 그 외 사례는 선택 지역의 아파트 중위가격과 지역별 LTV 기준을 사용합니다.

주의: 지역별 가격은 특정 가구가 실제로 구입할 주택의 가격이 아닙니다. 주택유형·면적·연식·입지에 따라 실제 거래가격은 달라집니다. 평균·중위가격은 지역 간 가격 수준 비교용이며, 미래 주택가격 상승률을 직접 나타내는 지표는 아닙니다.

자료:
- 한국부동산원 R-ONE 「전국주택가격동향조사」, 2025년 12월. [통계정보](https://www.reb.or.kr/reb/cm/cntnts/cntntsView.do?cntntsId=1033&mi=10333&statId=S234820263)
- 국토교통부 「2024년도 주거실태조사 결과」. [보도자료](https://www.molit.go.kr/USR/NEWS/dtl.jsp?id=95091415&lcmspage=2)
""")

    #--------------------------------------------------------
    # 6.06.16.00 | 15. 소득 기준곡선의 출처와 산정 방식
    #--------------------------------------------------------
    st.markdown('<div id="stats-anchor-income-curve-method" style="scroll-margin-top: 150px;"></div>', unsafe_allow_html=True)
    with st.expander("15. 소득 기준곡선의 출처와 산정 방식", expanded=_active_source_id == "6051600-00"):
        st.markdown("""
나침반의 소득 기준곡선은 국가데이터처의 연령별 임금근로일자리 평균보수를 참고하되, 그래프의 모든 연령별 점을 공식 통계값 그대로 연결한 것은 아닙니다. 공식 통계의 연령 구간은 20대·30대 등 10세 단위이므로, 나침반은 직장인·자영업자별로 5세 간격의 **모델 기준값**을 별도로 두고 연령대 사이를 보간합니다.

**우리 가정 소득곡선에 적용하는 순서**
1. 현재 입력한 본인 근로·사업소득을 해당 직업군의 기준값과 비교해 개인별 보정계수를 계산합니다.
2. 그 보정계수를 연령별 모델 기준곡선에 적용합니다.
3. 해당 연령이 속한 달력연도에 맞춰 2011~2025년 실제 임금지수로 명목 임금수준을 환산합니다.
4. 2027년 이후에는 2011~2025년 임금지수의 연평균 복합상승률 약 3.47%를 미래 가정으로 적용합니다. 2026년은 최신 실적연도인 2025년 수준을 기준점으로 둡니다.
5. 출산·육아 경력단절 및 복귀계수는 임금의 시간 보정과 별개의 생애사건 가정으로 적용합니다.

본인의 연간 상여금은 근로기간 동안 반복되는 연간 금액으로 모델링해 본인 근로소득에 더하고, 임금지수와 경력계수를 함께 적용합니다. 배우자의 상여금을 별도로 입력하는 항목은 현재 없습니다. 국민연금·추가연금·기타 연간소득은 현재 입력한 명목금액을 고정해 더하며 임금지수나 CPI로 자동 인상하지 않습니다.

**통계와 모델 기준값의 구분**

- 국가데이터처 임금근로일자리 평균보수: 임금근로일자리에 종사한 사람의 세전 월평균 보수이며, 취업하지 않은 사람을 0원으로 포함한 전체 인구 평균이 아닙니다.
- 직업군별 5세 간격 소득 기준값: 공식 통계의 원자료 구간을 그대로 옮긴 값이 아니라, 앱의 생애주기 시뮬레이션을 위해 설정한 모델 기준값입니다.
- 연도별 임금지수: 연령별 임금곡선을 만드는 자료가 아니라, 서로 다른 연도의 명목 임금수준을 환산하는 거시 보정지수입니다.

자료:
- 국가데이터처 「2024년 임금근로일자리 소득(보수) 결과」
- 고용노동부 「사업체노동력조사」 임금총액 통계
- 기준데이터: `국가데이터처_2024_연령별_임금근로일자리_평균보수.csv`
""")

    #--------------------------------------------------------
    # 6.06.17.00 | 16. 세대 계승 생애주기 재정곡선
    #--------------------------------------------------------
    st.markdown('<div id="stats-anchor-nta-generational" style="scroll-margin-top: 150px;"></div>', unsafe_allow_html=True)
    with st.expander("16. 세대 계승 생애주기 재정곡선", expanded=_active_source_id == "6051700-00"):
        st.markdown("""
**국민이전계정(NTA)은 무엇을 보여주는가?**

국민이전계정은 연령별 소비와 노동소득의 차이를 측정하고, 그 차이를 공공·민간 이전과 자산 재배분이 어떻게 보완하는지 살펴보는 통계입니다. 한 해의 개인별 가계부가 아니라, 대한민국 전체 인구를 연령별 1인당 평균으로 환산한 세대 간 자원 흐름입니다.

**2024년 기준 생애주기 세 분기점**

- **28세 — 생애 흑자 진입:** 이 연령부터 노동소득이 소비를 넘어섭니다.
- **45세 — 최대 흑자 정점:** 1인당 연간 노동소득과 소비의 차이가 **1,932만 원**으로 가장 큽니다.
- **61세 — 생애 적자 재진입:** 노동소득이 소비보다 작아지는 구간으로 다시 들어갑니다.

따라서 28~60세는 연간 노동소득이 소비보다 큰 흑자 구간이며, 0~27세와 61세 이후는 소비가 노동소득보다 큰 적자 구간입니다. 이는 근로소득만으로 생애 전체의 소비를 충당하는 구조가 아니라, 세대 간 이전과 자산의 활용이 함께 작동한다는 점을 보여줍니다.

**세대 간 자원은 어떻게 이동하는가?**

2024년 노동연령층(15~64세)에서는 공공·민간 이전을 합쳐 순유출이 발생했고, 유년층과 노년층은 순유입을 기록했습니다. 공공이전은 교육·보건·연금·사회보호 등을 통해, 민간이전은 가구 내 지원과 가구 간 이전 등을 통해 연령집단 사이의 자원을 연결합니다.

이 때문에 이 곡선의 ‘세대 계승’은 특정 가정의 상속이나 자녀에게 물려줄 재산을 뜻하지 않습니다. 사회 전체에서 한 세대가 다른 세대의 소비를 어떻게 뒷받침하는지를 나타내는 거시 통계입니다.

**나침반에서 읽는 방법**

- 이 곡선은 전국민 1인당 평균 기준선입니다. 우리 가정의 소득·지출 곡선과 같은 의미로 읽지 않습니다.
- 연간 흑자는 그 해의 노동소득이 소비보다 많다는 뜻이지, 그 금액이 실제 저축이나 순자산으로 남았다는 뜻은 아닙니다.
- 누적 노동잉여 역시 실제 예금·투자자산 잔액이 아닙니다. 공적·사적 이전, 자산소득, 투자수익, 주택 등 자산의 취득·처분을 모두 반영한 개인의 자산곡선과 구분해야 합니다.
- 따라서 이 통계는 개인의 은퇴 가능 시점을 직접 판정하는 도구가 아니라, 우리 가정의 생애주기를 사회 전체의 세대 간 흐름과 비교하는 참고선입니다.

자료: 국가데이터처 「2024년 국민이전계정」(2026. 9. 17. 발표). [보도자료](https://mods.go.kr/board.es?act=view&bid=11898&list_no=447028&mid=a10301130100) · [원문 PDF](https://mods.go.kr/boardDownload.es?bid=11898&list_no=447028&seq=3)
""")

    #--------------------------------------------------------
    # 6.06.18.00 | 17. 여성의 출산·육아와 경력단절
    #--------------------------------------------------------
    st.markdown('<div id="stats-anchor-career-break" style="scroll-margin-top: 150px;"></div>', unsafe_allow_html=True)
    with st.expander("17. 여성의 출산·육아와 경력단절", expanded=_active_source_id == "6051800-00"):
        st.markdown("""
**출산·육아로 인한 경력단절은 짧은 휴식이 아니라 소득 경로를 바꾸는 생애사건입니다.**

성평등가족부 「2025년 여성의 경제활동 및 경력단절 실태조사」는 만 19~54세 여성 8,177명을 대상으로 조사했습니다. 생애 한 번 이상 경력단절을 경험한 여성은 56.7%였고, 경력단절 사유 중 결혼·임신·출산 등 가족 관련 이유는 29.3%였습니다. 근로조건으로 인한 경력단절도 53.4%로 나타나, 모든 경력단절을 출산·육아만의 결과로 해석해서는 안 됩니다.

**재취업까지 걸리는 시간**

| 경력단절 사유 | 재취업까지 평균 기간 |
|---|---:|
| 결혼·임신·출산 등 | **7.5년** (89.9개월) |
| 근로조건 | 1.7년 (20.6개월) |

**복귀 후 일자리와 임금의 변화**

- 시간제 근로 비율: 경력단절 당시 7.2% → 재취업 후 첫 일자리 26.8%
- 주 평균 근로시간: 41.9시간 → 35.7시간
- 월평균 실질임금: 경력단절 당시 248만 5천 원 → 재취업 후 첫 일자리 198만 8천 원
- 재취업 후 첫 일자리 임금은 단절 당시의 **80.0% 수준**입니다.

**나침반의 소득곡선 적용**

나침반은 여성의 출산·육아 기간을 생애사건으로 설정하고, 해당 기간의 근로소득 감소와 경력 복귀 이후의 소득 수준 조정을 별도로 반영합니다. 현재 모델은 육아 기간 중 첫 2년은 기준소득의 35%, 이후 4년은 50%를 적용하고, 육아기간이 끝난 뒤에는 기준소득의 80%를 적용합니다. 이는 개인별 실제 경력과 임금 회복을 예측하는 값이 아니라, 통계에서 관찰되는 경력단절의 장기적 영향을 시뮬레이션하기 위한 단순화된 가정입니다.

특히 조사에서 관찰한 7.5년은 결혼·임신·출산 등으로 경력단절을 경험한 여성 집단의 평균 재취업 기간입니다. 모든 여성의 경력 공백이 7.5년이라는 뜻은 아니며, 나침반의 육아기간 6년 가정과도 서로 다른 지표입니다.

**자료 출처**

- 성평등가족부 「2025년 여성의 경제활동 및 경력단절 실태조사 결과」(2026.7.9.). [공식 보도자료](https://www.mogef.go.kr/nw/enw/nw_enw_s001d.do?bbtSn=714033&mid=mda700)
""")

    #--------------------------------------------------------
    # 6.06.19.00 | 18. 은퇴와 수입 단절
    #--------------------------------------------------------
    st.markdown('<div id="stats-anchor-retirement-income-stop" style="scroll-margin-top: 150px;"></div>', unsafe_allow_html=True)
    with st.expander("18. 은퇴와 수입 단절", expanded=_active_source_id == "6051900-00"):
        st.markdown("""
**은퇴는 특정 나이에 모든 소득이 한꺼번에 사라지는 사건이 아닙니다.** 주된 일자리에서 물러나는 시점, 근로·사업소득이 줄거나 멈추는 시점, 연금과 다른 소득원이 시작되는 시점은 서로 다를 수 있습니다.

**사회 통계가 보여주는 세 시점**

| 지표 | 연령 | 의미 |
|---|---:|---|
| 가장 오래 근무한 일자리에서 퇴직 | 평균 53.0세 | 주된 일자리 이탈 시점. 다른 일자리·사업으로 근로가 이어질 수 있음 |
| 국민이전계정의 적자 재진입 | 61세 | 국민 1인당 평균 노동소득보다 소비가 커지는 연령 |
| OECD 실질 노동시장 이탈 | 남성 67.4세 · 여성 69.6세 | 노동시장 참여율 변화를 이용해 추정한 평균 이탈 연령 |

국가데이터처 2026년 5월 고령층 부가조사에서 가장 오래 근무한 일자리를 그만둔 당시 평균 연령은 53.0세였습니다. OECD의 실질 노동시장 이탈 연령은 2024년 기준 남성 67.4세, 여성 69.6세입니다. 이 수치들은 서로 다른 정의와 방법으로 산출되므로 하나의 평균 은퇴연령처럼 합쳐서는 안 됩니다.

**나침반에서 근로소득과 연금은 별도로 다룹니다.**

- 우리 가정 생애주기 재정곡선의 본인·배우자 근로·사업소득은 각자 설정한 은퇴 연령부터 중단되는 조건을 적용합니다.
- 국민연금과 추가연금 등 입력한 연금소득은 각 수령 개시 시점부터 별도로 반영합니다. 근로소득이 중단되는 시점과 연금이 시작되는 시점 사이에는 소득 공백이 생길 수 있습니다.
- 통계적 보정 점선은 은퇴 이후에도 직업군별 기준소득 곡선을 연장한 비교 시나리오입니다. 실제 재취업을 예측하는 값이 아니며, 입력한 개인 연금은 더하지 않습니다.

따라서 은퇴 시점을 생각할 때는 '몇 살에 퇴직할까?'뿐 아니라 '근로소득이 줄어드는 시기와 연금·다른 파이프라인 소득이 시작되는 시기 사이를 어떻게 연결할까?'를 함께 살펴볼 필요가 있습니다.

**자료 출처**

- 국가데이터처 「2026년 5월 경제활동인구조사 고령층 부가조사 결과」. [보도자료](https://www.mods.go.kr/board.es?act=view&bid=210&list_no=446335&mid=a10301010000)
- 국가데이터처 「2024년 국민이전계정」. [보도자료](https://mods.go.kr/board.es?act=view&bid=11898&list_no=447028&mid=a10301130100)
- OECD 「Pensions at a Glance 2025: Korea」. [국가별 보고서](https://www.oecd.org/en/publications/pensions-at-a-glance-2025-country-notes_8a53ef12-en/korea-republic-of_5cd52913-en.html)
- 나침반 통계 리포트 11. 「우리 가정 생애주기 소득곡선의 통계적 보정」
""")

    #--------------------------------------------------------
    # 6.06.20.00 | 19. 나의 결혼
    #--------------------------------------------------------
    st.markdown('<div id="stats-anchor-event-own-marriage" style="scroll-margin-top: 150px;"></div>', unsafe_allow_html=True)
    with st.expander("19. 나의 결혼", expanded=_active_source_id == "6052000-00"):
        st.markdown("""
**결혼 비용은 신혼집 마련과 신혼집 외 비용을 구분해서 살펴봅니다.**

가연 「2024 결혼비용 리포트」가 제시한 평균 결혼비용은 3억 474만 원이며, 신혼집 2억 4,176만 원과 신혼집 외 비용 6,298만 원으로 구분됩니다. 이 가운데 나침반은 신혼집 외 비용 6,298만 원을 결혼 관련 비용의 기준으로 사용합니다.

**신혼집 자금은 누구의 몫이었을까?**

한국보건사회연구원 2020년 연구보고서(2019년 조사 분석)에서는 신혼집 주거자금 중 부모 지원 비중이 39.5%, 주거 이외 결혼비용에서 부모 지원 비중이 약 48.3%로 나타났습니다. 주거자금과 주거 이외 비용은 서로 다른 조사 항목이므로 단순 합산해 하나의 지원 비율로 읽지 않습니다.

**나침반의 적용 방식**

- 미래 결혼 이벤트의 총비용은 신혼집 자기자금 추정액의 1/2에 신혼집 외 비용 6,298만 원을 더합니다.
- 혼수 비용 중 2,615만 원은 가계의 가전·가구 등 내구재 지출과 겹칠 가능성이 있어 차감합니다.
- 과거 결혼은 실제 신혼집 부담액을 확인할 수 없으므로 신혼집 외 비용 6,298만 원을 기준으로 하고, 동일한 혼수 중복 의심액을 차감합니다.
- 차트의 결혼 이벤트는 **2년에 걸쳐 분산**합니다.

미래 결혼과 별도 주택구입 이벤트가 같은 신혼집을 뜻한다면 주택 자기자금이 중복 계산될 수 있습니다. 두 사건이 서로 다른 주택 마련인지 가정별 계획을 확인해야 합니다.

**자료 출처**

- 가연 「2024 결혼비용 리포트」
- 한국보건사회연구원 「신혼부부의 주거자금 조달방식과 부모 지원의 젠더-계층적 성격」, 연구보고서(수시) 2020-08. [원문 PDF](https://repository.kihasa.re.kr/bitstream/201002/37080/2/%EC%97%B0%EA%B5%AC%EB%B3%B4%EA%B3%A0%EC%84%9C%28%EC%88%98%EC%8B%9C%29%202020-08.pdf)
""")

    #--------------------------------------------------------
    # 6.06.21.00 | 20. 출산과 육아
    #--------------------------------------------------------
    st.markdown('<div id="stats-anchor-event-childcare" style="scroll-margin-top: 150px;"></div>', unsafe_allow_html=True)
    with st.expander("20. 출산과 육아", expanded=_active_source_id == "6052100-00"):
        st.markdown("""
**영유아 양육비는 가계의 일상 지출과 겹치는 부분을 구분해야 합니다.**

교육부 「2024년 전국보육실태조사 - 가구조사 보고」는 0~6세 미만 자녀가 있는 2,494가구를 조사했습니다.

| 구분 | 월평균 양육비 |
|---|---:|
| 영아 가구 | 109.1만 원 |
| 유아 가구 | 116.5만 원 |
| 영유아 가구 전체 | **111.6만 원** |

전체 평균 111.6만 원을 72개월에 단순 적용하면 **8,035.2만 원**입니다. 나침반의 모델 총액 8,064만 원과 약 0.36% 차이입니다. 다만 이는 동일한 월평균을 6년 동안 적용한 환산치이지, 같은 아동을 6년간 추적해 측정한 누적 지출액은 아닙니다.

**나침반의 적용 방식**

- 출산·육아 이벤트 총액: **8,064만 원**
- 차트 반영 기간: **6년**
- MDIS 가계지출에 이미 포함되었을 가능성이 있는 양육비: 111.6만 원 × 72개월 = **8,035.2만 원**
- 중복 조정 후 가구지출 곡선에 추가되는 금액: **28.8만 원**

차트의 이벤트 원은 중복 차감 전 총비용을 보여주고, 실제 가구지출 곡선에는 기존 생활비와 겹치는 부분을 차감한 금액을 더합니다. 따라서 차트의 이벤트 원 크기와 가구지출 곡선의 추가분은 서로 다릅니다.

**자료 출처**

- 육아정책연구소 「2024년 보육실태조사: 가구조사 보고」. [원문 PDF](https://repo.kicce.re.kr/bitstream/2019.oak/5843/11/CR2412_re3.pdf)
- 국회예산정책처 관련 분석자료. [자료 보기](https://nabo.go.kr/board/file/down.do?fid=33318651)
""")

    #--------------------------------------------------------
    # 6.06.22.00 | 21. 주택구입
    #--------------------------------------------------------
    st.markdown('<div id="stats-anchor-event-housing" style="scroll-margin-top: 150px;"></div>', unsafe_allow_html=True)
    with st.expander("21. 주택구입", expanded=_active_source_id == "6052200-00"):
        st.markdown("""
**주택구입은 소비가 아니라 자산을 취득하는 사건입니다.** 따라서 일반 생활비와 구분해 주택가격, 대출, 자기자금의 흐름을 살펴봅니다.

**생애최초 아파트 구입자의 자금 구성**

2024년 주거실태조사 원자료를 분석한 10,607가구의 생애최초 아파트 취득 사례에서 자기자금·금융기관 융자·부모 및 친지 지원의 구성을 연령별로 확인했습니다.

| 취득 연령 | 표본수 | 자기자금 | 금융기관 융자 | 부모·친지 지원 |
|---|---:|---:|---:|---:|
| 25~29세 | 556 | 54.28% | 30.01% | 15.15% |
| 30~34세 | 1,868 | 59.91% | 31.13% | 8.43% |
| 35~39세 | 2,261 | 65.29% | 28.54% | 5.79% |
| 40~44세 | 1,813 | 71.07% | 24.86% | 3.91% |
| 45~49세 | 1,273 | 75.15% | 22.26% | 2.44% |

여기서 금융기관 융자 비율은 조사에서 확인한 네 가지 자금 출처 중 금융기관 융자액의 비중입니다. 주택담보대출만을 분리한 규제상 LTV와는 다른 개념입니다.

**나침반의 적용 방식**

- 주택가격은 선택한 지역의 아파트 중위가격을 기준으로 삼습니다. 대표사례는 별도로 설정한 기본 가정값을 사용할 수 있습니다.
- 대출비율(LTV)을 적용해 자기자금 부담을 계산합니다.
- 주택구입 이벤트는 **4년에 걸쳐 분산**합니다.
- 자기자금은 자산 취득 성격이므로 일반 가계지출과 중복 차감하지 않고 별도 이벤트로 표시합니다.

조사 표본의 자금 구성은 과거 취득 가구의 평균적 조달 구조입니다. 특정 가구가 미래에 실제로 대출받을 비율이나 구입할 주택가격을 보장하지 않습니다.

**자료 출처 및 가공 파일**

- 국토교통부 「2024년도 주거실태조사 결과」. [보도자료](https://www.molit.go.kr/USR/NEWS/dtl.jsp?id=95091415&lcmspage=2)
- [가공 CSV — 생애최초 주택 구입자금 구성](https://github.com/ufreezone-ops/nachimpan/blob/dev/data/기준데이터/국토교통부_2024_주거실태조사_생애최초주택_구입자금구성.csv)
- [분석 README](https://github.com/ufreezone-ops/nachimpan/blob/dev/data/기준데이터/국토교통부_2024_주거실태조사_생애최초주택_구입자금구성_README.md)
""")

    #--------------------------------------------------------
    # 6.06.23.00 | 22. 자녀 대학
    #--------------------------------------------------------
    st.markdown('<div id="stats-anchor-event-college" style="scroll-margin-top: 150px;"></div>', unsafe_allow_html=True)
    with st.expander("22. 자녀 대학", expanded=_active_source_id == "6052300-00"):
        st.markdown("""
**대학 비용은 등록금과 생활비를 분리해 계산합니다.**

나침반의 기본 예시는 비수도권 4년제 일반대학·교육대학 평균 등록금과 대학생 생활비 조사 결과를 결합합니다.

**① 등록금 — 약 2,647.8만 원 / 4년**

교육부·한국대학교육협의회 「2026년 4월 대학정보공시 분석 결과」에 따르면 4년제 일반대학·교육대학 192개교의 2026학년도 비수도권 평균 연간 등록금은 **661만 9,600원**입니다.

- 연간 등록금: 661만 9,600원
- 4년 환산: **2,647만 8,400원**
- 장학금 차감 전 금액이며, 실제 부담액은 대학·전공·장학금에 따라 달라집니다.

**② 생활비 — 약 3,984만 원 / 4년**

학원복음화협의회 「2022 한국 대학생의 의식과 생활에 대한 조사」에서 학기 중 월평균 생활비는 **83만 원**으로 조사됐습니다. 나침반은 이를 48개월에 적용해 3,984만 원으로 환산합니다.

중요한 점은 83만 원이 연중 월평균이 아니라 학기 중 월평균이라는 것입니다. 방학을 포함한 48개월에 적용한 것은 모델 가정이며, 조사에서 직접 측정한 4년 누적액은 아닙니다.

**③ 총액과 가구지출 곡선의 관계**

| 항목 | 4년 환산액 |
|---|---:|
| 등록금 | 2,647.8만 원 |
| 생활비 | 3,984만 원 |
| **합계** | **약 6,631.8만 원** |

차트에는 약 6,632만 원의 총비용을 이벤트로 표시하지만, 등록금과 생활비가 기존 MDIS 교육비·일반생활 지출에 포함되었을 가능성을 고려해 현재 모델에서는 해당 금액을 전액 중복 차감합니다. 따라서 이 이벤트는 차트에 표시되지만 가구지출 곡선에 별도 추가되는 금액은 없습니다.

등록금은 2026학년도, 생활비는 2022년 조사 기준이므로 동일 기준연도로 물가 조정한 합계가 아닙니다.

**자료 출처**

- 교육부 「2026년 4월 대학정보공시 분석 결과」(2026.4.29.). [보도자료](https://www.moe.go.kr/boardCnts/viewRenew.do?boardID=294&boardSeq=106020&lev=0&m=020402&s=moe)
- 학원복음화협의회 「2022 한국 대학생의 의식과 생활에 대한 조사」 결과를 소개한 목회데이터연구소 「넘버즈 179호」. [원문 PDF](https://mhdata.or.kr/mailing/Numbers179_230214_Full_Report.pdf)
- [가공 CSV — 등록금·생활비 분리 기준](https://github.com/ufreezone-ops/nachimpan/blob/dev/data/기준데이터/교육부_2026_대학등록금_및_대학생생활비_기준.csv)
""")

    #--------------------------------------------------------
    # 6.06.24.00 | 23. 자녀 결혼
    #--------------------------------------------------------
    st.markdown('<div id="stats-anchor-event-child-marriage" style="scroll-margin-top: 150px;"></div>', unsafe_allow_html=True)
    with st.expander("23. 자녀 결혼", expanded=_active_source_id == "6052400-00"):
        st.markdown("""
**자녀 결혼 지원은 신혼집 주거자금과 신혼집 외 비용을 나누어 추정합니다.**

가연 「2024 결혼비용 리포트」의 평균 신혼집 비용은 2억 4,176만 원, 신혼집 외 비용은 6,298만 원입니다. 한국보건사회연구원 2020년 연구보고서(2019년 조사 분석)의 부모 지원 비율을 결합해 한쪽 부모의 평균 지원액을 추정합니다.

**자녀 한 명에 대한 부모 지원 추정액**

- 신혼집 지원: 24,176만 원 × (7,616 ÷ 19,292) ÷ 2 = 약 **4,772만 원**
- 신혼집 외 지원: 6,298만 원 × (1,745 ÷ 3,611) ÷ 2 = 약 **1,522만 원**
- 합계: 약 **6,294만 원**

이 값은 서로 다른 조사자료의 비용 수준과 부모 지원 비율을 결합한 모델 추정치입니다. 개별 가정의 실제 지원액이나 공식 예측값은 아닙니다.

**나침반의 중복 조정과 적용 방식**

- 총 이벤트 비용 약 6,293.8만 원 중 신혼집 외 부모지원 약 1,521.7만 원은 가구 간 이전지출과 겹칠 가능성이 있어 차감합니다.
- 신혼집 주거자금 지원 약 4,772만 원은 자산 이전 성격으로 보아 차감하지 않고 가구지출 곡선에 남깁니다.
- 차트의 자녀 결혼 이벤트는 **2년에 걸쳐 분산**합니다.

차트의 이벤트 원은 차감 전 총비용을 표시하고, 가구지출 곡선에는 중복 조정 후 금액을 반영합니다.

**자료 출처**

- 가연 「2024 결혼비용 리포트」
- 한국보건사회연구원 2020년 연구보고서(2019년 조사 분석). [원문 PDF](https://repository.kihasa.re.kr/bitstream/201002/37080/2/%EC%97%B0%EA%B5%AC%EB%B3%B4%EA%B3%A0%EC%84%9C%28%EC%88%98%EC%8B%9C%29%202020-08.pdf), 신혼부부 주거자금 및 주거 외 결혼비용 부모 지원 비율
""")

    st.caption("※ 이 자료실은 주제별 통계와 출처를 차근차근 확장하기 위한 구성입니다. 출처와 기준이 확인되지 않은 수치는 제시하지 않습니다.")


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
            let target = doc.getElementById("{_scroll_target_id}");
            if (!target && "{_scroll_target_id}" === "loan-payment-label-origin") {{
                const labels = Array.from(
                    doc.querySelectorAll('[data-testid="stWidgetLabel"]')
                );
                target = labels.find(
                    el => el.innerText.trim() === "대출 원리금 월상환액(원금+이자) [주석]"
                );
            }}

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