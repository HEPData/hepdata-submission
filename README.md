# HEP Data Submission

HEP data submission will largely involve the upload of archives that specify the data associated with a publication.

The main file for a submission is the *submission.yaml* file.
This links together all the data in to one submission and defines files such as scripts used to create the data, ROOT files, or even links to Github/Bitbucket/Zenodo etc. for more substantial pieces of code.

An additional important type of file is the data file that defines all the data, qualifiers, error bars, etc.


## Submission.yaml

The submission format would ideally be just via the ROOT files. These files should include the plots (that will be automatically plotted), and the data tables related to these plots.

The following representations are there to roughly model data in [Table 8](http://hepdata.cedar.ac.uk/view/ins1331782/d3) of [Aad, et. al, Search for anomalous production of prompt same-sign lepton pairs and pair-produced doubly charged Higgs bosons with s√=8 TeV pp collisions using the ATLAS detector, 2014](http://inspirehep.net/record/1331782).
More examples could be created to model other data tables, however our model defined below seems to represent the data tables we've so far observed in HEPData.

``` yaml

---
submission:
  data:
   - name: "Table 1"
     related_publication_figure: 2
     description: "The measured fiducial cross sections. The first systematic uncertainty is the combined systematic uncertainty excluding luminosity, the second is the luminosity."
     data_file: "table1.json"
     additional_files:
      - file_name: "analysis_script.py"
        description: "Analysis script"
        file_type: "python"
      - file_name: "root_file.root"
        description: "root file containing additional data"
        file_type: "root"


   - name: "Table 2"
     related_publication_figure: 3
     description: "The fitted slope parameter for the elastic cross section fitted over 4 |T| ranges."
     data_file: "table2.json"
     additional_files:
      - file_name: "HEPData/hepdata"
        description: "Full source code for creating this data"
        file_type: "github"


```

### Data Files

``` json

{
              "x": {
                  "values": [
                      "0.005 TO 0.1",
                      "0.005 TO 0.2",
                      "0.020 TO 0.1",
                      "0.020 TO 0.2"
                  ],
                  "name": "mass range [GeV]"
              },
              "groups": [
                  {
                      "qualifiers": [
                          {
                              "type": "reaction",
                              "value": "P P --> P P"
                          },
                          {
                              "type": "sqrt(s)",
                              "value": "9000.0 GeV"
                          }
                      ],
                      "measurements": [
                          {
                              "name": "SLOPE IN GEV**-4",
                              "values": [
                                  {
                                      "errors": [
                                          {
                                              "err_plus": 0.04,
                                              "err_minus": 0.02,
                                              "label": "stat"
                                          },
                                          {
                                              "err_plus": 0.22,
                                              "err_minus": 0.22,
                                              "label": "sys"
                                          }
                                      ],
                                      "value": 19.96
                                  },
                                  {
                                      "errors": [
                                          {
                                              "err_plus": 0.02,
                                              "err_minus": 0.02,
                                              "label": "stat"
                                          },
                                          {
                                              "err_plus": 0.27,
                                              "err_minus": 0.27,
                                              "label": "sys"
                                          }
                                      ],
                                      "value": 19.89
                                  },
                                  {
                                      "errors": [
                                          {
                                              "err_plus": 0.05,
                                              "err_minus": 0.05,
                                              "label": "stat"
                                          },
                                          {
                                              "err_plus": 0.26,
                                              "err_minus": 0.21,
                                              "label": "sys"
                                          }
                                      ],
                                      "value": 19.93
                                  },
                                  {
                                      "errors": [
                                          {
                                              "err_plus": 0.03,
                                              "err_minus": 0.03,
                                              "label": "stat"
                                          },
                                          {
                                              "err_plus": 0.33,
                                              "err_minus": 0.33,
                                              "label": "sys"
                                          }
                                      ],
                                      "value": 19.87
                                  }
                              ]
                          }
                      ]
                  }
              ]
          }


```