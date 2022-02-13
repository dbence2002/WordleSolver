from flask import Flask, request, render_template, url_for, redirect, session, current_app
from solver import WordleState, find_optimum, adjust_color
from sys import stderr
from threading import Thread

fileids = set()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcxyz'

@app.route('/clear', methods=['GET'])
def clear():

    wordlist = session.get('wordlist')
    if wordlist and wordlist.startswith('wordlist'):
        try:
            fileids.remove(int(wordlist[8:]))
        except:
            stderr.write("Invalid file id!")

    session.clear()
    return redirect(url_for('index'))

def get_id():

    index = 0
    while index in fileids: index += 1
    return index

def is_valid_word(word):

    if word == None or len(word) != 5: 
        return False
    return all(map(lambda c: c.isalpha(), word))

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'GET':
        wordlist = list(map(lambda arg: arg.strip(), open(session.get("wordlist") or 'final_words').readlines()))
        optimum = session.get('optimum') or find_optimum(WordleState(wordlist))
        color = session.get('color') or dict((chr(ord('A') + char), 'gray') for char in range(0, 26))
        return render_template('index.html', wordlist=wordlist, optimum=optimum, color=color)

    wordlist = []
    response = []

    for i in range(5):
        response.append(int(request.form.get(f'resp{i}')))

    if not all(map(lambda elem: elem != None and elem >= 0 and elem <= 2, response)):
        return redirect(url_for('index'))

    if not is_valid_word(request.form.get('guess')):
        return redirect(url_for('index'))

    wordlist = list(map(lambda arg: arg.strip(), open(session.get("wordlist") or 'final_words').readlines()))
    state = WordleState(wordlist)
    state.adjust(request.form.get('guess'), response)

    wordlist = session.get('wordlist')
    if wordlist and wordlist.startswith('wordlist'):
        try:
            fileids.remove(int(wordlist[8:]))
        except:
            stderr.write("Invalid file id!")
    
    fileid = get_id()
    fileids.add(fileid)

    with open(f'wordlist{fileid}', 'w') as file:
        file.write('\n'.join(state.wordlist))

    session['wordlist'] = f'wordlist{fileid}'
    session['optimum'] = find_optimum(state)
    session['color'] = adjust_color(session.get('color'), request.form.get('guess'), response)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0")