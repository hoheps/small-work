import imaplib
import re

def email_read():
    with open('cred', 'r') as f:
        cred = f.read().split('\n')
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    # allow less secure apps from google if it fails with '[AUTHENTICATIONFAILED] Invalid credentials (Failure)'
    mail.login(cred[0]+"@gmail.com",cred[1])
    mail.select('inbox','readonly')
    # search strings for this file
    type, data = mail.search(None, cred[2], cred[3], cred[4])
    # chooses latest email
    i = data[0].split()[-1] 
    typ, data = mail.fetch(i, '(RFC822)' )
    # cred[5] is the regex formula 
    output = re.search(cred[5],str(data[0][1])).group()
    mail.close()
    mail.logout()
    return output
