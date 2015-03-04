from plone.app.vocabularies.catalog import KeywordsVocabulary


class VenuesVocabulary(KeywordsVocabulary):
    keyword_index = 'venues'
VenuesVocabularyFactory = VenuesVocabulary()
