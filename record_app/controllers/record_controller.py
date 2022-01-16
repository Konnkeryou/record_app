from flask import Blueprint, jsonify, request, render_template, redirect, url_for, abort, current_app
from main import db
from models.records import Record
from schemas.record_schema import records_schema, record_schema
from flask_login import login_required, current_user
import boto3

records = Blueprint('records', __name__)

# This one is just a placeholder for now, no CRUD here
@records.route('/')
def homepage():
    data = {
        "page_title": "RECORD SHARE"
    }
    return render_template("homepage.html", page_data=data)

# The GET routes endpoint
@records.route("/records/", methods=["GET"])
def get_records():
    data = {
        "page_title": "Record Index",
        "records": records_schema.dump(Record.query.all())
    }
    return render_template("record_index.html", page_data=data)

# The POST route endpoint
@records.route("/records/", methods=["POST"])
@login_required
def create_record():
    new_record=record_schema.load(request.form)
    
    new_record.creator = current_user
    
    db.session.add(new_record)
    db.session.commit()

    return redirect(url_for("records.get_records"))

# An endpoint to GET info about a specific record
@records.route("/records/<int:id>/", methods = ["GET"])
def get_record(id):
    record = Record.query.get_or_404(id)
    
    s3_client=boto3.client("s3")
    bucket_name=current_app.config["AWS_S3_BUCKET"]
    image_url = s3_client.generate_presigned_url(
        'get_object',
        Params={
            "Bucket": bucket_name,
            "Key": record.image_filename
        },
        ExpiresIn=100
    )
    
    data = {
        "page_title": "Record Detail",
        "record": record_schema.dump(record),
        "image": image_url
    }
    return render_template("record_detail.html", page_data=data)

# A PUT/PATCH route to update record info
@records.route("/records/<int:id>/", methods=["POST"])
@login_required
def update_record(id):
    record = Record.query.filter_by(record_id=id)
    
    if current_user.id != record.first().creator_id:
        abort(403, "You do not have permission to alter this record!")
   
    updated_fields = record_schema.dump(request.form)
    if updated_fields:
        record.update(updated_fields)
        db.session.commit()

    data = {
        "page_title": "Record Detail",
        "record": record_schema.dump(record.first())
    }
    return render_template("record_detail.html", page_data=data)

@records.route("/records/<int:id>/enrol/", methods=["POST"])
@login_required
def enrol_in_record(id):
    record = Record.query.get_or_404(id)
    record.students.append(current_user)
    db.session.commit()
    return redirect(url_for('users.user_detail'))

@records.route("/records/<int:id>/drop/", methods=["POST"])
@login_required
def drop_record(id):
    record = Record.query.get_or_404(id)
    record.students.remove(current_user)
    db.session.commit()
    return redirect(url_for('users.user_detail'))

@records.route("/records/<int:id>/delete/", methods=["POST"])
@login_required
def delete_record(id):
    record = Record.query.get_or_404(id)

    if current_user.id != record.creator_id:
        abort(403, "You do not have permission to delete this record!")

    db.session.delete(record)
    db.session.commit()
    return redirect(url_for("records.get_records"))