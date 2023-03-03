import streamlit as st
from PIL import Image

st.title("New User Registration")

# Create an empty container
placeholder = st.empty()


# Input Fields

with st.form("my_form"):     
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    # Checkbox for agreeing to terms
    agree_to_terms = st.checkbox("I agree to the terms and conditions")
    submitted = st.form_submit_button("Submit")

  
# Validation logic
if submitted:
    if not first_name:
        st.warning("Please enter your first name")
    elif not last_name:
        st.warning("Please enter your last name")
    elif not email:
        st.warning("Please enter your email")
    elif not password:
        st.warning("Please enter your password")
    elif password != confirm_password:
        st.warning("Passwords do not match")
    elif not agree_to_terms:
        st.warning("Please agree to the terms and conditions")
    else:
        st.success("Registration successful!")



# creating three columns
column_1,column_2,column_3 = st.columns(3)

#displaying an image in each column
with column_1:
    st.image("/Users/krishicagopalakrishnan/Downloads/free-membership.png")
    #image address(https://eztechassist.com/wp-content/uploads/2018/04/FREE-Membership-green-01-1.png)
    st.write('Click here for more info on the free membership ')
    if st.button("Join as a free member"): 
        st.write("You're a free member!")


with column_2:
    st.image("/Users/krishicagopalakrishnan/Downloads/Silver-Membership.png")
    #image address(https://www.sicklecelldisease.org/wp-content/uploads/2019/01/Silver-Membership.png)
    st.write('Click here for more info on the Gold membership details')
    if st.button("Join as a gold member"): 
        st.write("You're a Gold member!")

with column_3:
    st.image("/Users/krishicagopalakrishnan/Downloads/Gold-Membership.png")
    #image address(https://www.sicklecelldisease.org/wp-content/uploads/2019/01/Gold-Membership.png)
    st.write('Click here for more info on the Silver membership details')
    if st.button("Join as a silver member"): 
        st.write("You're a Silver member!")

    


