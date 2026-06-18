from flask import Flask, render_template, request, redirect, url_for

from assistant import answer_question, get_suggested_questions

app = Flask(__name__)
JOURNAL_FILE = "journal.txt"


def read_entries():
    try:
        with open(JOURNAL_FILE, "r") as file:
            lines = file.readlines()
        return [line.rstrip() for line in lines if line.strip()]
    except FileNotFoundError:
        return []


def add_entry_to_file(entry):
    with open(JOURNAL_FILE, "a") as file:
        file.write(entry + "\n")


def search_entries(keyword):
    entries = read_entries()
    if not keyword:
        return []
    return [entry for entry in entries if keyword.lower() in entry.lower()]


@app.route("/")
def index():
    entries = read_entries()
    recent_notes = entries[-3:] if len(entries) >= 3 else entries
    return render_template(
        "index.html",
        total_notes=len(entries),
        recent_notes=recent_notes,
    )


@app.route("/add", methods=["GET", "POST"])
def add_entry():
    if request.method == "POST":
        entry = request.form.get("entry", "").strip()
        if entry:
            add_entry_to_file(entry)
        return redirect(url_for("view_entries"))
    return render_template("add_entry.html")


@app.route("/view")
def view_entries():
    entries = read_entries()
    return render_template("view_entries.html", entries=entries)


@app.route("/search", methods=["GET", "POST"])
def search():
    matches = []
    keyword = ""
    if request.method == "POST":
        keyword = request.form.get("keyword", "").strip()
        if keyword:
            matches = search_entries(keyword)
    return render_template("search_entries.html", matches=matches, keyword=keyword)


@app.route("/assistant", methods=["GET", "POST"])
def assistant():
    answer = ""
    question = ""
    if request.method == "POST":
        question = request.form.get("question", "").strip()
        if question:
            answer = answer_question(question, read_entries())
    return render_template(
        "assistant.html",
        answer=answer,
        question=question,
        suggestions=get_suggested_questions(),
    )


if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
