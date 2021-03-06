from flask import Flask, render_template, request, escape, session
from search4letters import search_for_letters
from DBcm import UseDatabase, CredentialsError
from checker import check_logged_in

app = Flask(__name__)

app.config['dbconfig']={'host': '127.0.0.1', 'user': 'vsearch', 'password': 'king_9999', 'database': 'vsearchlogDB'}

def log_request(req: 'flask_request',res: str) -> None:
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = '''insert into log (phrase, letters, ip, browser_string, results) values (%s, %s, %s, %s,%s)'''
        cursor.execute(_SQL, (req.form['phrase'], req.form['letters'], req.remote_addr, req.user_agent.browser, res,))

@app.route('/search', methods=['POST'])
def do_search() -> 'html' :
    letters = request.form['letters']
    phrase = request.form['phrase']
    title = 'here are your results'
    results = str(search_for_letters(phrase,letters))
    try:
        log_request(request,results)
    except Exception as err:
        print('error', str(err))
    return render_template('results.html', the_phrase = phrase, the_letters=letters, the_tile=title, the_results=results)

@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html',the_title='welcome to search on the web!')

@app.route('/viewlog')
@check_logged_in
def view_the_log() -> 'html':
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL='''select phrase, letters, ip, browser_string, results from log'''
            cursor.execute(_SQL)
            contents = cursor.fetchall()
        titles=('phrase', 'lettes', 'remote_addr', 'user_agent', 'results')
        return render_template('viewlog.html', the_title='view log', the_row_titles=titles, the_data=contents)
    except CredentialsError as err:
        print('username or password issues. error:', str(err))

@app.route('/login')
def do_login() -> str:
    session['logged_in']=True
    return 'you are now logged in'

app.secret_key='king_9999'

@app.route('/logout')
def do_logout() -> str:
    session.pop('logged_in')
    return 'you are now logged out'

@app.route('/status')
def cheeck_status() -> str:
    if 'logged_in' in session:
        return 'you are currently logged in'
    return 'you are not logged in'
if __name__ == '__main__':
    app.run(debug=True)