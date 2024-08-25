from flask import Flask, jsonify, request
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!doctype html>
    <html>
    <head>
        <title>Run Script</title>
        <script>
            function runScript() {
                fetch('/run-script', { method: 'POST' })
                    .then(response => response.json())
                    .then(data => {
                        alert(data.message);
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
            }
        </script>
    </head>
    <body>
        <h1>Run Python Script</h1>
        <button onclick="runScript()">Run Script</button>
    </body>
    </html>
    '''

@app.route('/run-script', methods=['POST'])
def run_script():
    try:
        # Adjust the path to your script as necessary
        result = subprocess.run(['python', 'final-project.py'], capture_output=True, text=True)
        return jsonify({'message': result.stdout if result.returncode == 0 else 'Error running script.'})
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)
