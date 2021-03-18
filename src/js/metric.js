import $ from 'jquery';
import { FORMATTERS } from './utils';
import { VizProgress } from './viz-progress';

const CONTAINER_SELECTOR = '.tab-inner .feature-value__inner';
const NAME_SELECTOR = '.feature-value__label';
const METRIC_SELECTOR = '.div-block-4';
const VALUE_SELECTOR = '.feature-value__metric .feature-value__amount';
const TARGET_SELECTOR = '.feature-value__metric .text-block';

const PROGRESS_CLASS = 'feature-value__chart';

const $containerTemplate = $(CONTAINER_SELECTOR).first().clone(true, true);

export class Metric {
  constructor($parent, title, type, value, target) {
    this._$parent = $parent;
    this._title = title;
    this._type = type;
    this._value = value;
    this._target = target === -1 ? null : target;
    this._formatter = FORMATTERS[type];
    this.render();
  }

  get $el() {
    return this._$el;
  }

  render() {
    this._$el = $containerTemplate.clone(true, true);
    this._$parent.append(this._$el);
    this._$el.find(NAME_SELECTOR).text(this._title);
    const metricId = `metric-${Math.round(Math.random() * 1000000)}`;
    const $metric = this._$el.find(METRIC_SELECTOR)
      .attr('id', metricId);
    $metric.find('img').remove();
    if (!this._value) {
      $metric.remove();
    } else {
      this._$el.find(VALUE_SELECTOR).text(this._formatter(this._value));
      const $target = $metric.find(TARGET_SELECTOR);
      if (!this._target) {
        $target.remove();
      } else {
        $target.text(`TARGET: ${this._formatter(this._target)}`);
        $metric.prepend(`<div class="${PROGRESS_CLASS}"></div>`);
        const progressQuotient = (this._value / this._target);
        new VizProgress(`#${metricId} .${PROGRESS_CLASS}`, progressQuotient);
      }
    }
  }
}
