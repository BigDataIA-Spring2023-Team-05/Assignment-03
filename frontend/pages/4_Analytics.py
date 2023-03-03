import datetime
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import streamlit as st
import requests
import plotly.express as px

if 'user_status' not in st.session_state:
    st.session_state['user_status'] = 1  ## 1 for Admin and 2 for User
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = False
if "visibility" not in st.session_state:
    st.session_state.visibility = "hidden"
    st.session_state.disabled = False

## Inputs
data = pd.read_csv("user_data.csv")
hours = [str(x).zfill(2) for x in range(24)]

print(data)
if st.session_state['user_status']== 1:
    st.subheader("Daily API calls per User")
    column_1,column_2,column_3 = st.columns(3)
    with column_1:
        user = st.selectbox(
        "Select the User",
        data['Name'],
        label_visibility="visible",
        disabled=st.session_state.disabled,
        key = "Plotly_1")
    with column_2:
        d1 = st.date_input(
        "Select the date",
        # value = datetime.date(2022, 7, 28),
        min_value= datetime.date(2023, 2, 28), max_value=datetime.date.today(),key = "d1")
    with column_3:
        st.caption('Search')
        if st.button("GO"):
           st.session_state.visibility = "visible" 
        else:
            st.write(' ')
    if st.session_state.visibility == "visible":
        fig_admin_requests = go.Figure()
        df_count = data.groupby('user')['TimeFrame'].count()  #group by date and user and count the number of requests
        fig_admin_requests = px.line(df_count, x='hours', y='endpoint', color='user', title='Request Count by User') #plot the line chart
        st.plotly_chart(fig_admin_requests)
    st.subheader("Total API calls the previous day")
    variable_output = '10'
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
    variable_output_1 = '100'
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
        variable_output_2 = '150'
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
        variable_output_3 = '100'
        html_str_3 = f"""
        <style>
        p.a {{
        font: bold 25px red;
        }}
        </style>
        <p class="a">{variable_output_3}</p>
        """
        st.markdown(html_str_3, unsafe_allow_html=True)

    st.subheader("Each endpoint total number of calls")
    column_1,column_2,column_3 = st.columns(3)
    with column_1:
        user = st.selectbox(
        "Select the User",
        data['Name'],
        label_visibility="visible",
        disabled=st.session_state.disabled,)
    with column_2:
        d2 = st.date_input(
        "Select the date",
        # value = datetime.date(2022, 7, 28),
        min_value= datetime.date(2023, 2, 28), max_value=datetime.date.today(),key = "d2")
    with column_3:
        st.caption('Search')
        if st.button("GO", key = "go1"):
            variable_output_4 = '100'
            html_str_4 = f"""
            <style>
            p.a {{
            font: bold 25px red;
            }}
            </style>
            <p class="a">{variable_output_4}</p>
            """
            st.markdown(html_str_4, unsafe_allow_html=True)
        else:
            st.write(' ')
  ########################################################
       
elif st.session_state['user_status']== 2:
    st.subheader("Daily API calls per User")
    
    # fig_user_requests = go.Figure()
    # df_count = data.groupby('user')['TimeFrame'].count()  #group by date and user and count the number of requests
    # fig_user_requests = px.line(df_count, x='hours', y='endpoint', color='user', title='Request Count by User') #plot the line chart
    # st.plotly_chart(fig_user_requests)
    st.subheader("Total API calls the previous day")
    variable_output = '10'
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
    variable_output_1 = '100'
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
        variable_output_2 = '150'
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
        variable_output_3 = '100'
        html_str_3 = f"""
        <style>
        p.a {{
        font: bold 25px red;
        }}
        </style>
        <p class="a">{variable_output_3}</p>
        """
        st.markdown(html_str_3, unsafe_allow_html=True)

    st.subheader("Each endpoint total number of calls")
    column_1,column_2,column_3 = st.columns(3)
    with column_1:
        user = st.selectbox(
        "Select the User",
        data['Name'],
        label_visibility="visible",
        disabled=st.session_state.disabled,)
    with column_2:
        d2 = st.date_input(
        "Select the date",
        # value = datetime.date(2022, 7, 28),
        min_value= datetime.date(2023, 2, 28), max_value=datetime.date.today(),key = "d2")
    with column_3:
        st.caption('Search')
        if st.button("GO", key = "go1"):
            variable_output_4 = '100'
            html_str_4 = f"""
            <style>
            p.a {{
            font: bold 25px red;
            }}
            </style>
            <p class="a">{variable_output_4}</p>
            """
            st.markdown(html_str_4, unsafe_allow_html=True)
        else:
            st.write(' ')



# clientLogs.put_log_events(      #logging to AWS CloudWatch logs
#     logGroupName = "assignment-03",
#     logStreamName = "ui",
#     logEvents = [
#         {
#         'timestamp' : int(time.time() * 1e3),
#         'message' : "User opened Dashboard page as admin"
#         }
#     ]
# )
# st.title("API Dashboard-Admin")
# st.markdown(
#     """
#     <style>
#         .title {
#             text-align: center;
#             color: #2F80ED;
#         }
#     </style>
#     <h2 class="title">View application API calls data through dashboard</h2>
#     <p></p>
#     """,
#     unsafe_allow_html=True,
# )

# header = {}
# header['Authorization'] = f"Bearer {st.session_state['access_token']}"
# response = requests.request("GET", f"{API_URL}/logs/admin", headers=header)  #call to relevant fastapi endpoint with authorization
# logs_resp = json.loads(response.text)   #store log responses from api

# if response.status_code == 200:
#     df_requests = pd.DataFrame({
#     'timestamp': logs_resp['timestamp'].values(),   
#     'user': logs_resp['user'].values(),
#     'endpoint': logs_resp['endpoint'].values(),
#     'response': logs_resp['response'].values(),

#     }, index = np.arange(len(logs_resp['timestamp'].values()))) #set values from log response api
#     df_requests["timestamp"] = pd.to_datetime(df_requests["timestamp"]) #cover timestamp

#     #display dashboard options
#     options = ['User Requests', 'Total API calls yesterday', 'Avg Calls Last Week', 'Success vs Failed Calls', 'Endpoint Calls']
#     choice = st.sidebar.selectbox('Select option', options)
    
#     if choice == 'User Requests':
#         #creating figure for Plotting a line chart of count of request by each user against time (date)
#         fig_user_requests = go.Figure()
#         for user in df_requests['user'].unique():
#             df_count = df_requests.groupby([pd.Grouper(key='timestamp', freq='D'), 'user']).count()['endpoint'].reset_index()   #group by date and user and count the number of requests
#             fig_user_requests = px.line(df_count, x='timestamp', y='endpoint', color='user', title='Request Count by User') #plot the line chart
    
#         st.plotly_chart(fig_user_requests)  #display as plotly chart

#     elif choice == 'Total API calls yesterday':
#         #creating Metric for total API calls the previous day
#         now = datetime.now()
#         yesterday = (now - timedelta(days=1)).date()
#         previous_day_df = df_requests.loc[df_requests["timestamp"].dt.date == yesterday]    #filter logs for all events yesterday
#         total_calls_yesterday = previous_day_df["endpoint"].count()     #get the total number of API calls
        
#         st.metric('Total API Calls (previous day)', total_calls_yesterday)  #display metric

#     elif choice == 'Avg Calls Last Week':
#         #creating Metric to show total average calls during the last week
#         today = datetime.now().date()
#         one_week_ago = today - timedelta(days=7)
#         last_week_df = df_requests.loc[(df_requests["timestamp"].dt.date >= one_week_ago) & (df_requests["timestamp"].dt.date <= today)]    #filter the dataframe for the last week
#         total_calls_last_week = last_week_df["endpoint"].count()     #calculate the total number of API calls during the last week
#         days_in_last_week = (today - one_week_ago).days     #calculate the number of days in the last week
#         average_calls_per_day_last_week = total_calls_last_week / days_in_last_week #calculate the average number of API calls per day during the last week
        
#         st.metric('Avg Calls Last Week', average_calls_per_day_last_week)   #display metric

#     elif choice == 'Success vs Failed Calls':
#         #doing Comparison of Success ( 200 response code) and Failed request calls(ie non 200 response codes)
#         num_success = len(df_requests[df_requests['response'] == '200'])    #filter for success code 200 records
#         num_failed = len(df_requests) - num_success     #all others are failed calls

#         st.metric('Successful Calls', num_success)  #display metric
#         st.metric('Failed Calls', num_failed)   #display metric

#     elif choice == 'Endpoint Calls':
#         #creating figure for Each endpoint total number of calls
#         fig_endpoint_calls = go.Figure()
#         fig_endpoint_calls = px.histogram(df_requests, x='endpoint', title='Total Number of Calls per Endpoint')
#         fig_endpoint_calls.update_layout(xaxis_title='Endpoint', yaxis_title='Number of Calls')
#         endpoint_calls_total = len(df_requests) #also display overall call count
        
#         st.plotly_chart(fig_endpoint_calls) #display as plotly chart
#         st.metric('Total endpoint calls', endpoint_calls_total) #display metric
    
# else: #elif response.status_code == 401:   #when token is not authorized
#     st.error("Session token expired, please login again")   #display error
#     clientLogs.put_log_events(      #logging to AWS CloudWatch logs
#         logGroupName = "assignment-03",
#         logStreamName = "api",
#         logEvents = [
#             {
#             'timestamp' : int(time.time() * 1e3),
#             'message' : "API endpoint: /logs/admin\n Called by: " + st.session_state['username'] + " \n Response: 401 \nSession token expired"
#             }
#         ]
#     )
#     st.stop()
