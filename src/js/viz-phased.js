import { thresholdScott } from 'd3-array';
import $ from 'jquery';
import { FORMATTERS } from './utils';
import { VizProgress } from './viz-progress';

const ICONS_SELECTOR = '.icons';
const $iconsTemplate = $(ICONS_SELECTOR).first().clone(true, true);

const FEATURE_BLOCK_SELECTOR = '.feature-value__header.is--phased';
const PHASED_HEADER_SELECTOR = '.phased-header';
const PHASE1_SELECTOR = '.indicator-phase.is--phase-1'; // TODO - need classes here
const PHASE2_SELECTOR = '.indicator-phase.is--phase-2'; // TODO - need classes here
const PHASED_SPLIT_SELECTOR = '.indicator-phase.is--split-column';
const PHASE1_SPLIT_SELECTOR = '.is--split-column.is--phase-1';
const PHASE2_SPLIT_SELECTOR = '.is--split-column.is--phase-2';

const $featureBlockTemplate = $(FEATURE_BLOCK_SELECTOR).first().clone(true, true);
const $phasedHeaderTemplate = $(PHASED_HEADER_SELECTOR).first().clone(true, true);
const $phase1Template = $(PHASE1_SELECTOR).first().clone(true, true);
const $phase2Template = $(PHASE2_SELECTOR).first().clone(true, true);
const $phasedSplitTemplate = $(PHASED_SPLIT_SELECTOR).first().clone(true, true);
const $phase1SplitTemplate = $(PHASE1_SPLIT_SELECTOR).first().clone(true, true);
const $phase2SplitTemplate = $(PHASE2_SPLIT_SELECTOR).first().clone(true, true);


export class VizPhased {
  constructor(lookups, $parent, section_type, viz, metric_type, title, value, value_target, total_value) {
    this._lookups = lookups;
    this._$parent = $parent;
    this._section_type = section_type;
    this._viz = viz;
    this._metric_type = metric_type;
    this._title = title;
    this._value = value;
    this._value_target = value_target;
    this._total_value = total_value;

    this.render();

    }

    render() {


        let formatter = FORMATTERS[this._metric_type];

        let $featureBlock = $featureBlockTemplate.clone(true, true);
        $featureBlock.empty();

        // HEADER
        
        let $phasedHeader = $phasedHeaderTemplate.clone(true, true);
        $phasedHeader.find('.phased-header__title').text(this._title);
        $phasedHeader.find('.phased-header__value').text(this._total_value ? formatter(this._total_value) : '');

        if($phasedHeader.find('.phased-header__title').text() == 'Total opportunities') {
            $phasedHeader.find('.phased-header__content').attr('style', 'flex-wrap: wrap;');
            $phasedHeader.find('.phased-header__content').append('<div style="flex: 2, order: 3; font-size: 0.9em; color: #666; margin-top: 5px;">1.27m direct beneficiaries - because some worked across both periods</div>');
        } 
        

        // Hack for SONA 2023 - Remove ASAP

        if(this._total_value == 23588178000) {
            $phasedHeader.find('.phased-header__value').text('R32.6 billion'); 
        }

        let $icons = $iconsTemplate.clone(true, true);
        $phasedHeader.find('.phased-header__icon').empty();
        $phasedHeader.find('.phased-header__icon').append($icons.find('.icon--' + this._lookups["icon"][this._title]));

        $featureBlock.append($phasedHeader);

        // PHASES
        
        

        if(this._viz == 'compact') {

         

            let $splitContainer = $phasedSplitTemplate.clone(true, true);
            $splitContainer.empty();

            for (const key in this._value) {

                let $phase = $phase1SplitTemplate.clone(true, true);
    
                if(key == "1") {
                    $phase = $phase2SplitTemplate.clone(true, true);
                }

                let $progressContainer = $phase.find('.feature-value__phase_chart-wrapper');
                $progressContainer.empty();
                
                new VizProgress(
                    $progressContainer[0], 
                    this._value[key],
                    key
                );
    
                $splitContainer.append($phase);
            

            }

            $featureBlock.append($splitContainer);


        } else {

            


            for (const key in this._value) {

                let $phase = $phase1Template.clone(true, true);
    
                if(key == "1") {
                    $phase = $phase2Template.clone(true, true);
                }

                $phase.find('.feature-value__amount').text(formatter(this._value[key]));

                // Hack for SONA 2023 - Remove ASAP

                if(this._value[key] == 10954000000) {
                    $phase.find('.feature-value__amount').text('R11 billion and R9 billion'); 
                }

                if(this._value_target != null) {

                    if(this._value_target[key] != undefined) {
                        $phase.find('.feature-value__value-description').text('Target: ' + formatter(this._value_target[key]));
                    } else {
                        $phase.find('.feature-value__value-description').text('');
                    }

                }

                let $progressContainer = $phase.find('.feature-value__header_chart-wrapper');
                $progressContainer.empty();

                if (this._metric_type == 'currency') {
                    $progressContainer.remove();
                } else {

                    if(this._value_target != null && !isNaN(this._value[key] / this._value_target[key])) {

                        new VizProgress(
                            $progressContainer[0], 
                            this._value[key] / this._value_target[key],
                            key
                        );

                    }
                   
                }
    
                $featureBlock.append($phase);

            }
            
        }

        this._$parent.append($featureBlock);

    }
}
