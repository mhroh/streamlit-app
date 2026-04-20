import streamlit as st

st.set_page_config(page_title="바바리안 덱", page_icon="⚔️", layout="wide")

CARDS = [
    {
        "id": 1,
        "name": "선제 돌격",
        "type": "attack",
        "power": 5,
        "category": "입론",
        "argument": "우리 측의 핵심 주장을 강력하고 명확하게 제시합니다.",
        "phrase": "\"우리는 명확히 주장합니다...\"",
        "tip": "첫 번째 발언에서 청중의 주의를 집중시키세요.",
    },
    {
        "id": 2,
        "name": "증거의 방패",
        "type": "defense",
        "power": 4,
        "category": "근거",
        "argument": "통계 자료와 전문가 의견으로 주장을 강화합니다.",
        "phrase": "\"연구에 따르면...\"",
        "tip": "신뢰할 수 있는 출처를 항상 준비하세요.",
    },
    {
        "id": 3,
        "name": "반박의 창",
        "type": "attack",
        "power": 5,
        "category": "반박",
        "argument": "상대방의 핵심 근거를 정면으로 반박합니다.",
        "phrase": "\"상대측의 주장은 다음과 같은 이유로 틀렸습니다...\"",
        "tip": "상대방의 약점을 미리 파악해 두세요.",
    },
    {
        "id": 4,
        "name": "질문 폭격",
        "type": "attack",
        "power": 4,
        "category": "교차조사",
        "argument": "날카로운 질문으로 상대방의 논리적 허점을 드러냅니다.",
        "phrase": "\"그렇다면 귀하는 어떻게 설명하시겠습니까?\"",
        "tip": "예/아니오로 답할 수 있는 질문을 활용하세요.",
    },
    {
        "id": 5,
        "name": "인과의 검",
        "type": "attack",
        "power": 4,
        "category": "논리",
        "argument": "원인과 결과를 명확히 연결하여 주장의 타당성을 높입니다.",
        "phrase": "\"이로 인해 필연적으로...\"",
        "tip": "인과관계를 단계적으로 설명하세요.",
    },
    {
        "id": 6,
        "name": "재구성 전술",
        "type": "defense",
        "power": 3,
        "category": "반박",
        "argument": "상대방의 주장을 재구성하여 유리하게 해석합니다.",
        "phrase": "\"상대측의 주장은 오히려 우리 입장을 지지합니다.\"",
        "tip": "상대방의 말을 역이용하세요.",
    },
    {
        "id": 7,
        "name": "공감 방어",
        "type": "defense",
        "power": 3,
        "category": "설득",
        "argument": "청중의 감정에 호소하여 동의를 이끌어냅니다.",
        "phrase": "\"우리 모두가 바라는 것은...\"",
        "tip": "청중과 공감대를 형성하세요.",
    },
    {
        "id": 8,
        "name": "실례 강타",
        "type": "attack",
        "power": 3,
        "category": "근거",
        "argument": "구체적인 실례로 추상적인 주장을 현실화합니다.",
        "phrase": "\"실제 사례를 보면...\"",
        "tip": "청중이 공감할 수 있는 사례를 선택하세요.",
    },
    {
        "id": 9,
        "name": "비교 분석",
        "type": "defense",
        "power": 4,
        "category": "논리",
        "argument": "비교와 대조를 통해 우리 측 입장의 우월성을 입증합니다.",
        "phrase": "\"A와 B를 비교했을 때...\"",
        "tip": "공정한 비교 기준을 제시하세요.",
    },
    {
        "id": 10,
        "name": "최후 마무리",
        "type": "special",
        "power": 5,
        "category": "최종발언",
        "argument": "핵심 논점을 정리하고 강렬한 인상을 남깁니다.",
        "phrase": "\"오늘 토론에서 우리가 증명한 것은...\"",
        "tip": "감정과 논리를 결합한 마무리를 준비하세요.",
    },
    {
        "id": 11,
        "name": "전문가 소환",
        "type": "defense",
        "power": 4,
        "category": "근거",
        "argument": "분야 전문가의 의견을 인용하여 신뢰성을 높입니다.",
        "phrase": "\"전문가 ○○○에 따르면...\"",
        "tip": "권위 있는 출처를 미리 조사하세요.",
    },
    {
        "id": 12,
        "name": "딜레마 함정",
        "type": "special",
        "power": 5,
        "category": "교차조사",
        "argument": "상대방이 어떤 선택을 해도 불리하게 만드는 질문을 던집니다.",
        "phrase": "\"A를 인정한다면 B가 되고, A를 부정한다면 C가 됩니다.\"",
        "tip": "양도논법을 활용한 강력한 공격 기술입니다.",
    },
]

TYPE_CONFIG = {
    "attack": {"label": "⚔️ 공격", "color": "#c0392b", "bg": "#2c0a0a"},
    "defense": {"label": "🛡️ 방어", "color": "#2980b9", "bg": "#0a1a2c"},
    "special": {"label": "✨ 특수", "color": "#f39c12", "bg": "#2c1a00"},
}

POWER_STARS = {1: "★☆☆☆☆", 2: "★★☆☆☆", 3: "★★★☆☆", 4: "★★★★☆", 5: "★★★★★"}

st.markdown("""
<style>
    .main { background-color: #1a1a2e; }
    .deck-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 900;
        color: #e74c3c;
        text-shadow: 0 0 20px #e74c3c88;
        letter-spacing: 3px;
        margin-bottom: 0.2rem;
    }
    .deck-subtitle {
        text-align: center;
        color: #aaa;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .card-container {
        border: 2px solid;
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
        transition: transform 0.2s;
        cursor: pointer;
    }
    .card-name {
        font-size: 1.1rem;
        font-weight: 800;
        margin-bottom: 4px;
    }
    .card-category {
        font-size: 0.75rem;
        opacity: 0.7;
        margin-bottom: 8px;
    }
    .card-argument {
        font-size: 0.85rem;
        line-height: 1.5;
        margin-bottom: 8px;
        color: #ddd;
    }
    .card-phrase {
        font-size: 0.8rem;
        font-style: italic;
        color: #f9ca24;
        border-left: 3px solid #f9ca24;
        padding-left: 8px;
        margin-bottom: 8px;
    }
    .card-tip {
        font-size: 0.75rem;
        color: #95a5a6;
    }
    .power-bar {
        font-size: 1rem;
        letter-spacing: 2px;
        margin-top: 4px;
    }
    .deck-slot {
        background: #2d2d44;
        border: 1px dashed #555;
        border-radius: 8px;
        padding: 8px;
        text-align: center;
        font-size: 0.8rem;
        color: #888;
        min-height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .deck-slot-filled {
        background: #2c3e50;
        border: 1px solid #3498db;
        border-radius: 8px;
        padding: 8px;
        text-align: center;
        font-size: 0.8rem;
        color: #ecf0f1;
        min-height: 60px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="deck-title">⚔️ 바바리안 덱 ⚔️</div>', unsafe_allow_html=True)
st.markdown('<div class="deck-subtitle">강력한 토론 카드를 선택하여 나만의 덱을 구성하세요 (최대 8장)</div>', unsafe_allow_html=True)

if "selected_cards" not in st.session_state:
    st.session_state.selected_cards = []

col_main, col_deck = st.columns([3, 1])

with col_main:
    filter_cols = st.columns(4)
    with filter_cols[0]:
        type_filter = st.selectbox("유형", ["전체", "⚔️ 공격", "🛡️ 방어", "✨ 특수"])
    with filter_cols[1]:
        cat_filter = st.selectbox("분류", ["전체"] + sorted(set(c["category"] for c in CARDS)))
    with filter_cols[2]:
        power_filter = st.selectbox("최소 파워", ["전체", "3+", "4+", "5"])
    with filter_cols[3]:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 초기화", use_container_width=True):
            st.session_state.selected_cards = []
            st.rerun()

    filtered = CARDS[:]
    if type_filter != "전체":
        type_map = {"⚔️ 공격": "attack", "🛡️ 방어": "defense", "✨ 특수": "special"}
        filtered = [c for c in filtered if c["type"] == type_map[type_filter]]
    if cat_filter != "전체":
        filtered = [c for c in filtered if c["category"] == cat_filter]
    if power_filter != "전체":
        min_power = int(power_filter[0])
        filtered = [c for c in filtered if c["power"] >= min_power]

    st.markdown(f"**{len(filtered)}장의 카드**")

    grid_cols = st.columns(3)
    for i, card in enumerate(filtered):
        with grid_cols[i % 3]:
            cfg = TYPE_CONFIG[card["type"]]
            is_selected = card["id"] in st.session_state.selected_cards

            border_color = "#f9ca24" if is_selected else cfg["color"]
            bg = "#1e3a1e" if is_selected else cfg["bg"]
            badge = "✅ " if is_selected else ""

            st.markdown(f"""
            <div class="card-container" style="border-color: {border_color}; background: {bg};">
                <div class="card-name" style="color: {cfg['color']};">{badge}{card['name']}</div>
                <div class="card-category">{cfg['label']} · {card['category']}</div>
                <div class="power-bar" style="color: {cfg['color']};">{POWER_STARS[card['power']]}</div>
                <hr style="border-color: {cfg['color']}33; margin: 8px 0;">
                <div class="card-argument">{card['argument']}</div>
                <div class="card-phrase">{card['phrase']}</div>
                <div class="card-tip">💡 {card['tip']}</div>
            </div>
            """, unsafe_allow_html=True)

            if is_selected:
                if st.button(f"❌ 제거", key=f"remove_{card['id']}", use_container_width=True):
                    st.session_state.selected_cards.remove(card["id"])
                    st.rerun()
            else:
                disabled = len(st.session_state.selected_cards) >= 8
                if st.button(f"+ 덱에 추가", key=f"add_{card['id']}", use_container_width=True, disabled=disabled):
                    st.session_state.selected_cards.append(card["id"])
                    st.rerun()

with col_deck:
    selected_count = len(st.session_state.selected_cards)
    st.markdown(f"### 🗡️ 내 덱 ({selected_count}/8)")

    progress_color = "#e74c3c" if selected_count == 8 else "#3498db"
    st.markdown(f"""
    <div style="background:#2d2d44; border-radius: 8px; height: 12px; margin-bottom: 12px;">
        <div style="background:{progress_color}; width:{selected_count/8*100}%; height:100%; border-radius:8px; transition: width 0.3s;"></div>
    </div>
    """, unsafe_allow_html=True)

    selected_cards_data = [c for c in CARDS if c["id"] in st.session_state.selected_cards]
    for i in range(8):
        if i < len(selected_cards_data):
            card = selected_cards_data[i]
            cfg = TYPE_CONFIG[card["type"]]
            st.markdown(f"""
            <div class="deck-slot-filled">
                <strong style="color:{cfg['color']};">{card['name']}</strong><br>
                <small>{cfg['label']} · {POWER_STARS[card['power']]}</small>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="deck-slot">빈 슬롯</div>', unsafe_allow_html=True)

    if selected_count > 0:
        st.markdown("---")
        attack = sum(1 for c in selected_cards_data if c["type"] == "attack")
        defense = sum(1 for c in selected_cards_data if c["type"] == "defense")
        special = sum(1 for c in selected_cards_data if c["type"] == "special")
        avg_power = sum(c["power"] for c in selected_cards_data) / selected_count

        st.markdown("**덱 분석**")
        st.markdown(f"⚔️ 공격: {attack}장 · 🛡️ 방어: {defense}장 · ✨ 특수: {special}장")
        st.markdown(f"평균 파워: {avg_power:.1f} {POWER_STARS[round(avg_power)]}")

        if selected_count == 8:
            st.success("덱 완성! 토론 준비 완료!")
            if st.button("🎯 토론 시작", type="primary", use_container_width=True):
                st.balloons()
                st.info("선택한 카드를 활용하여 강력한 토론을 펼치세요!")
