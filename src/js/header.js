import $ from 'jquery';

const SELECTOR = '.tab-pane .tab-header';

const $template = $(SELECTOR).first().clone(true, true);

export class Header {
  constructor($parent, title, lead, paragraph) {
    this._$parent = $parent;
    this._title = title;
    this._lead = lead;
    this._paragraph = paragraph;
    this.render();
  }

  render() {
    const $el = $template.clone(true, true);
    $el.find('h2').text(this._title);
    $el.find('h3').text(this._lead);
    $el.find('p').text(this._paragraph);
    this._$parent.append($el);
  }
}