# URL bilgilerinin bulunduğu alan
# Buradan çeşitli adreslere routing işlemi yapabilirsiniz

from flask import Blueprint
from controllers.Controller import *

pclist = Blueprint('pclist', __name__)
pclist.route('/', methods=['GET'])(controller_index)