#!/usr/bin/env python

"""
Offline validation of submission.yaml and YAML data files.
Call this script from the directory containing these files:
  ./check.py
Or specify the directory as an additional argument:
  ./check.py directory
"""

# Get directory as optional command-line argument.
import sys
if len(sys.argv) == 2:
    directory = sys.argv[1]
    print('Checking YAML files in directory %s.' % directory)
elif len(sys.argv) > 2:
    print('Invalid number of arguments: %d' % len(sys.argv))
    quit()
else:
    directory = ''
    print('Checking YAML files in current directory.')

# Import a YAML parser if available.
try:
    import yaml
except ImportError:
    print('ImportError: please install a YAML implementation for Python.')
    quit()

# Import the hepdata-validator package if installed.
# If not, the script will only try to parse the YAML without validating the schema.
try:
    from hepdata_validator.submission_file_validator import SubmissionFileValidator
    from hepdata_validator.data_file_validator import DataFileValidator
    validator_imported = True
except ImportError:
    print('hepdata-validator not installed: only check YAML parsing.')
    print('See https://github.com/HEPData/hepdata-validator to install.')
    validator_imported = False

# Give location of the submission.yaml file.
submission_file_path = directory + '/submission.yaml' if directory else 'submission.yaml'

# Validate the submission.yaml file if validator imported.
if validator_imported:
    submission_file_validator = SubmissionFileValidator()
    is_valid_submission_file = submission_file_validator.validate(file_path=submission_file_path)
    if not is_valid_submission_file:
        print('%s is invalid HEPData YAML.' % submission_file_path)
        submission_file_validator.print_errors(submission_file_path)
        quit()
    else:
        print('%s is valid HEPData YAML.' % submission_file_path)

# Open the submission.yaml file and load all YAML documents.
with open(submission_file_path, 'r') as stream:
    docs = yaml.safe_load_all(stream)

    # Loop over all YAML documents in the submission.yaml file.
    for doc in docs:

        # Check for non-empty YAML documents with a 'data_file' key.
        if doc and 'data_file' in doc:

            # Extract data file from YAML document.
            data_file_path = directory + '/' + doc['data_file'] if directory else doc['data_file']

            # Validate the YAML data file if validator imported.
            if validator_imported:
                data_file_validator = DataFileValidator()
                is_valid_data_file = data_file_validator.validate(file_path=data_file_path)
                if not is_valid_data_file:
                    print('%s is invalid HEPData YAML.' % data_file_path)
                    data_file_validator.print_errors(data_file_path)
                else:
                    print('%s is valid HEPData YAML.' % data_file_path)
            else:
                # Just try to load YAML data file without validating schema.
                # Script will terminate with an exception if there is a problem.
                contents = yaml.safe_load(open(data_file_path, 'r'))
                print('%s is valid YAML.' % data_file_path)