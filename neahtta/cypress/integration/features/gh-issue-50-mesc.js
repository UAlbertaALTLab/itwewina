describe('Our collaboration with MESC', function () {
  it('should be mentioned on the about page', function () {
    cy.visit('/about/');

    cy.contains('Maskwacîs Education Schools Commission')
      .should('be.visible');
  });
});
