import $ from 'jquery';
import Swiper from 'swiper/bundle';
import 'swiper/swiper-bundle.css';

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

    // if($(this._tabs[i]._$container[0]).find('.swiper-container').length > 0) {
      
    //   let swiperClass = $(this._tabs[i]._$container[0]).find('.swiper-container')[0].classList[1];

    //   new Swiper('.' + swiperClass, {
    //     slidesPerView: 3,
    //     spaceBetween: 10,
        
        
    //     navigation: {
    //         nextEl: '.swiper-button-next',
    //         prevEl: '.swiper-button-prev',
    //     },
    //     effect: 'card',
    //     loop: false,
        
    //   });
      
    // }

  }
}
