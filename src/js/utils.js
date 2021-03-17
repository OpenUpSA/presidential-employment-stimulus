export function formatAmount(value) {
  return `R${Number(value).toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,')}`;
}

export function formatCount(value) {
  return Number(value).toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,');
}

export function formatPercentage(value) {
  return `${Math.round(Number(value) * 100)}%`;
}

export const FORMATTERS = {
  count: formatCount,
  currency: formatAmount,
  percentage: formatPercentage,
};
