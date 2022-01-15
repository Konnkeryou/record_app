from enum import unique
import os 
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

(
    db_user,db_pass,db_name,db_domain
) = (os.environ.get(item) for item in [
    "DB_USER",
    "DB_PASS",
    "DB_NAME",
    "DB_DOMAIN"
    ]
)

app = Flask (__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_domain}/{db_name}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db = SQLAlchemy(app)

class Record (db.Model): 
    __tablename__ = "records"
    record_id = db.Column(db.Integer, primary_key=True)
    record_name = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, reccord_name):
        self.record_name = reccord_name
    
    @property
    def serialize(self):
        return {
            "record_id": self.record_id,
            "record_name": self.record_name
        }

db.create_all()

@app.route('/')
def HomePage():
    return "hello, world!"

@app.route("/records/", methods=["GET"])
def get_records(): 
    records = Record.query.all()
    return jsonify([record.serialize for record in records])

@app.route("/records/", methods=["POST"])
def create_record():
    new_record=Record(request.json['record_name'])
    db.session.add(new_record)
    db.session.commit()
    return jsonify(new_record.serialize)

@app.route("/records/<int:id>/", methods = ["GET"])
def get_record(id):
    record = Record.query.get_or_404(id)
    return jsonify(record.serialize)

@app.route("/records/<int:id>/", methods = ["PUT", "PATCH"])
def update_record(id):
    record = Record.query.filter_by(record_id=id)
    record.update(dict(record_name=request.json["record_name"]))
    db.session.commit()
    return jsonify(record.first().serialize)

@app.route("/records/<int:id>/", methods = ["DELETE"])
def delete_record(id):
    record = Record.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    return jsonify(record.serialize)

if __name__ == '__main__':
    app.run(debug=True)

