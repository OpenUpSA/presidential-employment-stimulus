import $ from 'jquery';
import { FORMATTERS } from './utils';
import { isObject } from './utils';


// const CONTAINER_SELECTOR = '.components .feature-value__bar-chart';
// const ROW_SELECTOR_NO_TARGET = '.components .bar-chart__row:not(.bar-chart__row--with-target)';
// const ROW_SELECTOR_WITH_TARGET = '.components .bar-chart__row.bar-chart__row--with-target';
// const ROW_INNER_SELECTOR = '.bar-chart__row_inner';

// const BAR_SELECTOR = '.bar-chart__row_bar';
// const BAR_SELECTOR_PHASED = '.bar-chart__row_bar.is--phase-2';
// const BAR_TARGET_SELECTOR = '.bar-chart__row_target';
// const BAR_TOOLTIP_SELECTOR = '.bar-chart__row_tooltip';
// const BAR_TARGET_TOOLTIP_SELECTOR = '.bar-chart__row_target-tooltip';
// const BAR_CAT_LABEL_SELECTOR = '.bar-chart__row_label';
// const BAR_VAL_LABEL_SELECTOR = '.bar-chart__row_value';
// const BAR_VALUE_TOOLTIP = '.bar-value__wrapper';

// const $containerTemplate = $(CONTAINER_SELECTOR).first().clone(true, true).empty();
// const $rowTemplateNoTarget = $(ROW_SELECTOR_NO_TARGET).first().clone(true, true);
// const $rowTemplateWithTarget = $(ROW_SELECTOR_WITH_TARGET).first().clone(true, true);

const BARCHART_CONTAINER = '.components .bar-chart__row';

const $barchartContainer = $('.components .bar-chart__row').not('.bar-chart__row--with-target').first().clone(true, true);

export class VizBars {
  constructor($parent, rows, lookup, hideZeros, phase) {
    this._$parent = $parent;
    this._rows = rows;
    this._lookup = lookup;
    this._hideZeros = hideZeros;
    this._phase = phase;
    this.render();
  }

  render() {

    let maxValue = 0;

    for (let row = 0; row < this._rows.length; row++) {
      
      let value;

      if(typeof(this._rows[row].value) === 'number') {
        value = this._rows[row].value;
      } else {
        let value0 = this._rows[row].value[0] ? this._rows[row].value[0] : 0;
        let value1 = this._rows[row].value[1] ? this._rows[row].value[1] : 0;
        value = value0 + value1;
      }
      if (value > maxValue) {
        maxValue = value;
      }
    }


    for (let row = 0; row < this._rows.length; row++) {

      let $el = $barchartContainer.clone(true, true);

      // This is for departments on the Overview Page
      if("DALRRD" in this._lookup) {

        let value0 = this._rows[row].value[0] ? this._rows[row].value[0] : 0;
        let value1 = this._rows[row].value[1] ? this._rows[row].value[1] : 0;

        $el.find('.bar-chart__row_label').text(this._rows[row].key).css('text-transform', 'uppercase');
        $el.find('.bar-chart__row_bar').css('background-color','#666');
        $el.find('.bar-chart__row_bar.is--phase-2').css('background-color','transparent'); // Hide Phase 2 bar

        let summedValues = value0 + value1;

        $el.find('.bar-chart__row_value.small').text(FORMATTERS.count(summedValues));

        $el.find('.bar-chart__row_bar').width((summedValues / maxValue) * 100 + '%');

      } else if(typeof(this._rows[row].value) === 'number') {

        // This is for provinces, but single value phase bars.

        $el.find('.bar-chart__row_label').text(this._rows[row].key).css('text-transform', 'uppercase');
        $el.find('.bar-chart__row_value.small').text(FORMATTERS.count(this._rows[row].value));
        $el.find('.bar-chart__row_bar').width((this._rows[row].value / maxValue) * 100 + '%');
        if(this._phase == 0) {
          $el.find('.bar-chart__row_bar.is--phase-1').css('background-color','transparent'); // Hide Phase 2 bar
        } else {
          $el.find('.bar-chart__row_bar.is--phase-1').width('100%'); // Hide Phase 2 bar
          $el.find('.bar-chart__row_bar').not('.bar-chart__row_bar.is--phase-1').css('background-color','transparent'); // Hide Phase 2 bar
        }

      } else {

        // This is for provinces

        let value1 = this._rows[row].value[0] ? this._rows[row].value[0] : 0;
        let value0 = this._rows[row].value[1] ? this._rows[row].value[1] : 0;

        $el.find('.bar-chart__row_label').text(this._rows[row].key).css('text-transform', 'uppercase');

        $el.find('.bar-chart__row_value.small').text(FORMATTERS.count(value0 + value1));

        $el.find('.bar-chart__row_bar').width(((value0 + value1) / maxValue) * 100 + '%');
        $el.find('.bar-chart__row_bar.is--phase-1').width((value1 / (value0 + value1)) * 100 + '%');

      }

      // LABEL TOOLTIP

      $el.find('.bar-chart__row_tooltip').text(this._lookup[this._rows[row].key])

      $el.find('.bar-chart__row_label').on('mouseover', () => 
        $el.find('.bar-chart__row_tooltip').show()
      ).on('mouseout', () => 
        $el.find('.bar-chart__row_tooltip').hide()
      );

      // VALUE TOOLTIP

      if(!("DALRRD" in this._lookup) && typeof(this._rows[row].value) != 'number') { // Don't show tooltip for departments
        $el.find('.bar-value__wrapper .bar-value').text(FORMATTERS.count(this._rows[row].value[0]) + ' | ' + FORMATTERS.count(this._rows[row].value[1]))

        $el.find('.bar-chart__row_bar').on('mouseover', () =>
          $el.find('.bar-value__wrapper').show().css('opacity', 1)
        ).on('mouseout', () => 
          $el.find('.bar-value__wrapper').hide().css('opacity', 0)
        );
      }




      this._$parent.append($el);


    }


  }
}
