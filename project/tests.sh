#!/bin/bash
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

script_dir="$(dirname "$0")"
echo -e "$GREEN Testing in progress...$NC"
env_name="etl_test_pipeline"
echo -e "$YELLOW Script directory name: $script_dir $NC"
echo -e "$GREEN Install virtual environment(20.24.6) requirements...$NC"
# Install virtual environment
pip install virtualenv==20.24.6
echo -e "$GREEN Create a virtual environment called [.$env_name]...$NC"
# The directory of the script
virtualenv "$script_dir/.$env_name"
source "$script_dir/.$env_name/bin/activate"
echo -e "$GREEN Install requirements.txt...$NC"
# Install "requirements.txt"
pip install -r "$script_dir/pipeline/requirements.txt"
echo -e "$GREEN All requirements are installed successfully!$NC"
echo -e "$GREEN Testing Pipeline started...$NC"
pytest "$script_dir/tests/"
echo -e "$GREEN Testing Pipeline Finished$NC"
# Deactivate virtual environment
deactivate
echo -e "$GREEN Deactivated the virtual environment$NC"
