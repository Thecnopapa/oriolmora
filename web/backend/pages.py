from flask import render_template
from .database import hi


def template(template, lan):



    return render_template(template, lan=lan)



def page_index(lan="cat"):
    return template("index.html", lan)