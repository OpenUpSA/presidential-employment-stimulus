import { d3 } from './d3';
import { formatPercentage } from './utils';

const COLORS = {
  done: 'rgb(5,65,104)',
  notdone: 'rgb(220,220,220)',
};

export class VizProgress {
  constructor(parentSelector, quotient) {
    this._parentSelector = parentSelector;
    this._quotient = quotient;
    this.render();
  }

  render() {
    const size = 56;
    const margin = 7;
    const radius = size / 2;
    const data = { done: this._quotient, notdone: 1 - this._quotient };
    const pie = d3.pie()
      .value((d) => d.value);
    pie.sort((a, b) => a.key < b.key);
    const pieData = pie(d3.entries(data));
    const svg = d3.select(this._parentSelector)
      .append('svg')
      .attr('width', size)
      .attr('height', size)
      .append('g')
      .attr('transform', `translate(${radius}, ${radius})`);
    svg.append('text')
      .attr('text-anchor', 'middle')
      .attr('dominant-baseline', 'hanging')
      .attr('font-size', '1em;')
      .attr('dy', '-0.5em')
      .text(formatPercentage(this._quotient));
    svg
      .selectAll('any')
      .data(pieData)
      .enter()
      .append('path')
      .attr('d', d3.arc()
        .innerRadius(radius - margin)
        .outerRadius(radius))
      .attr('fill', (d) => COLORS[d.data.key])
      .style('stroke-width', 0);
  }
}
