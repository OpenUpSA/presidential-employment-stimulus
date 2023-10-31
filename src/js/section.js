import $ from 'jquery';

const HEADER_SELECTOR = '.tab-inner .header';
const SUBHEADER_SELECTOR = '.tab-inner .header.is--v2';
const CONTENT_GRID_SELECTOR = '.tab-inner .half-grid';

const $headerTemplate = $(HEADER_SELECTOR).first().clone(true, true);
const $subHeaderTemplate = $(SUBHEADER_SELECTOR).first().clone(true, true);
const $contentGridTemplate = $(CONTENT_GRID_SELECTOR).first().clone(true, true);
const $overviewHeaderTemplate = $('.header.is--legend').first().clone(true,true);

export class Section {
  constructor(lookups, $parent, title, lead, paragraph, section_type, phase_legend, tabData) {
    this._lookups = lookups;
    this._$parent = $parent;
    this._title = title;
    this._lead = lead;
    this._paragraph = paragraph;
    this._type = section_type;
    this._phase_legend = phase_legend;
    this._tab_data = tabData
    this.render();
  }

  get $container() {
    return this._$container;
  }

  render() {

    let $header = $headerTemplate.clone(true, true);
    const $subHeader = $subHeaderTemplate.clone(true, true);


    if(this._phase_legend) {
      $header = $overviewHeaderTemplate.clone(true,true);
      // $header.find('.phase-legend__date').text("Up to Mar '23");
      // $header.find('.phase-legend__date').first().text("Up to Mar '22");
      $header.css('margin-top', 0);
    }

    $header.find('.header__label').text(''); // TODO Put this back if needed (e.g. "Dec '20 - Jan '21")

    $header.find('h3').text(this._title);

    if (this._lead) {
      $header.find('h4').text(this._lead);
    }
    if (this._paragraph) {
      $header.find('p').text(this._paragraph);
    }

    if(this._type == 'targets') {
      $subHeader.find('.tab-h4').text('Overall Achievements');
    } else if(this._title == 'Programme Achievements') {
      $subHeader.find('.tab-h4').text('Overall Achievements');
    } else {
      $header.hide();
      $subHeader.find('.tab-h4').text(this._title);
    }

    this._$container = $contentGridTemplate.clone(true, true);

    const $el = $('<div></div>');

    $el.append(
      $header,
      $subHeader,
      this._$container,
    );


    this._$container.empty();
    this._$parent.append($el);
  }
}
