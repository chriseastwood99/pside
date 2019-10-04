import time
from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class ParksideExerciseTestCase(unittest.TestCase):
    # Starting with Wikipedia's https://en.wikipedia.org/wiki/Metis_(mythology) page, please test for the following:

    def setUp(self):
        """Call before every test case."""
        self.driver = webdriver.Chrome()
        self.driver.get('https://en.wikipedia.org/wiki/Metis_(mythology)')
        time.sleep(1)  # Let me actually see something!

    def tearDown(self):
        """Call after every test case."""
        self.driver.quit()

    def testATOCsareHeadersOnPage(self):
        # the headings listed in the `Contents` box are used as headings on the page
        driver = self.driver
        toc_titles = driver.find_elements_by_xpath('//*[@id="toc"]/ul/li[*]/a/span[2]')
        headings = driver.find_elements_by_tag_name('H2')
        tocs = len(toc_titles)
        actual_h2s = 0
        for title in toc_titles:
            for value in headings:
                if title.text in value.text:
                    actual_h2s = actual_h2s + 1
        assert tocs == actual_h2s

    def testBTOCsareHyperLinke(self):
        # b) the headings listed in the `Contents` box have functioning hyperlinks
        driver = self.driver
        toc_links = driver.find_elements_by_xpath('//*[@id="toc"]/ul/li[*]/a')
        for link in toc_links:
            att = link.get_attribute('href')
            assert att is not 'null', "There is no link for: " + link.text
            link.click()
            time.sleep(2)
            # todo - add a verification wrt where the link navigated to
            driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
            time.sleep(1)
            att = 'null'

    def testCPersonifiedNikeText(self):
        # c) in the _Personified concepts_, `Nike` has a popup that contains the following text:
        driver = self.driver
        pc_links = driver.find_elements_by_xpath('//*[@id="mw-content-text"]/div/table[1]/tbody/tr[6]/td/div/ul/li[*]/a')
        for link in pc_links:
            hover = ActionChains(driver).move_to_element(link)
            hover.perform()
            time.sleep(1)
            pocontent = driver.find_elements_by_xpath('//*[@class="mwe-popups-extract"]/p')
            for item in pocontent:
                if item.text in 'In ancient Greek religion, Nike was a goddess who personified victory. Her Roman equivalent was Victoria.':
                    tpass = True
        assert tpass == True

    def testDNikeFamilyTree(self):
          # d) in the _Personified concepts_, if you click on `Nike`, it takes you to a page that displays a family tree
          driver = self.driver
          nike = driver.find_elements_by_xpath('//*[@id="mw-content-text"]/div/table[1]/tbody/tr[6]/td/div/ul/li[13]/a')
          for link in nike:
            link.click()
          familytree = driver.find_element_by_xpath('//*[@id="Family_tree"]')
          assert familytree is not 'null'

if __name__ == "__main__":
    unittest.main() # run all tests
