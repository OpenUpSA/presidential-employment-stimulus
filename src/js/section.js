import $ from 'jquery';

const HEADER_SELECTOR = '.tab-inner .header';
const CONTENT_GRID_SELECTOR = '.tab-inner .thirds-grid';

const $headerTemplate = $(HEADER_SELECTOR).first().clone(true, true);
const $contentGridTemplate = $(CONTENT_GRID_SELECTOR).first().clone(true, true);

export class Section {
  constructor($parent, title, lead, paragraph) {
    this._$parent = $parent;
    this._title = title;
    this._lead = lead;
    this._paragraph = paragraph;
    this.render();
  }

  get $container() {
    return this._$container;
  }

  render() {
    const $header = $headerTemplate.clone(true, true);
    $header.find('h3').text(this._title);
    if (this._lead) {
      $header.find('h4').text(this._lead);
    }
    if (this._paragraph) {
      $header.find('p').text(this._paragraph);
    }
    this._$container = $contentGridTemplate.clone(true, true);
    const $el = $('<div></div>');
    $el.append(
      $header,
      this._$container,
    );
    this._$container.empty();
    this._$parent.append($el);
  }
}
