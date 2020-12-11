#!/usr/bin/python3

from flask import Flask, render_template, request
#import Counter as counter
# from utils.notes import createNotes
from utils.obnotes import createNotes

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('ui.html')

@app.route('/notes', methods=["POST"])
def notes():
    res = request.form.get("article")
    input = 0
    if not res:
        res = request.form.get("url")
        kw = request.form.get("kw")
        src = request.form.get("domain")
        input = 1
        allNotes = createNotes("u", res, src, "none", kw)

        return render_template('notes.html', kw = allNotes[0], notes = allNotes[1], quotes = allNotes[2])
    else:
        kw = request.form.get("kw")
        allNotes = createNotes("c", "none", "none", res, kw)

        return render_template('notes.html', kw = allNotes[0], notes = allNotes[1], quotes = allNotes[2])









