import { bisector, extent, max } from 'd3-array';
import { axisBottom, axisLeft } from 'd3-axis';
import { entries } from 'd3-collection';
import { json } from 'd3-fetch';
import { scaleLinear, scaleTime } from 'd3-scale';
import {
  data, pointer, select, selectAll,
} from 'd3-selection';
import { arc, line, pie } from 'd3-shape';
import { timeFormat, timeParse } from 'd3-time-format';

export const d3 = {
  arc,
  axisBottom,
  axisLeft,
  bisector,
  data,
  entries,
  extent,
  json,
  line,
  max,
  pie,
  pointer,
  scaleLinear,
  scaleTime,
  select,
  selectAll,
  timeFormat,
  timeParse,
};
