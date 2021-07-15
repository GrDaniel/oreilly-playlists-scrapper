from requests import Session
from http import HTTPStatus


class WebScrapper():

    def __init__(self):
        self._session = Session()
        self.login()

    def login(self):
        login_url = 'login_url'
        headers = {'content-type': 'application/json'}
        payload = {'email': 'xxx','password': 'xxx'}
        response = self._session.post(url=login_url, json=payload, headers=headers)                                
        if response.status_code == HTTPStatus.OK:                                                                  
            print("Logged correctly")                                                                              
        else:                                                                                                      
            print(f"Problem with login occurred. Status code: {response.status_code}")                             
                                                                                                                   
                                                                                                                   
if __name__ =="__main__":                                                                                          
    scrapper = WebScrapper()  