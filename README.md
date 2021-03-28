# Presidential employment stimulus

This repo provides a webpage that is embedded in [stateofthenation.gov.za](https://www.stateofthenation.gov.za/). This webpage is published at [pres-employment.openup.org.za](https://pres-employment.openup.org.za). An embedded preview is available at [sona-shell.netlify.app](https://sona-shell.netlify.app).

## TODO

- [ ] Make JSON interface more generic (see below) (later)
- [x] Import webflow export once Matt is done
- [x] Format number over 1 million using long (x billion) and short (x b)
- [ ] Time line chart
- [ ] Make province etc. more general = 'bar' {'key', 'value'}
- [ ] Must e.g. "Dec '20 - Jan '21" in tab header?
- [ ] More direct selectors
- [ ] Metric target selector `span` instead of writing 'TARGET {}'
- [ ] Use webflow event handling for tabs and tooltips?

### Make JSON interface more generic:

Instead of:

```json
"metrics": [
  {
    "name": "Social Development",
    "metric_type": "count",
    "value": 0,
    "time": null,
    "gender": null,
    "age": null,
    "province": null,
    "value_target": 108833
  }
]
```

Do something like:

```json
"metrics": [
  {
    "name": "Social Development",
    "metric_type": "count",
    "value": 0,
    "value_target": 108833,
    "dimensions": [
      {
        "type": "time"
      },
      {
        "type": "split"
      },
      {
        "type": "percentage"
      },
      {
        "type": "bars"
      }
    ]
  }
]
```


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

Commits to `main` are deployed to [presidency-employment-stimulus.netlify.app](https://presidency-employment-stimulus.netlify.app) by [Netlify](https://app.netlify.com/sites/presidency-employment-stimulus).

Once DNS records have been updated, [pres-employment.openup.org.za](http://pres-employment.openup.org.za) will point to this deployment.
