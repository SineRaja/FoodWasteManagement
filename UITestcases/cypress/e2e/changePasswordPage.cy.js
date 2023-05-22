/// <reference types="cypress" />


describe('Change Password Page FoodWaste Management', () => {
    beforeEach(() => {
        cy.viewport(1243, 844)
        cy.visit('http://127.0.0.1:8000/login/');
        const emailInput = cy.get('#login_email');
        const passwordInput = cy.get('#login_password');

        emailInput.type('sinerajarc@gmail.com');
        passwordInput.type('raja1234');
        
        cy.get('#loginButton').click();
        cy.wait(1000);
        cy.visit('http://127.0.0.1:8000/change-password/')
    })
  
    it('Checking all fields exists or not', () => {
        cy.get('#old_password')
        cy.get('#password')
        cy.get('#confirm_password')
        cy.get('#changePassword')
    })

    it('Trying to change password with empty data', () => {
        const old_password = cy.get('#old_password')
        old_password.should('have.class', 'form-control')
        old_password.should('have.class', 'form-control-user')
        old_password.should('have.attr', 'placeholder', 'Enter Old Password');
        
        const password = cy.get('#password')
        password.should('have.class', 'form-control')
        password.should('have.class', 'form-control-user')
        password.should('have.attr', 'placeholder', 'Enter New Password');
        
        const cpassword = cy.get('#confirm_password')
        cpassword.should('have.class', 'form-control')
        cpassword.should('have.class', 'form-control-user')
        cpassword.should('have.attr', 'placeholder', 'Confirm New Password');

        const changePassword = cy.get('#changePassword');
        changePassword.click();
        
        cy.get('#old_password_error').should('have.text', 'Please enter old password');
        cy.get('#password_error').should('have.text', 'Please enter password');

    });

    it('Trying to change password with different password and confirm password', () => {
        const old_password = cy.get('#old_password')
        const password = cy.get('#password')
        const cpassword = cy.get('#confirm_password')
        
        old_password.type('somepassword', {force: true});
        password.type('password', {force: true});
        cpassword.type('differentpassword', {force: true});
        
        const changePassword = cy.get('#changePassword');
        changePassword.click();
        
        cy.get('#confirm_password_error').should('have.text', "Passwords didn't match");

    });

    it('Trying to change password with incorrect old password', () => {
        cy.get('#old_password').type('somepassword', {force: true});
        cy.get('#password').type('newsineraja', {force: true});
        cy.get('#confirm_password').type('newsineraja', {force: true});
        
        cy.get('#changePassword').click();
        
        cy.get('#old_password_error').should('have.text', 'Invalid Old Password');   
    })

    it('Change password with valid data', async () => {
        
        cy.get('#old_password').type('password', {force: true});
        cy.get('#password').type('password', {force: true});
        cy.get('#confirm_password').type('password', {force: true});
        cy.get('#changePassword').click();
        cy.get('.swal-modal')
        cy.get('.swal-text').should('have.text', 'Password reset Successful');
        cy.get('.swal-button').click();
        cy.url().should('include', 'http://127.0.0.1:8000/');
    });
})
