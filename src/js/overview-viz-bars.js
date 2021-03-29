import $ from 'jquery';
import {formatCount} from "./utils";

const CONTAINER_SELECTOR = '.feature-value__bar-chart';
const ROW_SELECTOR = '.bar-chart__row.small.w-inline-block';

const BAR_SELECTOR = '.bar-chart__row_bar';
const BAR_TOOLTIP_SELECTOR = '.bar-chart__row_tooltip';
const BAR_CAT_LABEL_SELECTOR = '.bar-chart__row_label';
const BAR_VAL_LABEL_SELECTOR = '.bar-chart__row_value';

const $containerTemplate = $(CONTAINER_SELECTOR).first().clone(true, true).empty();
const $rowTemplate = $(ROW_SELECTOR).first().clone(true, true);
const name_to_abbrev = {
    'Trade, Industry and Competition': 'DTIC',
    'Basic Education': 'DBE',
    'Social Development': 'DSD',
    'Health': 'DoH',
    'Agriculture, Land Reform and Rural Development': 'DALLRD',
    'Science and Innovation': 'DSI',
    'Sports, Arts and Culture': 'DSAC',
    'Transport': 'DoT',
    'Public Works and Infrastructure': 'DPWI',
    'Environment, Forestry and Fisheries': 'DEFF',
    'Co-operative government': 'DCOGTA',
};

export class OverviewVizBars {
    constructor($parent, rows) {
        this._$parent = $parent;
        this._rows = rows;
        this._max = this._rows
            .map((row) => row.value)
            .reduce((max, curr) => Math.max(max, curr), 0);
        this.render();
    }

    render() {
        const $el = $containerTemplate.clone(true, true);
        this._rows.forEach((row) => {
            const width = Math.round((row.value / this._max) * 100);
            const $row = $rowTemplate.clone(true, true);
            $row.find(BAR_SELECTOR).width(`${width}%`);
            const $tooltip = $row.find(BAR_TOOLTIP_SELECTOR).text(row.name);
            $row.on('mouseover', () => $tooltip.show());
            $row.on('mouseout', () => $tooltip.hide());
            $row.find(BAR_CAT_LABEL_SELECTOR).text(name_to_abbrev[row.name].toUpperCase());
            $row.find(BAR_VAL_LABEL_SELECTOR).text(formatCount(row.value));
            $el.append($row);
        });
        this._$parent.append($el);
    }
}
