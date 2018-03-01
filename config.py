# Config for google-api package

from __future__ import unicode_literals

SEPARATOR       = ";"  # character used for field separation of output
LANG            = "en_US" # can be en_US, fr_FR, ...
ANDROID_ID      = "fcaf78d9a193bbbd" # "38c6523ac43ef9e1"
GOOGLE_LOGIN    = 'campana.mattia@gmail.com' # 'someone@gmail.com'
GOOGLE_PASSWORD = 'F117hmab204!' # 'yourpassword'
AUTH_TOKEN      = "886998949540-b6if6dfbngffabgjbglli9n2gjqv92cv.apps.googleusercontent.com"

# force the user to edit this file
if ANDROID_ID == None \
    or all([each is None for each in [GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN]]):
    raise Exception("config.py not updated")