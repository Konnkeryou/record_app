from main import db
from models.users import User

enrolments = db.Table(
    'enrolments',
    db.Column('user_id', db.Integer, db.ForeignKey('flasklogin-users.id'), primary_key=True),
    db.Column('record_id', db.Integer, db.ForeignKey('records.record_id'), primary_key=True)
)

class Record(db.Model):
    # The tablename attribute specifies what the name of the table should be
    __tablename__ = "records"

    # These attributes specify what columns the table should have
    record_id = db.Column(db.Integer, primary_key=True)
    record_name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(200), server_default="No Description Provided")
    cost = db.Column(db.Integer, nullable=False, server_default="0")

    creator_id = db.Column(db.Integer, db.ForeignKey('flasklogin-users.id'))

    students = db.relationship(
        User,
        secondary=enrolments,
        backref=db.backref('enrolled_records'),
        lazy="joined"
    )

    @property
    def image_filename(self):
        return f"record_images/{self.record_id}.png"
