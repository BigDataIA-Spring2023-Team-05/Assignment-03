import requests
import streamlit as st
from streamlit_extras.switch_page_button import switch_page


## 
def fetch(session, url):
    try:
        result = session.get(url)
        return result.json()
    except Exception:
        return {}

# Create an empty container
placeholder = st.empty()
placeholder_2 = st.empty()
placeholder_3 = st.empty()
placeholder_4 = st.empty()
placeholder_5 = st.empty()
# submit = False
# submit_2 = False
# submit_3 = False
# submit_4 = False
# submit_5 = False
# if 'submit_2' not in st.session_state:
#     st.session_state['submit_2'] = False
# if 'submit_3' not in st.session_state:
#     st.session_state['submit_3'] = False
# if 'submit_4' not in st.session_state:
#     st.session_state['submit_4'] = False
# if 'submit_5' not in st.session_state:
#     st.session_state['submit_5'] = False
# if st.session_state.get('submit_5') != True:

#     st.session_state['submit_2'] = submit_2

# if st.session_state.get('submit_3') != True:
#     st.session_state['submit_3'] = submit_3

# if st.session_state.get('submit_4') != True:
#     st.session_state['submit_4'] = submit_4

# if st.session_state.get('submit_5') != True:
#     st.session_state['submit_5'] = submit_5
# var = False
# var_2 = False
# var_3 = False
# var_4 = False
# var_5 = False
actual_email = "admin"
actual_password = "admin"
session = requests.Session()

# Insert a form in the container
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = False
if 'forgot_status' not in st.session_state:
    st.session_state['forgot_status'] = False
if 'reg_status' not in st.session_state:
    st.session_state['reg_status'] = False
if st.session_state["authentication_status"] == False:
    with placeholder.form("login"):
        var = True
        # var_2 = True
        # var_3 = True
        # var_4 = True
        # var_5 = True
        st.markdown("#### Enter your credentials")
        username = st.text_input("UserName")
        password = st.text_input("Password", type="password")
        column_1,column_2,column_3 = st.columns([1,6,1.75])
        with column_1:
            submit = st.form_submit_button("Login")
            
        with column_2:
            submit_3 = st.form_submit_button("Register")
        with column_3:
            submit_2 = st.form_submit_button("Forgot Password")
            
    # if st.button    
        if submit_2:
            st.session_state['forgot_status'] = True
            switch_page('Forgot_password')
        if submit_3:
            st.session_state['reg_status'] = True
            switch_page('Register')


    # if st.session_state['submit_2']: 
    #     placeholder_2.empty()
    #     # var = True
    #     # var_2 = True
    #     # var_3 = True
    #     # var_4 = True
    #     # var_5 = True
    #     with placeholder_2.form("forgot"):    
    #         # placeholder.empty()
    #         # with placeholder.form("Forgot_Password"):
    #         f_email = st.text_input("Please enter your email")
    #         submit_3 = st.form_submit_button("Send OTP")
    #         print("submit_3  "+str(submit_3))
    #         if submit_3:

    #             st.session_state['submit_3'] = True
    #             # var_3 = True
    #             # var_2 = True

    # if st.session_state['submit_3']:
    #     with placeholder_3.form("otp"): 
    #         print("send otp button working")
    #         otp = st.text_input("Enter verfication OTP")
    #         submit_4 = st.form_submit_button("Verify")
    #         if submit_4:
    #             st.session_state['submit_4'] = True
    # if st.session_state['submit_4']:
    #     with placeholder_4.form("password"): 
    #         password = st.text_input("Password", type="password")
    #         confirm_password = st.text_input("Confirm Password", type="password")
    #         submit_5 = st.form_submit_button("Done")
    #         if submit_5:
    #           st.session_state.done = True  
    # if st.session_state.done:
    #     st.success("Password changed") 



    if submit:
        # If the form is submitted and the email and password are correct,
        # clear the form/container and display a success message
        placeholder.empty()
        url = 'http://backend:8000/user/login'
        myobj = {'username': username ,'password': password }
        x_status = requests.post(url, data = myobj).status_code
        # print(x_status)
        st.write(x_status)
        if x_status == 200:
            x = requests.post(url, data = myobj).json()    
            st.success("Login successful")
            log_username = x['username']
            log_token = x['access_token']
            # goes_ui.goes_ui()

            # print(log_username)
            # print(log_token)
        # Initialization of session state:
        
            st.session_state["authentication_status"] = log_token
            st.success("Login successful") 
            st.write(x)
            # if logout:
            #     st.session_state["authentication_status"] == False
            #     placeholder.empty()
        elif x_status == 404 or x_status == 401:
            # if 'shared' not in st.session_state:
            st.session_state["authentication_status"] == False
            st.error("Login failed ... Invalid credentials")
        # if st.session_state["authentication_status"] == log_token:
        #     st.success("Login successful") 
        # else:
        #     pass
else:
    st.header("User logged in Successfully")
    logout = st.button("Log Out")
    if logout:
        st.session_state["authentication_status"] == False
        st.header("Logged Out Successfully")
# if st.session_state["authentication_status"]:
#     authenticator.logout('Logout', 'main')
#     st.write(f'Welcome *{st.session_state["name"]}*')
#     st.title('Some content')
# elif st.session_state["authentication_status"] == False:
#     st.error('Username/password is incorrect')
# elif st.session_state["authentication_status"] == None:
#     st.warning('Please enter your username and password')


