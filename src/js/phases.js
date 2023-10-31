import $ from 'jquery';

const PHASE_TABS_SELECTOR = '.phase-tabs';
const PHASE_MENU_SELECTOR = '.phase-menu';
const PHASE_MENU_ITEM_SELECTOR = '.phase-tab';
const PHASE_CONTENT_SELECTOR = '.phase-content';
const PHASE_CONTENT_PANE_SELECTOR = '.phase-pane';
const SELECTED_PHASE_MENU_ITEM_CLASS = 'w--current';
const SELECTED_PHASE_PANE_CLASS = 'w--tab-active';
const CTA_BUTTON_SELECTOR = '.button.is--performance-cta';

const $phaseTabsTemplate = $(PHASE_TABS_SELECTOR).first().clone(true, true);
const $phaseMenuTemplate = $(PHASE_MENU_SELECTOR).first().clone(true, true);
const $phaseContentTemplate = $(PHASE_CONTENT_SELECTOR).first().clone(true, true);
const $phaseMenuItemTemplate = $(PHASE_MENU_ITEM_SELECTOR).first().clone(true, true);
const $phaseContentPaneTemplate = $(PHASE_CONTENT_PANE_SELECTOR).first().clone(true, true);


export class Phases {
    constructor($parent) {
        this._$parent = $parent;
        this._$phasesMenu = null;
        this._$phasesContent = null;
        this._$phasesContentPane = null;
        this.render();
    }

    add(phasesLength, phaseIndex, phaseContent) {

        let $phaseMenuItem = $phaseMenuItemTemplate.clone(true, true);

        $phaseMenuItem.attr('data-w-tab','Phase ' + (phaseIndex + 1));

        $phaseMenuItem.find('.phase-tab__text').text(phaseIndex == 0 ? 'October 2020 - March 2022' : 'April 2022 - March 2023');

        $phaseMenuItem.removeClass(SELECTED_PHASE_MENU_ITEM_CLASS);


        if(phaseIndex == phasesLength - 1 || phasesLength == 1) {
            $phaseMenuItem.addClass(SELECTED_PHASE_MENU_ITEM_CLASS);
        }

        this._$phasesMenu.append($phaseMenuItem);

        this._$phasesContentPane = $phaseContentPaneTemplate.clone(true, true);
        this._$phasesContentPane.attr('data-w-tab','Phase ' + (phaseIndex + 1));
        this._$phasesContentPane.empty();

        this._$phasesContentPane.append(phaseContent);

        this._$phasesContentPane.removeClass(SELECTED_PHASE_PANE_CLASS);

        if(phaseIndex == phasesLength - 1 || phasesLength == 1) {
            this._$phasesContentPane.addClass(SELECTED_PHASE_PANE_CLASS);
        }

        this._$phasesContent.append(this._$phasesContentPane);

    }

    render() {

        this._$phasesTabs = $phaseTabsTemplate.clone(true, true);
        this._$phasesTabs.empty();

        this._$phasesMenu = $phaseMenuTemplate.clone(true, true);
        this._$phasesMenu.empty();

        this._$phasesContent = $phaseContentTemplate.clone(true, true);
        this._$phasesContent.empty();

        this._$phasesTabs.append(this._$phasesMenu);
        this._$phasesTabs.append(this._$phasesContent);

        this._$parent.append(this._$phasesTabs);


        // PHASE TABS SELECT

        $(PHASE_MENU_ITEM_SELECTOR).on('click', function() {

            let tab = $(this).attr('data-w-tab');
            let tabs_menu = $(this).parent();
            let tabs_content = $(this).parent().parent();

            $(tabs_menu).find(PHASE_MENU_ITEM_SELECTOR).removeClass(SELECTED_PHASE_MENU_ITEM_CLASS);
            $(this).addClass(SELECTED_PHASE_MENU_ITEM_CLASS);
            $(tabs_content).find(PHASE_CONTENT_SELECTOR + ' ' + PHASE_CONTENT_PANE_SELECTOR).removeClass(SELECTED_PHASE_PANE_CLASS);
            $(tabs_content).find(PHASE_CONTENT_PANE_SELECTOR + '[data-w-tab="' + tab + '"]').addClass(SELECTED_PHASE_PANE_CLASS);

        })





    }

}
