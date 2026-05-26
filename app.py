import streamlit as st
import random

# 페이지 설정
st.set_page_config(
    page_title="연애 코칭 앱",
    page_icon="💖",
    layout="centered"
)

# 제목
st.title("💖 연애 코칭 웹앱")
st.write("연애 고민을 입력하면 코칭 답변을 해주는 앱입니다!")

# 사용자 입력
name = st.text_input("이름 또는 닉네임")

situation = st.selectbox(
    "현재 상황을 선택하세요",
    [
        "짝사랑",
        "썸",
        "연애 중",
        "이별",
        "재회 고민"
    ]
)

tone = st.radio(
    "답변 말투 선택",
    ["다정한 스타일", "친구 스타일", "현실 조언 스타일"]
)

problem = st.text_area("연애 고민을 자세히 적어보세요")

# 코칭 함수
def generate_coaching(situation, tone, problem):
    
    if not problem.strip():
        return "고민 내용을 입력해주세요!"

    intro_dict = {
        "다정한 스타일": [
            "많이 고민됐겠다.",
            "그 상황이면 충분히 힘들 수 있어.",
            "네 마음이 이해돼."
        ],
        "친구 스타일": [
            "오 이거 꽤 복잡한데?",
            "솔직히 신경 많이 쓰일 듯.",
            "그 마음 완전 이해감."
        ],
        "현실 조언 스타일": [
            "냉정하게 보면 중요한 건 행동이야.",
            "감정보다 상황 판단도 필요해.",
            "상대 반응을 잘 보는 게 중요해."
        ]
    }

    advice_dict = {
        "짝사랑": "상대에게 조금씩 자연스럽게 다가가보는 게 좋아.",
        "썸": "너무 조급해하지 말고 대화 흐름을 편하게 이어가봐.",
        "연애 중": "감정보다 솔직한 대화가 가장 중요해.",
        "이별": "억지로 잊으려 하기보다 시간을 주는 게 좋아.",
        "재회 고민": "재회 전에 왜 멀어졌는지 먼저 돌아보는 게 중요해."
    }

    ending_dict = {
        "다정한 스타일": "너 자신을 너무 힘들게 하지 않았으면 좋겠어 💖",
        "친구 스타일": "너무 혼자 끙끙 앓지 마!",
        "현실 조언 스타일": "결국 중요한 건 건강한 관계야."
    }

    intro = random.choice(intro_dict[tone])
    advice = advice_dict[situation]
    ending = ending_dict[tone]

    result = f"""
{intro}

현재 상황: {situation}

내 조언:
{advice}

추가로 보면,
{problem[:80]}...

{ending}
"""

    return result

# 버튼
if st.button("코칭 받기 💌"):

    if not name.strip():
        st.warning("이름 또는 닉네임을 입력해주세요!")
    else:
        answer = generate_coaching(situation, tone, problem)

        st.success(f"{name}님을 위한 연애 코칭 결과")
        st.write(answer)

# 하단
st.divider()
st.caption("Made with Streamlit 💖")
