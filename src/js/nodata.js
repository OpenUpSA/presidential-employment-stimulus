import $ from 'jquery';

const NO_DATA_SELECTOR = '.no-data';
const $noDataTemplate = $(NO_DATA_SELECTOR).clone(true, true);

export class NoData {
    constructor($parent, name) {
        this._$parent = $parent;
        this._name = name;
        this.render();
    }

    render() {
        const $el = $noDataTemplate.clone(true, true);
        $el.text(this._name + ' : NO DATA AVAILABLE');
        this._$parent.append($el);
    }
}
