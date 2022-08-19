import $ from 'jquery';

const SELECTOR = '.tab-pane .tab-header';
const TITLE_SELECTOR = '.tab-title';

const PHASE_STATUS = '.tab-title__wrapper .phase-status';
const $phaseStatusTemplate = $(PHASE_STATUS).first().clone(true, true);

const $template = $(SELECTOR).first().clone(true, true);

export class Header {
  constructor($parent, title, lead, paragraph, months_text, active) {
    this._$parent = $parent;
    this._title = title;
    this._lead = lead;
    this._paragraph = paragraph;
    this._months_text = months_text;
    this._active = active;
    this.render();
  }

  render() {
    const $phaseStatus = $phaseStatusTemplate.clone(true, true);
    const $el = $template.clone(true, true);
    const month_text = (this._months_text) ? "Data captured up until " + this._months_text : '';

    $el.find('.phase-status').remove();
    
    if (this._active > 1) {
      $phaseStatus.find('.phase-marker').addClass('is--phase-2');
      $phaseStatus.find('.phase-status__text').text('Currently Participating');
      $el.find('.tab-title__wrapper').append($phaseStatus);
    }
    
    $el.find('.header__label').text(month_text);
    $el.find(TITLE_SELECTOR).text(this._title);
    $el.find('h3').text(this._lead);
    $el.find('p.header-description').text(this._paragraph);
    $el.find('.button-wrap a:first-child').attr('href','/img/Presidential Employment Stimulus Review and Introduction to Phase 2.pdf');
    $el.find('.button-wrap a[href="#"]').attr('href','/img/PES Implementation Update January 2022 final.pdf').removeClass('button--secondary');
    
    this._$parent.append($el);
  }
}
