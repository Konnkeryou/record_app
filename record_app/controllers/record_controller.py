from flask import Blueprint, jsonify, request
from main import db
from models.records import Record

records = Blueprint('records', __name__)

@records.route('/')
def HomePage():
    return "hello, world!"

@records.route("/records/", methods=["GET"])
def get_records(): 
        records = Record.query.all()
        return jsonify([record.serialize for record in records])

@records.route("/records/", methods=["POST"])
def create_record():
        new_record=Record(request.json['record_name'])
        db.session.add(new_record)
        db.session.commit()
        return jsonify(new_record.serialize)

@records.route("/records/<int:id>/", methods = ["GET"])
def get_record(id):
        record = Record.query.get_or_404(id)
        return jsonify(record.serialize)

@records.route("/records/<int:id>/", methods = ["PUT", "PATCH"])
def update_record(id):
        record = Record.query.filter_by(record_id=id)
        record.update(dict(record_name=request.json["record_name"]))
        db.session.commit()
        return jsonify(record.first().serialize)

@records.route("/records/<int:id>/", methods = ["DELETE"])
def delete_record(id):
        record = Record.query.get_or_404(id)
        db.session.delete(record)
        db.session.commit()
        return jsonify(record.serialize)
