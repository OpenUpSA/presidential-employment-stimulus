import { d3 } from './d3';
import { formatPercentage } from './utils';

const COLORS = [
  {
    done: 'rgb(5,65,104)',
    notdone: 'rgb(220,220,220)',
    exceeded: 'rgb(37, 120, 75)',
  },
  {
    done: 'rgb(245, 130, 31)',
    notdone: 'rgb(220,220,220)',
    exceeded: 'rgb(255, 189, 82)',
  },
  {
    done: 'rgb(37, 120, 75)',
    notdone: 'rgb(37,120,75)',
    exceeded: 'rgb(37, 120, 75)',
  }
];

export class VizProgress {
  constructor(parentSelector, quotient, phase) {
    this._parentSelector = parentSelector;
    this._quotient = quotient;
    this._phase = phase;
    this.render();
  }

  render() {

    

    const size = 56;
    const margin = 7;
    const radius = size / 2;
    const pie = d3.pie()
      .value((d) => d.value);
    pie.sort((a, b) => a.key < b.key);
    const data = {};
    if (this._quotient > 1) {
      data.done = 1;
      data.exceeded = this._quotient - 1;
      const endA = this._quotient * 2 * Math.PI;
      pie.endAngle(endA);
    } else {
      data.done = this._quotient;
      data.notdone = 1 - this._quotient;
    }
    const circ = 2 * Math.PI;
    const pieData = [
      {
        data: {
          key: 'done',
          value: this._quotient,
        },
        index: 0,
        startAngle: 0,
        endAngle: this._quotient > 1 ? circ : circ * this._quotient,
        padAngle: 0,
        value: this._quotient,
      },
    ];
    let key;
    let value;
    if (this._quotient > 1) {
      key = 'exceeded';
      value = this._quotient - 1;
    } else {
      key = 'notdone';
      value = 1 - this._quotient;
    }
    pieData.push({
      data: {
        key,
        value,
      },
      index: 1,
      startAngle: pieData[0].endAngle,
      endAngle: pieData[0].endAngle + circ * value,
      padAngle: 0,
      value,
    });

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
        .innerRadius((d) => radius - (margin * (d.data.key === 'exceeded' ? 1.5 : 1)))
        .outerRadius((d) => radius - (d.data.key === 'exceeded' ? margin + 1 : 0)))
      .attr('fill', (d) =>  COLORS[parseInt(this._phase)][d.data.key] )
      .style('stroke-width', 0);
  }
}
