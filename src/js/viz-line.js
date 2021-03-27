import $ from 'jquery';
import { d3 } from './d3';
import { formatCount } from './utils';

const SELECTOR = '.feature-value__line-graph';
const $template = $(SELECTOR).clone().empty();

export class VizLine {
  constructor($parent, values) {
    this._$parent = $parent;
    this._values = values;
    this.render();
  }

  render() {
    const parseDate = d3.timeParse('%Y%m');
    const data = this._values.map((d) => ({
      ...d,
      date: parseDate(d.month),
    }));
    const id = `line-chart-${Math.round(Math.random() * 1000000)}`;
    this._$parent.append($template.clone().attr('id', id));
    const selector = `#${id}`;
    const margin = {
      top: 30,
      right: 50,
      bottom: 20,
      left: 30,
    };
    const width = 300;
    const height = 80;
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;
    const xScale = d3.scaleTime().range([0, innerWidth]);
    const yScale = d3.scaleLinear().range([innerHeight, 0]);
    xScale.domain(d3.extent(data, (d) => d.date));
    yScale.domain([0, d3.max(data, (d) => d.value)]);
    const xAxis = d3.axisBottom().scale(xScale).ticks(data.length);
    const valueline = d3.line()
      .x((d) => xScale(d.date))
      .y((d) => yScale(d.value));
    const svg = d3.select(selector)
      .append('svg')
      .attr('xmlns:xhtml', 'http://www.w3.org/1999/xhtml')
      .attr('viewBox', `0 0 ${width} ${height}`)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);
    // const tooltip = svg.append('foreignObject')
    //   .attr('width', '10')
    //   .attr('height', '10')
    //   .style('overflow', 'visible')
    //   .style('opacity', 0)
    //   .attr('alignment-baseline', 'middle');

    // tooltip
    //   .append('xhtml:div')
    //   .attr('style', 'padding: 4px 6px; border-radius: 4px; background-color: black; box-shadow: 0 3px 3px 0 rgb(0 0 0 / 10%); color: white; line-height: 1; white-space: nowrap;')
    //
    //   .text('hello');
    const tooltip = svg.append('g')
      .append('text')
      .style('opacity', 0)
      .attr('font-size', '10px')
      .attr('alignment-baseline', 'middle');
    svg.append('path')
      .attr('class', 'line')
      .attr('stroke', 'lightgrey')
      .attr('stroke-width', 1)
      .attr('d', valueline(data));
    svg.append('g')
      .attr('transform', `translate(0,${innerHeight})`)
      .call(xAxis);
    const bisect = d3.bisector((d) => d.date).right;
    const mousemove = (evt) => {
      const x0 = xScale.invert(d3.pointer(evt)[0]);
      const i = bisect(data, x0, 1) - 1;
      const selectedData = data[i];
      tooltip
        .html(formatCount(selectedData.value))
        .attr('x', xScale(selectedData.date))
        .attr('y', yScale(selectedData.value) - 15);
    };
    svg.selectAll('markers')
      .data(data)
      .enter()
      .append('circle')
      .attr('r', 3)
      .attr('cx', (d) => xScale(d.date))
      .attr('cy', (d) => yScale(d.value))
      .attr('fill', '#124069')
      .on('mouseover', () => {
        // aaa.attr('display', 'block')
        tooltip.style('opacity', 1);
      })
      .on('mousemove', mousemove)
      .on('mouseout', () => {
        tooltip.style('opacity', 0);
      });
  }
}
