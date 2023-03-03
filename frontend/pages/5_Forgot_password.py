import streamlit as st
import requests
placeholder = st.empty()
var = True
if 'forgot_status' not in st.session_state:
    st.session_state['forgot_status'] = False
if 'status_code' not in st.session_state:
    st.session_state['status_code'] = 0
if 'done_status' not in st.session_state:
    st.session_state['done_status'] = False
if st.session_state['forgot_status'] == False and st.session_state['done_status'] == False:
    st.markdown("#### Please Use the Login Screen")
placeholder.empty()
if st.session_state['done_status'] == True:
        #  placeholder.empty()
         st.success("Password changed")
elif st.session_state['forgot_status'] == True and st.session_state['done_status'] == False:
    
    # st.markdown("#### Enter your credentials")
    with placeholder.form("forgot"):    
            # placeholder.empty()
    #         # with placeholder.form("Forgot_Password"):
            if st.session_state['done_status'] == True:
                st.success("Password changed")
            f_email = st.text_input("Please enter your email")
            submit = st.form_submit_button("Send OTP")
            if submit:
                url = 'http://backend:8000/user/forgot-password'
                myobj = {'email': f_email}
        
                check = requests.post(url, json = myobj)
                print(check)
            otp = st.text_input("Please enter your OTP")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit_2 = st.form_submit_button("Confirm")
            if submit_2:
                st.session_state['done_status'] = True
                url = 'http://backend:8000/user/reset-password'
                myobj = {'email': f_email ,'otp': otp, 'new_password' : password,'confirm_password': confirm_password}
                result = requests.post(url, json = myobj)
                print(result)
                st.session_state['status_code'] = result.status_code
                if st.session_state['status_code'] == 201:
                        st.session_state['done_status'] == True
                        st.success("Password changed")
                elif st.session_state['status_code'] == 422:
                        st.error("Invalid OTP or password match")
                     

                # if submit_4:
                #      st.success("Password changed")
    #             st.session_state['submit_3'] = True
    #             # var_3 = True
    #             # var_2 = True
