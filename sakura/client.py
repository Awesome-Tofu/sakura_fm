from .db import *
from .sakura import Sakura

class Client:
    def __init__(self, username: str, password: str, mongo: str):
        self.sakura_username = username
        self.sakura_password = password
        self.mongoURI = mongo
        self.sakura = Sakura(self.sakura_username, self.sakura_password, self.mongoURI)
        
    # SEND MESSAGE
    def sendMessage(self, uid: int, char_id: str, prompt: str):
        try:
            char_id_data = getChatId(uid, self.mongoURI)
            if char_id_data is None:
                # If no chat exists, create a new chat and store it in the database
                # print("Chat id does not exist, creating new chat")
                chat_data = self.sakura.create_chat(char_id, prompt)
                insertChat(chat_data['chat_id'], uid, char_id, self.mongoURI)
                return chat_data
            if char_id_data['char_id'] is not None and char_id_data['char_id'] != char_id:
                # If char id is changed, create a new chat and update it in the database with the new char id
                # print("Char id changed")
                new_char_id = char_id
                chat_data = self.sakura.create_chat(new_char_id, prompt)
                updateChatandCharId(uid, chat_data['chat_id'], new_char_id, self.mongoURI)
                return chat_data
            else:
                # If a chat exists, continue the chat
                # print("Chat id exists")
                chat_data = self.sakura.continue_chat(char_id_data['chat_id'], prompt)
                return chat_data

        except Exception as e:
            raise RuntimeError(f"An error occurred while sending the message: {str(e)}")

    # GET SELFIE
    def get_selfie(self, uid: int):
        try:
            chat_id = getChatId(uid, self.mongoURI)['chat_id']
            if chat_id:
                selfie = self.sakura.get_selfie(chat_id)
                return selfie
            else:
                raise RuntimeError("No chat found for the user. Cannot get the selfie.")
        except Exception as e:
            raise RuntimeError("An error occurred while getting the selfie: {}".format(str(e)))
    
    # DELETE DATABASE
    def delete_db(self):
        try:
            return delete_sakura_database(self.mongoURI)
        except Exception as e:
            raise RuntimeError("An error occurred while deleting the database: {}".format(str(e)))
        