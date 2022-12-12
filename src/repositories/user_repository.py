from src.models.models import Person

class user_repository:

    def person_info(self, person_id):
        return Person.query.get(person_id)

    def get_person_by_email(self, email):
        return Person.query.filter_by(email=email).first()
        
user_repository_singleton = user_repository()