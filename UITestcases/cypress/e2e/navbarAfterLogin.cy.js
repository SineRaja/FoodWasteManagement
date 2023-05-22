
/// <reference types="cypress" />


describe('LoginPage FoodWaste Management', () => {
    beforeEach(() => {
        cy.viewport(1243, 844)
        cy.visit('http://127.0.0.1:8000/login/');
        const emailInput = cy.get('#login_email');
        const passwordInput = cy.get('#login_password');

        emailInput.type('sinerajarc@gmail.com');
        passwordInput.type('raja1234');
        
        cy.get('#loginButton').click();
        cy.wait(2000);
    })
  
    it('Navbar items', () => {
        cy.get('.main-header__logo > a > img');
    
        cy.get('.main-menu > .main-menu__main-menu-box > .main-menu__list > #home > a').should('have.text', 'Home');
        cy.get('.main-menu > .main-menu__main-menu-box > .main-menu__list > #about_us > a').should('have.text', 'About');
        cy.get('.main-menu > .main-menu__main-menu-box > .main-menu__list > #gallery > a').should('have.text', 'Gallery');
        cy.get('.main-menu > .main-menu__main-menu-box > .main-menu__list > #contact > a').should('have.text', 'Contact');
        cy.get('.main-menu > .main-menu__main-menu-box > .main-menu__list > .dropdown > #user_name').realHover();
        cy.get('.sticky-header__content > .main-menu__main-menu-box > .main-menu__list > .dropdown > ul > :nth-child(1) > a').should('have.text', 'Change Password');
        cy.get('.sticky-header__content > .main-menu__main-menu-box > .main-menu__list > .dropdown > ul > :nth-child(2) > a').should('have.text', 'My Requests');
        cy.get('.sticky-header__content > .main-menu__main-menu-box > .main-menu__list > .dropdown > ul > :nth-child(3) > a').should('have.text', 'Logout');
    })
    
    it('Navbar onclick redirections', () => {
        cy.get('.main-menu > .main-menu__main-menu-box > .main-menu__list > #about_us > a').click();
        cy.url().should('include', 'http://127.0.0.1:8000/about-us/');
        cy.get('.main-menu > .main-menu__main-menu-box > .main-menu__list > #gallery > a').click();
        cy.url().should('include', 'http://127.0.0.1:8000/gallery/');
        cy.get('.main-menu > .main-menu__main-menu-box > .main-menu__list > #contact > a').click();
        cy.url().should('include', 'http://127.0.0.1:8000/contact/');
        cy.get('.main-menu > .main-menu__main-menu-box > .main-menu__list > #home > a').click();
        cy.url().should('include', 'http://127.0.0.1:8000/');
        cy.get('.main-header__logo > a > img').click();
        cy.url().should('include', 'http://127.0.0.1:8000/');
        cy.get('.main-menu > .main-menu__main-menu-box > .main-menu__list > .dropdown > #user_name').realHover();
        cy.get('.sticky-header__content > .main-menu__main-menu-box > .main-menu__list > .dropdown > ul > :nth-child(1) > a').click({force: true});
        cy.url().should('include', 'http://127.0.0.1:8000/change-password/');
        cy.get('.sticky-header__content > .main-menu__main-menu-box > .main-menu__list > .dropdown > ul > :nth-child(2) > a').click({force: true});
        cy.url().should('include', 'http://127.0.0.1:8000/my-requests/');
        cy.get('.sticky-header__content > .main-menu__main-menu-box > .main-menu__list > .dropdown > ul > :nth-child(3) > a').click({force: true});
        cy.url().should('include', 'http://127.0.0.1:8000/logout/');
        
    })

})
