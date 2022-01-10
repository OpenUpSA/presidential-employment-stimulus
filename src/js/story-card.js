import $ from 'jquery';

const CARD_SELECTOR=".block.is--story .story__inner";
const MODAL_SELECTOR=".block.is--story .is--story-modal";

const cardTemplate = $(CARD_SELECTOR).first().clone(true, true);
const modalTemplate = $(MODAL_SELECTOR).first().clone(true, true);
export class StoryCard {
    constructor($parent, name, blurb, paragraph, picture_url) {
        this.$parent = $parent;
        this.name = name;
        this.blurb = blurb;
        this.paragraph = paragraph;
        this.picture_url = picture_url;
        this.modalVisible = false;
        this.render();
    }

    select(on) {
        this.$modal.animate({
           display: on ? "block" : "none",
           opacity: on ? 1 : 0
        }, on ? 500 : 0);
    }

    render() {
        const $el = cardTemplate.clone(true, true);
        $el.find('.story-title').text(this.blurb);
        $el.find('.story-image').attr('src', "url(" + this.picture_url + ")");
        $el.find('.story-description').text(this.paragraph);
        $el.on("click", () => {
            this.select(true);
        })
        this.$parent.append($el);

        const $modal = modalTemplate.clone(true, true);
        $modal.find(".story-title").text("AAAAAA");
        $modal.find(".story-image").attr('src', this.picture_url);
        $modal.find(".story-description").text(this.paragraph);
        $('body').append($modal);
        this.$modal = $modal;
        this.select(false);
        $modal.on("click", () => {
            this.select(false);
        })
    }
}
