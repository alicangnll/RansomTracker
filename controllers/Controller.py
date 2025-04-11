# Controller alanı
# Tüm uygulamanın beyni buradan olacak. DB bağlantıları ve çeşitli bağlantılar dahil
# Bu alandan modele sorgular gönderilecek ve alınan cevaplar route alanında belirtilen linkte sergilenecek

from models.DBModel import *
from flask import render_template

def controller_index():
    last_hacked_websites = Group.query.limit(10).all()
    return render_template("index.html", hacked_list = last_hacked_websites)