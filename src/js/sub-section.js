import $ from 'jquery';

export class SubSection {
  constructor($parent) {
    this._$parent = $parent;
    this.render();
  }

  get $container() {
    return this._$el;
  }

  render() {
    this._$el = $('<div></div>').addClass('block');
    this._$parent.append(this._$el);
  }
}
