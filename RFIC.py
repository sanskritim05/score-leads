from flask import Flask, render_template, request, send_file
import os
from scoring_logic.calc_score import findScores
import csv

app = Flask(__name__)

UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    results = []
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            results = findScores(filepath) #call scoring func

            #write the file to export
            csv_path = os.path.join(app.config['UPLOAD_FOLDER'], 'results.csv')
            with open(csv_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=["Client Name", "Score", "Max Score"])
                writer.writeheader()
                writer.writerows(results)

    return render_template('index.html', results=results)

if __name__ == "__main__":
    app.run(debug=True)
