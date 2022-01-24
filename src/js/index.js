import $ from 'jquery';
import { d3 } from './d3';
import { Tabs } from './tabs';
import { Tab } from './tab';
import { Header } from './header';
import { Footer } from "./footer";
import { OverviewVizBars } from './overview-viz-bars';
import { Section } from './section';
import { SubSection } from './sub-section';
import { Metric } from './metric';
import { VizHeading } from './viz-heading';
import { VizSplit } from './viz-split';
import { VizValue } from './viz-value';
import { VizBars } from './viz-bars';
import { VizLine } from './viz-line';
import { VizShout } from './viz-shout';
import { VizPhased } from './viz-phased';
import { NoData } from "./nodata";
import { ImplementationDetail } from './implementation-detail';
import { organizeByZero, fillInMissingSections } from './utils';
import { BeneficiaryStories} from "./beneficiary-stories";
import { FORMATTERS } from './utils';

const TEMPORARY_HIDDEN_SELECTOR = '.tabs-wrapper';

const TAB_MENU_SELECTOR = '.tab-menu';
const TAB_CONTENT_SELECTOR = '.tab-content';
const CONTENT_GRID_SELECTOR = '.thirds-grid';


const PHASE_TABS_SELECTOR = '.phase-tabs';
const PHASE_MENU_SELECTOR = '.phase-menu';
const PHASE_MENU_ITEM_SELECTOR = '.phase-tab';
const PHASE_CONTENT_SELECTOR = '.phase-content';
const PHASE_CONTENT_PANE_SELECTOR = '.phase-pane';
const SELECTED_PHASE_MENU_ITEM_CLASS = 'w--current';
const SELECTED_PHASE_PANE_CLASS = 'w--tab-active';

const $thirdsGrid = $(CONTENT_GRID_SELECTOR).first().clone(true, true);

const $phaseTabsTemplate = $(PHASE_TABS_SELECTOR).first().clone(true, true);
const $phaseMenuTemplate = $(PHASE_MENU_SELECTOR).first().clone(true, true);
const $phaseMenuItemTemplate = $(PHASE_MENU_ITEM_SELECTOR).first().clone(true, true);
const $phaseContentTemplate = $(PHASE_CONTENT_SELECTOR).first().clone(true, true);
const $phaseContentPaneTemplate = $(PHASE_CONTENT_PANE_SELECTOR).first().clone(true, true);

const $performanceCtaTemplate = $('.is--performance-cta').first().clone(true, true);


$(TAB_MENU_SELECTOR).empty();
$(TAB_CONTENT_SELECTOR).empty();
$(CONTENT_GRID_SELECTOR).empty();


Promise.all([
  d3.json('data/all_data_work.json'),
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

    const tab = new Tab(
      TAB_MENU_SELECTOR,
      TAB_CONTENT_SELECTOR,
      tabData.name,
      () => tabs.select(i),
      tabData.name == 'Programme overview' ? 'overview' : 'department',
      tabData.name == 'Programme overview' ? 0 : tabData.phases.length

    );

    tabs.add(tab);
    
    const months_text = lookups["time"][tabData.month];
    
    new Header(tab.$container, tabData.name, tabData.lead, tabData.paragraph, months_text, tabData.phases == undefined ? 0 : tabData.phases.length);
    
    new BeneficiaryStories(tab.$container, beneficiaries);
    

    // THIS IS GOING TO BE MESSY!!
    // WILL ABSTRACT LATER
 

    // PHASES

    const phasesArr = tabData.phases || [];

    // DEPARTMENTS PHASES


    if(tab.tabType != 'overview') {

      let $phaseTabs = $phaseTabsTemplate.clone(true, true);
      $phaseTabs.empty();

      let $phaseMenu = $phaseMenuTemplate.clone(true, true);
      $phaseMenu.empty();

      let $phaseContent = $phaseContentTemplate.clone(true, true);
      $phaseContent.empty();

      phasesArr.forEach((phase,i) => {
        let $phaseMenuItem = $phaseMenuItemTemplate.clone(true, true);
        $phaseMenuItem.attr('data-w-tab','Phase ' + (i+1));

        $phaseMenuItem.find('.phase-tab__text').text('Phase ' + (i+1));

        $phaseMenuItem.removeClass(SELECTED_PHASE_MENU_ITEM_CLASS);

        if(i == phasesArr.length-1) {
          $phaseMenuItem.addClass(SELECTED_PHASE_MENU_ITEM_CLASS);
        }

        $phaseMenu.append($phaseMenuItem);

      })

      $phaseTabs.append($phaseMenu);

      // PHASES CONTENT

      phasesArr.forEach((phase,i) => {

        let $phaseContentPane = $phaseContentPaneTemplate.clone(true, true);
        $phaseContentPane.attr('data-w-tab','Phase ' + (i+1));

        $phaseContentPane.empty();

        // PANEL CONTENT HERE

        const sectionDataArr = phase.sections || [];
        sectionDataArr.forEach((sectionData, sectionIndex) => {

          if (sectionData.metrics.length !== 0) {
            
            const section = new Section($phaseContentPane, sectionData.name, '', '', sectionData.section_type);
            const sectionType = sectionData.section_type;
            const subSectionDataArr = organizeByZero(sectionData.metrics || []);

            subSectionDataArr.forEach((subSectionData) => {


              const subSection = new SubSection(section.$container);

              new VizShout(
                lookups,
                subSection.$container,
                sectionType,
                subSectionData.metric_type,
                subSectionData.name,
                subSectionData.value,
                subSectionData.value_target,
                sectionType == 'targets' ? true : false,
                sectionType == 'targets' ? false : true,
              );

              new Metric(
                  subSection.$container,
                  subSectionData.name,
                  sectionType,
                  subSectionData.metric_type,
                  subSectionData.value,
                  subSectionData.value_target, tabData.sheet_name
              );

              const has_vets = tabData.sheet_name === "DALRRD" && sectionType === "livelihoods";

              const dimensions = ((sectionType === "targets" || sectionType === "overview") ? subSectionData.dimensions : fillInMissingSections(subSectionData.dimensions, has_vets));
              dimensions.forEach((dimension) => {

                if (dimension.data_missing) {
                  new VizHeading(subSection.$container, metric_titles[sectionType][subSectionData.metric_type + '_' + dimension.lookup] + ' : NO DATA AVAILABLE');
                } else {
                  const hideHeading = sectionType === 'overview' & subSectionData.metric_type === 'targets_count';
                  new VizHeading(subSection.$container, dimension.name, hideHeading);
                  if (dimension.viz === 'line') {
                    new VizLine(subSection.$container, dimension.values, lookups[dimension.lookup], (i+1));
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
                        (i+1)
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

          if(i == 1 && sectionIndex == 0) {

            
            let $performanceCta = $performanceCtaTemplate.clone(true,true);


            $phaseContentPane.append($performanceCta);
          }
        
        });
        
       

        if (typeof phase.implementation_details !== 'undefined' && phase.implementation_details.length > 0) {
          
          new Section($phaseContentPane, 'Implementation status reports', '', '', '');
          
          phase.implementation_details.forEach((implData) => {
          
            const $implGrid = $thirdsGrid.clone(true, true);

            $implGrid.find('.loading').hide();
            $phaseContentPane.append($implGrid);
    
            new ImplementationDetail(
                $implGrid,
                implData.programme_name,
                implData.status,
                implData.detail,
                true
            );
          });
        }

        $phaseContentPane.removeClass(SELECTED_PHASE_PANE_CLASS);

        if(i == phasesArr.length-1) {
          $phaseContentPane.addClass(SELECTED_PHASE_PANE_CLASS);
        }

        $phaseContent.append($phaseContentPane);

      })

      // END PHASES CONTENT


      $phaseTabs.append($phaseContent);

      tab.$container.append($phaseTabs);
      
      
    } else {

      // OVERVIEW PAGE HERE

      const sectionDataArr = tabData.sections || [];
        sectionDataArr.forEach((sectionData) => {

          if (sectionData.metrics.length !== 0) {
            
            const section = new Section(tab.$container, sectionData.name, '', '', sectionData.section_type, true, tabData);

            const sectionType = sectionData.section_type;
            const subSectionDataArr = organizeByZero(sectionData.metrics || []);

            subSectionDataArr.forEach((subSectionData) => {

              const subSection = new SubSection(section.$container);

              new VizPhased(
                lookups,
                subSection.$container,
                sectionType,
                subSectionData.viz_type,
                subSectionData.metric_type,
                subSectionData.name,
                subSectionData.value,
                subSectionData.value_target,
                subSectionData.phases
              );

              new Metric(
                  subSection.$container,
                  subSectionData.name,
                  sectionType,
                  subSectionData.metric_type,
                  subSectionData.value,
                  subSectionData.value_target, tabData.sheet_name
              );

              const has_vets = tabData.sheet_name === "DALRRD" && sectionType === "livelihoods";

              const dimensions = ((sectionType === "targets" || sectionType === "overview") ? subSectionData.dimensions : fillInMissingSections(subSectionData.dimensions, has_vets));
              dimensions.forEach((dimension) => {

                if (dimension.data_missing) {
                  new VizHeading(subSection.$container, metric_titles[sectionType][subSectionData.metric_type + '_' + dimension.lookup] + ' : NO DATA AVAILABLE');
                } else {
                  const hideHeading = sectionType === 'overview' & subSectionData.metric_type === 'targets_count';
                  new VizHeading(subSection.$container, dimension.name, hideHeading);
                  if (dimension.viz === 'line') {
                    new VizLine(subSection.$container, dimension.values, lookups[dimension.lookup], (i+1));
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
                        (i+1)
                    );
                  }
                }

              });

              // if (subSectionData.implementation_detail) {
              //   const implData = subSectionData.implementation_detail;
              //   new ImplementationDetail(
              //       subSection.$container,
              //       implData.programme_name,
              //       implData.status,
              //       implData.detail,
              //       false,
              //   );
              // }

            });


          }
        
        });




    }


    

    




   

       

    if (typeof tabData.footer_header !== 'undefined' && tabData.footer_header) {
      new Footer(tab.$container, '', tabData.footer_header, tabData.footer_paragraph);
    }
  });

  // Webflow.require('ix2').init();
  tabs.select(0);

  // PHASE TABS SELECT

  $(PHASE_MENU_ITEM_SELECTOR).on('click', function() {
    
    let tab = $(this).attr('data-w-tab');
    let tabs_menu = $(this).parent();
    let tabs_content = $(this).parent().parent();

    $(tabs_menu).find(PHASE_MENU_ITEM_SELECTOR).removeClass(SELECTED_PHASE_MENU_ITEM_CLASS);
    $(this).addClass(SELECTED_PHASE_MENU_ITEM_CLASS);
    $(tabs_content).find(PHASE_CONTENT_SELECTOR + ' ' + PHASE_CONTENT_PANE_SELECTOR).removeClass(SELECTED_PHASE_PANE_CLASS);
    $(tabs_content).find(PHASE_CONTENT_PANE_SELECTOR + '[data-w-tab="' + tab + '"]').addClass(SELECTED_PHASE_PANE_CLASS);

  })

  $(TEMPORARY_HIDDEN_SELECTOR).show();
});