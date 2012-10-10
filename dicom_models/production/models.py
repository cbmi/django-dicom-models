"Models are loosely listed by dependency."

from django.db import models
from dicom_models.core import models as core
from vocab.managers import ItemThroughManager

APP_LABEL = 'dicom_production'

class Base(models.Model):
    class Meta(object):
        abstract = True
        app_label = APP_LABEL

class Patient(core.Patient, Base):
    pass

class Encounter(core.Encounter, PatientMixin):
    pass

class RadiologyStudy(core.RadiologyStudy, EncounterMixin):
    pass
