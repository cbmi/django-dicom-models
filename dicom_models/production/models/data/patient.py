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
import random
from datetime import date, timedelta

from django.db import models

from core.utils import conversions
from core.models.base import Base

__all__ = ('PatientPhi', 'Patient')

MAX_ALIAS_NUM = 10 ** 6 - 1
MIN_ALIAS_NUM = 10 ** 5
ALIAS_FORMAT = 'P%d'
DOB_OFFSET_RANGE = (-15, 15)

class PatientPhi(Base):
    """This model decouples private health information from the base `patient`
    model ensuring that any cross query reference will not return PHI to
    unauthorized users.
    """
    mrn = models.CharField(max_length=50, unique=True, db_index=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50)
    dob = models.DateField('adjusted date of birth')
    real_dob = models.DateField('date of birth', null=True)
    dob_offset = models.IntegerField(null=True)
    zipcode = models.CharField(max_length=10, null=True)

    class Meta(object):
        abstract = True
        verbose_name_plural = u'patient phi'

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

    @property
    def pretty_age(self):
        "Returns the patient's current age in a pretty format."
        # we need today's date to compare against the adjusted dob. we cannot
        # have a negative age, therefore if the randomized offset is greater
        # than the patient's current age, we must round up to 0
        today = date.today()
        dob = self.dob

        if (today - self.dob).days < 0:
            dob = today

        return conversions.dates_to_age(dob, today)

    def offset_dob(self):
        "Generates a random offset for the adjusted dob."
        r = random.SystemRandom()
        offset = r.randint(*DOB_OFFSET_RANGE)
        self.dob_offset = offset
        self.dob = self.real_dob + timedelta(days=offset)

        return offset


class PatientManager(models.Manager):
    def generate_alias(self, attempts=20):
        "Randomly generates an alias that is unique."
        qs = self._get_query_set()
        r = random.SystemRandom()

        for i in xrange(attempts):
            n = r.randint(MIN_ALIAS_NUM, MAX_ALIAS_NUM)
            alias = ALIAS_FORMAT % n

            # ensure this alias is not already taken
            if not qs.filter(alias=alias).exists():
                return alias

        raise StandardError, 'max attempts have been reached (n=%d)' % attempts


class Patient(Base):
    """Defines the patient model.

    `alias` is an arbitrary public identifier for users to be able to reference
    when traversing the data.
    """
    SEX_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    alias = models.CharField(max_length=100, unique=True, db_index=True)
    sex = models.CharField(max_length=20, choices=SEX_CHOICES, null=True)
    ethnicity = models.CharField(max_length=50, null=True)

    objects = PatientManager()

    class Meta(object):
        abstract = True

    def __unicode__(self):
        return u'%s' % self.alias

    def save(self, generate_alias=True):
        "Extended to auto-generate an alias if one does not already exist."
        if generate_alias and not self.alias:
            self.alias = self.objects.generate_alias()
        super(Patient, self).save()
