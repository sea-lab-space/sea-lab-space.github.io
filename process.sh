#!/bin/bash

################
#### uncomment only if need to process exported files
#################


# generate bib file backup with specific datetime (yyyy-mm-dd-hh-mm-ss)
# timestamp=$(date +"%Y-%m-%d-%H-%M-%S")
# cp sea-lab-publication.bib "bak/sea-lab-publication-$timestamp.bib"
# python3 ./processing/bib_post_processing.py


# Needs the import tool, the same version the import Action uses (Python 3.11.5+):
#   python3 -m pip install academic==0.10.0
# Never add --overwrite: it deletes the directions and other hand-added fields.
academic import ./sea-lab-publication.bib ./content/publication/ --compact