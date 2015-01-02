__author__ = 'simone.decristofaro'

from flask import Flask, request

app=Flask(__name__)

@app.route('/')
@app.route('/hello')
def hello():
    return sayHello('World')

@app.route('/hello/<name>')
def sayHello(name):
    """
    Say hello to a person
    :param str name:
    :return:
    """
    return 'Hello ' + name

@app.route('/methodType', methods=['GET', 'POST'])
def methodType():
    if request.method == 'POST':
        return 'The method is: POST'
    else:
        return 'The method is: GET'


def main():
    app.run(debug=True)

if __name__=='__main__':
    main()
