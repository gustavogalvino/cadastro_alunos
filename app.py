from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from requests import api


def busca_cep(cep):
    try:
        url = api.get(f"https://viacep.com.br/ws/{cep}/json/")
        if url.status_code == 200:
            return url.json()
        else:
            raise ValueError
    except ValueError:
        return False


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////logbox.db'
db = SQLAlchemy(app)


class Logbox(db.Model):
    ra = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(60))
    email = db.Column(db.String(50), unique=True)
    logradouro = db.Column(db.String(50))
    numero = db.Column(db.String(20))
    cep = db.Column(db.String(10))
    complemento = db.Column(db.String(60))

    def __init__(self, nome, email, logra, num, cep, compl):
        self.nome = nome
        self.email = email
        self. logradouro = logra
        self.numero = num
        self.cep = cep
        self.complemento = compl


@app.route('/')
def index():
    cadastro_alunos = Logbox.query.all()
    return render_template("index.html", cadastro_alunos=cadastro_alunos)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        end = busca_cep(request.form['cep'])
        aluno = Logbox(
            request.form['nome'], request.form['email'], end['logradouro'],
            request.form['num'], end['cep'], request.form['compl'])
        db.session.add(aluno)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/edit/<int:ra>', methods=['GET', 'POST'])
def edit(ra):
    aluno = Logbox.query.get(ra)
    if request.method == 'POST':
        aluno.nome = request.form['nome']
        aluno.email = request.form['email']
        aluno.logradouro = request.form['logra']
        aluno.numero = request.form['num']
        aluno.cep = request.form['cep']
        aluno.complemento = request.form['compl']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', aluno=aluno)


@app.route('/delete/<int:ra>')
def delete(ra):
    aluno = Logbox.query.get(ra)
    db.session.delete(aluno)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
