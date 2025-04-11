from flask import Flask, render_template, request, redirect, send_file
from sheets import get_all_data, add_row, delete_row, update_row
from docs import generate_doc_and_export_pdf

app = Flask(__name__)

@app.route('/')
def index():
    data = get_all_data()
    return render_template('index.html', data=data)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    email = request.form['email']
    note = request.form['note']
    add_row([name, email, note])
    return redirect('/')

@app.route('/delete/<int:index>')
def delete(index):
    delete_row(index)
    return redirect('/')

@app.route('/update/<int:index>', methods=['POST'])
def update(index):
    name = request.form['name']
    email = request.form['email']
    note = request.form['note']
    update_row(index, [name, email, note])
    return redirect('/')

@app.route('/export/<int:index>')
def export(index):
    pdf_path = generate_doc_and_export_pdf(index)
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)