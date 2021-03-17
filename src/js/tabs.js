import $ from 'jquery';

const TAB_MENU_SELECTOR = '.tab-menu';
const TAB_CONTENT_SELECTOR = '.tab-content';

export class Tabs {
  constructor() {
    this._tabs = [];
    this._$menuContainer = $(TAB_MENU_SELECTOR);
    this._$contentContainer = $(TAB_CONTENT_SELECTOR);
  }

  add(tab) {
    this._tabs.push(tab);
    this._$menuContainer.append(tab.$menuItem);
    this._$contentContainer.append(tab.$contentPane);
  }

  select(i) {
    this._tabs.forEach((tab) => {
      tab.select(false);
    });
    this._tabs[i].select(true);
  }
}
