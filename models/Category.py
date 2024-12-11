from extensions import db
from sqlalchemy.exc import SQLAlchemyError
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    post_id=db.Column(db.Integer,db.ForeignKey('posts.id'), nullable=False)

    posts = db.relationship('Post', back_populates='category', lazy='dynamic')

    @property
    def data(self):
        return {
            'id':self.id,
            'name':self.name
        }
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e :
            db.session.rollback()
            print(f"Error saving to the database: {e}")
    def delete(self):
        try: 
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error deleting from the database: {e}")
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self,key):
                setattr(self, key, value)
        self.save()