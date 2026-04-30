from flask import Blueprint, render_template, jsonify
import random
import string

typing = Blueprint("typing", __name__)

# 🔥 Generate fake word dynamically (no dictionary)
def generate_word():
    length = random.randint(3, 10)
    vowels = "aeiou"
    consonants = "bcdfghjklmnpqrstvwxyz"

    word = ""
    for i in range(length):
        if i % 2 == 0:
            word += random.choice(consonants)
        else:
            word += random.choice(vowels)

    return word


# 🔥 Generate random sentence structure
def generate_sentence():
    patterns = [
        "S V O",
        "S V O A",
        "A S V O",
        "S V A O",
        "S V O O"
    ]

    pattern = random.choice(patterns).split()  # ✅ FIX HERE

    parts = {
        "S": generate_word(),
        "V": generate_word(),
        "O": generate_word(),
        "A": generate_word()
    }

    sentence = " ".join(parts[p] for p in pattern)
    return sentence.capitalize() + "."

# 🔥 Paragraph generator
def generate_paragraph(level):
    if level == "easy":
        count = 15
    elif level == "medium":
        count = 20
    else:
        count = 25

    return " ".join(generate_sentence() for _ in range(count))


@typing.route("/typing")
def typing_test():
    return render_template("typing.html")


@typing.route("/get-paragraph/<level>")
def get_paragraph(level):
    text = generate_paragraph(level)
    return jsonify({"text": text})