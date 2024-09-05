#!/usr/bin/env python3
""" Main 5
"""
import uuid
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user import User

sa = SessionExpAuth()

user = User()
user.email = "bobsession@hbtn.io"
user.password = "fake pwd"
user.save()

print("User with ID: {} has a Session ID: {}".format(user.id, sa.create_session(user.id)))

print("---")

session_id = str(uuid.uuid4())
token = sa.create_session(user.id)

print("User with ID: {} has a Session ID: {}".format(user.id, token))

print("---")

user_id = sa.user_id_for_session_id(token)
print("User ID for Session ID {}: {}".format(token, user_id))

print("---")

import time
time.sleep(6)  # 6 seconds
user_id = sa.user_id_for_session_id(token)
print("User ID for Session ID {} after 6 seconds: {}".format(token, user_id))

print("---")

time.sleep(10)  # 10 seconds
user_id = sa.user_id_for_session_id(token)
print("User ID for Session ID {} after 10 seconds: {}".format(token, user_id))
