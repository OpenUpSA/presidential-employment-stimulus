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

const LATEST_UPDATE_SELECTOR = '.uppercase-label.uppercase-label--border-top';
const DETAIL_SELECTOR = '.status-update__description.w-richtext';
const CURRENT_STATUS_SELECTOR = '.feature-value__current-status';
const STATUS_BLOCK_SELECTOR = '.block.status-update';
const STATUS_BLOCK_HEADER_SELECTOR = '.status-update__label';
const STATUS_BLOCK_CS_SELECTOR = '.status-update__current-status';
const STATUS_BLOCK_UPPERCASE_LABEL_SELECTOR = '.uppercase-label';
const STATUS_BLOCK_DETAIL_SELECTOR = '.status-update__description.w-richtext>p';

const $currentStatusTemplate = $(CURRENT_STATUS_SELECTOR).first().clone(true, true);
const $topHeaderTemplate = $(LATEST_UPDATE_SELECTOR).first().clone(true, true);

const $detailTemplate = $(DETAIL_SELECTOR).first().clone();

const $statusBlockTemplate = $(STATUS_BLOCK_SELECTOR).first().clone(true, true);

const statusText = {
    OnTrack: 'On Track',
    MinorChallenges: 'Minor Challenges',
    CriticalChallenges: 'Critical Challenges'
}

const statusToColour = {
    OnTrack: 'feature-value__current-status--green',
    MinorChallenges: 'feature-value__current-status--yellow',
    CriticalChallenges: 'feature-value__current-status--red',
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
            let $statusDisplay = $currentStatusTemplate.clone(true, true);
            $statusDisplay.addClass(statusToColour[this._status]);
            $statusDisplay.text(statusText[this._status]);

            let topHeader = $topHeaderTemplate.clone(true, true);
            topHeader.text('Status update');
            this._$parent.append(topHeader);
            this._$parent.append($statusDisplay);

            const $detailSelector = $detailTemplate.clone(true, true);
            $detailSelector.find('p').text(this._detail);
            this._$parent.append($detailSelector);
        }
    }
}
