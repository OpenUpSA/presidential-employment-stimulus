import $ from 'jquery';
import { d3 } from './d3';
import { Tabs } from './tabs';
import { Tab } from './tab';
import { Header } from './header';
import { OverviewSection } from "./overview-section";
import { OverviewVizBars} from "./overview-viz-bars";
import { Section } from './section';
import { SubSection } from './sub-section';
import { Metric } from './metric';
import { VizHeading } from './viz-heading';
import { VizSplit } from './viz-split';
import { VizValue } from './viz-value';
import { VizBars } from './viz-bars';
import { VizLine } from './viz-line';
import {ImplementationDetail} from "./implementation-detail";
import {organizeByZero} from "./utils";

const TEMPORARY_HIDDEN_SELECTOR = '.tabs-wrapper';

const TAB_MENU_SELECTOR = '.tab-menu';
const TAB_CONTENT_SELECTOR = '.tab-content';
$(TAB_MENU_SELECTOR).empty();
$(TAB_CONTENT_SELECTOR).empty();

d3.json('data/all_data.json').then((data) => {
  const merged = [data.overview, ...data.departments];
  const tabs = new Tabs();
  const overviewTab = new Tab(
      TAB_MENU_SELECTOR,
      TAB_CONTENT_SELECTOR,
      data.overview.name,
      () => tabs.select(0)
  );



  new Header(overviewTab.$container, data.overview.name, data.overview.lead, data.overview.paragraph);
  // TODO: Clean up this ugly code using components etc
  const CONTENT_GRID_SELECTOR = '.thirds-grid';
  const $overviewGrid = $(CONTENT_GRID_SELECTOR).first().clone(true, true);
  $overviewGrid.empty();
  const overviewSectionArr = data.overview.sections || [];
  overviewSectionArr.forEach((overviewSectionData) => {
    const $el = $('<div></div>');
    const overviewSection = new OverviewSection($el, overviewSectionData.name, overviewSectionData.section_type,
        'count', overviewSectionData.value, overviewSectionData.value_target);
    new VizHeading($el, overviewSectionData.name);
    new OverviewVizBars($el, overviewSectionData.metrics);
    $overviewGrid.append($el);
  });

  overviewTab.$container.append($overviewGrid);
  tabs.add(overviewTab);
  data.departments.forEach((tabData, i) => {
    const tab = new Tab(
      TAB_MENU_SELECTOR,
      TAB_CONTENT_SELECTOR,
      tabData.name,
      () => tabs.select(i+1),
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
        if (subSectionData.time) {
          new VizHeading(subSection.$container, subSectionData.time.name);
          new VizLine(subSection.$container, subSectionData.time.values);
        }
        if (subSectionData.gender) {
          new VizHeading(subSection.$container, subSectionData.gender.name);
          const genderOne = subSectionData.gender.values[0];
          const genderTwo = subSectionData.gender.values[1];
          new VizSplit(
            subSection.$container,
            'percentage',
            genderOne.gender, genderOne.value,
            genderTwo.gender, genderTwo.value,
          );
        }
        if (subSectionData.age) {
          new VizHeading(subSection.$container, subSectionData.age.name);
          const ageValue = subSectionData.age.values[0].value;
          new VizValue(
            subSection.$container,
            'count',
            ageValue,
          );
        }
        if (subSectionData.province) {
          new VizHeading(subSection.$container, subSectionData.province.name);
          new VizBars(subSection.$container, subSectionData.province.values);
        }
      });
    });
    if (tabData.implementation_details.length > 0) {
      const implDetails = new Section(tab.$container, 'Implementation details', '', '', '');
      tabData.implementation_details.forEach((implData) => {
        const subSection = new SubSection(tab.$container);
        new ImplementationDetail(subSection.$container, implData.programme_name, implData.status, implData.detail);
      });
    }
  });
  tabs.select(0);
  $(TEMPORARY_HIDDEN_SELECTOR).show();
});
