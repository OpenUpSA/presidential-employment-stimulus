import $ from 'jquery';
import { d3 } from './d3';
import { Tabs } from './tabs';
import { Tab } from './tab';
import { Header } from './header';
import { Footer } from "./footer";
import { Section } from './section';
import { SubSection } from './sub-section';
import { Metric } from './metric';
import { VizHeading } from './viz-heading';
import { VizSplit } from './viz-split';
import { VizValue } from './viz-value';
import { VizBars } from './viz-bars';
import { OverviewVizBars } from './overview-viz-bars';
import { VizLine } from './viz-line';
import { VizHeader } from './viz-header';
import { VizPhased } from './viz-phased';
import { NoData } from "./nodata";
import { ImplementationDetail } from './implementation-detail';
import { organizeByZero, fillInMissingSections } from './utils';
import { BeneficiaryStories} from "./beneficiary-stories";
import { FORMATTERS, hasPhase } from './utils';
import { Phases } from './phases';
import { filter } from 'd3-array';

const TEMPORARY_HIDDEN_SELECTOR = '.tabs-wrapper';

const TAB_MENU_SELECTOR = '.tab-menu';
const TAB_CONTENT_SELECTOR = '.tab-content';
const CONTENT_GRID_SELECTOR = '.thirds-grid';

const ICONS_SELECTOR = '.icons';
const $iconsTemplate = $(ICONS_SELECTOR).first().clone(true, true);

const $thirdsGrid = $(CONTENT_GRID_SELECTOR).first().clone(true, true);

const $performanceCtaTemplate = $('.is--performance-cta').first().clone(true, true);

$(TAB_MENU_SELECTOR).empty();
$(TAB_CONTENT_SELECTOR).empty();
$(CONTENT_GRID_SELECTOR).empty();


Promise.all([
  d3.json('data/all_data.json'),
  d3.json('data/beneficiaries.json'),
  d3.json('data/lookups.json'),
  d3.json('data/metric_titles.json'),
]).then(([
  data,
  beneficiaries,
  lookups,
  metric_titles,
]) => {

  const merged = [data.overview, ...data.departments];

  const tabs = new Tabs();

  merged.forEach((tabData, i) => {

    let startPhase = 0;

    if(tabData.name != 'Programme overview') {

      startPhase = tabData.phases.map((phase) => phase.phase_num)
      .reduce((max, curr) => Math.max(max, curr), 0);

    }

    const tab = new Tab(
      TAB_MENU_SELECTOR,
      TAB_CONTENT_SELECTOR,
      tabData.name,
      () => tabs.select(i),
      tabData.name == 'Programme overview' ? 'overview' : 'department',
      tabData.name == 'Programme overview' ? 0 : tabData.phases.length,
      startPhase
    );

    tabs.add(tab);

    const months_text = lookups["time"][tabData.month];

    new Header(tab.$container, tabData.name, tabData.lead, tabData.paragraph, months_text, hasPhase(1, tabData));

    let filteredBeneficiaries = [];

    if(tabData.name != 'Programme overview') {

      let department_abbr = ''

      for (const key in lookups["department"]) {
        if(lookups["department"][key] == tabData.name) {
          department_abbr = key;
        }
      }

      filteredBeneficiaries = beneficiaries.filter(function (story) {
        return story.department === department_abbr && story.featured != true;
      });

    } else {

      filteredBeneficiaries = beneficiaries.filter(function (story) {
        return story.featured === true
      });


    }

    if(filteredBeneficiaries.length > 0) {

      new BeneficiaryStories(lookups, tab.$container, filteredBeneficiaries, tabData.name == 'Programme overview' ? true : false, tabData.name);

    }

    let phases;

    if(tabData.name != 'Programme overview') {
      phases = new Phases(tab.$container);
    }

    const phasesArr = tabData.phases || [];

    if(tabData.name == 'Programme overview') {
      phasesArr.push(
        {
          sections: tabData.sections
        }
      )
    }


    for (let phase = 0; phase < phasesArr.length; phase++) {

      let $phaseContent = $('<div></div>');

      const sectionDataArr = phasesArr[phase].sections || [];
      sectionDataArr.forEach((sectionData, sectionIndex) => {

        if (sectionData.metrics.length !== 0) {

          let section;

          if(tabData.name == 'Programme overview') {
            section = new Section(lookups, tab.$container, sectionData.name, '', '', sectionData.section_type, true, tabData);
          } else {
            section = new Section(null, $phaseContent, sectionData.name, '', '', sectionData.section_type);
          }

          const sectionType = sectionData.section_type;

          const subSectionDataArr = organizeByZero(sectionData.metrics || []);

          subSectionDataArr.forEach((subSectionData) => {

            const subSection = new SubSection(section.$container);

            if(tabData.name == 'Programme overview') {

              new VizPhased(
                lookups,
                subSection.$container,
                sectionType,
                subSectionData.viz,
                subSectionData.metric_type,
                subSectionData.name,
                subSectionData.value,
                subSectionData.value_target,
                subSectionData.total_value
              );

            } else {

              new VizHeader(
                lookups,
                subSection.$container,
                sectionType,
                subSectionData.metric_type,
                subSectionData.name,
                subSectionData.value,
                subSectionData.value_target,
                sectionType == 'targets' ? true : false,
                sectionType == 'targets' ? false : true,
                phase
              );

            }


            new Metric(
                subSection.$container,
                subSectionData.name,
                sectionType,
                subSectionData.metric_type,
                subSectionData.value,
                subSectionData.value_target, tabData.sheet_name
            );

            const has_vets = tabData.sheet_name === "DALRRD" && sectionType === "livelihoods";



            const dimensions = ((sectionType === "targets" || sectionType === "overview" || sectionType === "job_opportunities" || sectionType === "livelihoods") ? subSectionData.dimensions : fillInMissingSections(subSectionData.dimensions, has_vets));
            dimensions.forEach((dimension) => {

              if (dimension.data_missing) {

                // new VizHeading(subSection.$container, metric_titles[sectionType][subSectionData.metric_type + '_' + dimension.lookup] + ' : NO DATA AVAILABLE');

              } else {

                const hideHeading = sectionType === 'overview' & subSectionData.metric_type === 'targets_count';

                if (dimension.viz != 'line') {
                  new VizHeading(subSection.$container, dimension.name, hideHeading);
                }

                if (dimension.viz === 'two_value') {

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

                  const {value} = dimension.values[0];

                  new VizValue(
                      subSection.$container,
                      dimension.viz,
                      value,
                  );
                }

                if (dimension.viz === 'bar') {

                  const hideZeros = sectionType === 'overview';

                  new VizBars(
                      subSection.$container,
                      dimension.values,
                      lookups[dimension.lookup],
                      hideZeros,
                      tabData.name == 'Programme overview' ? 0 : tabData.phases[phase].phase_num
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

        }

        if(phasesArr.length > 1 && sectionIndex == 0) {

          let otherPhase = phase == 0 ? 1 : 0;

          let formatter = FORMATTERS[phasesArr[otherPhase].sections[0].metrics[1].metric_type];

          let $performanceCta = $performanceCtaTemplate.clone(true,true);
          $performanceCta.find('img').remove();

          let $icons = $iconsTemplate.clone(true, true);

          if(otherPhase == 0) {
            $performanceCta.prepend($icons.find('.icon--performance-' + (otherPhase + 1) ));
            $performanceCta.find('.performance-cta__heading').text('This department participated previously with ' + formatter(phasesArr[otherPhase].sections[0].metrics[1].value) + ' beneficiaries')
            $performanceCta.find('.performance-cta__text').text('Explore previous performance');
            $performanceCta.find('.performance-cta__button-text').text('Explore');
            $performanceCta.find('.button.is--performance-cta').attr('data-w-tab','Completed');
          } else {
            $performanceCta.prepend($icons.find('.icon--performance-' + (otherPhase + 1) ));
            $performanceCta.find('.performance-cta__heading').text('This department is currently participating with ' + formatter(phasesArr[otherPhase].sections[0].metrics[1].value) + ' beneficiaries')
            $performanceCta.find('.performance-cta__text').text('Explore Current performance');
            $performanceCta.find('.performance-cta__button-text').text('Explore');
            $performanceCta.find('.button.is--performance-cta').attr('data-w-tab','Current');
          }

          $phaseContent.append($performanceCta);

        }

      });


      if (typeof phasesArr[phase].implementation_details !== 'undefined' && phasesArr[phase].implementation_details.length > 0) {

        new Section(null, $phaseContent, 'Implementation status reports', '', '', '');

        phasesArr[phase].implementation_details.forEach((implData) => {

          const $implGrid = $thirdsGrid.clone(true, true);

          $implGrid.find('.loading').hide();
          $phaseContent.append($implGrid);

          if(implData) {

            new ImplementationDetail(
                $implGrid,
                implData.programme_name,
                implData.status,
                implData.detail,
                true
            );

          }

        });
      }

      if(tabData.name != 'Programme overview') {

        phases.add(phasesArr.length, tabData.phases[phase].phase_num, $phaseContent);
      } else {
        $phaseContent.addClass('progamme-achievements')
        tab.$container.append($phaseContent);
      }

    }





    if (typeof tabData.footer_header !== 'undefined' && tabData.footer_header) {
      new Footer(tab.$container, '', tabData.footer_header, tabData.footer_paragraph);
    }



  });

  // Webflow.require('ix2').init();
  tabs.select(0);

  $(TEMPORARY_HIDDEN_SELECTOR).show();

  $('.button.is--performance-cta').on('click', function() {

    let phase = $(this).attr('data-w-tab');
    $(this).parents().eq(4).find('a.phase-tab[data-w-tab="' + phase + '"]').trigger('click');

  })

});
