import $ from 'jquery';
import { formatCount } from './utils';

const HEIGHT = 70;
const MARGIN = 20;

const CONTAINER_SELECTOR = '.feature-value__line-graph';
const PERIOD_SELECTOR = '.line-graph__period';
const DATE_SELECTOR = '.line-graph__period_label.line-graph__period_label--1';
const MARKER_SELECTOR = '.line-graph__period_marker';
const TOOLTOP_SELECTOR = '.line-graph__period_tooltip';

const $containerTemplate = $(CONTAINER_SELECTOR).clone();
const $periodTemplate = $containerTemplate.find(PERIOD_SELECTOR).first().clone(true, true);
$containerTemplate.empty();

const marginPercent = (MARGIN / HEIGHT) * 100;
const maxPercent = 100 - marginPercent;

export class VizLine {
  constructor($parent, values) {
    this._$parent = $parent;
    this._values = values;
    this.render();
  }

  render() {
    const max = this._values.reduce((res, record) => Math.max(res, record.value), 0);
    const min = this._values.reduce((res, record) => Math.min(res, record.value), 0);
    const range = max - min;
    const data = this._values.map((record) => ({
      ...record,
      y: ((max - record.value) / range) * maxPercent + marginPercent,
      height: ((record.value - min) / range) * (HEIGHT - MARGIN),
    }));
    const $graph = $containerTemplate.clone();
    data.forEach((record, i) => {
      const $period = $periodTemplate.clone(true, true);
      $period.find(DATE_SELECTOR).text(record.name);
      const $tooltip = $period.find(TOOLTOP_SELECTOR)
        .text(formatCount(record.value));
      $period
        .on('mouseover', () => $tooltip.show())
        .on('mouseout', () => $tooltip.hide());
      $period.find(MARKER_SELECTOR).css('margin-bottom', `${record.height}px`);
      if (i !== 0) {
        const x1 = 2;
        const x2 = 98;
        const y1 = data[i - 1].y;
        const y2 = record.y;
        const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><line x1="${x1}" x2="${x2}" y1="${y1}" y2="${y2}" style="stroke:rgba(0,0,0,0.5);stroke-width:1" /></svg>`;
        const uri = encodeURI(`data:image/svg+xml;base64,${btoa(unescape(encodeURIComponent(svg)))}`);
        $period.css({
          'background-image': `url(${uri})`,
          'background-size': '100% 100%',
        });
      }
      $graph.append($period);
    });
    this._$parent.append($graph);
  }
}
