from uuid import UUID
from sqlmodel import select
from app.models.persons import Person, PersonIn, PersonOut
from app.db.session import get_session

def create_person(person: PersonIn) -> PersonOut:
    with next(get_session()) as session:
        db_person = Person.model_validate(person)
        session.add(db_person)
        session.commit()
        session.refresh(db_person)
        return PersonOut.model_validate(db_person)

def list_persons() -> list[PersonOut]:
    with next(get_session()) as session:
        persons = session.exec(select(Person)).all()
        return [PersonOut.model_validate(p) for p in persons]

def update_person(person_id: UUID, updated_data: PersonIn) -> PersonOut:
    with next(get_session()) as session:
        db_person = session.get(Person, person_id)
        if not db_person:
            raise ValueError("Person not found")

        # Update the fields
        for field, value in updated_data.model_dump(exclude_unset=True).items():
            setattr(db_person, field, value)

        session.add(db_person)
        session.commit()
        session.refresh(db_person)
        return PersonOut.model_validate(db_person)

def delete_person(person_id: UUID) -> None:
    with next(get_session()) as session:
        db_person = session.get(Person, person_id)
        if not db_person:
            raise ValueError("Person not found")

        session.delete(db_person)
        session.commit()