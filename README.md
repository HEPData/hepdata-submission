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

### JSON

We have created two versions of the JSON representation, one verbose, and one that is more compact. For a data submitter, it should not matter as writing a script to generate such a file would be fairly simple. However, for data transmission, smaller files are obviously better. 

#### Verbose JSON

```json
{
  "name": "Table 3",
  "title": "Upper limit at 95% CL on the fiducial cross section for ℓ±ℓ± pairs from non-SM signals. The expected limits and their 1σ uncertainties are given together with the observed limits derived from the data. Limits are given separately for the e±e±,e±μ± and μ±μ± channel inclusively and separated by charge.",
  "reaction": "P P --> $e/\mu{\pm} e/\mu{\pm}$ (+X)",
  "qualifiers": [
    {
      "type": "sqrt(s)",
      "value": "8000.0 GeV"
    },
    {
      "type": "",
      "value": "95% CL upper limit [fb]"
    }
  ],
  "data": [
    {
      "x": {
        "header": "mass range [GeV]",
        "value": "m($e^{\pm}e^{\pm}$"
      },
      "y": [
        {
          "header": "Expected",
          "value": 39,
          "value_err_plus": 10,
          "value_err_minus": -13
        },
        {
          "header": "Observed",
          "value": 32,
          "value_err_plus": 0,
          "value_err_minus": 0
        }
      ]
    },

    {
      "x": {
        "header": "mass range [GeV]",
        "value": "> 15.0"
      },
      "y": [
        {
          "header": "Expected",
          "value": 19,
          "value_err_plus": 6,
          "value_err_minus": -6
        },
        {
          "header": "Observed",
          "value": 14,
          "value_err_plus": 0,
          "value_err_minus": 0
        }
      ]
    }
  ]
}
```

#### Compact JSON

### YAML

YAML may be a little more difficult to format than JSON, but it is widely used and using it as a data source would add little overhead to HEPData. Again, we've created verbose and compact representations of the YAML files.

#### Verbose YAML

```yaml
Table:
  name: "Table 3"
  title: "Upper limit at 95% CL on the fiducial cross section for ℓ±ℓ± pairs from non-SM signals. The expected limits and their 1σ uncertainties are given together with the observed limits derived from the data. Limits are given separately for the e±e±,e±μ± and μ±μ± channel inclusively and separated by charge."
  reaction: "P P --> $e/\mu{\pm} e/\mu{\pm}$ (+X)"
  qualifier: 
    type: "sqrt(s)"
    value: "8000.0 GeV"
  qualifier: 
    type: 
    value: "95% CL upper limit [fb]"
  data:
    record:
      x: 
        header: "mass range [GeV]"
        value: "m($e^{\pm}e^{\pm}$"
      y:
        header: "Expected"
        value: 39
        value_err_minus: -13
        value_err_plus: 10     
      y:
        header: "Observed"
        value: 32
        value_err_minus: 0
        value_err_plus: 0     

    record:
      x:
        header: "mass_range [GeV]"
        value: "> 15.0"
      y:
        header: "Expected"
        value: 19
        value_err_minus: -6
        value_err_plus: 6   
      y:
        header: "Observed"
        value: 14
        value_err_minus: 0
        value_err_plus: 0     
        
```

#### Compact YAML