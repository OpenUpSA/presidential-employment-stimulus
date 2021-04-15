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

const CONTAINER_SELECTOR = '.feature-value__current-status';
const NAME_SELECTOR = '.status-update__label';
const ICON_CONTAINER_SELECTOR = '.feature-value__header_icon-wrapper';
// const VALUE_SELECTOR = '.feature-value__amount';
const STATUS_SELECTOR = '.feature-value__current-status';
const LATEST_UPDATE_SELECTOR = '.uppercase-label.uppercase-label--border-top';
const DETAIL_SELECTOR = '.status-update__description.w-richtext';
const PROGRESS_CLASS = 'feature-value__header_chart-wrapper';
const GREEN_STATUS_SELECTOR = '.feature-value__amount.feature-value__amount--green';
const YELLOW_STATUS_SELECTOR = '.feature-value__amount.feature-value__amount--yellow';
const RED_STATUS_SELECTOR = '.feature-value__amount.feature-value__amount--red';
const STATUS_BLOCK_SELECTOR = '.block.status-update';
const STATUS_BLOCK_HEADER_SELECTOR = '.status-update__label';
const STATUS_BLOCK_CS_SELECTOR = '.status-update__current-status';
const STATUS_BLOCK_GREEN_STATUS_SELECTOR = '.status-update__current-status.feature-value__amount--green';
const STATUS_BLOCK_YELLOW_STATUS_SELECTOR = '.status-update__current-status.feature-value__amount--yellow';
const STATUS_BLOCK_RED_STATUS_SELECTOR = '.status-update__current-status.feature-value__amount--red';
const STATUS_BLOCK_UPPERCASE_LABEL_SELECTOR = '.uppercase-label.uppercase-label--border-top';
const STATUS_BLOCK_DETAIL_SELECTOR = '.status-update__description.w-richtext>p';

const $topHeaderTemplate = $(LATEST_UPDATE_SELECTOR).first().clone(true, true);
const $greenStatus = $(GREEN_STATUS_SELECTOR).first().clone(true, true);
const $redStatus = $(RED_STATUS_SELECTOR).first().clone(true, true);
const $yellowStatus = $(YELLOW_STATUS_SELECTOR).first().clone(true, true);
const $greenBlockStatus = $(STATUS_BLOCK_GREEN_STATUS_SELECTOR).first().clone(true, true);
const $yellowBlockStatus = $(STATUS_BLOCK_YELLOW_STATUS_SELECTOR).first().clone(true, true);
const $redBlockStatus = $(STATUS_BLOCK_RED_STATUS_SELECTOR).first().clone(true, true);

const $detailTemplate = $(DETAIL_SELECTOR).first().clone();

const $statusBlockTemplate = $(STATUS_BLOCK_SELECTOR).first().clone(true, true);

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

const blockStatusToColour = {
    OnTrack: 'status-update__current-status--green',
    MinorChallenges: 'status-update__current-status--yellow',
    CriticalChallenges: 'status-update__current-status--red'
}

export class ImplementationDetail {
    constructor($parent, title, status, detail, isblock) {
        this._$parent = $parent;
        this._title = title;
        this._status = status;
        this._detail = detail;
        this._isblock = isblock;
        this.render();
    }

    get $el() {
        return this._$el;
    }

    render() {
        if (this._isblock) {
            let block = $statusBlockTemplate.clone(true, true);
            block.find(STATUS_BLOCK_HEADER_SELECTOR).text(this._title);
            block.find(STATUS_BLOCK_CS_SELECTOR).addClass(blockStatusToColour[this._status]);
            block.find(STATUS_BLOCK_CS_SELECTOR).text(statusText[this._status]);
            block.find(STATUS_BLOCK_UPPERCASE_LABEL_SELECTOR).text('Status update');
            block.find(STATUS_BLOCK_DETAIL_SELECTOR).text(this._detail);
            this._$parent.append(block);
        } else {
            let $statusDisplay = statusToColour[this._status].clone(true, true);
            $statusDisplay.text(statusText[this._status]);

            let topHeader = $topHeaderTemplate.clone(true, true);
            topHeader.text('Status update');
            this._$parent.append(topHeader);
            this._$parent.append($statusDisplay);

            const $detailSelector = $detailTemplate.clone(true, true);
            $detailSelector.find('p').text(this._detail);
            // const $detailElement = $('<p>' + this._detail + '</p>');
            // $detailSelector.empty();
            // $detailSelector.append($detailElement);
            this._$parent.append($detailSelector);
        }
    }
}
