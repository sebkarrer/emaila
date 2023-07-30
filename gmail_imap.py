import imaplib
import email
from email.header import decode_header

# your email and password
username = "your-email@gmail.com"
password = "your-password"

# create an IMAP4 class with SSL 
mail = imaplib.IMAP4_SSL("imap.gmail.com")
# authenticate
mail.login(username, password)

# select the mailbox you want to delete in
# if you want SPAM, use "INBOX.SPAM"
mailbox = "INBOX"
mail.select(mailbox)

# get the latest email ID
result, data = mail.uid('search', None, "ALL")
latest_email_id = data[0].split()[-1]

# fetch the email body (RFC822) for the given ID
result, email_data = mail.uid('fetch', latest_email_id, '(BODY.PEEK[TEXT])')
raw_email = email_data[0][1].decode("utf-8")
email_message = email.message_from_string(raw_email)

# print the email body
print(email_message.get_payload())
