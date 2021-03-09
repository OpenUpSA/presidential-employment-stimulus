import {DepartmentTabs} from './components/DepartmentList';

const dataUrl = 'https://gist.githubusercontent.com/pvanheus/d278b81a6c5a9a1c7e19ad5fb884aeb8/raw/0d194ce7cf1ef79c305abda3840addc68ae1b713/test.js';
class PageState {
    constructor() {
        this.departmentList = new DepartmentTabs();
        this.dataRequest = null;
        this.fetchData(dataUrl);
    }

    fetchData(url) {
        if (this.dataRequest !== null)
            this.dataRequest.abort();

        this.dataRequest = $.get(url, )
            .done((responseRaw) => {
                const response = JSON.parse(responseRaw);
                let tabData = Array();
                response.forEach((descriptor) => {
                    tabData.push(descriptor.abbrev)
            });
            this.departmentList.addTabs(tabData);
        })
        .fail(function(jqXHR, textStatus, errorThrown) {
            console.error(jqXHR, textStatus, errorThrown);
        }, "json");
    }
}

const pageState = new PageState();
