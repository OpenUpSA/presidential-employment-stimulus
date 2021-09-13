import $ from 'jquery';

const SELECTOR = '.uppercase-label:not(.hide-mobile)';

const $template = $(SELECTOR).first().clone(true, true);

export class VizHeading {
  constructor($parent, name, hideHeading) {
    this._$parent = $parent;
    if (!hideHeading) {
      this._name = name;
    } else {
      this._name = '';
    }
    this.render();
  }

  render() {
    const $el = $template.clone(true, true).text(this._name);
    this._$parent.append($el);
  }
}
