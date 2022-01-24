import $ from 'jquery';
import { FORMATTERS } from './utils';
import { VizProgress } from './viz-progress';

const ICONS_SELECTOR = '.icons';
const $iconsTemplate = $(ICONS_SELECTOR).first().clone(true, true);

export class VizPhased {
  constructor(lookups, $parent, section_type, viz_type, metric_type, title, value, value_target, phases) {
    this._lookups = lookups;
    this._$parent = $parent;
    this._section_type = section_type;
    this._viz_type = viz_type;
    this._metric_type = metric_type;
    this._title = title;
    this._value = value;
    this._value_target = value_target;
    this._phases = phases;
   

    this.render();

    }

    render() {

        let $featureBlock = $('.feature-value').first().clone(true, true);
        let $phasedHeader = $featureBlock.find('.feature-value__header.is--phased');

        $featureBlock.empty();

        $phasedHeader.find('.phased-header__title').text(this._title);
        
        let formatter = FORMATTERS[this._metric_type];

        $phasedHeader.find('.phased-header__value').text(formatter(this._value));


        if(this._viz_type == 'percentile') {

            $phasedHeader.find('.indicator-phase').not('.indicator-phase:last-child').hide();

            for (let index = 0; index < this._phases.length; index++) {
            
                let $phaseContent = $phasedHeader.find('.feature-value__phase_content:nth-child(' + (index + 1) + ')');
                $phaseContent.find('.feature-value__phase-label').text('Phase ' + (index + 1));

                let $progressContainer = $phaseContent.find('.feature-value__phase_chart-wrapper');
                $progressContainer.empty();

                new VizProgress(
                    $progressContainer[0],
                    this._phases[index].value / this._phases[index].value_target,
                    (index+1)
                );
                
            }

        } else {

            $phasedHeader.find('.indicator-phase:last-child').hide();            

            if(this._phases != undefined) {

                
                for (let index = 0; index <= this._phases.length; index++) {

                    let $indicatorPhase = $phasedHeader.find('.indicator-phase:nth-child(' + (index + 1) + ')');

                    $indicatorPhase.find('.feature-value__amount').text(formatter(this._value));

                    $indicatorPhase.find('.feature-value__value-description').text(formatter(this._value_target));
                    
                    let $progressContainer = $indicatorPhase.find('.feature-value__header_chart-wrapper');
                    $progressContainer.empty();

                    new VizProgress(
                        $progressContainer[0],
                        this._value / this._value_target,
                        (index)
                    );

                   



                    
                }

            }




        }


        // ICON

        let $icons = $iconsTemplate.clone(true, true);

        let $iconWrapper = $phasedHeader.find('.phased-header__icon');
        
        $iconWrapper.empty();

        if(this._section_type == 'targets' || this._section_type == 'overview') {
            this._section_type = this._title;
        }

        $iconWrapper.append($icons.find('.icon--' + this._lookups["icon"][this._section_type]));


        


    

        this._$parent.append($phasedHeader.html());
    }
}
