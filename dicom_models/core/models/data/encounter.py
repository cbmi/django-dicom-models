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

from dicom_models.core.utils import conversions
from dicom_models.core.models.base import Base

__all__ = ('Encounter',)

class Encounter(Base):
    """An `encounter` refers to any interaction in which a patient or guardian
    is involved. This holds the generic information independent of department.
    """
    visit_date = models.DateField()
    specialty = models.CharField(max_length=255, null=True)
    age = models.FloatField(null=True, db_index=True, help_text='age in years')

    class Meta(object):
        abstract = True

    def _set_age(self):
        "Helper method to set the age for this visit."
        self.age = conversions.dates_to_age(self.visit_date,
            self.patient.patientphi.dob, to_string=False)

    @property
    def pretty_age(self):
        return conversions.years_to_age(self.age)

    def reset_calculated_fields(self, save=False):
        self.age = None
        self._set_age()

        if save:
            self.save()
