from flask import Flask
from search4letters import search_for_letters
from flask import render_template
from flask import request

app = Flask(__name__)

def log_request(req: 'flask_request',res: str) -> None:
    with open('vsearch.log', 'a') as log:
        print(req, res, file=log)

'''
@app.route('/')
def hello() -> str:
    return  'hello world from Flask!'
'''
@app.route('/search', methods=['POST'])
def do_search() -> 'html' :
    letters = request.form['letters']
    phrase = request.form['phrase']
    title = 'here are your results'
    #return str(search_for_letters(phrase,letters))
    results = str(search_for_letters(phrase,letters))
    log_request(request,results)
    return render_template('results.html', the_phrase = phrase, the_letters=letters, the_tile=title, the_results=results)

@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html',the_title='welcome to search on teh web!')

if __name__ == '__main__':
    app.run(debug=True)