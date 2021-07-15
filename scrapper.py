from requests import Session
from http import HTTPStatus
from dotenv import dotenv_values

config = dotenv_values(".env")


class WebScrapper():

    def __init__(self):
        self._session = Session()
        self.login()

    def login(self):
        login_url = config.get('LOGIN_URL')
        headers = {'content-type': 'application/json'}
        payload = {'email': config.get('AUTH_EMAIL'),'password': config.get('AUTH_PASSWORD')}
        response = self._session.post(url=login_url, json=payload, headers=headers)                                
        if response.status_code == HTTPStatus.OK:                                                                  
            print("Logged correctly")                                                                              
        else:                                                                                                      
            print(f"Problem with login occurred. Status code: {response.status_code}")                             
                                                                                                                   
                                                                                                                   
if __name__ =="__main__":                                                                                          
    scrapper = WebScrapper()   