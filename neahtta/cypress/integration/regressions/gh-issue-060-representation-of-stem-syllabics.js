describe('The stem of a syllabics analysis', function () {
  it('should be displayed in SRO', function () {
    cy.instantNeahttaSearch('crkS', 'eng', 'ka-kî-awâsisîwiyân');

    cy.contains('√awâsisîwi-')
  });
});
