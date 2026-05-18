import sys
import os
import json
import resend
from typing import List

import webview

if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

HTML_PATH = os.path.join(BASE_DIR, 'Mailvoid.html')

# API keys mentesenek helye 
if getattr(sys, 'frozen', False):
    DATA_DIR = os.path.dirname(sys.executable)
else:
    DATA_DIR = BASE_DIR

KEYS_FILE = os.path.join(DATA_DIR, 'saved_keys.json')


def load_keys():
    if os.path.exists(KEYS_FILE):
        try:
            with open(KEYS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return []

def save_keys(keys):
    with open(KEYS_FILE, 'w', encoding='utf-8') as f:
        json.dump(keys, f, ensure_ascii=False, indent=2)


class MailAPI:

    # API key elmento
    def get_saved_keys(self):
        return json.dumps(load_keys())

    def save_key(self, payload_json: str):
        try:
            data = json.loads(payload_json)
            name = data.get('name', '').strip()
            key  = data.get('key', '').strip()
            if not name or not key:
                return json.dumps({'ok': False, 'error': 'Name and key required'})
            keys = load_keys()
            # Ha ugyanaz a nev akk a regit frissitjuk
            for k in keys:
                if k['name'] == name:
                    k['key'] = key
                    save_keys(keys)
                    return json.dumps({'ok': True})
            keys.append({'name': name, 'key': key})
            save_keys(keys)
            return json.dumps({'ok': True})
        except Exception as ex:
            return json.dumps({'ok': False, 'error': str(ex)})

    def delete_key(self, name: str):
        try:
            keys = load_keys()
            keys = [k for k in keys if k['name'] != name]
            save_keys(keys)
            return json.dumps({'ok': True})
        except Exception as ex:
            return json.dumps({'ok': False, 'error': str(ex)})

    # Kuldes script es errorok mert hat klari nincs itt hogy ne legyenek hibak a kuldesnel :(
    def send(self, payload_json: str):
        try:
            data = json.loads(payload_json)

            api_key      = data.get('apiKey', '').strip()
            sender_name  = data.get('senderName', '').strip()
            sender_email = data.get('senderEmail', '').strip()
            recipients   = data.get('recipients', [])
            subject      = data.get('subject', '').strip()
            html_body    = data.get('htmlBody', '').strip()
            attachments  = data.get('attachments', [])

            if not api_key:      return json.dumps({'ok': False, 'error': 'No API key'})
            if not sender_email: return json.dumps({'ok': False, 'error': 'No sender email'})
            if not recipients:   return json.dumps({'ok': False, 'error': 'No recipients'})
            if not subject:      return json.dumps({'ok': False, 'error': 'No subject'})
            if not html_body:    return json.dumps({'ok': False, 'error': 'Empty content'})

            resend.api_key = api_key
            from_field = f"{sender_name} <{sender_email}>" if sender_name else sender_email

            params: List[resend.Emails.SendParams] = []
            for recipient in recipients:
                p: resend.Emails.SendParams = {
                    'from': from_field,
                    'to': [recipient],
                    'subject': subject,
                    'html': html_body,
                }
                if attachments:
                    p['attachments'] = attachments
                params.append(p)

            if len(params) == 1:
                result = resend.Emails.send(params[0])
                email_ids = [result.get('id', '')]
            else:
                result = resend.Batch.send(params)
                if isinstance(result, dict) and 'data' in result:
                    email_ids = [r.get('id', '') for r in result['data']]
                elif isinstance(result, list):
                    email_ids = [r.get('id', '') for r in result]
                else:
                    email_ids = []

            return json.dumps({'ok': True, 'recipients': len(recipients), 'email_ids': email_ids})

        except Exception as ex:
            return json.dumps({'ok': False, 'error': str(ex)})

    # Email lista lekerese API keyvel
    def list_emails(self, api_key: str):
        try:
            resend.api_key = api_key.strip()
            result = resend.Emails.list()
            if isinstance(result, dict):
                emails = result.get('data', [])
            else:
                emails = result if isinstance(result, list) else []
            return json.dumps({'ok': True, 'emails': emails})
        except Exception as ex:
            return json.dumps({'ok': False, 'error': str(ex)})

    def get_email(self, payload_json: str):
        try:
            data = json.loads(payload_json)
            resend.api_key = data.get('apiKey', '').strip()
            email_id = data.get('emailId', '').strip()
            result = resend.Emails.get(email_id=email_id)
            return json.dumps({'ok': True, 'email': dict(result)})
        except Exception as ex:
            return json.dumps({'ok': False, 'error': str(ex)})

    def cancel_email(self, payload_json: str):
        try:
            data = json.loads(payload_json)
            resend.api_key = data.get('apiKey', '').strip()
            email_id = data.get('emailId', '').strip()
            resend.Emails.cancel(email_id=email_id)
            return json.dumps({'ok': True})
        except Exception as ex:
            return json.dumps({'ok': False, 'error': str(ex)})

    def update_email(self, payload_json: str):
        try:
            data = json.loads(payload_json)
            resend.api_key = data.get('apiKey', '').strip()
            email_id = data.get('emailId', '').strip()
            scheduled_at = data.get('scheduledAt', '').strip()
            update_params: resend.Emails.UpdateParams = {
                'id': email_id,
                'scheduled_at': scheduled_at,
            }
            resend.Emails.update(params=update_params)
            return json.dumps({'ok': True})
        except Exception as ex:
            return json.dumps({'ok': False, 'error': str(ex)})

    def list_attachments(self, payload_json: str):
        try:
            data = json.loads(payload_json)
            resend.api_key = data.get('apiKey', '').strip()
            email_id = data.get('emailId', '').strip()
            result = resend.Emails.Attachments.list(email_id=email_id)
            if isinstance(result, dict):
                attachments = result.get('data', [])
            else:
                attachments = result if isinstance(result, list) else []
            return json.dumps({'ok': True, 'attachments': attachments})
        except Exception as ex:
            return json.dumps({'ok': False, 'error': str(ex)})

    def get_attachment(self, payload_json: str):
        try:
            data = json.loads(payload_json)
            resend.api_key = data.get('apiKey', '').strip()
            email_id = data.get('emailId', '').strip()
            attachment_id = data.get('attachmentId', '').strip()
            result = resend.Emails.Attachments.get(email_id=email_id, attachment_id=attachment_id)
            return json.dumps({'ok': True, 'attachment': dict(result)})
        except Exception as ex:
            return json.dumps({'ok': False, 'error': str(ex)})


if __name__ == '__main__':
    api = MailAPI()

    window = webview.create_window(
        title='MAILVOID | Resend Mailer',
        url=f'file:///{HTML_PATH.replace(os.sep, "/")}',
        js_api=api,
        width=1800,
        height=1060,
        min_size=(1800, 800),
        background_color='#05071a',
        text_select=False,
    )

    webview.start(debug=False)
