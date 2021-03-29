import $ from 'jquery';
import { FORMATTERS } from './utils';
import { VizProgress } from './viz-progress';

const ICON_SELECTORS = {
    livelihoods: '.icon.icon--support',
    job_opportunities: '.icon.icon--jobs-created',
    jobs_retain: '.icon.icon--jobs-retained',
    targets: '.icon.icon--budget',
    budget_allocated: '.icon.icon--budget',
};
const icons = Object.keys(ICON_SELECTORS).reduce((obj, key) => ({
    ...obj,
    [key]: $(ICON_SELECTORS[key]).clone(true, true),
}), {});

const CONTAINER_SELECTOR = '.components .feature-value__inner';
const NAME_SELECTOR = '.feature-value__label';
const ICON_CONTAINER_SELECTOR = '.feature-value__header_icon-wrapper';
const VALUE_SELECTOR = '.feature-value__amount';
const SUB_VALUE_SELECTOR = '.feautre-value__sub-amount';

const PROGRESS_CLASS = 'feature-value__header_chart-wrapper';

const $containerTemplate = $(CONTAINER_SELECTOR).first().clone(true, true);

const statusText = {
    OnTrack: 'On Track',
    MinorChallenges: 'Minor Challenges',
    CriticalChallenges: 'Critical Challenges'
}
export class ImplementationDetail {
    constructor($parent, title, status, detail) {
        this._$parent = $parent;
        this._title = title;
        this._status = status;
        this._detail = detail;
        this.render();
    }

    get $el() {
        return this._$el;
    }

    render() {
        this._$el = $containerTemplate.clone(true, true);
        this._$parent.append(this._$el);
        const $subValue = this._$el.find(SUB_VALUE_SELECTOR);
        $subValue.text(this._detail);
        this._$el.find(VALUE_SELECTOR).text(statusText[this._status]);

        // $subValue.remove();
        const $chartWrapper = this._$el.find(`.${PROGRESS_CLASS}`);
        $chartWrapper.remove();
        this._$el.find(NAME_SELECTOR).text(this._title);
        this._$el.find('img').remove();
    }
}
