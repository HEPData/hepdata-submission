#!/usr/bin/env python3

"""Try to validate a submission file and possible data files

See https://github.com/HEPData/hepdata-submission/issues/8
Specify the path to the schema files with either the -s option
or by giving the location of the hepdata-validator repository
using the PYTHONPATH environment variable.

Author: Christian Holm Christensen <cholm@nbi.dk>

"""
import yaml
import json
import jsonschema
import os
import importlib
from pprint import pprint,pformat

# ====================================================================
class Message:
    """Container of messages with a severity level"""
    ERROR = 2
    WARNING = 1
    INFO = 0
    
    def __init__(self,filename='',message='',level=None):
        """Create a message for a file and a specific severity level"""
        self._file    = filename
        self._level   = level
        self._message = message
        self._tables  = {}
        if self._level is None:
            self._level = self.ERROR

    @classmethod
    def levelStr(cls,lvl):
        """Stringify severity level"""
        return ("Error"   if lvl == cls.ERROR else
                "Warning" if lvl == cls.WARNING else
                "Info"    if lvl == cls.INFO else
                "Unknown")
    
    def __str__(self):
        """Get string representation"""
        return "{:10s} - {}".format(Message.levelStr(self._level),
                                    self._message)

# ====================================================================
class Validator:
    """Validates HepData files"""

    def __init__(self,schemadir):
        if schemadir is None:
            spec = importlib.util.find_spec('hepdata_validator')
            pprint(spec)
            schemadir = os.path.join(os.path.dirname(spec.origin), 'schemas')
            print(schemadir)
            
        sub_schema_file = os.path.join(schemadir,'submission_schema.json')
        dat_schema_file = os.path.join(schemadir,'data_schema.json')
        add_schema_file = os.path.join(schemadir,'additional_info_schema.json')
        
        self._messages = {}
        self._tables = {}
        try:
            self._sub_schema = json.load(open(sub_schema_file,'r'))
            self._dat_schema = json.load(open(dat_schema_file,'r'))
            self._add_schema = json.load(open(add_schema_file,'r'))
        except Exception as e:
            raise RuntimeError('Failed to load one or more schemas: {}',e)

    def ensure_messages(self,filename):
        if filename not in self._messages:
            self._messages[filename] = []

        return self._messages[filename]
        
    def add_error(self,filename,message):
        """Add a message to the output

        :param filename: Current filename
        :param message: Content of the message 
        :param level: Severity of the message 
        """
        self.ensure_messages(filename)\
            .append(Message(filename,message,Message.ERROR))

    def add_warning(self,filename,message):
        """Add a message to the output

        :param filename: Current filename
        :param message: Content of the message 
        :param level: Severity of the message 
        """
        self.ensure_messages(filename)\
            .append(Message(filename,message,Message.WARNING))
        
    def add_info(self,filename,message):
        """Add a message to the output

        :param filename: Current filename
        :param message: Content of the message 
        :param level: Severity of the message 
        """
        self.ensure_messages(filename)\
            .append(Message(filename,message,Message.INFO))

    def filter_messages(self,filename,least,exact=False):
        return [m for m in self.ensure_messages(filename)
                if (m._level == least and exact) or 
                (m._level>=least and not exact)]
                
    def get_messages(self,filename=None,least=None,exact=False):
        """Get messages for a given filename or all messages
        
        :param filename: File to get messages for, or None to get all
        :param least: Least level of messages 
        """
        if filename is None:
            if least is None:
                return self._messages

            ret = {}
            for f in self._messages:
                ret[f] = self.filter_messages(f,least,exact)
            return ret

        if least is None:
            return self.ensure_messages(filename)
        return self.filter_messages(filename,least,exact)

    def clear_messages(self):
        """Reset messages"""
        self._messages = {}

    def has_errors(self,filename=None):
        """Check if a file has errors 
        
        :param filename: File to check for or all if None
        """
        if filename is None:
            for f in self._messages:
                if self.has_errors(f):
                    return True
            return False
        
        return len(self.get_messages(filename,Message.ERROR,exact=True)) > 0

    def has_warnings(self,filename):
        """Check if a file has errors 
        
        :param filename: File to check for 
        """
        return len(self.get_messages(filename,Message.WARNING,exact=True)) > 0

    def print_messages(self,filename=None,least=Message.INFO):
        """Print all errors associated with a file 
        
        :param filename: File to get errors for or None for all 
        :param least: Least level to print
        """
        if filename is None:
            for f in self._messages:
                self.print_messages(f,least)
            return

        m = self.get_messages(filename,least)
        if len(m) <= 0 and least > Message.INFO:
            return
        
        print(filename)
        for e in m:
            print("\t{}".format(e.__str__()))

    def summarize(self,least=Message.INFO):
        """Summarize findings"""
        if least > Message.INFO:
            return
        
        for f in self._messages:
            print('{}'.format(f),end='')

            e = self.has_errors(f)
            w = self.has_warnings(f)

            print(' {}'.format('has warnings' if w else
                               'is clean'),end='')
            print(' {}'.format('but' if (not w and e) or (w and not e) else
                                'and'),end='')
            print(' {}'.format('has errors' if e else
                               'is valid'))
                
    def validate(self,**kwargs):
        """Validate a submission or data file 

        :param file_path: Path to file to check 
        :param data: YAML document already read
        :return: True on success 
        """
        data     = kwargs.pop('data',None)
        filename = kwargs.pop('file_path',None)
        verb     = kwargs.pop('verbose',False)
                  
        # Check argument 
        if filename is None:
            raise LookupError('The file_path argument is mandatory')

        if verb:
            print('Validating {}'.format(filename))
                  
        try:
            # Check if we have data 
            if data is None:
                if verb:
                    print('Reading in {}'.format(filename))

                data = yaml.load_all(open(filename,'r'),
                                     Loader=yaml.SafeLoader)

            # Make a list of this 
            data = list(data)

            # Loop over documents in data to extract tables.
            # We build a dictionary from table name to data table document
            for doc in data:
                # Check for empty document 
                if doc is None:
                    continue

                # if verb:
                #     pprint(doc)
                    
                if (('independent_variables' in doc or
                     'dependent_variables' in doc) and 
                    'name' in doc):
                    if verb:
                        print('Found data table {} in {}'
                              .format(doc['name'],filename))
                        
                    self._tables[doc.get('name','')] = doc
                
            # Loop over documents in data
            if verb:
                print("Looping over documents in {}".format(filename))
                
            for doc in data:
                # Check for empty document 
                if doc is None:
                    continue

                if verb:
                    print('Check a document')
                    
                try:
                    # If the document has the field 'data_file', it is
                    # a submission (table meta data) entry
                    #
                    # If the document has the field
                    # 'independent_variables', then it is a data table
                    # entry.
                    # If the same document also has a 'description' field,
                    # then it comes from a single YAML file.
                    #
                    # If neither of those fields are found, we assume
                    # that we have additional information in the
                    # document
                    #
                    if 'data_file' in doc:
                        self.validate_sub(filename,doc,verb)
                    elif 'independent_variables' in doc:
                        if 'description' in doc:  # check for single-YAML-file format
                            doc_dat = {
                                'independent_variables': doc.pop('independent_variables', None),
                                'dependent_variables': doc.pop('dependent_variables', None)
                            }
                            self.validate_dat(filename, doc_dat, verb)
                            doc['data_file'] = ''  # since schema requires a data_file
                            self.validate_sub(filename, doc, verb)
                        else:  # usual YAML data file
                            self.validate_dat(filename,doc,verb)
                    else:
                        self.validate_add(filename,doc,verb)

                except jsonschema.ValidationError as ve:
                    if verb:
                        print(ve)
                    self.add_error(filename,
                                   ve.message+' in\n'+
                                   pformat(ve.instance,compact=True))

            return not self.has_errors()

        except yaml.scanner.ScannerError as e:
            if verb:
                print('Scanning error: {}'.format(e))
            self.add_error(filename,
                             'Problem parsing file.\n'
                             + str(e))

        except Exception as e:
            if verb:
                print('General exception: {}'.format(e))
            self.add_error(filename, str(e))

        return False

    def validate_res(self,filename,doc,verb):
        """Validates additional resources

        :param filename: The name of the file we're looking at
        :param doc: Current YAML document 
        """
        if verb:
            print('Validating additional resources')
            
        for resource in doc.get('additional_resources',[]):
            location = resource.get('location','')
            if verb:
                print(' additional resource: {}'.format(location))

            if location.startswith('http'):
                # Do not check external resources
                continue

            location = os.path.join(os.path.dirname(filename),location)
            if not os.path.isfile(location):
                  self.add_warning(filename,'Resource {} not found'
                                   .format(location))
            if '/' in resource.get('location',''):
                  self.add_warning(filename,'Resource {} should not contain "/"'
                                   .format(location))
            
                            
    def validate_sub(self,filename,doc,verb):
        """Validates a submission file entry (table meta data)

        :param filename: Name of the file processed 
        :param doc: YAML document 
        """
        if verb:
            print('Validating submission entry {}'
                  .format(doc.get('name','')))
            
        # This throws in case of errors - handled one level up 
        jsonschema.validate(doc,self._sub_schema)

        # Validate additional resources in the document
        self.validate_res(filename,doc,verb)
        
        # Now check the data file if not part of this file
        if doc['name'] not in self._tables:
            # We haven't seen the data file yet, so we check it here 
            df = doc['data_file']

            # Check sanity of file path
            if '/' in df:
                self.add_warning(Message(filename,
                                         'Data file names should not contain "/": {}'
                                         .format(df)))

            rdf = os.path.join(os.path.dirname(filename),df)
            ret = self.validate(file_path=rdf,data=None,verb=verb)

        self.add_info(filename,"Contains the valid submission {}".format(doc['name']))

        
    def validate_dat(self,filename,doc,verb):
        """Validate data entry (a table)

        :param filename: Current file name 
        :param doc: Current YAML document
        """
        if verb:
            print('Validating data entry {}'
                  .format(doc.get('name','')))
            
        # This raises in case of problems - handled one level up
        jsonschema.validate(doc,self._dat_schema)

        len_indep = [len(i['values']) for i in doc['independent_variables']]
        len_dep   = [len(d['values']) for d in doc['dependent_variables']]
        
        if len(set(len_indep+len_dep)) > 1:
            # If we have one or more unique counts, it's a problem
            self.add_warning(filename,"Inconsistent lengths of independent "
                        "variables {} and dependent variables {}"
                        .format(str(len_indep),str(len_dep)))

        self.add_info(filename,"Contains a valid data table {}"
                      .format(doc.get('name','')))

    def validate_add(self,filename,doc,verb):
        """Validate additional information (header)

        :param filename: Current filename 
        :param doc: Current YAML document 
        """
        if verb:
            print('Validating header entry')
            
        # This raises in case of problems - handled one level up
        jsonschema.validate(doc,self._add_schema)
        
        # Validate additional resources in the document
        self.validate_res(filename,doc,verb)
        
        self.add_info(filename,"Contains valid additional information")
            
if __name__ == "__main__":
    import argparse as ap
    import sys
    
    def check_dir(val):
        if not os.path.isdir(val):
            raise ap.ArgumentTypeError('{} is not a directory'
                                       .format(val))
        return val

    parser = ap.ArgumentParser(description="Validates HepData files")
    parser.add_argument('input',
                        type=ap.FileType('r'),
                        help='File to parse',
                        default='submission.yaml')
    parser.add_argument('-v',
                        '--verbose',
                        dest='verbose',
                        action='store_true',
                        help='Be verbose')
    parser.add_argument('-q',
                        '--quiet',
                        dest='verbose',
                        action='store_false',
                        help='Be quiet')
    parser.add_argument('-l',
                        '--level',
                        default='WARNING',
                        choices=['INFO','WARNING','ERROR'],
                        help='Level of output')
    parser.add_argument('-s',
                        '--schema',
                        type=check_dir,
                        help='Location of schema files')
    parser.set_defaults(verbose=False)
    
    args = parser.parse_args()

    lvl = getattr(Message, args.level)

    v = Validator(args.schema)

    v.validate(file_path=args.input.name,
               data=None,
               verbose=args.verbose)
    v.summarize(lvl)
    e = v.has_errors(None)
    if e or v.has_warnings(None):
        v.print_messages(None,Message.WARNING)
        if e:
            print('There was a problem')
            sys.exit(1)

# ====================================================================
#
# EOF
#
