import $ from 'jquery';
import {StoryCard} from "./story-card";
import Swiper from 'swiper/bundle';
import 'swiper/swiper-bundle.css';

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
        $el.append('<div class="swiper-container ' + this._identifier + '"><div class="swiper-wrapper"></div><div class="swiper-pagination"></div><div class="swiper-button-prev"></div><div class="swiper-button-next"></div></div>');
        
        $el.find('.header .tab-h4').first().text('Beneficiary impact');
        const $thirds_grid = $el.find(TG_SELECTOR);
        $thirds_grid.empty()

        var $swiper_wrapper = $el.find('.' + this._identifier + ' .swiper-wrapper');
        

        this.beneficiaries.forEach(beneficiary => {
           const $card = new StoryCard(
                this._lookups,
                $swiper_wrapper,
                beneficiary.name,
                beneficiary.department,
                beneficiary.blurb,
                beneficiary.paragraph,
                beneficiary.picture_url,
                this._label)
        });

        this.$parent.append($el);
        
      
        new Swiper('.' + this._identifier, {
            slidesPerView: 3,
            spaceBetween: 10,
            
            pagination: {
                el: '.swiper-pagination',
                clickable: true
            },
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
            effect: 'card',
            loop: false,
            
        });
        
        

    }
}
