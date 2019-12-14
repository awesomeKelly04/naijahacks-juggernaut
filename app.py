import json
from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

app = Flask(__name__)

juggernaut_bot = ChatBot("Juggernaut Bot", storage_adapter="chatterbot.storage.SQLStorageAdapter")

trainer = ListTrainer(juggernaut_bot)

with open("data/number_word_std.all.json".format(), buffering=1000) as f:
    data = json.load(f)
    interactions = []
    for row in data:
        equations = ""
        answers = "Answer: "
        question = row['text']
        interactions.append(question)
        for equation in row['equations']:
            equations += f'{equation} => '
        for answer in row['ans_simple']:
            answers += f'{answer}, '
        solution = f'Solution: {equations}{answers}\n'
        interactions.append(solution)

trainer.train(interactions)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    while True:
        userText = request.args.get('msg')
        if userText.strip() == 'bye':
            return str("Bye bye")
            break
        else:
            return str(juggernaut_bot.get_response(userText))


if __name__ == "__main__":
    app.run()
