from flask import Flask, jsonify, request
from spellcorrect import *

# define Flask app
app = Flask(__name__)

@app.route('/spellCorrect')
def spellcorrect():
    """
    urls should take the form '/spellCorrect?text=my%20text'
    """
    text = request.args.get('text', '')
    
    return jsonify(**multiwordcheck(text))



if __name__ == '__main__':
    # app runs in debug mode, turn this off if you're deploying
    app.run(debug=True)