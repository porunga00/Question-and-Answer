from flask import Flask, render_template, request, session
import random
import pandas as pd


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # セキュリティのためのシークレットキー

# CSVファイルから単語とフレーズを読み込む
words = pd.read_csv('words.csv').to_dict(orient='records')
phrases = pd.read_csv('phrases.csv').to_dict(orient='records')

@app.route('/', methods=['GET'])
def main():
    return render_template('main.html')

@app.route('/word_quiz', methods=['GET', 'POST'])
def word_quiz():
    session['quiz_type'] = 'word_quiz'
    return quiz(words, 'word_quiz')

@app.route('/phrase_quiz', methods=['GET', 'POST'])
def phrase_quiz():
    session['quiz_type'] = 'phrase_quiz'
    return quiz(phrases, 'phrase_quiz')

def quiz(data, template):
    if request.method == 'POST':
        answer = request.form.get('answer')
        correct_answer = request.form.get('correct_answer')

        if answer.lower() == correct_answer.lower():
            return render_template('correct.html')
        else:
            return render_template('incorrect.html', correct_answer=correct_answer)

    item = random.choice(data)
    question = f"How do you say '{item['japanese']}' in English?"
    return render_template(f'{template}.html', question=question, correct_answer=item['english'])

if __name__ == '__main__':
    app.run(debug=True, port=5001)
