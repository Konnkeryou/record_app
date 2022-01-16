from main import ma 
from models.records import Record
from marshmallow_sqlalchemy import auto_field 
from marshmallow.validate import Length, Range

class RecordSchema(ma.SQLAlchemyAutoSchema):
    record_id = auto_field(dump_only=True)
    record_name = auto_field(required=True, validate=Length(min=1))
    description = auto_field(validate=Length(min=1))
    cost = auto_field(required = False, validate=Range(0, 500))
    creator = ma.Nested(
        "UserSchema",
        only=("id", "name", "email",)
    )
    students = ma.Nested(
        "UserSchema",
        only=("id", "name", "email",)
    )

    class Meta:
        model = Record
        load_instance = True

record_schema = RecordSchema()
records_schema = RecordSchema(many=True)