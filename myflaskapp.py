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
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
                background-color: #f4f4f4;
            }
            h1 {
                margin-bottom: 20px;
            }
            button {
                background-color: #007bff;
                border: none;
                color: white;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 5px;
                transition: background-color 0.3s ease;
            }
            button:hover {
                background-color: #0056b3;
            }
            @media (max-width: 600px) {
                button {
                    padding: 12px 24px;
                    font-size: 14px;
                }
            }
        </style>
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
    app.run(host='0.0.0.0', port=5000, debug=True)
