#!/usr/bin/env python

"""
Offline validation of submission.yaml and YAML data files.
Call this script from the directory containing these files:
  ./check.py
Or specify the directory as an additional argument:
  ./check.py directory
"""

import os.path

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
submission_file_path = os.path.join(directory, 'submission.yaml')

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

        # Skip empty YAML documents.
        if not doc:
            continue

        # Check for presence of local files given as additional_resources.
        if 'additional_resources' in doc:
            for resource in doc['additional_resources']:
                location = os.path.join(directory, resource['location'])
                if not location.startswith('http'):
                    if not os.path.isfile(location):
                        print('%s is missing.' % location)
                    elif '/' in resource['location']:
                        print('%s should not contain "/".' % resource['location'])

        # Check for non-empty YAML documents with a 'data_file' key.
        if 'data_file' in doc:

            # Check for presence of '/' in data_file value.
            if '/' in doc['data_file']:
                print('%s should not contain "/".' % doc['data_file'])
                continue

            # Extract data file from YAML document.
            data_file_path = directory + '/' + doc['data_file'] if directory else doc['data_file']

            # Just try to load YAML data file without validating schema.
            # Script will terminate with an exception if there is a problem.
            contents = yaml.safe_load(open(data_file_path, 'r'))

            # Validate the YAML data file if validator imported.
            if not validator_imported:
                print('%s is valid YAML.' % data_file_path)
            else:
                data_file_validator = DataFileValidator()
                is_valid_data_file = data_file_validator.validate(file_path=data_file_path, data=contents)
                if not is_valid_data_file:
                    print('%s is invalid HEPData YAML.' % data_file_path)
                    data_file_validator.print_errors(data_file_path)
                else:
                    # Check that the length of the 'values' list is consistent for
                    # each of the independent_variables and dependent_variables.
                    indep_count = [len(indep['values']) for indep in contents['independent_variables']]
                    dep_count = [len(dep['values']) for dep in contents['dependent_variables']]
                    if len(set(indep_count + dep_count)) > 1: # if more than one unique count
                        print("%s has inconsistent length of 'values' list: " % data_file_path +
                              "independent_variables%s, dependent_variables%s." % (str(indep_count), str(dep_count)))
                    else:
                        print('%s is valid HEPData YAML.' % data_file_path)