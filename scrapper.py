import json
import time

from dotenv import dotenv_values
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

PATH = "/home/daniel/Documents/Projects/oreilly-playlists-scrapper/chromedriver"
config = dotenv_values(".env")


class Scrapper():

    LOGIN_PAGE_URL = "https://www.oreilly.com/member/login"
    PLAYLISTS_PAGE_URL = "https://learning.oreilly.com/playlists/"

    def __init__(self):
        self._webdriver = webdriver.Chrome(PATH)
        self.login()
        self.playlists = {}
        self.links = {}

    def login(self):
        self._webdriver.get(self.LOGIN_PAGE_URL)
        self._fill_login_form()

    def _fill_login_form(self):
        email_input_field = self._webdriver.find_element_by_name("email")
        password_input_field = self._webdriver.find_element_by_name("password")
        email_input_field.send_keys(config.get("AUTH_EMAIL"))
        password_input_field.send_keys(config.get("AUTH_PASSWORD"))
        submit_button = WebDriverWait(self._webdriver, 20).until(
            expected_conditions.element_to_be_clickable((By.XPATH, '//*[@id="main"]/section/div[1]/form/button[2]')))
        submit_button.click()
        time.sleep(3)  # Replace by selenium wait function

    def get_playlists_details(self):
        self._webdriver.get(self.PLAYLISTS_PAGE_URL)
        WebDriverWait(self._webdriver, 10).until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, 'orm-Card-link')))
        playlist_cards = self._webdriver.find_elements_by_class_name('orm-Card-link')
        self.playlists = {card.get_attribute('text'): card.get_attribute('href') for card in playlist_cards}

    def extract_playlist_details(self):
        for playlist_name, playlist_url in self.playlists.items():
            tmp = {'url': playlist_url,
                   'books': self._extract_books_from_playlist(playlist_url)}
            self.playlists[playlist_name] = tmp
        print(self.playlists)

    def _extract_books_from_playlist(self, playlist_url):
        self._webdriver.get(playlist_url)
        WebDriverWait(self._webdriver, 10).until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, 'orm-Card-link')))
        book_tiles = self._webdriver.find_elements_by_class_name('orm-Card-link')
        return {book.get_attribute('text'): book.get_attribute('href') for book in book_tiles}

    def save_to_file(self):
        with open('data.json', 'w') as outfile:
            json.dump(self.playlists, outfile)

    def close_browser(self):
        self._webdriver.quit()


if __name__ == '__main__':
    scrapper = Scrapper()
    scrapper.get_playlists_details()
    scrapper.extract_playlist_details()
    scrapper.save_to_file()
    scrapper.close_browser()
