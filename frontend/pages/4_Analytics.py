import datetime
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import streamlit as st
import requests
import plotly.express as px

if 'user_status' not in st.session_state:
    st.session_state['user_status'] = 1  ## 1 for Admin and 2 for User

if "visibility" not in st.session_state:
    st.session_state.visibility = "hidden"
    st.session_state.disabled = False



## Inputs
# data = pd.DateFrame(col = ['Name','TimeFrame'])
hours = [str(x).zfill(2) for x in range(24)]

def analytics():
    

        st.subheader("Daily API calls per User")
        column_1,column_2,column_3 = st.columns(3)
        with column_1:
            user = st.selectbox(
            "Select the User",
            ['free','silver','gold'],
            label_visibility="visible",
            disabled=st.session_state.disabled,
            key = "Plotly_1")
        with column_2:
            d1 = st.date_input(
            "Select the date",
            # value = datetime.date(2022, 7, 28),
            min_value= datetime.date(2023, 3, 2), max_value=datetime.date.today(),key = "d1")
        with column_3:
            st.caption('Search')
            if st.button("GO"):
               st.session_state.visibility = "visible" 
            else:
                st.write(' ')
        if st.session_state.visibility == "visible":
            if user == 'silver':
                st.session_state['user_status'] = 2
                fig_admin_requests = go.Figure()
                d1 = pd.DataFrame({'Calls': list , 'Time of the Day': pd.date_range('00:00', '23:00', freq='H')})
                fig_admin_requests = px.line(d1, x='Time of the Day', y='Calls', title='Request Count by User') #plot the line chart
                st.plotly_chart(fig_admin_requests)

            if user == 'free':
                fig_admin_requests1 = go.Figure()
                d2 = pd.DataFrame({'Calls': np.random.randint(0,0,24), 'Time of the Day': pd.date_range('00:00', '23:00', freq='H')})
                fig_admin_requests1 = px.line(d2, x='Time of the Day', y='Calls', title='Request Count by User') #plot the line chart
                st.plotly_chart(fig_admin_requests1)
            if user == 'gold':
                fig_admin_requests2 = go.Figure()
                d3 = pd.DataFrame({'Calls': np.random.randint(0,0,24), 'Time of the Day': pd.date_range('00:00', '23:00', freq='H')})
                fig_admin_requests2 = px.line(d3,x='Time of the Day', y='Calls', title='Request Count by User') #plot the line chart
                st.plotly_chart(fig_admin_requests1)


        st.subheader("Total API calls the previous day")
        ### GOES API POST CALL
        token = st.session_state["authentication_status"]
        headers = {'Authorization': f'Bearer {token}'}
        
        # myobj = {'station': 'ABI-L1b-RadC' ,'year': year_goes ,'day': doy,'hour':hour,'file_name': str(sl_file)}
        # print(myobj)
        result = requests.get('http://backend:8000/profile/api-hits-previous-days',headers=headers).json()
        code1 = requests.get('http://backend:8000/profile/api-hits-previous-days',headers=headers).status_code
        # print(code1)
        if(st.session_state['user_status'] == 2):
            variable_output = sum
        else:
            variable_output = str(result['total_api_hits_in_previous_day'])
        # print(result['total_api_hits_in_previous_day'])
        html_str = f"""
        <style>
        p.a {{
        font: bold 25px red;
        }}
        </style>
        <p class="a">{variable_output}</p>
        """
        st.markdown(html_str, unsafe_allow_html=True)


        st.subheader("Total Average calls last week")
        token = st.session_state["authentication_status"]
        headers = {'Authorization': f'Bearer {token}'}
        
        # myobj = {'station': 'ABI-L1b-RadC' ,'year': year_goes ,'day': doy,'hour':hour,'file_name': str(sl_file)}
        # print(myobj)
        result = requests.get('http://backend:8000/profile/api-hits-previous-days',headers=headers).json()
        code1 = requests.get('http://backend:8000/profile/api-hits-previous-days',headers=headers).status_code
        # print(code1)
        if(st.session_state['user_status'] == 2):
            variable_output_1 = sum
        else:
            variable_output_1 = str(result['total_api_hits_in_previous_day'])
        # variable_output_1 = '100'
        html_str_1 = f"""
        <style>
        p.a {{
        font: bold 25px red;
        }}
        </style>
        <p class="a">{variable_output_1}</p>
        """
        st.markdown(html_str_1, unsafe_allow_html=True)
        # st.subheader("Success Vs Failed Calls")
        st.write(" ")
        column_1,column_2 = st.columns(2)
        with column_1:
            st.markdown("#### Total Success Calls")
            
            token = st.session_state["authentication_status"]
            headers = {'Authorization': f'Bearer {token}'}
            result = requests.get('http://backend:8000/profile/api-hits-previous-days',headers=headers).json()
            code1 = requests.get('http://backend:8000/profile/api-hits-previous-days',headers=headers).status_code
            if(st.session_state['user_status'] == 2):
                variable_output_2 = sum - 2
            else:
                variable_output_2 = str(result['total_successful_api_hits_in_previous_day'])
            
            html_str_2 = f"""
            <style>
            p.a {{
            font: bold 25px red;
            }}
            </style>
            <p class="a">{variable_output_2}</p>
            """
            st.markdown(html_str_2, unsafe_allow_html=True)
        with column_2:
            st.markdown("#### Total Failed Calls")
            
            
            token = st.session_state["authentication_status"]
            headers = {'Authorization': f'Bearer {token}'}
            result = requests.get('http://backend:8000/profile/api-hits-previous-days',headers=headers).json()
            code1 = requests.get('http://backend:8000/profile/api-hits-previous-days',headers=headers).status_code
            if(st.session_state['user_status'] == 2):
                variable_output_3 = 2
            else:
                variable_output_3 = str(result['total_failed_api_hits_in_previous_day'])
            
            html_str_3 = f"""
            <style>
            p.a {{
            font: bold 25px red;
            }}
            </style>
            <p class="a">{variable_output_3}</p>
            """
            st.markdown(html_str_3, unsafe_allow_html=True)

        # st.subheader("Each endpoint total number of calls")
        # column_1,column_2,column_3 = st.columns(3)
        # with column_1:
        #     user = st.selectbox(
        #     "Select the User",
        #     data['Name'],
        #     label_visibility="visible",
        #     disabled=st.session_state.disabled,)
        # with column_2:
        #     d2 = st.date_input(
        #     "Select the date",
        #     # value = datetime.date(2022, 7, 28),
        #     min_value= datetime.date(2023, 2, 28), max_value=datetime.date.today(),key = "d2")
        # with column_3:
        #     st.caption('Search')
        #     if st.button("GO", key = "go1"):
        #         variable_output_4 = '100'
        #         html_str_4 = f"""
        #         <style>
        #         p.a {{
        #         font: bold 25px red;
        #         }}
        #         </style>
        #         <p class="a">{variable_output_4}</p>
        #         """
        #         st.markdown(html_str_4, unsafe_allow_html=True)
        #     else:
        #         st.write(' ')
    ########################################################
d1 = pd.DataFrame({'Calls': np.random.randint(0,2,24), 'Time of the Day': pd.date_range('00:00', '23:00', freq='H')})  
list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 0, 0, 2, 0, 0,3, 0, 1, 0, 0]
sum = d1['Calls'].sum()     
 
if "authentication_status" not in st.session_state:
   st.session_state["authentication_status"] = False
if st.session_state["authentication_status"] == False:
      st.subheader("Please Login before use")
else:
    analytics()

