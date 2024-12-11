from extensions import db 
from sqlalchemy.exc import SQLAlchemyError
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique= True)
    email = db.Column(db.String(200),nullable=False, unique=True)
    password = db.Column(db.String(200))
    created_at = db.Column(db.DateTime(),nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(),nullable=False, server_default=db.func.now(),onupdate=db.func.now())

    posts = db.relationship('Post', back_populates='author', lazy='dynamic')

    comments = db.relationship('Comment', back_populates='user', lazy='dynamic')

    @property
    def data(self):
        return{
            'id':self.id, 
            'email':self.email, 
            'name':self.name, 
            'password':self.password
        }
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error saving in the database: {e}")
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit(self)
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error deleting from the database: {e}")

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()