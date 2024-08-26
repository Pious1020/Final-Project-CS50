from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    run_script()
    return '', 204

def run_script():
    try:
        subprocess.run(['python', 'final-project.py'], capture_output=True, text=True)
    except Exception as x:
        print(f'Error running script: {str(x)}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
