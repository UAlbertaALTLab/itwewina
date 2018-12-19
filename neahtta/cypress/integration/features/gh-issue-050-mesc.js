describe('Our collaboration with MESC', function () {
  it('should be mentioned on the about page', function () {
    cy.visit('/about/');

    cy.contains('Maskwacîs Education Schools Commission')
      .should('be.visible');
  });

  it('should be displayed as a logo on the about page', function () {
    cy.visit('/about/');

    // It should have an alt caption with "Maskwacîs" in it. 
    cy.get('img[alt~="Maskwacîs" i]')
      .should('be.visible');
  });

  it('should be displayed as a logo on the front page', function () {
    cy.visit('/');

    // It should have an alt caption with "Maskwacîs" in it. 
    cy.get('img[alt~="Maskwacîs" i]')
      .should('be.visible');
  });
});
