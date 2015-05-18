__author__ = 'simone.decristofaro'

from flask import Flask, request
import time

app = Flask(__name__)


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


@app.route('/wait')
def waitForService():
    # here we want to get the value of user (i.e. ?user=some-value)
    waitTime = request.args.get('waitTime')
    secToWait = float(waitTime)
    print "Wait for " + str(secToWait) + " seconds"
    time.sleep(secToWait)
    return 'Waiting time = ' + str(secToWait) + ' sec, expired'


def main():
    app.run(debug=True, host='localhost')  # default host=localhost, default port=5000


if __name__ == '__main__':
    main()
