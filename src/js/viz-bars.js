import $ from 'jquery';
import { FORMATTERS } from './utils';

const CONTAINER_SELECTOR = '.components .feature-value__bar-chart';
const ROW_SELECTOR_NO_TARGET = '.components .bar-chart__row:not(.bar-chart__row--with-target)';
const ROW_SELECTOR_WITH_TARGET = '.components .bar-chart__row.bar-chart__row--with-target';
const ROW_INNER_SELECTOR = '.bar-chart__row_inner';

const BAR_SELECTOR = '.bar-chart__row_bar';
const BAR_TARGET_SELECTOR = '.bar-chart__row_target';
const BAR_TOOLTIP_SELECTOR = '.bar-chart__row_tooltip';
const BAR_TARGET_TOOLTIP_SELECTOR = '.bar-chart__row_target-tooltip';
const BAR_CAT_LABEL_SELECTOR = '.bar-chart__row_label';
const BAR_VAL_LABEL_SELECTOR = '.bar-chart__row_value';

const $containerTemplate = $(CONTAINER_SELECTOR).first().clone(true, true).empty();
const $rowTemplateNoTarget = $(ROW_SELECTOR_NO_TARGET).first().clone(true, true);
const $rowTemplateWithTarget = $(ROW_SELECTOR_WITH_TARGET).first().clone(true, true);

export class VizBars {
  constructor($parent, rows, lookup, hideZeros) {
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
    this.render();
  }

  render() {
    const $el = $containerTemplate.clone(true, true);
    this._rows.forEach((row) => {
      if (!this._hideZeros || (this._hideZeros && row.value_target !== 0 )) {
        const width = Math.round((row.value / this._max) * 100);
        const target = Math.round((row.value_target / this._max) * 100);
        // NOTE: removed display of target
        // const $row = (row.value_target ? $rowTemplateWithTarget : $rowTemplateNoTarget)
        //   .clone(true, true);
        const $row = $rowTemplateNoTarget.clone(true, true);
        $row.find(BAR_SELECTOR).width(`${width}%`);
        // $row.find(BAR_TARGET_SELECTOR).css('left', `${target}%`);
        // const $targetTooltip = $row.find(BAR_TARGET_TOOLTIP_SELECTOR).text(`TARGET: ${FORMATTERS.count(row.value_target)}`);
        // $row.find(ROW_INNER_SELECTOR)
        //     .on('mouseover', () => $targetTooltip.show() )
        //     .on('mouseout', () => $targetTooltip.hide() );
        const $label = $row.find(BAR_CAT_LABEL_SELECTOR).text(row.key.toUpperCase());
        const $tooltip = $row.find(BAR_TOOLTIP_SELECTOR).text(this._lookup[row.key]);
        $label
            .on('mouseover', () => $tooltip.show())
            .on('mouseout', () => $tooltip.hide());
        $row.find(BAR_VAL_LABEL_SELECTOR).text(FORMATTERS.count(row.value));
        $el.append($row);
      }
    });
    this._$parent.append($el);
  }
}
