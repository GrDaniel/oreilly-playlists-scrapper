import json
import os
import time

from dotenv import dotenv_values
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from utils import extract_book_id_from_url

config = dotenv_values(".env")


class Scrapper():

    LOGIN_PAGE_URL = "https://www.oreilly.com/member/login"
    PLAYLISTS_PAGE_URL = "https://learning.oreilly.com/playlists/"

    def __init__(self):
        chromedriver_path = os.path.dirname(os.path.abspath(__file__)) + "/chromedriver"
        options = webdriver.chrome.options.Options()
        options.headless = True
        self._webdriver = webdriver.Chrome(chromedriver_path, options=options)
        self.login()
        self.playlists = {}
        self.links = {}
        self.books = []

    def login(self):
        self._webdriver.get(self.LOGIN_PAGE_URL)
        self._fill_login_form()

    def _fill_login_form(self):
        email_input_field = self._webdriver.find_element_by_name("email")
        password_input_field = self._webdriver.find_element_by_name("password")
        email_input_field.send_keys(config.get("AUTH_EMAIL_PLAYLISTS"))
        password_input_field.send_keys(config.get("AUTH_PASSWORD_PLAYLISTS"))
        submit_button = WebDriverWait(self._webdriver, 20).until(
            expected_conditions.element_to_be_clickable((By.XPATH, '//*[@id="main"]/section/div[1]/form/button[2]')))
        submit_button.click()
        time.sleep(3)  # Replace by selenium wait function

    def get_books(self):
        self.get_playlists_details()
        self.extract_playlist_details()
        self.save_to_file()
        self.close_browser()

    def get_playlists_details(self):
        self._webdriver.get(self.PLAYLISTS_PAGE_URL)
        WebDriverWait(self._webdriver, 10).until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, 'orm-Card-link')))
        playlist_cards = self._webdriver.find_elements_by_class_name('orm-Card-link')
        self.playlists = {card.get_attribute('text'): card.get_attribute('href') for card in playlist_cards}

    def extract_playlist_details(self):
        for playlist_name, playlist_url in self.playlists.items():
            for book in self._get_books_from_playlist(playlist_url):
                book_dict = self._extract_books_details(book, playlist_name)
                self.books.append(book_dict)

    def _get_books_from_playlist(self, playlist_url):
        self._webdriver.get(playlist_url)
        WebDriverWait(self._webdriver, 10).until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, 'orm-Card-link')))
        book_tiles = self._webdriver.find_elements_by_class_name('orm-Card-link')
        return book_tiles

    def _extract_books_details(self, book, playlist_name):
        return {
            "book_name": book.get_attribute('text'),
            "book_id": extract_book_id_from_url(book.get_attribute('href')),
            "book_url": book.get_attribute('href'),
            "playlist_name": playlist_name
        }

    def save_to_file(self):
        with open('books.json', 'w') as outfile:
            json.dump(self.books, outfile)

    def close_browser(self):
        self._webdriver.quit()


if __name__ == '__main__':
    scrapper = Scrapper()
    scrapper.get_books()
