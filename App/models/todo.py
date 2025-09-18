from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from App.models.user import User

class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(120), default="personal")
    done = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_due = db.Column(db.DateTime, default=datetime.now)
    date_completed = db.Column(db.DateTime)

    def __init__(self, text, user_id, date_due, category):
        self.text = text
        self.user_id = user_id
        self.date_due = date_due
        self.category = category


    def toggle(self):
        self.done = not self.done
        db.session.add(self)
        db.session.commit()



    def calculate_time_elapsed(self, date_due, date_created):
        diff = date_due - date_created
        seconds = diff.total_seconds()

        if(seconds < 60):
            return f"{int(seconds)}s"
        elif(seconds < 3600):
            return f"{int(seconds//60)}m"
        elif(seconds < 86400):
            return f"{int(seconds//3600)}h"
        elif(seconds < 604800):
            return f"{int(seconds//86400)}d"
        elif(seconds < 2419200):
            return f"{int(seconds//604800)}w"
        else:
            return f"{diff}"
        


    def get_user_type(self):
        user = User.query.filter_by(id=self.user_id).first()
        return user.get_user_type()
    
    def get_username(self): 
        user = User.query.filter_by(id=self.user_id).first()

        if not user:
            return None
        return user.username
        

    def get_json(self):

        if self.done:

            if self.date_due:

                if self.date_created:
                    return {
                        "id": self.id,
                        "user_id": self.user_id,
                        "text": self.text,
                        "done": self.done,
                        "category": self.category,
                        "date_created": self.date_created.strftime("%a, %b %d, %Y %I:%M %p"),
                        "create_date": self.date_created.strftime("%Y-%m-%d"),
                        "date_due": self.date_due.strftime("%Y-%m-%d"),
                        "time_due": self.date_due.strftime("%I:%M %p"),
                        "date_time_due": self.date_due.strftime("%a, %b %d, %Y %I:%M %p"),
                        "date_completed": self.date_completed.strftime("%a, %b %d, %Y %I:%M %p"),
                        "time_taken": self.calculate_time_elapsed(self.date_completed, self.date_created)
                    }
                else:
                    return {
                        "id": self.id,
                        "user_id": self.user_id,
                        "text": self.text,
                        "done": self.done,
                        "category": self.category,
                        "date_created": None,
                        "create_date": None,
                        "date_due": self.date_due.strftime("%Y-%m-%d"),
                        "time_due": self.date_due.strftime("%I:%M %p"),
                        "date_time_due": self.date_due.strftime("%a, %b %d, %Y %I:%M %p"),
                        "date_completed": self.date_completed.strftime("%a, %b %d, %Y %I:%M %p"),
                        "time_taken": self.calculate_time_elapsed(self.date_completed, self.date_created)
                    }
            
            else:

                if self.date_created:
                    return {
                        "id": self.id,
                        "user_id": self.user_id,
                        "text": self.text,
                        "done": self.done,
                        "category": self.category,
                        "date_created": self.date_created.strftime("%a, %b %d, %Y %I:%M %p"),
                        "create_date": None,
                        "date_due": None,
                        "time_due": None,
                        "date_completed": None,
                        "time_taken": None
                    }
                else:
                     return {
                        "id": self.id,
                        "user_id": self.user_id,
                        "text": self.text,
                        "done": self.done,
                        "category": self.category,
                        "date_created": None,
                        "create_date": None,
                        "date_due": None,
                        "time_due": None,
                        "date_completed": None,
                        "time_taken": None
                    }
        
        else:
            if self.date_due:

                if self.date_created:
                    return {
                        "id": self.id,
                        "user_id": self.user_id,
                        "text": self.text,
                        "done": self.done,
                        "category": self.category,
                        "date_created": self.date_created.strftime("%a, %b %d, %Y %I:%M %p"),
                        "create_date": self.date_created.strftime("%Y-%m-%d"),
                        "date_due": self.date_due.strftime("%Y-%m-%d"),
                        "time_due": self.date_due.strftime("%I:%M %p"),
                        "date_time_due": self.date_due.strftime("%a, %b %d, %Y %I:%M %p"),
                        "date_completed": None,
                        "time_taken": None
                    }
                else:
                    return {
                        "id": self.id,
                        "user_id": self.user_id,
                        "text": self.text,
                        "done": self.done,
                        "category": self.category,
                        "date_created": None,
                        "create_date": None,
                        "date_due": self.date_due.strftime("%Y-%m-%d"),
                        "time_due": self.date_due.strftime("%I:%M %p"),
                        "date_time_due": self.date_due.strftime("%a, %b %d, %Y %I:%M %p"),
                        "date_completed": None,
                        "time_taken": None
                    }
            
            else:

                if self.date_created:
                    return {
                        "id": self.id,
                        "user_id": self.user_id,
                        "text": self.text,
                        "done": self.done,
                        "category": self.category,
                        "date_created": self.date_created.strftime("%a, %b %d, %Y %I:%M %p"),
                        "create_date": self.date_created.strftime("%Y-%m-%d"),
                        "date_due": None,
                        "date_completed": None,
                        "time_taken": None
                    }
                else:
                    return {
                        "id": self.id,
                        "user_id": self.user_id,
                        "text": self.text,
                        "done": self.done,
                        "category": self.category,
                        "date_created": None,
                        "create_date": None,
                        "date_due": None,
                        "date_completed": None,
                        "time_taken": None
                    }
                


    
