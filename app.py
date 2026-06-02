import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="달콤살벌 연애상담소", page_icon="💖")
st.title("💖 달콤살벌 연애상담소")
st.caption("연애 고민, 썸, 이별... 혼자 앓지 말고 Gemini에게 물어보세요!")

# 2. Streamlit Secrets에서 API 키 불러오기 및 설정
try:
    # Streamlit Secrets에 저장된 키를 가져옵니다.
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("API 키를 찾을 수 없습니다. Streamlit Secrets 설정을 확인해주세요.")
    st.stop()

# 3. 세션 상태(Session State)로 채팅 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
    # 챗봇에게 연애 상담사라는 페르소나(역할)를 부여하는 초기 시스템 프롬프트 (선택사항)
    st.session_state.system_instruction = (
        "당신은 공감 능력이 뛰어나고 때로는 뼈 때리는 조언도 아끼지 않는 전문 연애 상담사입니다. "
        "사용자의 연애 고민에 대해 친근하고 따뜻한 말투로 조언해 주세요."
    )

# 4. 기존 대화 기록 화면에 출력
for message in st.secrets.get("messages", st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. 사용자 입력 받기
if prompt := st.chat_input("연애 고민을 입력하세요... (예: 썸남이 선톡을 안 해요)"):
    # 사용자 메시지를 화면에 표시 및 세션에 저장
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 6. Gemini 모델을 통한 답변 생성 및 오류 처리
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🤔 고민을 분석 중입니다...")
        
        try:
            # gemini-2.5-flash-lite 모델 로드
            model = genai.GenerativeModel(
                model_name="gemini-2.5-flash-lite",
                system_instruction=st.session_state.system_instruction
            )
            
            # Gemini 대화 형식으로 기존 기록 변환 (role 변환 필요: user -> user, assistant -> model)
            chat_history = []
            for msg in st.session_state.messages[:-1]: # 현재 입력 제외한 이전 기록
                role = "user" if msg["role"] == "user" else "model"
                chat_history.append({"role": role, "parts": [msg["content"]]})
            
            # 멀티턴 대화 시작
            chat = model.start_chat(history=chat_history)
            
            # 답변 요청
            response = chat.send_message(prompt)
            full_response = response.text
            
            # 화면에 최종 답변 출력 및 세션에 저장
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            # API 호출 중 에러 발생 시 처리
            error_msg = f"죄송합니다. 답변을 생성하는 중 오류가 발생했습니다. (에러 내용: {str(e)})"
            message_placeholder.markdown(error_msg)
            # 에러 메시지는 세션 기록에 넣지 않음
