from src.models.models import SQLAlchemy
from src.models.models import db, Person

class user_repository:

    def person_info(self, person_id):
        return Person.query.get(person_id)
        
user_repository_singleton = user_repository()