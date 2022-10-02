import $ from 'jquery';
import {StoryCard} from "./story-card";
// import Swiper from 'swiper/bundle';
// import 'swiper/swiper-bundle.css';

const CONTAINER_SELECTOR = ".beneficiary-stories";
const TG_SELECTOR = ".thirds-grid";

const storiesTemplate = $(CONTAINER_SELECTOR).first().clone(true, true);

export class BeneficiaryStories {
    constructor(lookups, $parent, beneficiaries, label, identifier) {
        this._lookups = lookups;
        this.$parent = $parent;
        this.beneficiaries = beneficiaries;
        this._label = label;
        this._identifier = identifier.replaceAll(' ','-').replaceAll(',','-').replaceAll('--','-').toLowerCase();
        this.render();
    }

    render() {
        const $el = storiesTemplate.clone(true, true);

        // var swiper_markup = '<div class="swiper-container ' + this._identifier + '"><div class="swiper-wrapper"></div>';
        
        // if(this.beneficiaries.length > 3) {

        //     swiper_markup += '<div class="swiper-button-prev"></div><div class="swiper-button-next"></div>';

        // }
        
        // swiper_markup += '</div>'

        // $el.append(swiper_markup);
        
        $el.find('.header .tab-h4').first().text('Beneficiary impact');
        const $thirds_grid = $el.find(TG_SELECTOR);
        $thirds_grid.empty()

        // var $swiper_wrapper = $el.find('.' + this._identifier + ' .swiper-wrapper');

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

        // this.beneficiaries.forEach(beneficiary => {
        //    const $card = new StoryCard(
        //         this._lookups,
        //         $swiper_wrapper,
        //         beneficiary.name,
        //         beneficiary.department,
        //         beneficiary.blurb,
        //         beneficiary.paragraph,
        //         beneficiary.picture_url,
        //         this._label)
        // });

        
        this.$parent.append($el);
        
      
        // new Swiper('.' + this._identifier, {
        //     spaceBetween: 10,
        //     navigation: {
        //         nextEl: '.swiper-button-next',
        //         prevEl: '.swiper-button-prev',
        //     },
        //     effect: 'card',
        //     loop: false
        // });
        
        

    }
}
