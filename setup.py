import sys
from setuptools import setup, find_packages
from setuptools.command import install as _install

if sys.version_info < (2, 7):
    sys.stdout.write('Python versions < 2.7 are not supported\n')
    sys.exit(1)

# For some reason, using this prevents it from installing
# the module as an egg
class install(_install.install):
    def run(self):
        _install.install.run(self)

setup(
    cmdclass = {'install': install},
    name='django-dicom-models',
    version="0.9",
    description='Django DICOM Models',
    long_description='Django models used with CBMi\'s DICOM related applications',
    author='CBMi',
    author_email='millerjm1@email.chop.edu',
    url='https://github.com/cbmi/django-dicom-models',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7'
        'Framework :: Django',
        'Topic :: Internet :: WWW/HTTP',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Information Technology'
    ],
    install_requires =[
            'django>=1.4',
    ],
    packages=['dicom_models',
        'dicom_models.production',
        'dicom_models.production.models',
        'dicom_models.production.models.data',
        'dicom_models.production.utils',
        'dicom_models.staging',],
)
