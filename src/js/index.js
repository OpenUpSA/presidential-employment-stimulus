import $ from 'jquery';
import { d3 } from './d3';
import { Tabs } from './tabs';
import { Tab } from './tab';
import { Header } from './header';
import { OverviewVizBars } from './overview-viz-bars';
import { Section } from './section';
import { SubSection } from './sub-section';
import { Metric } from './metric';
import { VizHeading } from './viz-heading';
import { VizSplit } from './viz-split';
import { VizValue } from './viz-value';
import { VizBars } from './viz-bars';
import { VizLine } from './viz-line';
import { NoData } from "./nodata";
import { ImplementationDetail } from './implementation-detail';
import { organizeByZero, fillInMissingSections } from './utils';

const TEMPORARY_HIDDEN_SELECTOR = '.tabs-wrapper';

const TAB_MENU_SELECTOR = '.tab-menu';
const TAB_CONTENT_SELECTOR = '.tab-content';
$(TAB_MENU_SELECTOR).empty();
$(TAB_CONTENT_SELECTOR).empty();
const CONTENT_GRID_SELECTOR = '.thirds-grid';
$(CONTENT_GRID_SELECTOR).empty();
const $thirdsGrid = $(CONTENT_GRID_SELECTOR).first().clone(true, true);

Promise.all([
  d3.json('data/all_data.json'),
  d3.json('data/lookups.json'),
  d3.json('data/metric_titles.json'),
]).then(([
  data,
  lookups,
  metric_titles,
]) => {
  const merged = [data.overview, ...data.departments];
  const tabs = new Tabs();
  // const overviewTab = new Tab(
  //     TAB_MENU_SELECTOR,
  //     TAB_CONTENT_SELECTOR,
  //     data.overview.name,
  //     () => tabs.select(0)
  // );
  //
  //
  //
  // new Header(overviewTab.$container, data.overview.name, data.overview.lead, data.overview.paragraph);
  // // TODO: Clean up this ugly code using components etc
  // const $overviewGrid = $thirdsGrid.clone(true, true);
  // const overviewSectionArr = data.overview.sections || [];
  // const overviewSection = new Section(overviewTab.$container, 'Overview', 'An overview of the programmes', '', 'livelihoods');
  //
  // overviewSectionArr.forEach((overviewSectionData) => {
  //   const subSection = new SubSection(overviewSection.$container);
  //   new Metric(
  //     subSection.$container,
  //     overviewSectionData.name,
  //     overviewSectionData.section_type,
  //     'count',
  //     overviewSectionData.value,
  //     overviewSectionData.value_target,
  //   );
  //   new VizHeading(subSection.$container, overviewSectionData.name);
  //   new OverviewVizBars(subSection.$container, overviewSectionData.metrics, lookups.province);
  //   // $overviewGrid.append($el);
  // });
  //
  // overviewTab.$container.append($overviewGrid);
  // tabs.add(overviewTab);
  merged.forEach((tabData, i) => {
    const tab = new Tab(
      TAB_MENU_SELECTOR,
      TAB_CONTENT_SELECTOR,
      tabData.name,
      () => tabs.select(i),
    );
    tabs.add(tab);
    new Header(tab.$container, tabData.name, tabData.lead, tabData.paragraph);
    const sectionDataArr = tabData.sections || [];
    sectionDataArr.forEach((sectionData) => {
      const section = new Section(tab.$container, sectionData.name, '', '', sectionData.sectionType);
      const sectionType = sectionData.section_type;
      const subSectionDataArr = organizeByZero(sectionData.metrics || []);
      subSectionDataArr.forEach((subSectionData) => {
        const subSection = new SubSection(section.$container);
        new Metric(
          subSection.$container,
          subSectionData.name,
          sectionType,
          subSectionData.metric_type,
          subSectionData.value,
          subSectionData.value_target,
        );
        const has_vets = tabData.sheet_name === "DALRRD" && sectionType === "livelihoods";
        const dimensions = ((sectionType === "targets" || sectionType === "overview") ? subSectionData.dimensions : fillInMissingSections(subSectionData.dimensions, has_vets));
        dimensions.forEach((dimension) => {
          if (dimension.data_missing) {
            if (tabData.sheet_name === 'DALRRD') {
              console.log(sectionType, subSectionData.metric_type, dimension.lookup);
            }
            new VizHeading(subSection.$container, metric_titles[sectionType][subSectionData.metric_type + '_' + dimension.lookup] + ' : NO DATA AVAILABLE');
          } else {
            if (dimension.viz === 'line') {
              new VizHeading(subSection.$container, dimension.name);
              new VizLine(subSection.$container, dimension.values, lookups[dimension.lookup]);
            }
            if (dimension.viz === 'two_value') {
              new VizHeading(subSection.$container, dimension.name);
              const valueOne = dimension.values[0];
              const valueTwo = dimension.values[1];
              new VizSplit(
                  subSection.$container,
                  'percentage',
                  valueOne.key, valueOne.value,
                  valueTwo.key, valueTwo.value,
              );
            }
            if (dimension.viz === 'percentile' || dimension.viz === 'count') {
              new VizHeading(subSection.$container, dimension.name);
              const { value } = dimension.values[0];
              new VizValue(
                  subSection.$container,
                  dimension.viz,
                  value,
              );
            }
            if (dimension.viz === 'bar') {
              new VizHeading(subSection.$container, dimension.name);
              new VizBars(
                  subSection.$container,
                  dimension.values,
                  lookups[dimension.lookup],
              );
            }
          }
        });
        if (subSectionData.implementation_detail) {
          const implData = subSectionData.implementation_detail;
          new ImplementationDetail(
            subSection.$container,
            implData.programme_name,
            implData.status,
            implData.detail,
              false,
          );
        }
      });
    });
    if (typeof tabData.implementation_details !== 'undefined' && tabData.implementation_details.length > 0) {
      new Section(tab.$container, 'Implementation status reports', '', '', '');
      tabData.implementation_details.forEach((implData) => {
        const $implGrid = $thirdsGrid.clone(true, true);
        tab.$container.append($implGrid);
        // const subSection = new SubSection($implGrid);

        new ImplementationDetail(
            $implGrid,
            implData.programme_name,
            implData.status,
            implData.detail,
            true
        );
      });
    }
  });
  tabs.select(0);
  $(TEMPORARY_HIDDEN_SELECTOR).show();
});
