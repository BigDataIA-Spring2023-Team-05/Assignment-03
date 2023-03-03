import streamlit as st
placeholder = st.empty()
var = True
if 'forgot_status' not in st.session_state:
    st.session_state['forgot_status'] = False
if 'done_status' not in st.session_state:
    st.session_state['done_status'] = False
if st.session_state['forgot_status'] == False and st.session_state['done_status'] == False:
    st.markdown("#### Please Use the Login Screen")
elif st.session_state['forgot_status'] == True and st.session_state['done_status'] == False:
    
    # st.markdown("#### Enter your credentials")
    with placeholder.form("forgot"):    
    #         # placeholder.empty()
    #         # with placeholder.form("Forgot_Password"):
            f_email = st.text_input("Please enter your email")
            submit_3 = st.form_submit_button("Send OTP")
            
            if submit_3:
                var = False
                otp = st.text_input("Please enter your OTP")
                password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                submit_3 = st.form_submit_button("Confirm")
                st.session_state['done_status'] = True
if st.session_state['done_status'] == True and var == True:
         st.success("Password changed")
                # if submit_4:
                #      st.success("Password changed")
    #             st.session_state['submit_3'] = True
    #             # var_3 = True
    #             # var_2 = True
