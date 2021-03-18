import $ from 'jquery';
import { d3 } from './d3';
import { Tabs } from './tabs';
import { Tab } from './tab';
import { Header } from './header';
import { Section } from './section';
import { SubSection } from './sub-section';
import { Metric } from './metric';
import { VizHeading } from './viz-heading';
import { VizSplit } from './viz-split';
import { VizValue } from './viz-value';
import { VizBars } from './viz-bars';

const TAB_MENU_SELECTOR = '.tab-menu';
const TAB_CONTENT_SELECTOR = '.tab-content';
$(TAB_MENU_SELECTOR).empty();
$(TAB_CONTENT_SELECTOR).empty();

d3.json('data/all_data.json').then((data) => {
  const merged = [data.overview, ...data.departments];
  const tabs = new Tabs();
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
      const section = new Section(tab.$container, sectionData.name, '', '', sectionData.section_type);
      const section_type = sectionData.section_type;
      const subSectionDataArr = sectionData.metrics || [];
      subSectionDataArr.forEach((subSectionData) => {
        const subSection = new SubSection(section.$container);
        const totalValue = subSectionData.value;
        new Metric(
          subSection.$container,
          subSectionData.name,
          subSectionData.metric_type,
          totalValue,
          subSectionData.value_target,
            section_type
        );
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
  });
  tabs.select(0);
});
