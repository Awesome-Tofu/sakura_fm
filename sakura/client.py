from db import insertChat, getChatId, delete_sakura_database
from sakura import Sakura

class Client:
    def __init__(self, login):
        self.sakura_username = login["username"]
        self.sakura_password = login["password"]
        self.mongoURI = login["mongo"]
        self.sakura = Sakura(self.sakura_username, self.sakura_password, self.mongoURI)
        
    # SEND MESSAGE
    def sendMessage(self, uid: int, char_id: str, prompt: str):
        try:

            chat_id = getChatId(uid, self.mongoURI)

            if chat_id:
                # If a chat exists, continue the chat
                chat_data = self.sakura.continue_chat(chat_id, prompt)
            else:
                # If no chat exists, create a new chat and store it in the database
                chat_data = self.sakura.create_chat(char_id, prompt)
                insertChat(chat_data['chat_id'], uid, char_id, self.mongoURI)

        except Exception as e:
            raise RuntimeError("An error occurred while sending the message: {}".format(str(e)))

    # GET SELFIE
    def get_selfie(self, uid: int):
        try:
            chat_id = getChatId(uid, self.mongoURI)
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
            delete_sakura_database(self.mongoURI)
        except Exception as e:
            raise RuntimeError("An error occurred while deleting the database: {}".format(str(e)))
        