export class DepartmentTabs {
    constructor() {
        this.template = $(".embed-container > .tabs-wrapper");

        this.element = this.template.clone();
        console.assert(this.element.length === 1);

        this.menuElement = this.element.find('.tab-menu');
        console.assert(this.menuElement.length === 1);

        let navTabElement = this.element.find(".tab-link");
        console.log(this.element.find(".tab-link"));
        this.navTabTemplate = navTabElement.first().clone();
        navTabElement.first().remove();
        console.log(this.element.find(".tab-link"));

        this.tabListElement = this.element.find('.tab-content');

        let tabContentElement = this.element.find(".tab-pane");
        this.tabContentTemplate = tabContentElement.first().clone();
        tabContentElement.first().remove();
    }

    addTabs(departments) {
        departments.forEach((department) => {
           let navTab = this.navTabTemplate.clone();
           navTab.attr('data-w-tab', department.abbrev);
           navTab.find('div').text(department.abbrev);
           this.menuElement.append(navTab);
           let tabContentElement = this.tabContentTemplate.clone();
           tabContentElement.attr('data-w-tab', department.abbrev);
           tabContentElement.text('FOO');
           this.tabListElement.append(tabContentElement);
           console.log("got here", department);
        });
    }
}
