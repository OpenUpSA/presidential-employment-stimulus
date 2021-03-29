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

const CONTAINER_SELECTOR = '.block.status-update';
const NAME_SELECTOR = '.feature-value__label';
const ICON_CONTAINER_SELECTOR = '.feature-value__header_icon-wrapper';
// const VALUE_SELECTOR = '.feature-value__amount';
const STATUS_SELECTOR = '.feature-value__amount';
const LATEST_UPDATE_SELECTOR = '.uppercase-label.uppercase-label--border-top';
const DETAIL_SELECTOR = '.status-update.w-richtext';
const PROGRESS_CLASS = 'feature-value__header_chart-wrapper';
const GREEN_STATUS_SELECTOR = '.feature-value__amount.feature-value__amount--green';
const YELLOW_STATUS_SELECTOR = '.feature-value__amount.feature-value__amount--yellow';
const RED_STATUS_SELECTOR = '.feature-value__amount.feature-value__amount--red';

const $containerTemplate = $(CONTAINER_SELECTOR).first().clone(true, true);

const $greenStatus = $(GREEN_STATUS_SELECTOR).first().clone(true, true);
const $redStatus = $(RED_STATUS_SELECTOR).first().clone(true, true);
const $yellowStatus = $(YELLOW_STATUS_SELECTOR).first().clone(true, true);

const statusText = {
    OnTrack: 'On Track',
    MinorChallenges: 'Minor Challenges',
    CriticalChallenges: 'Critical Challenges'
}

const statusToColour = {
    OnTrack: $greenStatus,
    MinorChallenges: $yellowStatus,
    CriticalChallenges: $redStatus,
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
        // const $statusSelector = this._$el.find(STATUS_SELECTOR);
        // $statusSelector.text(this._detail);
        this._$el.find('.feature-value__header_icon-wrapper').remove();
        let $statusDisplay = statusToColour[this._status].clone(true, true);
        $statusDisplay.text(statusText[this._status]);
        this._$el.find(STATUS_SELECTOR).replaceWith($statusDisplay);

        this._$el.find(LATEST_UPDATE_SELECTOR).remove();

        const $detailSelector = this._$el.find(DETAIL_SELECTOR);
        const $detailElement = $('<p>' + this._detail + '</p>');
        $detailSelector.empty();
        $detailSelector.append($detailElement);
        // $subValue.remove();
        this._$el.find(NAME_SELECTOR).text(this._title);
        this._$el.find('img').remove();
    }
}
