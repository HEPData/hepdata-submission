# HEP Data Submission

## Submission Format

### ROOT Data Files

Creating [ROOT TTrees](https://root.cern.ch/root/html/TTree.html) is relatively easy. Formatting the data correctly is the hard part. We've tried to structure the tree to make it both easy to get the data in to the files, and to make it easy for us to reconstruct the data table following submission.

```python
def generate_root_file_with_tree(self, file_name):
        f = root_open(file_name, "recreate")
		
        tree = Tree(name="Table1",
                    title="The W dependence of the cross section after integrating..")
        # F - Float, I - Integer
        tree.create_branches(
            {'W_in_GEV_low': 'F',
             'W_in_GEV_high': 'F',
             'SIG_IN_NB_(<0.8)_ystatminus': 'F',
             'SIG_IN_NB_(<0.8)_ystat': 'F',
             'SIG_IN_NB_(<0.8)_ystatplus': 'F',
             'SIG_IN_NB_(<0.6)_ystatminus': 'F',
             'SIG_IN_NB_(<0.6)_ystat': 'F',
             'SIG_IN_NB_(<0.6)_ystatplus': 'F',
             'i': 'I'})
	 
 # Now we create our tree :)
        for i in xrange(10000):
            tree['W_in_GEV_low'] = gauss(1., 4.)
            tree['W_in_GEV_high'] = gauss(.3, 2.)
            tree['SIG_IN_NB_(<0.8)_ystatminus'] = gauss(0., 0.1)
            tree['SIG_IN_NB_(<0.8)_ystat'] = gauss(0., 5.)
            tree['SIG_IN_NB_(<0.8)_ystatplus'] = gauss(0., 0.1)
            tree['SIG_IN_NB_(<0.6)_ystatminus'] = gauss(0., 0.1)
            tree['SIG_IN_NB_(<0.6)_ystat'] = gauss(0., 5.)
            tree['SIG_IN_NB_(<0.6)_ystatplus'] = gauss(0., 0.1)
            tree.i = i
            tree.fill()

        tree.write()
        f.close()

```

### YAML

YAML may be a little more difficult to generate and parse than JSON, but it is widely used and using it as a data source would add little overhead to HEPData. Moreover, JSON representatiokns of the YAML can also be used. We've created verbose and compact representations of the YAML files that vary how data records are represented.
For each YAML presentation, it's JSON equivalent is also given.

#### YAML format

```yaml

---
Table:
  name: "Table 3"
  title: "Upper limit at 95% CL on the fiducial cross section for ℓ±ℓ± pairs from non-SM signals. The expected limits and their 1σ uncertainties are given together with the observed limits derived from the data. Limits are given separately for the e±e±,e±μ± and μ±μ± channel inclusively and separated by charge."
  reaction: "P P --> $e/\\mu{\\pm} e/\\mu{\\pm}$ (+X)"
  qualifiers:
    - type: "sqrt(s)"
      value: "8000.0 GeV"
    - type:
      value: "95% CL upper limit [fb]"
  data:
      - x:
         name: "mass range [GeV]"
         value: "m($e^{\\pm}e^{\\pm}$"
        observed:
         type: y
         name: "Expected"
         value: 39
         value_err_minus: -13
         value_err_plus: 10
        expected:
         type: y
         name: "Observed"
         value: 32
         value_err_minus: 0
         value_err_plus: 0
      - x:
         name: "mass_range [GeV]"
         value: "> 15.0"
        observed:
         name: "Expected"
         value: 19
         value_err_minus: -6
         value_err_plus: 6
        expected:
          name: "Expected"
          value: 14
          value_err_minus: 0
        value_err_plus: 0
                        
```

Its JSON representation is pretty similar, and translates to this.


```json

{
  "Table": {
    "name": "Table 3",
    "title": "Upper limit at 95% CL on the fiducial cross section for \u2113\u00b1\u2113\u00b1 pairs from non-SM signals. The expected limits and their 1\u03c3 uncertainties are given together with the observed limits derived from the data. Limits are given separately for the e\u00b1e\u00b1,e\u00b1\u03bc\u00b1 and \u03bc\u00b1\u03bc\u00b1 channel inclusively and separated by charge.",
    "reaction": "P P --> $e/\\mu{\\pm} e/\\mu{\\pm}$ (+X)",
    "qualifiers": [
      {
        "type": "sqrt(s)",
        "value": "8000.0 GeV"
      },
      {
        "type": null,
        "value": "95% CL upper limit [fb]"
      }
    ],
    "data": [
      {
        "observed": {
          "value_err_plus": 10,
          "value_err_minus": -13,
          "type": "y",
          "name": "Expected",
          "value": 39
        },
        "x": {
          "name": "mass range [GeV]",
          "value": "m($e^{\\pm}e^{\\pm}$"
        },
        "expected": {
          "value_err_plus": 0,
          "value_err_minus": 0,
          "type": "y",
          "name": "Observed",
          "value": 32
        }
      },
      {
        "observed": {
          "value_err_plus": 6,
          "value_err_minus": -6,
          "name": "Expected",
          "value": 19
        },
        "x": {
          "name": "mass_range [GeV]",
          "value": "> 15.0"
        },
        "expected": {
          "value_err_plus": 0,
          "value_err_minus": 0,
          "name": "Expected",
          "value": 14
        }
      }
    ]
  }
}

```

#### Compact YAML


```yaml
---
Table:
  name: "Table 3"
  title: "Upper limit at 95% CL on the fiducial cross section for ℓ±ℓ± pairs from non-SM signals. The expected limits and their 1σ uncertainties are given together with the observed limits derived from the data. Limits are given separately for the e±e±,e±μ± and μ±μ± channel inclusively and separated by charge."
  reaction: "P P --> $e/\\mu{\\pm} e/\\mu{\\pm}$ (+X)"
  qualifiers:
    - type: "sqrt(s)"
      value: "8000.0 GeV"
    - type:
      value: "95% CL upper limit [fb]"
  data:
      - x:
         name: "mass range [GeV]"
         value: "m($e^{\\pm}e^{\\pm}$"
        observed:
         type: y
         name: "Expected"
         value: 39
         value_err_minus: -13
         value_err_plus: 10
        expected:
         type: y
         name: "Observed"
         value: 32
         value_err_minus: 0
         value_err_plus: 0
      - x:
         name: "mass_range [GeV]"
         value: "> 15.0"
        observed:
         name: "Expected"
         value: 19
         value_err_minus: -6
         value_err_plus: 6
        expected:
          name: "Expected"
          value: 14
          value_err_minus: 0
          value_err_plus: 0
          
```

And here is the YAML file rendered using JSON.

```json

{
  "Table": {
    "name": "Table 3",
    "title": "Upper limit at 95% CL on the fiducial cross section for \u2113\u00b1\u2113\u00b1 pairs from non-SM signals. The expected limits and their 1\u03c3 uncertainties are given together with the observed limits derived from the data. Limits are given separately for the e\u00b1e\u00b1,e\u00b1\u03bc\u00b1 and \u03bc\u00b1\u03bc\u00b1 channel inclusively and separated by charge.",
    "reaction": "P P --> $e/\\mu{\\pm} e/\\mu{\\pm}$ (+X)",
    "qualifiers": [
      {
        "type": "sqrt(s)",
        "value": "8000.0 GeV"
      },
      {
        "type": null,
        "value": "95% CL upper limit [fb]"
      }
    ],
    "data": {
      "expected": [
        {
          "values": [
            {
              "err_plus": 10,
              "err_minus": -13,
              "value": 39
            },
            {
              "err_plus": -6,
              "err_minus": -6,
              "value": 19
            }
          ]
        }
      ],
      "x": {
        "values": [
          "m($e^{\\pm}e^{\\pm}$"
        ],
        "name": "mass range [GeV]"
      },
      "observed": [
        {
          "values": [
            {
              "value_err_plus": 0,
              "value_err_minus": 0,
              "value": 32
            },
            {
              "value_err_plus": 0,
              "value_err_minus": 0,
              "value": 14
            }
          ]
        }
      ]
    }
  }
}

```
