# HEPData Submission

HEPData submission will largely involve the upload of archives (.zip, .tar, .tar.gz) that specify the data associated with a publication.

The main file for a submission is the *submission.yaml* file.
This links together all the data tables into one submission and defines auxiliary files such as scripts used to create the data, ROOT files, or even links to GitHub/Bitbucket/Zenodo etc. for more substantial pieces of code.

The data files for each table, in either YAML or JSON format, specifies the data points in terms of independent and dependent variables.

 ![image](assets/hepdata_root_processing.png)

## submission.yaml

The *submission.yaml* file tells HEPdata about your entire submission, but most importantly, what data files are in your submission, what they contain, any related material, keywords, etc.

Some information, like the *name*, *description*, *keywords*, and the reference to the *data_file* are required.  For example, the table definition below is perfectly valid.

``` yaml
name: "Table 1"
description: Describe the data.  The more you say, the easier it'll be to search for it later.
keywords: # used for searching, possibly multiple values for each keyword
  - {name: reactions, values: [P P --> Z0 Z0 X]}
  - {name: observables, values: [SIG]}
  - {name: cmenergies, values: [7000.0]}
  - {name: phrases, values: [Inclusive, Integrated Cross Section, Cross Section, Proton-Proton Scattering, Z Production, Z pair Production]}
data_file: data1.yaml

```

Then, there are some *optional* things, such as the *location* of the data within the associated paper, a *license* for your data, or pointing to *additional_resources*, e.g. code or ROOT files you've used to create this data.
Sharing this will enable others to do meaningful things with your data long after you've finished with it...and that's a good thing.


``` yaml
name: "Table 1"
description: Describe the data.  The more you say, the easier it'll be to search for it later.
keywords: # used for searching, possibly multiple values for each keyword
  - {name: reactions, values: [P P --> Z0 Z0 X]}
  - {name: observables, values: [SIG]}
  - {name: cmenergies, values: [7000]}
  - {name: phrases, values: [Inclusive, Integrated Cross Section, Cross Section, Proton-Proton Scattering, Z Production, Z pair Production]}
data_file: data1.yaml
location: Data from Page 17 of preprint # (optional)
data_license: # (optional) you can specify a license for the data 
  name: "GPL 2"
  url: "url for license"
  description: "Tell me about it. This can appear in the main record display" # (optional)
additional_resources: # (optional)
  - location: "https://github.com/HEPData/hepdata"
    description: "Full source code for creating this data"
  - location: "root_file.root"
    description: "Some file"
    license: # (optional)
      name: 'GPL 2'
      url: "url for license"
      description: "Tell me about it. This can appear in the main record display" # (optional)
```

### submission.yaml Full Example


``` yaml

# Start a new submission. This section is optional for the provision of information about the overall submission.
---
  
additional_resources: # additional references (e.g. experiment TWiki page for analysis)
  - {location: "http://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/PAPERS/STDM-2012-02/", description: "web page with auxiliary material"}

comment: | # Information that applies to all data tables.
  CERN-LHC.  Measurements of the cross section  for ZZ production using the 4l and 2l2nu decay channels in proton-proton collisions at a centre-of-mass energy of 7 TeV with 4.6 fb^-1 of data collected in 2011.  The final states used are 4 electrons, 4 muons, 2 electrons and 2 muons, 2 electrons and missing transverse momentum, and 2 muons and missing transverse momentum (MET).

  The cross section values reported in the tables should be multiplied by a factor of 1.0141 to take into account the updated value of the integrated luminosity for the ATLAS 2011 data taking period.  The uncertainty on the global normalisation ("Lumi") remains at 1.8%.  See Eur.Phys.J. C73 (2013) 2518 for more details.

  The 4l channel fiducial region is defined as:
  - 4e, 4mu or 2e2mu
  - Ambiguities in pairing are resolved by choosing the combination that results in the smaller value of the sum |mll - mZ| for the two pairs, where mll is the mass of the dilepton system.
  - ptLepton > 7 GeV (at least one with ptLepton > 20 (25) GeV for muons (electrons))
  - |etaLepton| < 3.16
  - At least one lepton pair is required to have invariant mass between 66 and 116 GeV. If the second pair also satisfies this, the event is ZZ, otherwise if the second pair satisfies mll > 20 GeV it is ZZ*.
  - min(DeltaR(l,l)) > 0.2.

  The 2l2nu channel fiducial region is defined as:
  - 2e+MET or 2mu+MET
  - ptLepton > 20 GeV
  - |etaLepton| < 2.5
  - mll must be between 76 and 106 GeV
  - -MET*cos(phi_METZ)>75 GeV, where phi_METZ is the angle between the Z and the MET
  - |MET - pTZ| / pTZ < 0.4, where pTZ is the transverse momentum of the dilepton system
  - No events with a jet for which ptJet > 25 GeV and |etaJet| < 4.5
  - No events with a third lepton for which ptLepton > 10 GeV
  - min(DeltaR(l,l)) > 0.3

---
# Start of table entries
# This is Table 1.
name: "Table 1"
location: Data from Page 17 of preprint
description: The measured fiducial cross sections.  The first systematic uncertainty is the combined systematic uncertainty excluding luminosity, the second is the luminosity
keywords: # used for searching, possibly multiple values for each keyword
  - {name: reactions, values: [P P --> Z0 Z0 X]}
  - {name: observables, values: [SIG]}
  - {name: cmenergies, values: [7000.0]}
  - {name: phrases, values: [Inclusive, Integrated Cross Section, Cross Section, Proton-Proton Scattering, Z Production, Z pair Production]}
data_file: data1.yaml
data_license: # (optional) you can specify a license for the data 
  name: "GPL 2"
  url: "url for license"
  description: "Tell me about it. This can appear in the main record display" # (optional)
additional_resources: # (optional)
  - location: "https://github.com/HEPData/hepdata"
    description: "Full source code for creating this data"
  - location: "root.root"
    description: "Some file"
    license: # (optional)
      name: "GPL 2"
      url: "url for license"
      description: "Tell me about it. This can appear in the main record display" # (optional)

---
# This is Table 2.
name: "Table 2"
location: Data from Page 20 of preprint
description: The measured total cross sections.  The first systematic uncertainty is the combined systematic uncertainty excluding luminosity, the second is the luminosity
keywords: # used for searching, possibly multiple values for each keyword
  - {name: reactions, values: [P P --> Z0 Z0 X]}
  - {name: observables, values: [SIG]}
  - {name: cmenergies, values: [7000.0]}
  - {name: phrases, values: [Inclusive, Integrated Cross Section, Cross Section, Proton-Proton Scattering, Z Production, Z pair Production]
data_file: data2.yaml

---
# This is Table 3.
name: "Table 3"
location: Data from Figure 8A
description: Normalized ZZ fiducial cross section (multiplied by 10^6 for readability) in bins of the leading reconstructed dilepton pT for the 4 lepton channel.  The first systematic uncertainty is detector systematics, the second is background systematic uncertainties
keywords: # used for searching, possibly multiple values for each keyword
  - {name: reactions, values: [P P --> Z0 Z0 X]}
  - {name: observables, values: [DSIG/DPT]}
  - {name: cmenergies, values: [7000.0]}
  - {name: phrases, values: [Inclusive, Single Differential Cross Section, Transverse Momentum Dependence, Proton-Proton Scattering, Z Production, Z pair Production]
data_file: data3.yaml
additional_resources:
- {description: Image file, location: figFigure8A.png}
- {description: Thumbnail image file, location: thumb_figFigure8A.png}

```

## Data Files

Data files can be encoded as either YAML or JSON: the software deals with both the same way.
We define the data file in two parts which describe:

 - a) the independent variables (the x-axis of a plot)
 - b) the dependent variables (the thing you're measuring, e.g. the y-axis of a plot)
 
 Inside each you can define the header (the column name), and the values (the rows in your table).
 For the dependent variables, you can also define 'qualifiers'.  These are extra metadata describing the measurement,
 such as the energy, the reaction type, and possible kinematic cuts.


### YAML

``` yaml
independent_variables:
- header: {name: Leading dilepton PT, units: GEV}
  values:
  - {low: 0, high: 60}
  - {low: 60, high: 100}
  - {low: 100, high: 200}
  - {low: 200, high: 600}
dependent_variables:
- header: {name: 10**6 * 1/SIG(fiducial) * D(SIG(fiducial))/DPT, units: GEV**-1}
  qualifiers:
  - {name: RE, value: P P --> Z0 < LEPTON+ LEPTON- > Z0 < LEPTON+ LEPTON- > X}
  - {name: SQRT(S), units: GEV, value: 7000}
  values:
  - value: 7000
    errors:
    - {symerror: 1100, label: stat}
    - {symerror: 79, label: 'sys,detector'}
    - {symerror: 15, label: 'sys,background'}
  - value: 9800
    errors:
    - {symerror: 1600, label: stat}
    - {symerror: 75, label: 'sys,detector'}
    - {symerror: 15, label: 'sys,background'}
  - value: 1600
    errors:
    - {symerror: 490, label: stat}
    - {symerror: 41, label: 'sys,detector'}
    - {symerror: 2, label: 'sys,background'}
  - value: 80
    errors:
    - {symerror: 60, label: stat}
    - {symerror: 2, label: 'sys,detector'}
    - {symerror: 0, label: 'sys,background'}
```

### Uncertainties

There are two main classes of uncertainty that can be encoded: symmetric errors and asymmetric errors.
Symmetric errors allow you to specify plus and minus errors using one value, e.g. ```symerror: 0.4```.
Unsurprisingly, an asymmetric error allows both plus and minus errors to be explicitly encoded, e.g. ```asymerror: {plus: 0.4, minus: -0.3}```.
Note that "plus" and "minus" can refer to "up" and "down" variations of the source of uncertainty, and do not necessarily match the
sign of the resultant uncertainty on the measurement (which can change sign along a distribution).


## Common mistakes and how to avoid them

YAML has its idiosyncrasies, like all input formats.  We attempt to list some common problems here.

- ***Escape special characters***
  
  Some characters in YAML need to be escaped, otherwise they cause errors when parsing.
  The two characters that cause most trouble for YAML are ':' and '-'.
  So if you use these characters in some description string, make sure you quote the whole string.

- ***Ensure spacing between colons***
  
  Another annoyance can be with spacing. ```{symerror:0.4, label:stat}``` will give you an error.
  Change this to ```{symerror: 0.4, label: stat}``` however and everything will work nicely!
