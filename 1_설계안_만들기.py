import streamlit as st
from openai import OpenAI

# OpenAI API 키 설정
client = OpenAI(api_key=st.secrets["OPENAI"]["OPENAI_API_KEY"])

def request_chat_completion(
    prompt,
    system_role="당신은 교수학습 설계에 능숙한 베테랑 교사입니다. 언급된 AI 디지털교과서의 기능들을 반영하여 해당 교과의 수업 설계안을 작성합니다. 수업 설계안을 작성할 때에는 도입, 전개, 마무리로 구분하여 작성하세요.",
    model="gpt-4o",
    stream=False
):
    messages = [
        {"role": "system", "content": system_role},
        {"role": "user", "content": prompt},
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=stream
    )
    return response

st.set_page_config(
    page_title="GPT API를 활용한 챗봇",
    page_icon="🎇"
)

st.title("GPT-4를 활용한 설계안 만들어보기")
st.subheader("AI를 활용하여 설계안을 만들어봅시다")
with st.form("form"):
    st.text("과목, 단원, 수업주제를 입력해주세요")
    col1, col2, col3 = st.columns(3)
    with col1:
        subjects = st.text_input("과목")
    with col2:
        units = st.text_input("단원")
    with col3:
        topics = st.text_input("수업주제")
    
    st.text("포함하고 싶은 AIDT의 기능을 최대 3개까지 입력해주세요")
    col4, col5, col6 = st.columns(3)
    with col4:
        keyword_1 = st.text_input("AIDT 기능 1")
    with col5:
        keyword_2 = st.text_input("AIDT 기능 2")
    with col6:
        keyword_3 = st.text_input("AIDT 기능 3")
    
    submit = st.form_submit_button("Submit")
    
    if submit:
        with st.spinner("설계안을 생성 중입니다!"):
            prompt = f"수업시간은 50분이야. 과목: {subjects}\n단원명: {units}\n수업주제: {topics}\n포함하고 싶은 AI 디지털 교과서 기능: {keyword_1}, {keyword_2}, {keyword_3}"
            response = request_chat_completion(
                prompt=prompt,
                stream=False
            )
        st.success("제출 완료!")
        st.write(response.choices[0].message.content)
