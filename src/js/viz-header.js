import $ from 'jquery';
import { FORMATTERS } from './utils';
import { VizProgress } from './viz-progress';


const ICONS_SELECTOR = '.icons';
const $iconsTemplate = $(ICONS_SELECTOR).first().clone(true, true);

export class VizHeader {
  constructor(lookups, $parent, section_type, metric_type, title, value, target_value, show_progress, hide_values, phase) {
    this._lookups = lookups;
    this._$parent = $parent;
    this._section_type = section_type;
    this._metric_type = metric_type;
    this._title = title;
    this._value = value;
    this._target_value = target_value;
    this._show_progress = show_progress;
    this._hide_values = hide_values;
    this._phase = phase;

    this.render();

    }

    render() {


        let $featureBlock = $('.feature-value').first().clone(true, true);

        let $featureValue = $featureBlock.find('.feature-value__header').not('.feature-value__header.is--phased');

        // if(this._metric_type == 'count') {
        //     $featureValue = $featureBlock.find('.feature-value__header.is--phased .phased-header');
        // }

        $featureBlock.empty();

        $featureValue.find('.feature-value__label').text(this._title);

        // TOTAL FOR SUB-PROGRAMME
        // if(this._metric_type == 'count') {
        //     $featureValue.find('.phased-header__title').text(this._title);
        // }

        if(!this._hide_values) {
        
            let formatter = FORMATTERS[this._metric_type];

            if(this._value == -1) {
                $featureValue.find('.feature-value__amount').text(formatter(this._target_value));
                if(this._target_value == 0) {
                    $featureValue.find('.feature-value__value-description').text('Carried over from prior year');
                }
            } else {
                $featureValue.find('.feature-value__amount').text(formatter(this._value));

                if(this._target_value == 0) {
                    $featureValue.find('.feature-value__value-description').text('TARGET: ' + formatter(this._target_value) + ' (Carried over from prior year)');
                } else if(this._target_value != -1) {
                    $featureValue.find('.feature-value__value-description').text('TARGET: ' + formatter(this._target_value));
                }
            }

        } else {
            
            // TOTAL FOR SUB-PROGRAMME
            if(this._metric_type == 'count') {
                let formatter = FORMATTERS[this._metric_type];
                $featureValue.find('.feature-value__amount').text(formatter(this._value));
                if(this._target_value != -1 && this._target_value != 0) {
                    $featureValue.find('.feature-value__value-description').text('TARGET: ' + formatter(this._target_value));
                }
            } else {
                $featureValue.find('.feature-value__amount').hide();
                $featureValue.find('.feature-value__value-description').hide();
            }
            
            
        }

        // TOTAL FOR SUB-PROGRAMME
        // if(this._metric_type == 'count') {
        //     let formatter = FORMATTERS[this._metric_type];
        //     $featureValue.find('.phased-header__value').text(formatter(this._value));
        // }

        

        // ICON

        let $icons = $iconsTemplate.clone(true, true);

        let $iconWrapper = $featureValue.find('.feature-value__header_icon-wrapper');

        // if(this._metric_type == 'count') {
        //     $iconWrapper = $featureValue.find('.phased-header__icon');
        // }
        
        $iconWrapper.empty();

        if(this._section_type == 'targets') {
            this._section_type = this._title;
        }

        $iconWrapper.append($icons.find('.icon--' + this._lookups["icon"][this._section_type]));


        // DONUT ?

        

        if(this._show_progress && !isNaN(this._value / this._target_value)) {

            if(this._target_value == 0) {
                $featureValue.find('.feature-value__header_chart-wrapper').hide();
            } else {
                let $progressContainer = $featureValue.find('.feature-value__header_chart-wrapper');
                $progressContainer.empty();

                if (this._metric_type == 'currency') {
                    $progressContainer.remove();
                } else {

                    new VizProgress(
                        $progressContainer[0],
                        this._value / this._target_value,
                        this._phase
                    );
                    
                } 
            }
        } else {
            $featureValue.find('.feature-value__header_chart-wrapper').hide();
        }

        $featureBlock.append($featureValue);
        

        this._$parent.append($featureBlock.html());
    }
}
