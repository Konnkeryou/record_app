from main import db


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