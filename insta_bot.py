
#A simple bot that uses your instagram id and password and returns you with a list of all the people whom you follow but they don't follow you
#It uses selenium to access browser
#selenium==3.141.0
#urllib3==1.25.7


from selenium import webdriver
from time import sleep


class InstaBot:
    def __init__(self,usr,pw,id):
        self.usr = usr
        self.id = id
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.instagram.com")
        sleep(2)
        self.driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[1]/button').click()
        sleep(2)
        self.driver.find_element_by_xpath('//input[@name="email"]').send_keys(usr)
        self.driver.find_element_by_xpath('//input[@name="pass"]').send_keys(pw)
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()
        sleep(4)
        self.driver.find_element_by_xpath('//button[contains(text(), "Not Now")]').click()
        sleep(2)

    def get_unfollowers(self):
        self.driver.find_element_by_xpath('//a[contains(@href, "/{}")]'.format(self.id)).click()
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]").click()
        following = self._get_names()
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]").click()
        followers = self._get_names()
        not_following_back = [user for user in following if user not in followers]
        print(not_following_back)

    def _get_names(self):
        sleep(2)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script('''
                arguments[0].scrollTo(0, arguments[0].scrollHeight);
                return arguments[0].scrollHeight;
                ''', scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        # close button
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button")\
            .click()
        return names


my_bot = InstaBot(usr,pw,insta_id)
my_bot.get_unfollowers()
