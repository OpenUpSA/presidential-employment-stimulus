import $ from 'jquery';
import {StoryCard} from "./story-card";


const CONTAINER_SELECTOR = ".beneficiary-stories";
const TG_SELECTOR = ".thirds-grid";

const storiesTemplate = $(CONTAINER_SELECTOR).first().clone(true, true);
export class BeneficiaryStories {
    constructor(lookups, $parent, beneficiaries, label) {
        this._lookups = lookups;
        this.$parent = $parent;
        this.beneficiaries = beneficiaries;
        this._label = label;
        this.render();
    }

    render() {
        const $el = storiesTemplate.clone(true, true);
        $el.find('.header .tab-h4').first().text('Beneficiary impact');
        const $thirds_grid = $el.find(TG_SELECTOR);
        $thirds_grid.empty()
        this.beneficiaries.forEach(beneficiary => {
           const $card = new StoryCard(
                this._lookups,
                $thirds_grid,
                beneficiary.name,
                beneficiary.department,
                beneficiary.blurb,
                beneficiary.paragraph,
                beneficiary.picture_url,
                this._label)
        });
        this.$parent.append($el);
    }
}
