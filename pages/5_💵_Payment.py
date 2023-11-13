import logging
import streamlit as st
from pymongo import MongoClient
import time
import database
import random
def generate_unique_code():
    # Generate a random number between 100 and 999
    return str(random.randint(100, 999))
# Function to display the payment page
def display_payment_page():
    # Razorpay payment link
    payment_link = "https://rzp.io/l/3FTyewKI8f"
    if 'waiting_for_payment' not in st.session_state:
        st.session_state.waiting_for_payment = False
    # Displaying the payment button
    if st.button('Pay Now'):
        
        # Open the payment link in a new tab
        unique_code = generate_unique_code()
        st.markdown(f"<a href='{payment_link}?unique_code={unique_code}' target='_blank'>Click here to complete the payment</a>", unsafe_allow_html=True)
        # Set a flag indicating the payment process has started
        st.session_state['waiting_for_payment'] = True

        # Redirect to the payment page
        while st.session_state['waiting_for_payment']==True:
            st.info("⏳ Waiting for payment...")
            time.sleep(1)

   

# Initialize session state for payment waiting


# Check if the user is logged in
if st.session_state.get("user_logged_in"):
    display_payment_page()
else:
    st.error("⚠️ You need to log in to access this feature. Please log in. ⚠️")
