from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/searching_choice.html')
def searching_choice():
    return render_template('searching_choice.html')

@app.route('/navbar.html')
def navbar():
    return render_template('util/navbar.html')

@app.route('/file_picker.html')
def file_picker():
    return render_template('util/file_picker.html')

if __name__ == '__main__':
    app.run(debug=True)
