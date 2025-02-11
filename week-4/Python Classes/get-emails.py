import imaplib
import email
import json
import os
import pickle

class GmailDownloader:
    def __init__(self, email_address, password):
        self.email_address = email_address
        self.password = password
        self.download_dir='attachments'
        self.mail = None
        try:
            self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
            self.mail.login(self.email_address, self.password)
        except Exception as e:
            print(f"Connection error: {str(e)}")
            return
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

    def get_word_and_line_count(self, body):
        lines = body.split('\n')
        words = body.split()
        return len(words), len(lines)

    def process_attachments(self, msg):
        attachments = []
        has_image = False
        
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            if part.get_content_type().startswith('image/'):
                has_image = True
            filename = part.get_filename()
            if filename:                
                filepath = os.path.join(self.download_dir, filename)
                with open(filepath, 'wb') as f:
                    f.write(part.get_payload(decode=True))
                attachments.append(filename)
                
        return attachments, has_image

    def download_emails(self, options, max_emails=2):
        self.mail.select('inbox')
        
        _, messages = self.mail.search(None, 'ALL')
        emails = {}
        
        for num in messages[0].split()[::-1]:
            if len(emails)>=max_emails:
                break
            _, msg_data = self.mail.fetch(num, '(RFC822)')
            email_body = msg_data[0][1]
            msg = email.message_from_bytes(email_body)
            attachments, has_image = self.process_attachments(msg)
            
            if options["has_attachments"] and len(attachments)==0:
                continue

            if options["picture_attached"] and not has_image:
                continue

            if options["domain"] and options["domain"] not in msg["from"]:
                continue

            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        break
            else:
                body = msg.get_payload(decode=True).decode()
            
            
            word_count, line_count = self.get_word_and_line_count(body)
            
            email_data = {
                "subject": msg["subject"],
                "date": msg["date"],
                "from": msg["from"],
                "word_count": word_count,
                "line_count": line_count,
                "attachment_count": len(attachments),
                "attachments": attachments
            }
            emails[str(num)] = email_data
        
        with open("emails.json", 'w', encoding='utf-8') as f:
            json.dump(emails, f, indent=2)
        
        with open("Emails.pickle", 'wb') as f:
            pickle.dump(emails, f)
        
        self.mail.close()
        self.mail.logout()
        return True

if __name__ == "__main__":

    options = {
        "has_attachments":True,
        "domain": "@tothenew.com",
        "picture_attached": True
    }

    with open('.creds', 'r') as creds:
        lines = creds.readlines()
        EMAIL = lines[0].strip()
        PASSWORD = lines[1].strip()
        

    GmailDownloader(EMAIL, PASSWORD).download_emails(options)