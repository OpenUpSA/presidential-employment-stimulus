import $ from 'jquery';
import { FORMATTERS } from './utils';

const SELECTOR = '.feature-value__number-percent';

const $template = $(SELECTOR).first().clone(true, true);

export class VizValue {
  constructor($parent, type, quotient) {
    this._$parent = $parent;
    this._type = type;
    this._quotient = quotient;
    this._formatter = FORMATTERS[this._type];
    this.render();
  }

  render() {
    const $el = $template.clone(true, true);
    $el.text(
      this._formatter(this._quotient),
    );
    this._$parent.append($el);
  }
}
