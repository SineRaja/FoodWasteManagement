/// <reference types="cypress" />


describe('Register Page FoodWaste Management', () => {
    beforeEach(() => {
        cy.viewport(1243, 844)
        cy.visit('http://127.0.0.1:8000/register/')
        cy.get('.main-menu > .main-menu__main-menu-box > .main-menu__list > #login').should('have.class', 'current');
    })
  
    it('Checking all fields exists or not', () => {
        cy.get('#first_name')
        cy.get('#last_name')
        cy.get('#phone_no')
        cy.get('#email')
        cy.get('#password')
        cy.get('#cpassword')
        cy.get('#donor')
        cy.get('#ngo')
        cy.get('#terms_and_condistions')
        cy.get('#registerButton')
        cy.get(':nth-child(4) > .small').should('have.text', 'Forgot Password?');
        cy.get(':nth-child(5) > .small').should('have.text', 'Already have an account? Login!');
    })

    it('Checking login link functionality', () => {
        const createAnAccount = cy.get(':nth-child(5) > .small');
        createAnAccount.click();
        cy.url().should('include','http://127.0.0.1:8000/login/');
    })

    it('Checking forgot password functionality', () => {
        const forgotPassword = cy.get(':nth-child(4) > .small');
        forgotPassword.click();
        cy.url().should('include', 'http://127.0.0.1:8000/forgot-password/');
    });

    it('Trying to register with empty data', () => {
        const first_name = cy.get('#first_name')
        first_name.should('have.class', 'form-control')
        first_name.should('have.class', 'form-control-user')
        first_name.should('have.attr', 'placeholder', 'First Name');

        const last_name = cy.get('#last_name')
        last_name.should('have.class', 'form-control')
        last_name.should('have.class', 'form-control-user')
        last_name.should('have.attr', 'placeholder', 'Last Name');

        const phone_no = cy.get('#phone_no')
        phone_no.should('have.class', 'form-control')
        phone_no.should('have.class', 'form-control-user')
        phone_no.should('have.attr', 'placeholder', 'Phone Number');
        
        const email = cy.get('#email')
        email.should('have.class', 'form-control')
        email.should('have.class', 'form-control-user')
        email.should('have.attr', 'placeholder', 'Email Address');

        const password = cy.get('#password')
        password.should('have.class', 'form-control')
        password.should('have.class', 'form-control-user')
        password.should('have.attr', 'placeholder', 'Password');
        
        const cpassword = cy.get('#cpassword')
        cpassword.should('have.class', 'form-control')
        cpassword.should('have.class', 'form-control-user')
        cpassword.should('have.attr', 'placeholder', 'Repeat Password');
        
        const donor = cy.get('#donor')
        donor.should('have.attr', 'value', 'DONOR');

        const ngo = cy.get('#ngo')
        ngo.should('have.attr', 'value', 'NGO');

        cy.get('#terms_and_condistions')

        const registerButton = cy.get('#registerButton');
        registerButton.click();
        
        cy.get('#first_name_error').should('have.text', 'Please enter first name');
        cy.get('#last_name_error').should('have.text', 'Please enter last name');
        cy.get('#phone_no_error').should('have.text', 'Please enter phone number');
        cy.get('#email_error').should('have.text', 'Please enter email id');
        cy.get('#password_error').should('have.text', 'Please enter password');
        cy.get('#cpassword_error').should('have.text', 'Please enter confirm password');
        cy.get('#terms_and_condistions_error').should('have.text', 'Please select on terms and conditions');

    });

    it('Trying to register with wrong email id, phone no and different password confirm password', () => {
        const phone_no = cy.get('#phone_no')
        const email = cy.get('#email')
        const password = cy.get('#password')
        const cpassword = cy.get('#cpassword')
        
        phone_no.type('789344433', {force: true});
        email.type('random', {force: true});
        password.type('password', {force: true});
        cpassword.type('differentpassword', {force: true});
        
        const registerButton = cy.get('#registerButton');
        registerButton.click();
        
        cy.get('#phone_no_error').should('have.text', 'Please enter 10 numbers');
        cy.get('#email_error').should('have.text', 'Please enter valid mail id');
        cy.get('#cpassword_error').should('have.text', 'Password and confirm password should be same');

    });

    it('Trying to register with existing email id', () => {
        cy.get('#first_name').type('Sine', {force: true});
        cy.get('#last_name').type('Raja', {force: true});
        cy.get('#phone_no').type(7893444336, {force: true});
        cy.get('#email').type('sinerajarc@gmail.com', {force: true});
        cy.get('#password').type('sineraja', {force: true});
        cy.get('#cpassword').type('sineraja', {force: true});
        cy.get('#terms_and_condistions').check({force: true});
        cy.get('#registerButton').click();
        
        cy.get('#email_error').should('have.text', 'user with this email address already exists.');   
    })

    it('Register with valid data', async () => {
        cy.get('#first_name').type('Sine', {force: true});
        cy.get('#last_name').type('Raja', {force: true});
        cy.get('#phone_no').type(7893444336, {force: true});
        const random = Math.floor(Math.random() * (100));
        cy.get('#email').type(`sinerajarc+acc${random}@gmail.com`, {force: true});
        cy.get('#password').type('raja1234', {force: true});
        cy.get('#cpassword').type('raja1234', {force: true});
        cy.get('#terms_and_condistions').check({force: true});
        await cy.get('#registerButton').click();
        cy.get('.swal-modal')
        cy.get('.swal-text').should('have.text', `Verification mail has been sent to sinerajarc+acc${random}@gmail.com`);
        cy.get('.swal-button').click();
        cy.url().should('include', 'http://127.0.0.1:8000/login/');
    });

    
})
  