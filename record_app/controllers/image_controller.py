from flask import Blueprint, request, redirect, abort, url_for, current_app
from pathlib import Path
from models.records import Record
import boto3
from flask_login import login_required, current_user

record_images = Blueprint('record_images', __name__)

@record_images.route("/records/<int:id>/image/", methods=["POST"])
@login_required
def update_image(id):

    record = Record.query.get_or_404(id)
    
    if "image" in request.files:
        
        image = request.files["image"]
        
        if Path(image.filename).suffix != ".png":
            return abort(400, description="Invalid file type")
        
        bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
        bucket.upload_fileobj(image, record.image_filename)


        return redirect(url_for("records.get_record", id=id))

    return abort(400, description="No image")