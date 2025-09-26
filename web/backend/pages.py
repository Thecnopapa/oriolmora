from flask import render_template
from .database import get_products


def template(template, lan):
    products = get_products()


    return render_template(template, lan=lan, products=products)



def page_index(lan="cat"):
    return template("index.html", lan)