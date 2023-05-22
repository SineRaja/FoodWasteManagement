/// <reference types="cypress" />


describe('Request Pickup Page FoodWaste Management', () => {
    beforeEach(() => {
        cy.viewport(1243, 844)
        cy.visit('http://127.0.0.1:8000/login/');
        const emailInput = cy.get('#login_email');
        const passwordInput = cy.get('#login_password');

        emailInput.type('sinerajarc@gmail.com');
        passwordInput.type('raja1234');
        
        cy.get('#loginButton').click();
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
        cy.get(':nth-child(1) > .card > .row > :nth-child(5) > #reject').should('have.text', 'Delete');
        cy.get(':nth-child(1) > .card > .row > :nth-child(5) > .btn-info').should('have.text', 'Raise an issue');
    })

    it('Checking Raise an issue functionality', () => {
        cy.get(':nth-child(1) > .card > .row > :nth-child(5) > #raise_an_issue').click({force: true});
        cy.url().should('include', 'http://127.0.0.1:8000/issue/');
    })

    it('Checking Delete Popup functionality', () => {
        const deleteButton = cy.get(':nth-child(1) > .card > .row > :nth-child(5) > #reject')
        deleteButton.click({force: true});
        cy.get('#deleteModal > .modal-dialog > .modal-content').should('be.visible')
        cy.get('#deleteModal > .modal-dialog > .modal-content > .modal-header > .modal-title').should('have.text', 'Are you sure to delete this request');
        cy.get('#deleteModalClose > span').should('be.visible')
        cy.get('#deleteModal > .modal-dialog > .modal-content > .modal-footer > .btn-secondary').should('have.text', 'Close');
        cy.get('#deleteModal > .modal-dialog > .modal-content > .modal-footer > .btn-danger').should('have.text', 'Confirm Delete');
    })

    it('Checking Delete Popup close functionality', async () => {
        const deleteButton = cy.get(':nth-child(1) > .card > .row > :nth-child(5) > #reject')
        deleteButton.click({force: true});
        cy.get('#deleteModal > .modal-dialog > .modal-content').should('be.visible');
        cy.get('#deleteCloseButton').click({force: true});
        cy.get('#deleteModal > .modal-dialog > .modal-content').should('not.be.visible');
    })

    it('Checking Delete  functionality', async () => {
        const deleteButton = cy.get(':nth-child(1) > .card > .row > :nth-child(5) > #reject')
        deleteButton.click({force: true});
        cy.get('#deleteModal > .modal-dialog > .modal-content').should('exist');
        cy.get('#deleteConfirmButton').click({force: true});
        cy.get('#deleteModal > .modal-dialog > .modal-content').should('not.exist');
    })

})
