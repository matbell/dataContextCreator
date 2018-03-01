from bs4 import BeautifulSoup
import requests


class GooglePlayStore:

    PLAYSTORE_URL = 'https://play.google.com/store/apps/details?hl=en&id='
    packages = {}
    cache_file = None
    cache_sep = "\t"

    def __init__(self, cache_file='known_apps.dat'):

        try:
            file = open(cache_file, 'r')
        except IOError:
            file = open(cache_file, 'w')

        file.close()

        self.cache_file = cache_file
        self.load_knwon_apps()

    def get_package_category(self, package):

        genre = None

        if package in self.packages:
            genre = self.packages[package]

        else:
            page = requests.get(GooglePlayStore.PLAYSTORE_URL + package)

            if page.status_code == 200:
                soup = BeautifulSoup(page.content, 'html.parser')
                genre = soup.find('body').find("div", {"class": "details-info"}).find(itemprop="genre").get_text()

                if genre is not None:
                    with open(self.cache_file, "a") as myfile:
                        myfile.write(package + self.cache_sep + genre + "\n")
                    self.packages[package] = genre

        return genre

    def load_knwon_apps(self):
        with open(self.cache_file) as f:
            content = f.readlines()
        content = [x.strip() for x in content]

        for element in content:
            app = element.split(self.cache_sep)[0]
            genre = element.split(self.cache_sep)[1]
            self.packages[app] = genre

    @staticmethod
    def get_apps_categories():

        categories = {}

        page = requests.get(GooglePlayStore.PLAYSTORE_URL + "com.google.android.dialer")

        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            genres = soup.find('body').find("div", {"class": "dropdown-submenu"})\
                .findAll("a", {"class": "child-submenu-link"})

            for genre in genres:
                if genre.get_text() != "Daydream" and genre.get_text() != "Games" and genre.get_text() != "Family":
                    categories[genre.get_text()] = 0

        return categories

