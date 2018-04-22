from bs4 import BeautifulSoup
import requests
import os


class GooglePlayStore:

    PLAYSTORE_URL = 'https://play.google.com/store/apps/details?hl=en&id='
    packages = {}
    cache_file = None
    app_categories_file = None
    cache_sep = "\t"
    store_categories = []
    new_files = False

    def __init__(self, out_dir, cache_file='./known_apps.dat', app_categories_file='./play_store_app_categories.dat',
                 new_files=False):

        self.cache_file = out_dir + "/" + cache_file
        self.app_categories_file = out_dir + "/" + app_categories_file
        self.new_files = new_files

        if not new_files:

            self.load_known_apps()
            self.read_apps_cateogires()

        else:

            if os.path.exists(cache_file):
                os.remove(cache_file)
            file = open(cache_file, 'w')
            file.close()

            if os.path.exists(app_categories_file):
                os.remove(app_categories_file)
            file = open(cache_file, 'w')
            file.close()

    def get_package_category(self, package):

        genres = None

        if package in self.packages:
            genres = self.packages[package]

        elif self.new_files:

            genres = set()

            page = requests.get(GooglePlayStore.PLAYSTORE_URL + package)

            if page.status_code == 200:
                soup = BeautifulSoup(page.content, 'html.parser')

                for link in soup.find_all('a', itemprop="genre"):
                    if "href" in link.attrs and "apps/category/" in link["href"]:
                        cat = link["href"].split("/")[-1]
                        if cat in self.store_categories:
                            genres.add(cat)

                if len(genres) > 0:

                    log_list = [package]
                    log_list.extend(genres)

                    self.packages[package] = genres

                    with open(self.cache_file, "a") as myfile:
                        myfile.write(self.cache_sep.join(log_list) + "\n")


                #details = soup.find('body').find("div", {"class": "details-info"})

                    #if details is not None:
                    #genre = details.find("a", {"class": "category"})["href"].split("/")[-1]

                        #if genre is not None:
                        #with open(self.cache_file, "a") as myfile:
                        #    myfile.write(package + self.cache_sep + genre + "\n")
                #self.packages[package] = genre

        return genres

    def load_known_apps(self):

        print("Reading known apps...")

        with open(self.cache_file) as f:
            content = f.readlines()
        content = [x.strip() for x in content]

        for element in content:
            app = element.split(self.cache_sep)[0]
            genre = element.split(self.cache_sep)[1]
            self.packages[app] = genre

    def fetch_apps_categories(self):
        print("Fetching Google Play Store Apps categories...")
        page = requests.get(GooglePlayStore.PLAYSTORE_URL + "com.facebook.katana")

        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')

            for link in soup.find('body').findAll("a"):
                if "href" in link.attrs and "apps/category/" in link["href"]:
                    cat = link["href"].split("/")[-1]
                    if cat != "APPLICATION" and cat != "GAME" and cat != "FAMILY" and "FAMILY?age=" not in cat:
                        self.store_categories.append(cat)
                        with open(self.app_categories_file, "a") as myfile:
                            myfile.write(cat + "\n")

            #genres = soup.find('body').find("div", {"class": "dropdown-submenu"}) \
            #    .findAll("a", {"class": "child-submenu-link"})

            #for genre in genres:
            #    if genre.get_text() != "Daydream" and genre.get_text() != "Games" and genre.get_text() != "Family":
            #        self.store_categories.append(genre["href"].split("/")[-1])
            #        with open(self.app_categories_file, "a") as myfile:
            #            myfile.write(genre["href"].split("/")[-1] + "\n")

    def read_apps_cateogires(self):

        print("Reading apps categories...")

        with open(self.app_categories_file) as f:
            content = f.readlines()

        self.store_categories = [x.strip() for x in content]

    def get_categories(self):
        cats = {}

        cat_id = 1
        for cat in self.store_categories:
            cats[cat] = cat_id
            cat_id = cat_id + 1

        return cats
