#!/bin/bash
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

script_dir="$(dirname "$0")"
echo -e "$GREEN starting...$NC"
# Remove old files
rm -f -r ".etl_pipeline"
rm -f "./data/"*.csv "./data/"*.tsv "./data/"*.sqlite
echo -e "$YELLOW Script directory name: $script_dir $NC"
echo -e "$GREEN Install virtual environment(20.24.6) requirements...$NC"
# Install virtual environment
pip install virtualenv==20.24.6
echo -e "$GREEN Create a virtual environment called [.etl_pipeline]...$NC"
# The directory of the script
virtualenv "$script_dir/.etl_pipeline"
source "$script_dir/.etl_pipeline/bin/activate"
echo -e "$GREEN Install requirements.txt...$NC"
# Install "requirements.txt"
pip install -r "$script_dir/pipeline/requirements.txt"
echo -e "$GREEN All requirements are installed successfully!$NC"
echo -e "$GREEN Pipeline started...$NC"
python3 "$script_dir/pipeline/pipeline.py"
echo -e "$GREEN Pipeline Finished$NC"
# Deactivate virtual environment
deactivate
echo -e "$GREEN Deactivated the virtual environment$NC"
