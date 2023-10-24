import random
from pymongo import MongoClient
from datetime import datetime
from PIL import Image
import requests
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import time
import database
from database import get_user_data, update_user
import pytz
import streamlit as st
#####################################################################################################################################################
from streamlit.components.v1 import html

@st.cache_resource(ttl=1200)
def get_users_collection():
    users_collection = database.users_collection
    return users_collection

def nav_page(page_name, timeout_secs=3):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    html(nav_script)


def send_otp():
    pass
    #a function to actually send the otp

# Call the function with the OTP
im = Image.open('icon.png')
st.set_page_config(page_title="SOP Generator", page_icon=im)
if 'gen_button' not in st.session_state:
    st.session_state.disabled = True
st.header("Sign In")
username = st.text_input("Name")
phone_number = st.text_input("Mobile Number", placeholder="9631331342")
if username is not None and phone_number is not None:
    st.session_state.disabled = False
generate_otp = st.button("Generate OTP", disabled=st.session_state.disabled, key='gen_button')

if st.session_state.get('button') != True:
    st.session_state['button'] = generate_otp
    st.session_state.disabled = True

if st.session_state['button'] == True:
    st.session_state.disabled = True
    if len(phone_number) != 10 or phone_number is None:
        st.error("Sorry, not a valid phone number")
        st.session_state.disabled = False
        time.sleep(1)
        st.experimental_rerun()
    else:
        users_collection = get_users_collection()
        if username in [user['username'] for user in users_collection.find()] and phone_number in [user['phone_number']
                                                                                                   for user in
                                                                                                   users_collection.find()]:
            otp = st.text_input("OTP")
            generated_otp = str(random.randint(1000, 9999))
            send_otp(phone_number, generated_otp)
            if st.button('Login'):
                if otp == "1234":
                    st.success("Logged in Successfully.")
                    st.session_state.user_logged_in = True
                    st.session_state.user_id = str(get_user_data(username)['_id'])
                    print(st.session_state.user_id)
                    ist = pytz.timezone('Asia/Kolkata')
                    time.sleep(2)

                    update_user(username=username,
                                data={"last_logged_in": datetime.now(ist).strftime("%A,%d %B %Y - %H:%M:%S")})
                    import os
                    os.rename(r'pages/2_🔑_Sign_In.py', r'lages/2_🔑_Sign_In.py')
                    os.rename(r'lages/2_🔑_Sign_Out.py', r'pages/2_🔑_Sign_Out.py')
                    nav_page("")

                else:
                    st.error("Invalid OTP")
                    st.session_state.disabled = False
                    time.sleep(1)
                    st.experimental_rerun()
        else:
            st.error("Invalid User")
            st.session_state.disabled = False
            time.sleep(1)
            st.experimental_rerun()
