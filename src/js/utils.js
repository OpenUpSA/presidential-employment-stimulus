export function formatCount(valueIn, short) {
  const value = Number(valueIn);
  let valueOut;
  if (value > 999999) {
    const minDigits =  (Math.floor(value) === value) ? 0 : 1;
    const display = short ? 'short' : 'long';
    valueOut = new Intl.NumberFormat('en', {
      minimumFractionDigits: minDigits,
      maximumFractionDigits: 1,
      notation: 'compact',
      compactDisplay: display,
    }).format(value);
  } else {
    valueOut = value.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,');
  }
  return valueOut;
}

export function formatAmount(valueIn, short) {
  const valueOut = formatCount(valueIn, short);
  return `R${valueOut}`;
}

export function formatPercentage(valueIn) {
  return `${Math.round(Number(valueIn) * 100)}%`;
}

export const FORMATTERS = {
  count: formatCount,
  currency: formatAmount,
  percentage: formatPercentage,
  percentile: formatPercentage,
  job_opportunities: formatCount,
  livelihoods: formatCount,
  jobs_retain: formatCount,
  targets_count: formatPercentage
};

export function organizeByZero(array) {
  // put programmes with non-zero achievements before those with zero achievements
    const [pass, fail] = array.reduce(([pass, fail], elem) => {
        return (elem.value !== 0) ? [[...pass, elem], fail] : [pass, [...fail, elem]];
    }, [[], []]);
    return pass.concat(fail);
}

export function fillInMissingSections(dimensions, has_vets) {
  const order = {
    time: 0,
    gender: 1,
    age: 2,
    vets: 3,
    disabled: 4,
    province: 5
  };

  dimensions.sort((a, b) => { return order[a.lookup] - order[b.lookup]});
  // expect dimensions to include:
  // time, gender, age, [ vets, disabled ], province
  const lookupList = Array("time", "gender", "age", "vets", "disabled", "province");
  const vizList = Array("line", "two_value", "percentile", "count", "count", "bar")
  let newDimensions = Array();
  let index = 0;
  let dimIndex = 0;
  while (index < lookupList.length) {
    // console.log(dimIndex);
    // console.log(dimensions.length);
    // console.log(dimensions);
    if (dimIndex < dimensions.length && dimensions[dimIndex].lookup === lookupList[index]) {
      newDimensions.push(dimensions[dimIndex]);
      dimIndex += 1;
    } else {
      newDimensions.push({name: "missing", viz: vizList[index], lookup: lookupList[index], values: [], data_missing: true});
    }
    if (!has_vets && lookupList[index] === "age") {
      index += 3;
    } else {
      index += 1;
    }
  }
  return newDimensions;
}

export function truncate(text, limit, after) {

	var content = text.trim();
	content = content.split(' ').slice(0, limit);
	content = content.join(' ') + (after ? after : '');
  return content;

}

export function isObject(obj) {
  return Object.prototype.toString.call(obj) === '[object Object]';
};

export function hasPhase(phase_num, tabData) {
  if (tabData.phases === undefined) {
    return false;
  } else {
    const phase_nums = tabData.phases.map( phase => { return phase === undefined ? undefined : phase.phase_num } );
    return phase_nums.includes(phase_num)
  }
}
