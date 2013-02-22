"Models are loosely listed by dependency."

from django.db import models
from dicom_models.core import models as core

APP_LABEL = 'dicom_production'

class Base(models.Model):
    class Meta(object):
        abstract = True
        app_label = APP_LABEL

class Patient(core.Patient, Base):
    pass

class PatientMixin(Base):
    "A mixin that provides a foreign key reference to Patient"
    patient = models.ForeignKey(Patient)

    class Meta(Base.Meta):
        abstract = True

class UniquePatientMixin(Base):
    "A mixin that provides a one2one reference to Patient"
    patient = models.OneToOneField(Patient)

    class Meta(Base.Meta):
        abstract = True
        
class Encounter(core.Encounter, PatientMixin):
    pass

class EncounterMixin(PatientMixin):
    """A mixin that provides a foreign key reference to Encounter as well as
    a reference the Patient. This future-proofs the model for new query
    capabilities that ignores the encounter constraint.
    """
    encounter = models.ForeignKey(Encounter)

    class Meta(PatientMixin.Meta):
        abstract = True

class RadiologyStudy(core.RadiologyStudy, EncounterMixin):
    pass

class DataAvailability(core.DataAvailability, UniquePatientMixin):
    pass
