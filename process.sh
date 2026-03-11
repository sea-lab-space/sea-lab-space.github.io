#/bin/bash

################
#### uncomment only if need to process exported files
#################


# generate bib file backup with specific datetime (yyyy-mm-dd-hh-mm-ss)
# timestamp=$(date +"%Y-%m-%d-%H-%M-%S")
# cp sea-lab-publication.bib "bak/sea-lab-publication-$timestamp.bib"
# python3 ./processing/bib_post_processing.py


# Make sure you have installed the HUGO academic tool: https://github.com/girtel/hugo-academic-cli-girtel
academic import ./sea-lab-publication.bib ./content/publication/ --compact