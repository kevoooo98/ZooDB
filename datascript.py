from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import pymysql.cursors
import time
import csv

class chromeWebDriver():

  def __init__(self):

      self.driver = webdriver.Firefox(
        executable_path = "./geckodriver"
      )

  def set_url (self, url):
      browser = self.driver.get(url)
      time.sleep(5)

  def get_current_url(self):
      return self.driver.current_url

  def input_field (self, css_field, input):
      field = self.get_field(css_field)
      field.send_keys(input)

  def click_field (self, css_field):
      field = self.get_field(css_field)
      field.click()

  def click_field_by_xpath (self, xpath_field):
      field = self.get_field_by_xpath(xpath_field)
      field.click()

  def field_exists (self, css_field):
      try:
          self.get_field(css_field)
      except NoSuchElementException:
          return False
      return True

  def field_exists_by_xpath(self, xpath):
      try:
          self.driver.find_element_by_xpath(xpath)
      except NoSuchElementException:
          return False
      return True

  def get_field (self, css_field):
      return self.driver.find_element_by_css_selector(css_field)


  def get_field_by_xpath (self, css_field):
      return self.driver.find_element_by_xpath(xpath)

  def get_all_fields_by_xpath (self, xpath):
      return self.driver.find_elements_by_xpath(xpath)

class DBController():

    def __init__(self):
        pass

    def fetch_query(self, query):
        con = self.get_connection()
        with con:
            with con.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return result

    def run_statement(self, query):
        con = self.get_connection()
        with con:
            with con.cursor() as cursor:
                cursor.execute(query)
            con.commit()

    def get_connection(self):
        return pymysql.connect(
            host='127.0.0.1',
            db = 'zoo',
            user='dbuser', passwd='geheim1',
            cursorclass=pymysql.cursors.DictCursor
        )

class lexikonDriver(chromeWebDriver):
    __base_url = 'https://www.zootier-lexikon.org'
    __url_alphabet = 'https://www.zootier-lexikon.org/index.php?option=com_k2&view=itemlist&task=category&id=7:deutsche-tiernamen&Itemid=654'
    __xpath_subcat_container = '//a[contains(@class,"subCategoryMore")]'
    __xpath_link_animal = '//div[contains(@class,"itemListCategory")]/table//ul/li/a'
    __xpath_german_name = '//span[contains(@style, "font-family: trebuchet ms, geneva; font-size: 24pt;")]'
    __xpath_science_name = '//span[contains(@style, "font-family: trebuchet ms,geneva;")]/em'
    __xpath_animal_info_child = '//div[contains(@class, "itemFullText")]/p/span/br'
    __xpath_redlist_img = '//div[contains(@class, "itemFullText")]/p/span/img//div[contains(@class, "itemFullText")]/p/span/img'

    def __init__(self) :
        super().__init__()
        self.cd = super()
        self.cd.set_url(self.__base_url)

    def getAnimalLinks(self):
        self.cd.set_url(self.__url_alphabet)
        list_animallinks = []
        list_alphabetlinks = []

        for anker in self.cd.get_all_fields_by_xpath(self.__xpath_subcat_container):
            list_alphabetlinks.add(self.cd.set_url(anker.get_attribute('href')))

        for link in list_alphabetlinks:
            self.cd.set_url(link)
            for li in self.cd.get_all_fields_by_xpath(self.__xpath_link_animal):
                print(li.get_attribute('href'))

                



class DataGrabber():
    def __init__ (self):
        self.ld = lexikonDriver()

    def run_data_grab(self):
        list_alphabetlinks = self.ld.getAnimalLinks()





dg = DataGrabber()
dg.run_data_grab()
