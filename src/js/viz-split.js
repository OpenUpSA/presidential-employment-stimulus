import $ from 'jquery';
import { FORMATTERS } from './utils';

const CONTAINER_SELECTOR = '.components .feature-value__split-chart';
const LEFT_SELECTOR = '.demo-bar.left';
const RIGHT_SELECTOR = '.demo-bar.right';

const $template = $(CONTAINER_SELECTOR).first().clone(true, true);

export class VizSplit {
  constructor($parent, type, leftLabel, leftValue, rightLabel, rightValue) {
    this._$parent = $parent;
    this._type = type;
    this._leftLabel = leftLabel;
    this._leftValue = leftValue;
    this._rightLabel = rightLabel;
    this._rightValue = rightValue;
    this.render();
  }

  render() {
    const $el = $template.clone(true, true);
    const leftWidthQuotient = this._leftValue / (this._leftValue + this._rightValue);
    $el.find(LEFT_SELECTOR)
      .text(`${FORMATTERS[this._type](this._leftValue)} ${this._leftLabel}`)
      .width(`${leftWidthQuotient * 100}%`);
    $el.find(RIGHT_SELECTOR)
      .text(`${FORMATTERS[this._type](this._rightValue)} ${this._rightLabel}`);
    this._$parent.append($el);
  }
}
