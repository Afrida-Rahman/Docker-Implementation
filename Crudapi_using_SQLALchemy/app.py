import os
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    body = db.Column(db.Text())

@app.route('/')
def root():
    return jsonify(message='hello world!'), 200

@app.route('/notes')
def index():
    # TODO: come up with solution for type incompatibility
    notes = Note.query.all()

    serialized_notes = []

    for note in notes:
        serialized_notes.append({
            'title': note.title,
            'body': note.body,
        })

    return jsonify(message='all notes', data=serialized_notes), 200

@app.route('/notes', methods=['POST'])
def store():
    title = request.json['title']
    body = request.json['body']

    note = Note(title=title, body=body)

    db.session.add(note)
    db.session.commit()

    return jsonify(message='note created', data={ 'title': note.title, 'body': note.body }), 201

@app.route('/notes/<id>')
def show(id):
    note = Note.query.filter_by(id=id).first()
    return jsonify(message='single note', data={ 'id':note.id ,'title': note.title, 'body': note.body }), 200

@app.route('/notes/<id>', methods=['PUT'])
def update(id):
    note = Note.query.filter_by(id=id).first()

    note.title = request.json['title'] if request.json['title'] else note.title
    note.body = request.json['body'] if request.json['body'] else note.body

    db.session.commit()

    return jsonify(message='udpate note', data={ 'id':note.id ,'title': note.title, 'body': note.body }), 200

@app.route('/notes/<id>', methods=['DELETE'])
def delete(id):
    note = Note.query.filter_by(id=id).first()

    db.session.delete(note)
    db.session.commit()

    return jsonify(message='delete note', data=None), 200
