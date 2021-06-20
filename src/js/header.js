import $ from 'jquery';

const SELECTOR = '.tab-pane .tab-header';
const TITLE_SELECTOR = '.tab-title';

const $template = $(SELECTOR).first().clone(true, true);

export class Header {
  constructor($parent, title, lead, paragraph, months_text) {
    this._$parent = $parent;
    this._title = title;
    this._lead = lead;
    this._paragraph = paragraph;
    this._months_text = months_text;
    this.render();
  }

  render() {
    const $el = $template.clone(true, true);
    const month_text = (this._months_text) ? "Data captured up until " + this._months_text : '';
    $el.find('.header__label').text(month_text);
    $el.find(TITLE_SELECTOR).text(this._title);
    $el.find('h3').text(this._lead);
    $el.find('p').text(this._paragraph);
    this._$parent.append($el);
  }
}
