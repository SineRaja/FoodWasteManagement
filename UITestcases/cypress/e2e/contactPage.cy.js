/// <reference types="cypress" />


describe('LoginPage FoodWaste Management', () => {
    beforeEach(() => {
        cy.viewport(1243, 844)
        cy.visit('http://127.0.0.1:8000/contact/')
        cy.get('.main-menu > .main-menu__main-menu-box > .main-menu__list > #contact').should('have.class', 'current');
    })
  
    it('Contactus Static Info', () => {
        cy.get(':nth-child(1) > .text > a').should('have.text', '+ 91 - 79898 01494');
        cy.get(':nth-child(2) > .text > a').should('have.text', 'needhelp@foodwastemanagement.com');
        cy.get('.text > span').should('have.text', '880 Leicester,Le2 1xp, England');
    })

    it('Checking all fields exists or not', () => {
        cy.get('#name').should('exist')
        cy.get('#email').should('exist')
        cy.get('#phone').should('exist')
        cy.get('#subject').should('exist')
        cy.get('#message').should('exist')
        cy.get('#contact-btn-submit').should('exist')
        
    })

    it('Trying to send a contact us mail with empty data', () => {
        const name = cy.get('#name');
        name.should('have.attr', 'placeholder', 'Your name');

        const email = cy.get('#email');
        email.should('have.attr', 'placeholder', 'Email address');

        const phone = cy.get('#phone');
        phone.should('have.attr', 'placeholder', 'Phone number');

        const subject = cy.get('#subject');
        subject.should('have.attr', 'placeholder', 'Subject');

        const message = cy.get('#message');
        message.should('have.attr', 'placeholder', 'Write message');
        
        cy.get('#contact-btn-submit').click({force: true});
        cy.get('#name_error').should('have.text', 'Please enter a name.');
        cy.get('#email_error').should('have.text', 'Please enter an email address.');
        cy.get('#phone_error').should('have.text', 'Please enter a phone number.');
        cy.get('#subject_error').should('have.text', 'Please enter a subject.');
        cy.get('#message_error').should('have.text', 'Please enter a message.');
    });
    it('Submitting contact us with valid data', async () => {
        const name = cy.get('#name');
        name.type('Sineraja', {force: true});
        const email = cy.get('#email');
        email.type('sineraja@gmail.com', {force: true});
        const phone = cy.get('#phone');
        phone.type('7989801494', {force: true});
        const subject = cy.get('#subject');
        subject.type('Feedback', {force: true});
        const message = cy.get('#message');
        message.type('Useful website', {force: true});
        await cy.get('#contact-btn-submit').click();
        cy.get('#res_message').should('have.text', 'Thanks for your feedback');
    });


})
  