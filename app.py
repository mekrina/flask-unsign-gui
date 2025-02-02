from flask import Flask, render_template, request, jsonify
from flask_unsign import session, decode, sign
from ast import literal_eval
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/decode', methods=['POST'])
def decode_cookie():
    # 获取用户输入的 Cookie
    encoded_data = request.form.get('encoded_data')
    secret = request.form.get('secret')

    try:
        # 解码 Cookie
        decoded_data = decode(encoded_data)
        for key,value in decoded_data.items():
            if(isinstance(value,bytes)):
                decoded_data[key] = value.decode()
        timestamp = datetime.fromtimestamp(decoded_data.get('_fresh', 0)).strftime('%Y-%m-%d %H:%M:%S')
        is_valid = session.verify(encoded_data, secret) if secret else False

        return jsonify({
            'success': True,
            'decoded_data': decoded_data,
            'timestamp': timestamp,
            'is_valid': is_valid
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })
@app.route('/sign', methods= ['POST'])
def sign_session():
    decoded_data = request.form.get('decoded_data')
    try:
        decoded_data = literal_eval(decoded_data)
    except:
        pass
    secret = request.form.get('secret')
    error = ''
    if(not isinstance(decoded_data,dict)):
       error = 'decoded_data should be a valid dictionary in python for example {"user": "admin"}'
    if(not secret and not error):
        error = 'secret should not be blank when sign_session'
    if(not error):
        try:
            encoded_data = sign(decoded_data,secret=secret)
        except Exception as e:
            error = str(e)
    if(error):
        return jsonify({
            'success': False,
            'error': error
        })
    else:
        print(encoded_data)
        return jsonify({
            'encoded_data': encoded_data,
            'success': True
        })
        
if __name__ == '__main__':
    app.run(debug=True)