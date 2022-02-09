import $ from 'jquery';
import { truncate } from './utils';

const CARD_SELECTOR=".block.is--story";
const MODAL_SELECTOR=".block.is--story .is--story-modal";
const QUOTE_CARD_SELECTOR = ".block.is--story.is--quote";

const $cardTemplate = $(CARD_SELECTOR).first().clone(true, true);
// const modalTemplate = $(MODAL_SELECTOR).first().clone(true, true);
const $quoteCardTemplate = $(QUOTE_CARD_SELECTOR).first().clone(true, true);

export class StoryCard {
    constructor(lookups, $parent, name, department, blurb, paragraph, picture_url, label) {
        this._lookups = lookups;
        this.$parent = $parent;
        this.name = name;
        this.department = department;
        this.blurb = blurb;
        this.paragraph = paragraph;
        this.picture_url = picture_url;
        this.label = label;
        this.modalVisible = false;
        this.render();
    }

    select(on, $modal) {
        $('.story-modal:first').remove();
        $('body').append($modal);
        $(".story-modal").css('display', on ? "block" : "none").css('opacity', on ? 1 : 0);
        $('.story-modal .block.is--story-modal').css('top','50%').css('left','50%').css('transform','translate(-50%,-50%)');
        $('.story-modal .story-modal__close').on("click", () => {
            this.select(false, $modal);
        })

    }

    render() {
        let $el;
        
        if(this.picture_url != null) {
            
            $el = $cardTemplate.clone(true, true);
            $el.find('.story-title').text(this.blurb);
            $el.find('.story-department').text(this._lookups["department"][this.department]);
            $el.find('.story-image').attr('srcset', 'img/' + this.picture_url);
            $el.find('.story-description').text(this.paragraph != null ? truncate(this.paragraph,40,'...') : '');
            $el.find('.story-description.is--modal').text(this.paragraph);
            $el.find('.story-image.is--modal').css('height','25em');
        
        } else {

            $el = $quoteCardTemplate.clone(true, true);
            $el.find('.story-department').text(this.department);
            $el.find('.quotation').text(this.paragraph);
            if(this.name != null) {
                $el.find('.quotation-credit').text('- ' + this.name);
            }
        }

        if(this.label == false) {
            $el.find('.story-department').remove();
        }
        

        const $modal = $el.find('.story-modal');
        
        $el.on("click", () => {
            this.select(true, $modal);
        })

        $el.find('.story-department').on("click", (e) => {
            e.stopPropagation();
            let department = $el.find('.story-department').text();

            $('.tab.is--department div:contains("' + department + '")').trigger('click');


        })

        this.$parent.append($el);

        this.select(false, $modal);

        
    }
}
