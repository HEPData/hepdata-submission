# HEP Data Submission

HEP data submission will largely involve the upload of ROOT files that specify the plots for the publication, and the data that underlay these plots.
It is unclear if ROOT will be completely suitable for the inclusion of data. This is a topic for discussion in the coming days.

However, there also needs to be an exchange format between the ROOT data extraction API and the front end to render the results. JSON would be used for this purpose regardless.

![image](assets/hepdata_root_processing-01.png =700x)

## Submission Format

The submission format would ideally be just via the ROOT files. These files should include the plots (that will be automatically plotted), and the data tables related to these plots.

The following representations are there to roughly model data in [Table 8](http://hepdata.cedar.ac.uk/view/ins1331782/d3) of [Aad, et. al, Search for anomalous production of prompt same-sign lepton pairs and pair-produced doubly charged Higgs bosons with s√=8 TeV pp collisions using the ATLAS detector, 2014](http://inspirehep.net/record/1331782).
More examples could be created to model other data tables, however our model defined below seems to represent the data tables we've so far observed in HEPData.

### ROOT Data Files

Creating [ROOT TTrees](https://root.cern.ch/root/html/TTree.html) is relatively easy. Formatting the data correctly is the hard part. We've tried to structure the tree to make it both easy to get the data in to the files, and to make it easy for us to reconstruct the data table following submission.

** IN DRAFT **

```python

class DataValue(TreeModel):
    """
        For each value, we have its error on the X and Y axes
    """
    val = FloatCol()
    err_y_minus = FloatCol()
    err_y_plus = FloatCol()
    err_x_minus = FloatCol()
    err_x_plus = FloatCol()


class DataRecord(DataValue.prefix('x_'), DataValue.prefix('expected_'), DataValue.prefix('observed_')):
    i = IntCol()


class DataGenerator(object):

    def generate_root_file_with_tree(self, file_name, mode="update"):

        f = root_open(file_name, mode)
        trees = ["hpx", "hpxpy", "hprof"]

        for tree_name in trees:

            tree = Tree(name=tree_name, title=tree_name, model=DataRecord)
            # F - Float, I - Integer

            for i in xrange(1000):
                tree.x_val = gauss(1., 4.)
                tree.x_err_y_minus = gauss(0., 1)
                tree.x_err_y_plus = gauss(0., 1)

                tree.expected_val = gauss(1., 4.)
                tree.expected_err_y_minus = gauss(1., 4.)
                tree.expected_err_x_minus = gauss(1., 4.)

                tree.observed_val = gauss(1., 4.)
                tree.observed_err_y_minus = gauss(1., 4.)
                tree.observed_err_x_minus = gauss(1., 4.)

                tree.i = i
                tree.fill()

            tree.write()

        f.close()

```

### YAML

YAML may be a little more difficult to generate and parse than JSON, but it is generally seen as more readable than JSON. YAML could be used and then translated to JSON (or use JSON directly for the upload).
Moreover, JSON representations of the YAML can also be used (these were generated using the YAML parser [here](http://yaml-online-parser.appspot.com/).
We've created verbose and compact representations of the YAML files that vary how data records are represented.
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
