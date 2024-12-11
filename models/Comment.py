from extensions import db

from sqlalchemy.exc import SQLAlchemyError

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    user_id =db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user = db.relationship('User', back_populates='comments')
    post = db.relationship('Post', back_populates='comments')

    @property
    def data(self):
        return{
            'id':self.id, 
            'content':self.content, 
            'author':self.author_data, 
            'post':self.post_data,
            'created_at':self.created_at.strftime('%Y-%m-%d %H:%M:%S'), 
            'updated_at':self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
    @property
    def author_data(self):
        return {
            'id':self.author.id, 
            'username':self.author.username, 
            'email':self.author.email
        }if self.author else None
    @property
    def post_data(self):
        return {
            'id':self.post.id,
            'title':self.post.tittle
        }if self.post else None
    
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error saving to the database: {e}")
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error deleting from the database")
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

