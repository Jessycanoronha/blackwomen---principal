from extensions import db 
from sqlalchemy import inspect
from sqlalchemy.exc import OperationalError 

class Woman(db.Model):
    __tablename__ = 'woman'  

    id = db.Column(db.String(50), primary_key=True)  
    description = db.Column(db.Text, nullable=True)
    additional_metadata = db.Column(db.JSON, nullable=True)
    order = db.Column(db.Integer, nullable=False)
    slug = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=True)
    birthdate = db.Column(db.String(100), nullable=True)
    deathdate = db.Column(db.String(100), nullable=True)
    credits = db.Column(db.String(100), nullable=True)
    image_url = db.Column(db.Text, nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'additional_metadata': self.additional_metadata,
            'order': self.order,
            'slug': self.slug,
            'title': self.title,
            'country': self.country,
            'birthdate': self.birthdate,
            'deathdate': self.deathdate,
            'credits': self.credits,
            'image_url': self.image_url
        }

    def __repr__(self):
        return f'<Woman {self.title}>'

def create_table_if_not_exists(model):
    inspector = inspect(db.engine)
    if not inspector.has_table(model.__tablename__):
        try:
            model.__table__.create(db.engine)
            print(f"Tabela '{model.__tablename__}' criada com sucesso.")
            return True
        except OperationalError as e:
            print(f"Erro ao criar tabela '{model.__tablename__}': {str(e)}")
            return False
    else:
        print(f"Tabela '{model.__tablename__}' já existe.")
        return True
    
