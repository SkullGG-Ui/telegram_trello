import requests

class TrelloClient():
    def __init__(self, trello_key, trello_token, trello_board_id, trello_list_id):
        self.trello_key = trello_key
        self.trello_token = trello_token
        self.trello_board_id = trello_board_id
        self.trello_list_id = trello_list_id

    def create_card(self, message, due_date, description=None, attachment_file_path=None):
        url = "https://api.trello.com/1/cards"
        querystring = {
            "name":message, "desc": description, "due": due_date,
            "pos": "top", "idList":self.trello_list_id,
            "keepFromSource": "all", "key": self.trello_key, "token": self.trello_token
            }
        response = requests.request("POST", url, params=querystring)
        if attachment_file_path:
            card_id = response.json()['id'] 
            url = 'https://api.trello.com/1/cards/{}/attachments'.format(card_id)
            params = {'key': self.trello_key, 'token': self.trello_token}
            files = {'file': open(attachment_file_path, 'rb')}
            response = requests.post(url, params=params, files=files)