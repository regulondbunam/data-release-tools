# Data Release Tools

# Description

These modules are used for the ETL process from Ecocyc to RegulonDB, they fulfill the tasks of schema loading, validation, ID creation, ID replacement and data loading.

# Motivation

These modules were created in order to create persistent IDs for Ecocyc data in RegulonDB. Together with Ecocyc Extractor module can perform the ETL process.

# System requirements

- Software:
  - Python 3.9
  - Python 2.7
- Hardware:
  - RAM: 4 GB / 6 GB
  - Storage: 500 MB

# Install

[Install guide](INSTALL.md)

# Quick start

It is recommended to use a Snakemake script to run all modules together.
For more details see the operation manuals of each module.

- [schema_loader](src/schema_loader/docs/MO.md)
- [data_validator](src/data_validator/docs/MO.md)
- [create_identifiers](src/create_identifiers/docs/MO.md)
- [replace_identifiers](src/replace_identifiers/docs/MO.md)
- [data_uploader](src/data_uploader/docs/MO.md)

# Project website

###### Pending

# License

**MIT**

# Support contact information

[Support contact](http://regulondb.ccg.unam.mx/menu/about_regulondb/contact_us/index.jsp)

# Software quality checklist

**Accessibility**

- [x] Version control system

**Documentation**

- [x] README file

**Learnability**

- [x] Quick start

**Buildability**

- [x] INSTALL file

**Identity**

- [ ] Website

**Copyright & Licensing**

- [x] LICENSE file

**Portability**

- [x] Multiple platforms

**Supportability**

- [x] E-mail address
- [x] Issue tracker

**Analysability**

- [x] Source code structured
- [x] Sensible names
- [x] Coding standards - [style guides](http://google.github.io/styleguide/)

**Changeability**

- [x] CONTRIBUTING file
- [x] Code of Conduct file
- [x] Code changes, and their authorship, publicly visible

**Reusability**

- [x] Source code set up in a modular fashion

**Security & Privacy**

- [x] Passwords must never be stored in unhashed form
