# Secure Login System

A command-line login system in Python that shows basic
authentication and access control ideas.

## How to run
python main.py

## Features
- Register with a username, password and role (admin or user)
- Passwords are stored as salted PBKDF2-SHA256 hashes, never as plain text
- Role-based access: admins can view all users, normal users cannot
- Account locks after 3 wrong password attempts

## Tools
Python (hashlib, json, os, getpass)
