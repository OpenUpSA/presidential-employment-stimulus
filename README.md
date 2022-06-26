# Presidential employment stimulus

This repo provides a webpage that is embedded in [stateofthenation.gov.za](https://www.stateofthenation.gov.za/). This webpage is published at [pres-employment.openup.org.za](https://pres-employment.openup.org.za). An embedded preview is available at [sona-shell.netlify.app](https://sona-shell.netlify.app).

## Development

Data processing is done using Python, website UX design in Webflow, and website dynamics using jQuery and D3.js.

### Structure of the spreadsheet file

**NOTE:** Read this is you are updating the spreadsheet used as input for the website.

The basic structure of the spreadsheet is as follows:

1. Targets - a sheet listing all programmes and their target number of beneficiaries.
   This stays the same for a phase, as targets are set once.

2. Trends - a sheet listing programme outcomes. As the spreadsheet is updated, columns are added to this sheet.

3. Provincial (beneficiaries) - the by-province breakdown of programmes - each province gets a column

4. Demographic data - all non-province breakdowns: gender, youth, etc.

5. Implementation status - the implementation status of each programme

6. Department Descriptions - the descriptions and blurbs ("lead" and "paragraph") for each department

General rules for the spreadsheet:

1. Keep it rectangular: the code expects a grid of rows and columns, so there must not be any merged cells, etc.

2. Pay attention to naming: the programme names need to be exactly the same throughout the spreadsheet

3. Whitespace matters: "Educational Assistants" is different to "Educational  Assistants" and "Educational Assistants "

4. Each change needs a new version: To make it clear which version of which, make sure that each time you change the spreadsheet you give the file a new name and store it in the appropriate place on Google Drive.

## Updating data

**NOTE:** Read this if you are running the data update code.

Data is processed by the Jupyter Lab notebook in `notebooks/p-e_to_json.ipynb`. A cell near the top of the notebook refers to the files that are processed.

As new files are released they are downloaded from Google Drive and put in the `notebooks` folder, the cell with input data names is updated and the whole notebook is re-run. This updates the `data/all_data.json` file. When the update is done, and everything is commited to git and pushed it updates the website. For new months, edit the rows starting with `months` in [python-src/presidential\_employment.py].

Commits made to the `data-updates` branch are visible at <https://data-updates--presidency-employment-stimulus.netlify.app/>.

## Adding months

The list of valid months and corresponding columns in the Trends sheet is in `python-src/presidential_employment.py` lines 342-383.
The months should correspond to the number of columns in the Trends sheet - no more, no less. For lookup on the web interface,
the `data/lookups.json` should be updated.

### Import Webflow export

To update the website with a Webflow export, save the Webflow export to `/webflow-export.zip`, then run:

```bash
npm run webflow-import
```

## Deployment

Commits to `main` are deployed to [presidency-employment-stimulus.netlify.app](https://presidency-employment-stimulus.netlify.app) by [Netlify](https://app.netlify.com/sites/presidency-employment-stimulus). The site [pres-employment.openup.org.za](http://pres-employment.openup.org.za) points at this site.

## Data structure and dependencies

Dependencies:

```yaml
python>=3.9
dataclasses-json>=0.5.6
pandas>=1.4.1
numpy>=1.21.5
```

The data structures in use are:

```pseudocode
Everything -> Overview
           -> List[Department]
           
Overview -> List[PhaseDates] # this describes the start and end dates of the phases
         -> List[Sections]   # the sections are for different types of beneficiary or other top-level divisions e.g. totals vs breakdowns

# when used in Overview
Section -> List[PhasedMetrics] # Metrics are both the top level summary (budget, total beneficiaries) and the different breakdowns
                               # a "PhasedMetric" has a list of total values and target values
PhasedMetric -> List[Dimension] # Dimensions hold the data displayed as line charts, bar charts, etc. i.e. breakdowns of a Metric
Dimension -> List[MultiMetricValue] # MultiMetricValues are used for dimensions that need values that map phase_num -> value

# when used in Department - in this case the phases are split apart at the top level as Phases, not via PhasedMetrics
Department -> Phase
Phase -> List[Section]
         List[Beneficiary]
         List[ImplementationDetail] # when the implementation status is stored on the Department level
Section -> List[Metric]
Metric -> List[Dimension]
          ImplementationDetail # when we have implementation status for a programme
Dimension -> List[MetricValue] # where the MetricValue stores value and value_target e.g. by time, by gender, etc

```
