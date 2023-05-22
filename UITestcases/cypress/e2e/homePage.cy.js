/// <reference types="cypress" />


describe('HomePage FoodWaste Management', () => {
    beforeEach(() => {
        cy.viewport(1243, 844)
        cy.visit('http://127.0.0.1:8000/')
        cy.get('.main-menu > .main-menu__main-menu-box > .main-menu__list > #home').should('have.class', 'current');
    })
  
    it('Carousel Request Pickup button', () => {
        const requestPickUpButton = cy.get('.swiper-slide-active > .container > .row > .col-xl-12 > .main-slider__content > .thm-btn');
        requestPickUpButton.should('have.text', 'Request a Pickup');
        requestPickUpButton.click({force: true});
        cy.url().should('include', 'http://127.0.0.1:8000/request-pickup/');
    })
})
  