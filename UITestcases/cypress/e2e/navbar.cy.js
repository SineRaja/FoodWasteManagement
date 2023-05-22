/// <reference types="cypress" />


describe('Navbar FoodWaste Management', () => {
    beforeEach(() => {
        cy.viewport(1243, 844)
        cy.visit('http://127.0.0.1:8000/');
        
    })
  
    it('Navbar items', () => {
        cy.get('.main-header__logo > a > img');

        cy.get('.main-menu > .main-menu__main-menu-box > .main-menu__list > #home > a').should('have.text', 'Home');
        cy.get('.main-menu > .main-menu__main-menu-box > .main-menu__list > #about_us > a').should('have.text', 'About');
        cy.get('.main-menu > .main-menu__main-menu-box > .main-menu__list > #gallery > a').should('have.text', 'Gallery');
        cy.get('.main-menu > .main-menu__main-menu-box > .main-menu__list > #contact > a').should('have.text', 'Contact');
        cy.get('.main-menu > .main-menu__main-menu-box > .main-menu__list > #login > a').should('have.text', 'Login');
    })

    it('Navbar onclick redirections', () => {
        cy.get('.main-menu > .main-menu__main-menu-box > .main-menu__list > #about_us > a').click();
        cy.url().should('include', 'http://127.0.0.1:8000/about-us/');
        cy.get('.main-menu > .main-menu__main-menu-box > .main-menu__list > #gallery > a').click();
        cy.url().should('include', 'http://127.0.0.1:8000/gallery/');
        cy.get('.main-menu > .main-menu__main-menu-box > .main-menu__list > #contact > a').click();
        cy.url().should('include', 'http://127.0.0.1:8000/contact/');
        cy.get('.main-menu > .main-menu__main-menu-box > .main-menu__list > #login > a').click();
        cy.url().should('include', 'http://127.0.0.1:8000/login/');
        cy.get('.main-menu > .main-menu__main-menu-box > .main-menu__list > #home > a').click();
        cy.url().should('include', 'http://127.0.0.1:8000/');
        cy.get('.main-header__logo > a > img').click();
        cy.url().should('include', 'http://127.0.0.1:8000/');
    })

})
  