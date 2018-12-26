from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import LiveServerTestCase
from django.core.urlresolvers import reverse
from selenium.common.exceptions import NoSuchElementException
import os
import sys
import time
from selenium import webdriver
from django.test import TestCase

'''
class AdminTestCase(LiveServerTestCase):
    def setUp(self):
        self.webdriver = webdriver.Chrome('/home/bubliks/chromedriver')
        self.webdriver.implicitly_wait(200)
        self.live_server_url = "http://localhost:8000"
        super(AdminTestCase, self).setUp()

    def tearDown(self):
        # Call tearDown to close the web browser
        self.webdriver.quit()
        super(AdminTestCase, self).tearDown()

    def test_01_create_user(self):
        self.webdriver.get('%s%s' % (self.live_server_url, "/signup"))
        login = self.webdriver.find_element_by_id("id_login")
        login.send_keys("keks")
        email = self.webdriver.find_element_by_id("id_email")
        email.send_keys("keks@maik.ru")
        name = self.webdriver.find_element_by_id("id_name")
        name.send_keys("keks_name")
        password = self.webdriver.find_element_by_id("id_password")
        password.send_keys("kekskeks")
        password_repeat = self.webdriver.find_element_by_id("id_password_repeat")
        password_repeat.send_keys("kekskeks")
        time.sleep(1)
        self.webdriver.find_element_by_xpath("//button[@type='submit'][@name='signup']").click()
        time.sleep(1)
        self.tearDown()

    def test_02_login_user(self):
        self.webdriver.get('%s%s' % (self.live_server_url, "/login"))
        login = self.webdriver.find_element_by_id("id_username")
        login.send_keys("keks")
        password = self.webdriver.find_element_by_id("id_password")
        password.send_keys("kekskeks")
        time.sleep(1)
        self.webdriver.find_element_by_xpath("//button[@type='submit'][@name='login']").click()
        time.sleep(1)
        self.tearDown()

    def test_03_logout_user(self):
        self.webdriver.get('%s%s' % (self.live_server_url, "/login"))
        login = self.webdriver.find_element_by_id("id_username")
        login.send_keys("keks")
        password = self.webdriver.find_element_by_id("id_password")
        password.send_keys("kekskeks")
        time.sleep(1)
        self.webdriver.find_element_by_xpath("//button[@type='submit'][@name='login']").click()
        time.sleep(1)

        self.webdriver.find_element_by_id("id_burger").click()
        time.sleep(1)
        self.webdriver.find_element_by_link_text('Log out').click()
        time.sleep(2)
        self.tearDown()

    def test_04_create_question(self):
        self.webdriver.get('%s%s' % (self.live_server_url, "/login"))
        login = self.webdriver.find_element_by_id("id_username")
        login.send_keys("keks")
        password = self.webdriver.find_element_by_id("id_password")
        password.send_keys("kekskeks")
        time.sleep(1)
        self.webdriver.find_element_by_xpath("//button[@type='submit'][@name='login']").click()
        time.sleep(1)

        self.webdriver.find_element_by_xpath("//button[@type='button'][@name='ask-button']").click()
        time.sleep(2)

        self.webdriver.find_element_by_id("id_title").send_keys("test_title")
        self.webdriver.find_element_by_id("id_text").send_keys("test_text")
        self.webdriver.find_element_by_id("id_tags").send_keys("test_tags")
        self.webdriver.find_element_by_xpath("//button[@type='submit'][@name='ask']").click()
        time.sleep(2)
        self.tearDown()

    def test_05_create_answer(self):
        self.webdriver.get('%s%s' % (self.live_server_url, "/login"))
        login = self.webdriver.find_element_by_id("id_username")
        login.send_keys("keks")
        password = self.webdriver.find_element_by_id("id_password")
        password.send_keys("kekskeks")
        time.sleep(1)
        self.webdriver.find_element_by_xpath("//button[@type='submit'][@name='login']").click()
        time.sleep(1)

        self.webdriver.find_element_by_link_text('test_title').click()
        time.sleep(2)

        self.webdriver.find_element_by_id("id_text").send_keys("test_text_answer")
        self.webdriver.find_element_by_xpath("//button[@type='submit'][@name='answer']").click()
        time.sleep(2)
        self.tearDown()

    def test_06_create_question_like(self):
        self.webdriver.get('%s%s' % (self.live_server_url, "/login"))
        login = self.webdriver.find_element_by_id("id_username")
        login.send_keys("keks")
        password = self.webdriver.find_element_by_id("id_password")
        password.send_keys("kekskeks")
        time.sleep(1)
        self.webdriver.find_element_by_xpath("//button[@type='submit'][@name='login']").click()
        time.sleep(1)

        self.webdriver.find_element_by_xpath("//button[@type='button'][@data-id='1'][@data-action='like']").click()
        time.sleep(2)
        self.tearDown()

    def test_07_create_question_dislike(self):
        self.webdriver.get('%s%s' % (self.live_server_url, "/login"))
        login = self.webdriver.find_element_by_id("id_username")
        login.send_keys("keks")
        password = self.webdriver.find_element_by_id("id_password")
        password.send_keys("kekskeks")
        time.sleep(1)
        self.webdriver.find_element_by_xpath("//button[@type='submit'][@name='login']").click()
        time.sleep(1)

        self.webdriver.find_element_by_xpath("//button[@type='button'][@data-id='1'][@data-action='dislike']").click()
        time.sleep(2)

        self.tearDown()

    def test_08_create_in_question_like(self):
        self.webdriver.get('%s%s' % (self.live_server_url, "/login"))
        login = self.webdriver.find_element_by_id("id_username")
        login.send_keys("keks")
        password = self.webdriver.find_element_by_id("id_password")
        password.send_keys("kekskeks")
        time.sleep(1)
        self.webdriver.find_element_by_xpath("//button[@type='submit'][@name='login']").click()
        time.sleep(1)

        self.webdriver.find_element_by_link_text('test_title').click()
        time.sleep(2)
        self.webdriver.find_element_by_xpath("//button[@type='button'][@data-id='1'][@data-type='article'][@data-action='like']").click()
        time.sleep(2)

        self.tearDown()

    def test_09_create_in_question_dislike(self):
        self.webdriver.get('%s%s' % (self.live_server_url, "/login"))
        login = self.webdriver.find_element_by_id("id_username")
        login.send_keys("keks")
        password = self.webdriver.find_element_by_id("id_password")
        password.send_keys("kekskeks")
        time.sleep(1)
        self.webdriver.find_element_by_xpath("//button[@type='submit'][@name='login']").click()
        time.sleep(1)

        self.webdriver.find_element_by_link_text('test_title').click()
        time.sleep(2)
        self.webdriver.find_element_by_xpath("//button[@type='button'][@data-id='1'][@data-type='article'][@data-action='dislike']").click()
        time.sleep(2)
        self.tearDown()

    def test_10_create_answer_like(self):
        self.webdriver.get('%s%s' % (self.live_server_url, "/login"))
        login = self.webdriver.find_element_by_id("id_username")
        login.send_keys("keks")
        password = self.webdriver.find_element_by_id("id_password")
        password.send_keys("kekskeks")
        time.sleep(1)
        self.webdriver.find_element_by_xpath("//button[@type='submit'][@name='login']").click()
        time.sleep(1)

        self.webdriver.find_element_by_link_text('test_title').click()
        time.sleep(2)
        self.webdriver.find_element_by_xpath("//button[@type='button'][@data-id='1'][@data-type='answer'][@data-action='like']").click()
        time.sleep(2)
        self.tearDown()

    def test_11_create_answer_dislike(self):
        self.webdriver.get('%s%s' % (self.live_server_url, "/login"))
        login = self.webdriver.find_element_by_id("id_username")
        login.send_keys("keks")
        password = self.webdriver.find_element_by_id("id_password")
        password.send_keys("kekskeks")
        time.sleep(1)
        self.webdriver.find_element_by_xpath("//button[@type='submit'][@name='login']").click()
        time.sleep(1)

        self.webdriver.find_element_by_link_text('test_title').click()
        time.sleep(2)
        self.webdriver.find_element_by_xpath("//button[@type='button'][@data-id='1'][@data-type='answer'][@data-action='dislike']").click()
        time.sleep(2)
        self.tearDown()

    def test_12_open_settings(self):
        self.webdriver.get('%s%s' % (self.live_server_url, "/login"))
        login = self.webdriver.find_element_by_id("id_username")
        login.send_keys("keks")
        password = self.webdriver.find_element_by_id("id_password")
        password.send_keys("kekskeks")
        time.sleep(1)
        self.webdriver.find_element_by_xpath("//button[@type='submit'][@name='login']").click()
        time.sleep(1)

        self.webdriver.find_element_by_id("id_burger").click()
        time.sleep(1)
        self.webdriver.find_element_by_link_text('Settings').click()
        time.sleep(2)
        self.tearDown()

    def test_13_open_hot_questions(self):
        self.webdriver.get('%s%s' % (self.live_server_url, "/login"))
        login = self.webdriver.find_element_by_id("id_username")
        login.send_keys("keks")
        password = self.webdriver.find_element_by_id("id_password")
        password.send_keys("kekskeks")
        time.sleep(1)
        self.webdriver.find_element_by_xpath("//button[@type='submit'][@name='login']").click()
        time.sleep(1)

        self.webdriver.find_element_by_link_text('Hot Questions').click()
        time.sleep(2)
        self.tearDown()

    def test_14_open_new_questions(self):
        self.webdriver.get('%s%s' % (self.live_server_url, "/hot_index"))
        self.webdriver.find_element_by_link_text('New Questions').click()
        time.sleep(2)
        self.tearDown()

    def test_15_open_search(self):
        self.webdriver.get('%s%s' % (self.live_server_url, "/index"))
        self.webdriver.find_element_by_id("id_search_word").send_keys("test_title")
        self.webdriver.find_element_by_xpath("//button[@type='submit'][@name='search-button']").click()
        time.sleep(2)
        self.tearDown()

    # add after template
    def test_16_open_new_questions(self):
        self.webdriver.get('%s%s' % (self.live_server_url, "/hot_index"))
        self.webdriver.find_element_by_link_text('New Questions').click()
        self.tearDown()

    def test_17_open_new_questions(self):
        self.webdriver.get('%s%s' % (self.live_server_url, "/hot_index"))
        self.webdriver.find_element_by_link_text('New Questions').click()
        self.tearDown()

    def test_18_open_new_questions(self):
        self.webdriver.get('%s%s' % (self.live_server_url, "/hot_index"))
        self.webdriver.find_element_by_link_text('New Questions').click()
        self.tearDown()


    def test_19_open_new_questions(self):
        self.webdriver.get('%s%s' % (self.live_server_url, "/hot_index"))
        self.webdriver.find_element_by_link_text('New Questions').click()
        self.tearDown()

    def test_20_open_new_questions(self):
        self.webdriver.get('%s%s' % (self.live_server_url, "/hot_index"))
        self.webdriver.find_element_by_link_text('New Questions').click()
        self.tearDown()
'''
