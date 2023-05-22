/// <reference types="cypress" />


describe('LoginPage FoodWaste Management', () => {
    beforeEach(() => {
        cy.viewport(1243, 844)
        cy.visit('http://127.0.0.1:8000/');
    })
  
    it('Footer link items', () => {
        cy.get('.footer-widget__links-list > :nth-child(1) > a').should('have.text', 'About');
        cy.get('.footer-widget__links-list > :nth-child(2) > a').should('have.text', 'Request Pickup');
        cy.get('.footer-widget__links-list > :nth-child(3) > a').should('have.text', 'Gallery');
        cy.get('.footer-widget__links-list > :nth-child(4) > a').should('have.text', 'Contact');
    })

    it('Navbar onclick redirections', () => {
        cy.get('.footer-widget__links-list > :nth-child(1) > a').click();
        cy.url().should('include', 'http://127.0.0.1:8000/about-us/');
        cy.get('.footer-widget__links-list > :nth-child(2) > a').click();
        cy.url().should('include', 'http://127.0.0.1:8000/request-pickup/');
        cy.get('.footer-widget__links-list > :nth-child(3) > a').click();
        cy.url().should('include', 'http://127.0.0.1:8000/gallery/');
        cy.get('.footer-widget__links-list > :nth-child(4) > a').click();
        cy.url().should('include', 'http://127.0.0.1:8000/contact/');
    })

})
  