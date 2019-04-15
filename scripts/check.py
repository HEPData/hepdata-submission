#!/usr/bin/env python

"""
Offline validation of submission.yaml and YAML data files.
Call this script from the directory containing these files:
  ./check.py
Or specify the directory as an additional argument:
  ./check.py directory
Or specify a single YAML file to validate:
  ./check.py single_yaml_file
"""

import sys
import os.path

# Get directory or single YAML file as optional command-line argument.
directory = ''
single_yaml_file = ''
if len(sys.argv) == 2:
    argument = sys.argv[1]
    if os.path.isdir(argument):
        directory = argument
        print('Checking YAML files in directory %s.' % directory)
    elif os.path.isfile(argument):
        single_yaml_file = argument
        print('Checking single YAML file %s.' % single_yaml_file)
    else:
        print('Argument %s is not a directory or file.' % argument)
elif len(sys.argv) > 2:
    print('Invalid number of arguments: %d' % len(sys.argv))
    quit()
else:
    print('Checking YAML files in current directory.')

# Import a YAML parser if available.
try:
    import yaml
    # We try to load using the CSafeLoader for speed improvements.
    try:
        from yaml import CSafeLoader as Loader
        from yaml import CSafeDumper as Dumper
    except ImportError:
        from yaml import SafeLoader as Loader
        from yaml import SafeDumper as Dumper
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

# Give location of the submission.yaml file or the single YAML file.
if single_yaml_file:
    submission_file_path = single_yaml_file
else:
    submission_file_path = os.path.join(directory, 'submission.yaml')

# Open the submission.yaml file and load all YAML documents.
with open(submission_file_path, 'r') as stream:
    docs = list(yaml.load_all(stream, Loader=Loader))

    # Need to remove independent_variables and dependent_variables from single YAML file.
    if single_yaml_file:
        for doc in docs:
            if 'name' in doc:
                file_name = doc['name'].replace(' ', '_').replace('/', '-') + '.yaml'
                doc['data_file'] = file_name
                with open(file_name, 'w') as data_file:
                    yaml.dump({'independent_variables': doc.pop('independent_variables', None),
                               'dependent_variables': doc.pop('dependent_variables', None)}, data_file, Dumper=Dumper)

    # Validate the submission.yaml file if validator imported.
    if validator_imported:
        submission_file_validator = SubmissionFileValidator()
        is_valid_submission_file = submission_file_validator.validate(file_path=submission_file_path, data=docs)
        if not is_valid_submission_file:
            print('%s is invalid HEPData YAML.' % submission_file_path)
            submission_file_validator.print_errors(submission_file_path)
            quit()
        else:
            print('%s is valid HEPData YAML.' % submission_file_path)

    # Loop over all YAML documents in the submission.yaml file.
    for doc in docs:

        # Skip empty YAML documents.
        if not doc:
            continue

        # Check for presence of local files given as additional_resources.
        if 'additional_resources' in doc:
            for resource in doc['additional_resources']:
                if not resource['location'].startswith('http'):
                    location = os.path.join(directory, resource['location'])
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
            contents = yaml.load(open(data_file_path, 'r'), Loader=Loader)

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

            # For single YAML file, clean up by removing temporary data_file created above.
            if single_yaml_file:
                print('Removing %s.' % doc['data_file'])
                os.remove(doc['data_file'])
