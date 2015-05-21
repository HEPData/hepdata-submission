# HEP Data Submission

HEP data submission will largely involve the upload of archives that specify the data associated with a publication.

The main file for a submission is the *submission.yaml* file.
This links together all the data in to one submission and defines files such as scripts used to create the data, ROOT files, or even links to Github/Bitbucket/Zenodo etc. for more substantial pieces of code.

An additional important type of file is the data file that defines all the data, qualifiers, error bars, etc.

 ![image](assets/hepdata_root_processing.png)

## Submission.yaml


``` yaml

# Start a new YAML document to indicate a new data table.
# This is Table 1.
name: "Table 1"
location: Page 17 of preprint
description: The measured fiducial cross sections.  The first systematic uncertainty is the combined systematic uncertainty excluding luminosity, the second is the luminosity
keywords: # used for searching, possibly multiple values for each keyword
  reactions: [P P --> Z0 Z0 X]
  observables: [SIG]
  energies: [7000, 8000, 9500] # centre-of-mass energy in GeV
data_file: data1.yaml
additional_resources:
  - location: "http:github.com/HEPData/hepdata"
    description: "Full source code for creating this data"
---
# This is Table 2.
name: "Table 2"
location: Page 20 of preprint
description: The measured total cross sections.  The first systematic uncertainty is the combined systematic uncertainty excluding luminosity, the second is the luminosity
keywords: # used for searching, possibly multiple values for each keyword
  reactions: [P P --> Z0 Z0 X]
  observables: [SIG]
  energies: [7000] # centre-of-mass energy in GeV
data_file: data2.yaml
---
# This is Table 3.
name: "Table 3"
location: Figure 8A
description: Normalized ZZ fiducial cross section (multiplied by 10^6 for readability) in bins of the leading reconstructed dilepton pT for the 4 lepton channel.  The first systematic uncertainty is detector systematics, the second is background systematic uncertainties
keywords: # used for searching, possibly multiple values for each keyword
  reactions: [P P --> Z0 Z0 X]
  observables: [DSIG/DPT]
  energies: [7000] # centre-of-mass energy in GeV
data_file: data3.yaml

```

### Data Files

Data Files can be encoded as either YAML or JSON, the software deals with both the same way.

#### YAML

``` yaml

---
xaxes:
  - header: {name: SQRT(S), units: GEV}
    bins:
      - value: 7000
      - value: 8000
yaxes:
  - header: {name: SIG(total), units: FB}
    qualifiers:
      - {name: RE, value: P P --> Z0 Z0 X}
    points:
      - value: 6.7
        errors:
          - {symerror: 0.45, label: stat}
          - {asymerror: {plus: 0.4, minus: 0.3}, label: sys}
          - {symerror: 0.34, label: "sys,lumi"}
      - value: 5.7
        errors:
          - {symerror: 0.4, label: stat}
          - {asymerror: {plus: 0.42, minus: 0.31}, label: sys}
          - {symerror: 0.4, label: "sys,lumi"}

```


#### JSON

``` json

{
    "xaxes": [
        {
            "header": {
                "name": "SQRT(S)",
                "units": "GEV"
            },
            "bins": [
                {
                    "value": 7000
                },
                {
                    "value": 8000
                }
            ]
        }
    ],
    "yaxes": [
        {
            "header": {
                "name": "SIG(total)",
                "units": "FB"
            },
            "qualifiers": [
                {
                    "name": "RE",
                    "value": "P P --> Z0 Z0 X"
                }
            ],
            "points": [
                {
                    "value": 6.7,
                    "errors": [
                        {"symerror": 0.45, "label": "stat"},
                        {"asymerror": {"plus": 0.4, "minus": 0.3}, "label": "sys"},
                        {"symerror": 0.34,"label": "sys,lumi"}
                    ]
                },
                {
                    "value": 5.7,
                    "errors": [
                        {"symerror": 0.4, "label": "stat"},
                        {"asymerror": {"plus": 0.42, "minus": 0.31}, "label": "sys"},
                        {"symerror": 0.4, "label": "sys,lumi"}
                    ]
                }
            ]
        }
    ]
}
```

#### Errors

There are two main classes of errors that can be encoded, symmetric errors, and asymmetric errors.
Symmetric errors allow you to specify a min and max error using one value, e.g. ```"symerror": 0.4```, will translate to min -0.4, max +0.4.
Unsurprisingly, an asymmetric error requires both plus and minus values to be explicitly encoded, e.g. ```"asymerror": {"plus": 0.4, "minus": 0.3}```.

#### How Does this translate when rendered by HEPdata?

Although perhaps not a very interesting example, the data table looks as follows in HEPdata.

![image](assets/table-2-rendering.png)
