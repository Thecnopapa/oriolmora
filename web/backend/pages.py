from flask import render_template


def page_index(lan="cat"):
    return render_template("index.html", lan=lan)