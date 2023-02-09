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

    if (this._active) {
      $phaseStatus.find('.phase-marker').addClass('is--phase-2');
      $phaseStatus.find('.phase-status__text').text('Currently Participating');
      $el.find('.tab-title__wrapper').append($phaseStatus);
    }

    $el.find('.header__label').text(month_text);
    $el.find(TITLE_SELECTOR).text(this._title);
    $el.find('h3').text(this._lead);
    $el.find('p.header-description').text(this._paragraph);
    
    $el.find('.button-wrap').html('<select><option value="" disabled selected hidden>More about the programme</option><option value="img/Presidential Employment Stimulus Launch October 2020.pdf">Launch October 2020</option><option value="img/Phase 2 Launch 2021.pdf">Phase 2 Launch 2021</option><option value="img/Presidential Employment Stimulus Update February 2023.pdf">February 2023 Update</option></select>');




    // $el.find('.button-wrap a:first-child').attr('href','/img/Presidential Employment Stimulus Review and Introduction to Phase 2.pdf');
    // $el.find('.button-wrap a[href="#"]').attr('href','/img/PES Implementation Update January 2022 final.pdf').removeClass('button--secondary');

    this._$parent.append($el);

    $('.button-wrap select').on('change', function () {
      window.open($(this).val(), '_blank');
      $(this).val('');
    });
  }
}
