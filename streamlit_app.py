import streamlit as st 
import requests 
import datetime 

import sys 

BASE_URL='http://127.0.0.1:8000' # backend end point 

st.set_page_config(
    page_title='Travel Planner Agentic Application',
    page_icon='',
    layout='centered',
    initial_sidebar_state='expanded'
)

st.title('UTD International Student Assistant')

if 'messages' not in st.session_state:
    st.session_state.messages=[]

# display chat history 
st.header('How can i help you? I can help you in housing, transportation, groceries and legal requirements')

with st.form(key='query_form',clear_on_submit=True):
    user_input=st.text_input('User Input',placeholder='e.g. what are some good restaurents near UTD')
    submit_button=st.form_submit_button('send')

if submit_button and user_input.strip():
    try:
        with st.spinner('Bot is thinking ...'):
            payload={'question':user_input}
            response=requests.post(f'{BASE_URL}/query',json=payload)
        if response.status_code==200:
            answer=response.json().get('answer','No answer returned')
            markdown_content=f""" 
                UTD Assistant response

                # **Generated:** {datetime.datetime.now().strftime('%Y-%m-%d at %H:%M')}
                # **Created by:** UTD assistant agent

                --- 
                {answer}

                --- 

                **
                """ 
            st.markdown(markdown_content)
        else:
            st.error('Bot failed to respond:'+response.text)

    except Exception as e:
        raise f'The response failed due to {e}'

