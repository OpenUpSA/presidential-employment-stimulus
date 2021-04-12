export function formatCount(valueIn, short) {
  const value = Number(valueIn);
  let valueOut;
  if (value > 999999) {
    const display = short ? 'short' : 'long';
    valueOut = new Intl.NumberFormat('en', {
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
  job_opportunities: formatCount,
  livelihoods: formatCount,
  jobs_retain: formatCount,
};

export function organizeByZero(array) {
  // put programmes with non-zero achievements before those with zero achievements
    const [pass, fail] = array.reduce(([pass, fail], elem) => {
        return (elem.value !== 0) ? [[...pass, elem], fail] : [pass, [...fail, elem]];
    }, [[], []]);
    return pass.concat(fail);
}
