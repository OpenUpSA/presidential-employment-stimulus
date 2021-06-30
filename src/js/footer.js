import $ from 'jquery';

const SELECTOR = '.tab-pane .tab-header';
const TITLE_SELECTOR = '.tab-title';

const $template = $(SELECTOR).first().clone(true, true);

export class Footer {
    constructor($parent, title, lead, paragraph, months_text) {
        this._$parent = $parent;
        this._title = title;
        this._lead = lead;
        this._paragraph = paragraph;
        this.render();
    }

    render() {
        const $el = $template.clone(true, true);
        $el.find('.header__label').text('');
        $el.find(TITLE_SELECTOR).text(this._title);
        $el.find('h3').text(this._lead);
        $el.find('p').text(this._paragraph);
        $el.find('.button-wrap').empty();
        this._$parent.append($el);
    }
}
