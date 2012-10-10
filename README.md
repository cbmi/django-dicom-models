Django Models for Research DICOM Applications

This repository contains models separated into two different Django Apps

1. production - These models are meant to be used in a production research system that must track information about de-identified DICOM studies. 
2. staging - These models inherit from the models found in production, but are meant to be used internally as part of a de-identification process. For example, staging.RadiologyStudy will inherit from production.RadiologyStudy but add metadata about the original Study UID and Accession Number.

These models are used within the [DICOM image reviewer](http://github.com/cbmi/dicom-reviewer) and the [DICOM anonymization pipeline](http://github.com/cbmi/dicom-pipeline).



