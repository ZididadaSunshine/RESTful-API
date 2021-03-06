import datetime

from app.main import db
from app.main.model.brand_synonym_association import BrandSynonym
from app.main.model.synonym_model import Synonym
from app.main.utility.datalogger import log_time


class SynonymServiceResponse:
    Success = 200
    Created = 201
    AlreadyExists = 409
    DoesNotExist = 404


def preprocess_synonym(synonym):
    return synonym.lower()


@log_time('get_active_synonyms')
def get_active_synonyms():
    """ Get a list of synonyms that are currently associated with a brand.
        Returns how many associations each synonym has. """
    return db.session.query(Synonym.synonym, db.func.count(Synonym.synonym)).join(Synonym.brands).\
        group_by(Synonym.id).all()


@log_time('get_brand_synonyms')
def get_brand_synonyms(brand_id):
    """ Get the synonyms associated with a brand. """
    return Synonym.query.\
        join(BrandSynonym, (Synonym.id == BrandSynonym.synonym_id) & (BrandSynonym.brand_id == brand_id)).all()


@log_time('add_synonym')
def add_synonym(brand_id, synonym_data):
    """ Add a synonym to be associate with a brand. """
    synonym = preprocess_synonym(synonym_data['synonym'])

    # Check if the synonym already exists
    # If it does not exist, create it
    existing = Synonym.query.filter(Synonym.synonym.ilike(synonym)).first()
    if not existing:
        synonym = Synonym(synonym=synonym)

        db.session.add(synonym)
        db.session.flush()

        # Refresh the current session in order to get the new synonym
        db.session.refresh(synonym)
        existing = synonym

    # Check if the synonym is already associated with the brand
    if BrandSynonym.query.filter((BrandSynonym.brand_id == brand_id) & (BrandSynonym.synonym_id == existing.id)).\
            scalar():
        return dict(success=False,
                    message="The synonym is already associated with the brand."), SynonymServiceResponse.AlreadyExists

    # Create an association between the synonym and the brand
    association = BrandSynonym(brand_id=brand_id, synonym_id=existing.id, created_at=datetime.datetime.utcnow())

    db.session.add(association)
    db.session.commit()

    return dict(success=True), SynonymServiceResponse.Created


@log_time('delete_synonym')
def delete_synonym(brand_id, synonym):
    processed_synonym = preprocess_synonym(synonym)

    # Get the associated synonym
    existing = Synonym.query.filter_by(synonym=processed_synonym).\
        join(BrandSynonym, (BrandSynonym.brand_id == brand_id) & (BrandSynonym.synonym_id == Synonym.id)).first()
    if not existing:
        return dict(success=False, message='The requested synonym does not exist.'), SynonymServiceResponse.DoesNotExist

    # Delete the association
    BrandSynonym.query.filter_by(synonym_id=existing.id, brand_id=brand_id).delete()
    db.session.commit()

    # Currently, we do not care about deleting orphaned synonyms
    # TODO: Might want to delete orphaned synonyms without mentions in the future

    return dict(success=True), SynonymServiceResponse.Success
