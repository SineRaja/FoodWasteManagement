# Food Waste Management

## Installation

### Install virtualenv
pip install virtualenv

### Create venv
python -m venv .vecnv

### Activate venv
cd .venv/Scripts
activate
cd ..
cd ..
#Back to Project folder
### Install requirements
pip install -r requirements.txt



<!-- Steps for UI testing -->
### Framework used - Cypress
Prerequisites - node 

### install cypress
cd UITestcases
npm install

### Commands
npx cypress open

### UI test cases files execution
navbar.cy.js
navbarAfterLogin.cy.js
footer.cy.js
homePage.cy.js
registerPage.cy.js
loginPage.cy.js
forgotPasswordPage.cy.js
changePasswordPage.cy.js
requestPickUpPage.cy.js
myRequestsPage.cy.js
NgoMyRequestsPage.cy.js
contactPage.cy.js

### Migrations
python manage.py makemigrations
python manage.py migrate

### Run Server
python manage.py runserver

### Create Super admin
python manage.py createsuperuser

### Run Testcases
python manage.py test --pattern="*_tests.py" -v 2

python manage.py test app_name --pattern="*_tests.py" -v 2

### Coverage Report
coverage run --source='.' .\manage.py test --pattern="*_tests.py"

coverage run --source='app_name' .\manage.py test app_name --pattern="*_tests.py"

coverage report
