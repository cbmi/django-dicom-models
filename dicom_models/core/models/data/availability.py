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
from django.db.models import Q

from dicom_models.core.models.base import Base

__all__ = ('DataAvailability',)

class DataAvailability(Base):

    # imaging
    has_radiology_study = models.BooleanField(default=False)
    has_mri = models.BooleanField(default=False)
    has_ct = models.BooleanField(default=False)


    class Meta(object):
        abstract = True

    def _has_radiology_study(self):
        queryset = self.patient.radiologystudy_set.filter(
            Q(modality__iexact='mr') | Q(modality__iexact='mri') | Q(modality__iexact='ct')
        )
        return queryset.exists()

    def _has_mri(self):
        queryset = self.patient.radiologystudy_set.filter(
            Q(modality__iexact='mri') | Q(modality__iexact='mr')
        )
        return queryset.exists()

    def _has_ct(self):
        queryset = self.patient.radiologystudy_set.filter(modality__iexact='ct')
        return queryset.exists()

    def reset_calculated_fields(self, save=False):
        """Run a set of queries to test for the existence of certain data
        for the associated patient.

        This should be called immediately prior to pushing this data to
        production.
        """
        self.has_radiology_study = self._has_radiology_study()
        # since MRIs and CTs are modalities of radiology studies, only test
        # if there are any studies to begin with
        if self.has_radiology_study:
            self.has_ct = self._has_ct()
            self.has_mri = self._has_mri()
        else:
            self.has_ct = False
            self.has_mri = False

        if save:
            self.save()
