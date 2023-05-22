/// <reference types="cypress" />


describe('Forgot Password Page FoodWaste Management', () => {
    beforeEach(() => {
        cy.viewport(1243, 844)
        cy.visit('http://127.0.0.1:8000/forgot-password/')
        cy.get('.main-menu > .main-menu__main-menu-box > .main-menu__list > #login').should('have.class', 'current');
    })
  
    it('Checking all fields exists or not', () => {
        cy.get('#email')
        cy.get('#forgotPass')
        cy.get(':nth-child(4) > .small').should('have.text', 'Create an Account!');
        cy.get(':nth-child(5) > .small').should('have.text', 'Already have an account? Login!');
    })

    it('Checking create an account button functionality', () => {
        const createAnAccount = cy.get(':nth-child(4) > .small');
        createAnAccount.click();
        cy.url().should('include','http://127.0.0.1:8000/register/');
    })

    it('Checking login  button functionality', () => {
        const forgotPassword = cy.get(':nth-child(5) > .small');
        forgotPassword.click();
        cy.url().should('include', 'http://127.0.0.1:8000/login/');
    });

    it('Trying to reset password with empty email', () => {
        const emailInput = cy.get('#email')
        emailInput.should('have.class', 'form-control')
        emailInput.should('have.class', 'form-control-user')
        emailInput.should('have.attr', 'placeholder', 'Enter Email Address...');

        
        cy.get('#forgotPass').click();
        cy.get('#email_error').should('have.text', 'Please enter valid email id');
    });

    it('Trying to login with invalid email', () => {
        const emailInput = cy.get('#email')

        emailInput.type('random@gmail.com');
        
        cy.get('#forgotPass').click();
        cy.get('.swal-modal');
        cy.get('.swal-text').should('have.text', "Can't reset password, Invalid Email");
        cy.get('.swal-button').click();
        cy.url().should('include', 'http://127.0.0.1:8000/forgot-password');
    });

    it('Trying to reset password with valid email', async () => {
        const emailInput = cy.get('#email')
        emailInput.type('sinerajarc@gmail.com');
        
        await cy.get('#forgotPass').click();
        cy.get('.swal-modal')
        cy.get('.swal-text').should('have.text', 'Password reset mail sent successfully');
        cy.get('.swal-button').click();
        cy.url().should('include', 'http://127.0.0.1:8000/');
    });  
})
  