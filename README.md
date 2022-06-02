# Presidential employment stimulus

This repo provides a webpage that is embedded in [stateofthenation.gov.za](https://www.stateofthenation.gov.za/). This webpage is published at [pres-employment.openup.org.za](https://pres-employment.openup.org.za). An embedded preview is available at [sona-shell.netlify.app](https://sona-shell.netlify.app).


## Development

Data processing is done using Python, website UX design in Webflow, and website dynamics using jQuery and D3.js.

### Generate data from spreadsheet files

TODO

### Import Webflow export

To update the website with a Webflow export, save the Webflow export to `/webflow-export.zip`, then run:

```bash
npm run webflow-import
```

## Deployment

Commits to `main` are deployed to [presidency-employment-stimulus.netlify.app](https://presidency-employment-stimulus.netlify.app) by [Netlify](https://app.netlify.com/sites/presidency-employment-stimulus). The site [pres-employment.openup.org.za](http://pres-employment.openup.org.za) points at this site.

## Updating data

Data is processed by the Jupyter Lab notebook in `notebooks/p-e_to_json.ipynb`. The notebook uses `pandas` (and `numpy`). A cell near the top of the notebook refers to the files that are processed. As new files are released they are downloaded from Google Drive and put in the `notebooks` folder, the cell with input data names is updated and the whole notebook is re-run. This updates the `data/all_data.json` file. When the update is done, and everything is commited to git and pushed it updates the website. For new months, edit the rows starting with `months` in [python-src/presidential\_employment.py].

Commits made to the `data-updates` branch are visible at <https://data-updates--presidency-employment-stimulus.netlify.app/>.

## Adding months

The list of valid months and corresponding columns in the Trends sheet is in `python-src/presidential_employment.py` lines 342-383.
The months should correspond to the number of columns in the Trends sheet - no more, no less. For lookup on the web interface,
the `data/lookups.json` should be updated.
