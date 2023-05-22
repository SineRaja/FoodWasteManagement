/// <reference types="cypress" />


describe('LoginPage FoodWaste Management', () => {
    beforeEach(() => {
        cy.viewport(1243, 844)
        cy.visit('http://127.0.0.1:8000/login/')
        cy.get('.main-menu > .main-menu__main-menu-box > .main-menu__list > #login').should('have.class', 'current');
    })
  
    it('Checking all fields exists or not', () => {
        cy.get('#login_email');
        cy.get('#login_password');
        cy.get('#loginButton');
        cy.get(':nth-child(4) > .small').should('have.text', 'Forgot Password?');
        cy.get(':nth-child(5) > .small').should('have.text', 'Create an Account!');
    })

    it('Checking create an account button functionality', () => {
        const createAnAccount = cy.get(':nth-child(5) > .small');
        createAnAccount.click();
        cy.url().should('include','http://127.0.0.1:8000/register/');
    })

    it('Checking forgot password button functionality', () => {
        const forgotPassword = cy.get(':nth-child(4) > .small');
        forgotPassword.click();
        cy.url().should('include', 'http://127.0.0.1:8000/forgot-password/');
    });

    it('Trying to login with empty email and password', () => {
        const emailInput = cy.get('#login_email');
        emailInput.should('have.class', 'form-control')
        emailInput.should('have.class', 'form-control-user')
        emailInput.should('have.attr', 'placeholder', 'Enter Email Address...');

        const passwordInput = cy.get('#login_password');
        passwordInput.should('have.class', 'form-control');
        passwordInput.should('have.class', 'form-control-user')
        passwordInput.should('have.attr', 'placeholder', 'Enter password');
        
        cy.get('#loginButton').click();
        cy.get('#login_email_error').should('have.text', 'Please enter registered email id');
        cy.get('#login_password_error').should('have.text', 'Please enter password');
    });

    it('Trying to login with invalid credentails', () => {
        const emailInput = cy.get('#login_email');
        const passwordInput = cy.get('#login_password');

        emailInput.type('random@gmail.com');
        passwordInput.type('invalidPassword');
        
        cy.get('#loginButton').click();
        cy.get('#incorrect_details').should('have.text', 'Incorrect Details');
    });

    it('Trying to login with valid credentails', () => {
        const emailInput = cy.get('#login_email');
        const passwordInput = cy.get('#login_password');

        emailInput.type('sinerajarc@gmail.com');
        passwordInput.type('raja1234');
        
        cy.get('#loginButton').click();
        
        const prev_page = localStorage.getItem("prev_page");
        if (prev_page) {
           cy.url().should('include', prev_page);
        } else {
            cy.url().should('include', 'http://127.0.0.1:8000/');
        }
    });

    
})
  