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
        cy.visit('http://127.0.0.1:8000/request-pickup/')
    })


    it('Checking all fields exists or not', () => {
        cy.get('#first_name')
        cy.get('#last_name')
        cy.get('#company_name')
        cy.get('.filter-option-inner-inner')
        cy.get('#address')
        cy.get('#pincode')
        cy.get('#brief_desc')
        cy.get('#email')
        cy.get('#quantity')
        cy.get('#datepicker')
        cy.get('#time')
        cy.get('#request-a-pickup-btn')
    })

    it('Trying to submit request pickup with empty data', () => {
        cy.get('#request-a-pickup-btn').click();
        
        cy.get('#company_name_error').should('have.text', 'Please enter a company name');
        cy.get('#company_type_error').should('have.text', 'Please select company type');
        cy.get('#address_error').should('have.text', 'Please enter address');
        cy.get('#pincode_error').should('have.text', 'Please enter pincode');
        cy.get('#brief_desc_error').should('have.text', 'Please enter a description');
        cy.get('#quantity_error').should('have.text', 'Please enter quantity');
        cy.get('#datepicker_error').should('have.text', 'Please select a date');
        cy.get('#time_error').should('have.text', 'Please select a time');

    });

    it('Submiting a request pickup', () => {
        cy.get('#company_name').type('University of Leicester', {force: true});
        cy.get('#company_type').select('COLLEGE', {force: true});
        
        cy.get('#address').type('Some party address', {force: true});
        cy.get('#pincode').type('123456', {force: true});
        cy.get('#brief_desc').type('Some party short description', {force: true});
        cy.get('#quantity').type('10', {force: true});
        cy.get('#datepicker').type('12/15/2022', {force: true});
        cy.get('#time').type('2:45 PM', {force: true});
        
        cy.get('#request-a-pickup-btn').click();
        cy.get('#res_message').should('have.text', 'Thanks for helping, will contact you soon.');
    });

})
