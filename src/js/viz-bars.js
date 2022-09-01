import $ from 'jquery';
import { FORMATTERS } from './utils';
import { isObject } from './utils';


const CONTAINER_SELECTOR = '.components .feature-value__bar-chart';
const ROW_SELECTOR_NO_TARGET = '.components .bar-chart__row:not(.bar-chart__row--with-target)';
const ROW_SELECTOR_WITH_TARGET = '.components .bar-chart__row.bar-chart__row--with-target';
const ROW_INNER_SELECTOR = '.bar-chart__row_inner';

const BAR_SELECTOR = '.bar-chart__row_bar';
const BAR_SELECTOR_PHASED = '.bar-chart__row_bar.is--phase-2';
const BAR_TARGET_SELECTOR = '.bar-chart__row_target';
const BAR_TOOLTIP_SELECTOR = '.bar-chart__row_tooltip';
const BAR_TARGET_TOOLTIP_SELECTOR = '.bar-chart__row_target-tooltip';
const BAR_CAT_LABEL_SELECTOR = '.bar-chart__row_label';
const BAR_VAL_LABEL_SELECTOR = '.bar-chart__row_value';

const $containerTemplate = $(CONTAINER_SELECTOR).first().clone(true, true).empty();
const $rowTemplateNoTarget = $(ROW_SELECTOR_NO_TARGET).first().clone(true, true);
const $rowTemplateWithTarget = $(ROW_SELECTOR_WITH_TARGET).first().clone(true, true);

export class VizBars {
  constructor($parent, rows, lookup, hideZeros, phase) {
    this._$parent = $parent;
    this._rows = rows;
    this._lookup = lookup;

    const maxValue = this._rows
      .map((row) => row.value)
      .reduce((max, curr) => Math.max(max, curr), 0);
    
    const maxTarget = this._rows
    .map((row) => (row.value_target ? row.value_target : 0))
    .reduce((max, curr) => Math.max(max, curr), 0);
  
    this._max = Math.max(maxValue, maxTarget);

    this._hideZeros = hideZeros;
    this._phase = phase;
    this.render();
  }

  render() {

    const $el = $containerTemplate.clone(true, true);

    let allValues = [];

    this._rows.forEach((row) => {

      if(isObject(row.value)) {

        let valueSum = 0;

        for (const key in row.value) {

          
          
          valueSum = valueSum + row.value[key];
         
        }

        allValues.push(valueSum);

      } else {
        if(Array.isArray(row.value)) {
          allValues.push(row.value[0]);
        }
      }

    })


    this._rows.forEach((row) => {

      

      if (!this._hideZeros || (this._hideZeros && row.value_target !== 0 )) {

        let width = [];
        let valueText = 0;
        
        if(isObject(row.value)) {

          let maxValue = allValues
            .map((row) => row)
            .reduce((max, curr) => Math.max(max, curr), 0);


            for (const key in row.value) {
              width.push(Math.round((row.value[key] / maxValue) * 100));
              valueText = valueText + row.value[key];
            }  

          // row.values.forEach((point) => {
          //   width.push(Math.round((point.value / maxValue) * 100));
          //   valueText = valueText + point.value;
          // })

        } else {
          
          if(Array.isArray(row.value)) {

            let maxValue = allValues
            .reduce((max, curr) => Math.max(max, curr), 0);


            for (let index = 0; index < row.value.length; index++) {
              width.push(Math.round((row.value[index] / maxValue) * 100));
              valueText = valueText + row.value[index];
            }

            

          } else {
            width.push(Math.round((row.value / this._max) * 100));
            valueText = row.value;
          }
          
        }
        
        const $row = $rowTemplateNoTarget.clone(true, true);
        
        if(isObject(row.value)) {

          $row.find(BAR_SELECTOR).width(`${width[0]}%`).css('background-color','#666').css('border-radius',0);
          
          let $phase2Bar = $row.find(BAR_SELECTOR_PHASED).clone(true,true);
          
          $phase2Bar.width(`${width[1]}%`).css('left','-3px').css('background-color','#666').css('border-radius',0);
          
          $row.find(BAR_SELECTOR_PHASED).width('100%');

          $phase2Bar.insertBefore($row.find(BAR_VAL_LABEL_SELECTOR));


        } else {

          

            if(this._phase == 1) {

              $row.find(BAR_SELECTOR).not(BAR_SELECTOR_PHASED).css('background-color','transparent');
              $row.find(BAR_SELECTOR).width(`${width[0]}%`);
              $row.find(BAR_SELECTOR_PHASED).width('100%');

            } else if (this._phase == 0) {

              $row.find(BAR_SELECTOR_PHASED).remove();
              $row.find(BAR_SELECTOR).width(`${width[0]}%`);
            
            } else {
              $row.find(BAR_SELECTOR).width(`${width[0]}%`);
            }

        }
        
        const $label = $row.find(BAR_CAT_LABEL_SELECTOR).text(row.key.toUpperCase());
        const $tooltip = $row.find(BAR_TOOLTIP_SELECTOR).text(this._lookup[row.key]);

        $label
          .on('mouseover', () => $tooltip.show())
          .on('mouseout', () => $tooltip.hide());

        $row.find(BAR_VAL_LABEL_SELECTOR).text(FORMATTERS.count(valueText));

        $el.append($row);

      }
    });

    this._$parent.append($el);
  }
}
