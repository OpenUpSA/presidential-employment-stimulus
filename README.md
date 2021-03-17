# Presidential employment stimulus

This repo provides a webpage that is embedded in [stateofthenation.gov.za](https://www.stateofthenation.gov.za/). This webpage is published at [pres-employment.openup.org.za](https://pres-employment.openup.org.za). An embedded preview is available at [sona-shell.netlify.app](https://sona-shell.netlify.app).

## TODO

- [ ] Make province etc. more general = 'bar' {'key', 'value'}
- [ ] Must e.g. "Dec '20 - Jan '21" in tab header?
- [ ] More direct selectors
- [ ] Metric target selector `span` instead of writing 'TARGET {}'
- [ ] Use webflow event handling for tabs and tooltips?

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
