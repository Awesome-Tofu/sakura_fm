from os import error
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class Sakura:
    def __init__(self, sakura_username, sakura_password, mongoURI):
        self.sakura_username = sakura_username
        self.sakura_password = sakura_password
        self.mongoURI = mongoURI
        self.baseUrl = "sakura.fm"
        
    # AUTHENTICATE
    def authenticate(self, jwt):
        headers = {
            'Content-Type': 'application/json',
            'Referer': f'https://www.{self.baseUrl}/',
            'Origin': f'https://www.{self.baseUrl}',
            'Authorization': f'Bearer {jwt}'
        }
        return headers


    # JWT
    def get_jwt(self):
        try:
            form_data = {
                'identifier': self.sakura_username,
                'password': self.sakura_password,
                'strategy': 'password'
            }
        
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': f'https://www.{self.baseUrl}/',
                'Origin': f'https://www.{self.baseUrl}',
            }
        
            response = requests.post(f'https://clerk.{self.baseUrl}/v1/client/sign_ins?_clerk_js_version=5.1.1', data=form_data, headers=headers)
            response.raise_for_status()
            data = response.json()
            client_uat = data['client']['sessions'][0]['user']['last_sign_in_at']
            client_uat = int(str(client_uat)[:10])
            
            return {'jwt': data['client']['sessions'][0]['last_active_token']['jwt'], 'client_uat': client_uat}
        except:
            raise error('Failed to authenticate. Please ensure thta your username and password are correct.')


    # CONTINUE CHAT
    def continue_chat(self, chat_id, prompt):
        req_data = {
            "action": {
                "type": "append",
                "content": prompt
            },
            "context": {
                "chatId": chat_id,
                "locale": "en"
            }
        }

        jwt_data = self.get_jwt()
        jwt = jwt_data['jwt']
        headers = self.authenticate(jwt)

        response = requests.post(f'https://api.{self.baseUrl}/api/chat', json=req_data, headers=headers)
        data = response.json()
        reply = data['messages'][-1]
        return {'chat_id': chat_id,'reply': reply['content']}


    # CREATE CHAT
    def create_chat(self, char_id, prompt):
        # Get character start text
        response = requests.post(f'https://www.{self.baseUrl}/chat/{char_id}')
        
        soup = BeautifulSoup(response.text, 'html.parser')
        button = soup.find('div', class_='text-muted-foreground line-clamp-5')

        if button is None:
            raise ValueError("Button with the specified class not found")

        button_text = button.text.strip()
        char_start_text = button_text.replace('"', '')
        
        # Create chat with prompt
        req_data = {
            "action": {
                "type": "append",
                "content": prompt
            },
            "context": {
                "characterId": char_id,
                "messages": [
                    {
                        "role": "assistant",
                        "content": char_start_text,
                        "type": "text"
                    }
                ],
                "locale": "en"
            }
        }

        jwt_data = self.get_jwt()
        jwt = jwt_data['jwt']
        headers = self.authenticate(jwt)

        response = requests.post(f'https://api.{self.baseUrl}/api/chat', json=req_data, headers=headers)
        data = response.json()
        return {'chat_id': data['chatId'], 'reply': data['messages'][-1]['content']}


    # GET SELFIE
    def get_selfie(self, chat_id):
        jwt_data = self.get_jwt()
        jwt = jwt_data['jwt']
        headers = self.authenticate(jwt)

        req_data = {
            "action": {
                "type": "generate-image",
                "variant": "selfie"
            },
            "context": {
                "chatId": chat_id,
                "locale": "en"
            }
        }

        response = requests.post(f'https://api.{self.baseUrl}/api/chat', json=req_data, headers=headers)
        data = response.json()
        reply = data['messages'][-1]
        return reply['uri']

