import $ from 'jquery';
import { FORMATTERS } from './utils';

const SELECTOR = '.feature-value__youth';

const $template = $(SELECTOR).first().clone(true, true);

export class VizValue {
  constructor($parent, type, value, total) {
    this._$parent = $parent;
    this._type = type;
    this._value = value;
    this._total = total;
    this.render();
  }

  render() {
    const $el = $template.clone(true, true);
    const quotient = this._value / this._total;
    $el.text(
      `${FORMATTERS[this._type](this._value)} (${FORMATTERS.percentage(quotient)})`,
    );
    this._$parent.append($el);
  }
}
