# Copyright (c) 2012, The Children's Hospital of Philadelphia
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
#    disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
#    following disclaimer in the documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.from datetime import datetime
from django.db import models
from dicom_models.core import models as core

APP_LABEL = 'dicom_staging'

class Base(models.Model):
    class Meta(object):
        abstract = True
        app_label = APP_LABEL

class Patient(core.Patient, Base):
    pass

# The below models are bound to the Patient model via a ForeignKey
# relationship. Multiple instances can be associated to a Patient.
class PatientMixin(Base):
    "A mixin that provides a foreign key reference to Patient"
    patient = models.ForeignKey(Patient)

    class Meta(Base.Meta):
        abstract = True

# The below models are uniqely bound to the Patient model via a 
# OneToOne relationship. Every must patient instance must have
# an associated object for each one of the below models.
class UniquePatientMixin(Base):
    "A mixin that provides a one2one reference to Patient"
    patient = models.OneToOneField(Patient)

    class Meta(Base.Meta):
        abstract = True

class PatientPhi(core.PatientPhi, UniquePatientMixin):
    pass

class Encounter(core.Encounter, PatientMixin):
    pass

# The next level of organization is the encounter
class EncounterMixin(PatientMixin):
    """A mixin that provides a foreign key reference to Encounter as well as
    a reference the Patient. This future-proofs the model for new query
    capabilities that ignores the encounter constraint.
    """
    encounter = models.ForeignKey(Encounter)

    class Meta(PatientMixin.Meta):
        abstract = True

class RadiologyStudy(core.RadiologyStudy, EncounterMixin):
    original_study_uid = models.CharField(null=True, max_length=64, blank=True)
    requested = models.BooleanField(default=False)
    exclude = models.BooleanField(default=False)
    image_published = models.BooleanField(default=False, blank=True)
    pub_date = models.DateTimeField(null=True, blank=True)
    study_date = models.DateTimeField(null=True, blank=True)
    accession_no = models.CharField(max_length=20, blank=True)
    high_risk_flag = models.BooleanField(default=False)
    high_risk_message = models.CharField(null=True, max_length=500, blank=True);

    def __unicode__(self):
        return u'Study UID %s' % (self.original_study_uid or 'Unknown')

    class Meta(object):
        verbose_name_plural = "Radiology Studies"

class RadiologyStudyReview(core.base.Base):
    study = models.ForeignKey(RadiologyStudy)
    user_id = models.IntegerField()
    has_phi = models.NullBooleanField("Has PHI?", default=None, help_text="This study contains images with PHI burnt in.")
    has_reconstruction = models.BooleanField("Has facial reconstruction?", default=False)
    has_protocol_series = models.BooleanField("Has a protocol series?", default=True, help_text="This study has a patient protocol series.")
    relevant = models.BooleanField("Relevant?", default=False, help_text="This study contains relevant images.")
    exclude = models.BooleanField("Exclude for other reasons?", default=False, help_text="Exclude study for other reasons (please use comment field).")
    comment = models.TextField("Reviewer Comment", blank=True, null=True)
