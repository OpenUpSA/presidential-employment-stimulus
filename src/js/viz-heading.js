import $ from 'jquery';

const SELECTOR = '.uppercase-label';

const $template = $(SELECTOR).first().clone(true, true);

export class VizHeading {
  constructor($parent, name) {
    this._$parent = $parent;
    this._name = name;
    this.render();
  }

  render() {
    const $el = $template.clone(true, true).text(this._name);
    this._$parent.append($el);
  }
}
