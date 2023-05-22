/// <reference types="cypress" />


describe('Request Pickup Page FoodWaste Management', () => {
    beforeEach(() => {
        cy.viewport(1243, 844)
        cy.visit('http://127.0.0.1:8000/login/');
        const emailInput = cy.get('#login_email');
        const passwordInput = cy.get('#login_password');

        emailInput.type('sineraja97@gmail.com',{force:true});
        passwordInput.type('prachi1234', {force:true});
        
        cy.get('#loginButton').click({force:true});
        cy.wait(2000);
        cy.visit('http://127.0.0.1:8000/my-requests/')
    })

    it('Checking requests are there or not', () => {
        cy.get('h1').should('have.text', 'Pending Requests');
        cy.get(':nth-child(1) > .card > .row > .col-md-7 > :nth-child(1)').should('have.text', 'University of Leicester');
        cy.get(':nth-child(1) > .card > .row > .col-md-7 > :nth-child(3)').should('have.text', 'sinerajarc@gmail.com');
        cy.get(':nth-child(1) > .card > .row > .col-md-5 > :nth-child(1)').should('have.text', 'COLLEGE');
        cy.get(':nth-child(1) > .card > .row > .col-md-5 > :nth-child(3)').should('have.text', 'COOKED');
        cy.get(':nth-child(1) > .card > .row > :nth-child(3) > :nth-child(3)').should('have.text', '10');
        cy.get(':nth-child(1) > .card > .row > :nth-child(3) > :nth-child(5)').should('have.text', 'Some party address, Leicester, Le2 1xp, England, 123456, 7767947467');
        cy.get(':nth-child(1) > .card > .row > :nth-child(3) > :nth-child(7)').should('have.text', 'Some party short description');
        cy.get(':nth-child(1) > .card > .row > :nth-child(5) > #accept').should('have.text', 'Accept');
        cy.get(':nth-child(1) > .card > .row > :nth-child(5) > #raise_an_issue').should('have.text', 'Raise an issue');
    })

    it('Checking Raise an issue functionality', () => {
        cy.get(':nth-child(1) > .card > .row > :nth-child(5) > #raise_an_issue').click({force: true});
        cy.url().should('include', 'http://127.0.0.1:8000/issue/');
    })

    it('Checking Accept Popup functionality', () => {
        const acceptButton = cy.get(':nth-child(1) > .card > .row > :nth-child(5) > #accept')
        acceptButton.click({force: true});
        cy.get('#acceptModal > .modal-dialog > .modal-content').should('be.visible')
        cy.get('#acceptModal > .modal-dialog > .modal-content > .modal-header > .modal-title').should('have.text', 'Are you sure to accept this request');
        cy.get('#acceptModalClose > span').should('be.visible')
        cy.get('#acceptCloseButton').should('have.text', 'Close');
        cy.get('#acceptConfirmButton').should('have.text', 'Confirm Accept');
    })

    it('Checking Accept Popup close functionality', async () => {
        cy.get(':nth-child(1) > .card > .row > :nth-child(5) > #accept').click({force: true});
        cy.get('#acceptModal > .modal-dialog > .modal-content').should('be.visible');
        cy.get('#acceptCloseButton').click({force: true});
        cy.get('#acceptModal > .modal-dialog > .modal-content').should('not.be.visible');
        cy.reload();
    })

    it('Checking Accept functionality', async () => {
        cy.get(':nth-child(1) > .card > .row > :nth-child(5) > #accept').click({force: true});
        cy.get('#acceptModal > .modal-dialog > .modal-content').should('be.visible');
        cy.get('#acceptConfirmButton').click({force: true});
        cy.get('#acceptModal > .modal-dialog > .modal-content').should('not.be.visible');
        cy.reload();
    })

})
