from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from App.models.user import User

class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.String(120), nullable=False)
    done = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_due = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, text, user_id, date_due):
        self.text = text
        self.user_id = user_id
        self.date_due = date_due


    def toggle(self):
        self.done = not self.done
        db.session.add(self)
        db.session.commit()

    def get_user_type(self):
        user = User.query.filter_by(id=self.user_id).first()
        return user.get_user_type()
    
    def get_username(self): 
        user = User.query.filter_by(id=self.user_id).first()

        if not user:
            return None
        return user.username
        

    def get_json(self):
        return {
      "id": self.id,
      "user_id": self.user_id,
      "text": self.text,
      "done": self.done,
      "date_due": self.date_due.strftime("%Y-%m-%d")
    }


    
