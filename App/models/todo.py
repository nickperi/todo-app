from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from App.models.user import User

class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('student.studentid'), nullable=False)
    text = db.Column(db.String(120), nullable=False, unique=True)
    done = db.Column(db.Boolean, default=False)

    def __init__(self, text, user_id):
        self.text = text
        self.user_id = user_id


    def toggle(self):
        self.done = not self.done
        db.session.add(self)
        db.session.commit()

    def get_username(self):
        user = User.query.filter_by(id=self.user_id).first() # type: ignore
        return user.username

    def get_json(self):
        return {
      "id": self.id,
      "student id": self.user_id,
      "text": self.text,
      "done": self.done,
    }


    
