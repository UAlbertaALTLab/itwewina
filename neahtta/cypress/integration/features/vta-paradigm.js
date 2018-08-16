/**
 * Test the display of a full VTA paradigm table.
 *
 * Test cases adpated from the YAML test cases in the Giellatekno,
 * namely:
 *
 * $GTLANG_crk/test/src/gt-norm-yamls/V-TA-kiskiswew_gt-norm.yaml
 */
describe("The full VTA paradigm table", function () {
  beforeEach(function () {
    // Search for the word.
    cy.visit('/crk/eng/');
    cy.neahttaSearch('kiskiswew');
    cy.contains('kîskiswêw')
      .click();

    // view the FULL paradigm
    cy.get('.nav')
      .contains('full').click();
  });

  it('should display all Prs, independent forms', function () {
    findAllWordforms([
      'kikîskison', 'kikîskisonân', 'kikîskisonân', 'kikîskisonâwâw', 'kikîskisotin', 'kikîskisotinân', 'kikîskisotinân', 'kikîskisotinâwâw', 'nikîskiswâw', 'kikîskiswâw', 'nikîskiswânân', 'kikîskiswânaw', 'kikîskiswâwâw', 'nikîskiswâwak', 'kikîskiswâwak', 'nikîskiswânânak', 'kikîskiswânawak', 'kikîskiswâwâwak', 'nikîskisomâwa', 'kikîskisomâwa', 'nikîskisomânâna', 'kikîskisomânawa', 'kikîskisomâwâwa', 'nikîskisok', 'kikîskisok', 'nikîskisokonân', 'kikîskisokonaw', 'kikîskisokowâw', 'nikîskisokowak', 'kîskisokwak', 'kikîskisokowak', 'kikîskisokwak', 'nikîskisokonânak', 'kikîskisokonawak', 'kikîskisokowâwak', 'nikîskisomâwa', 'kikîskisomâwa', 'nikîskisomânâna', 'kikîskisomânawa', 'kikîskisomâwâwa', 'kîskiswêw', 'kîskiswêwak', 'kîskiswêyiwa', 'kîskisomêw', 'kîskisomêwak', 'kîskisok', 'kîskisokow', 'kîskisokowak', 'kîskisokwak', 'kîskisokoyiwa',
    ]);
  });

  it('should display all Prs, conjunct forms', function () {
    findAllWordforms([
      'ê-kîskisoyan', 'ê-kîskisoyâhk', 'ê-kîskisoyâhk', 'ê-kîskisoyêk', 'ê-kîskisotân', 'ê-kîskisotâhk', 'ê-kîskisotâhk', 'ê-kîskisotakok', 'ê-kîskiswak', 'ê-kîskiswat', 'ê-kîskiswâyâhk', 'ê-kîskiswâyahk', 'ê-kîskiswâyêk', 'ê-kîskiswakik', 'ê-kîskiswacik', 'ê-kîskiswâyâhkik', 'ê-kîskiswâyahkok', 'ê-kîskiswâyêkok', 'ê-kîskisomak', 'ê-kîskisomat', 'ê-kîskisomâyâhk', 'ê-kîskisomâyahk', 'ê-kîskisomâyêk', 'ê-kîskisot', 'ê-kîskisosk', 'ê-kîskisokoyâhk', 'ê-kîskisokoyahk', 'ê-kîskisokoyêk', 'ê-kîskisocik', 'ê-kîskisoskik', 'ê-kîskisokoyâhkik', 'ê-kîskisokoyahkok', 'ê-kîskisokoyêkok', 'ê-kîskisomit', 'ê-kîskisomisk', 'ê-kîskisokoyâhk', 'ê-kîskisokoyahk', 'ê-kîskisokoyêk', 'ê-kîskiswât', 'ê-kîskiswâcik', 'ê-kîskiswâyit', 'ê-kîskisomât', 'ê-kîskisomâcik', 'ê-kîskisokot', 'ê-kîskisokocik', 'ê-kîskisokoyit',
    ]);
  });

  it('should display all future conditional forms', function () {
    findAllWordforms([
      'kîskisoyani', 'kîskisoyâhki', 'kîskisoyâhki', 'kîskisoyêko', 'kîskisotâni', 'kîskisotâhki', 'kîskisotâhki', 'kîskisotako', 'kîskiswaki', 'kîskiswaci', 'kîskiswâyâhki', 'kîskiswâyahko', 'kîskiswâyahki', 'kîskiswâyêko', 'kîskiswakwâwi', 'kîskiswatwâwi', 'kîskiswâyâhkwâwi', 'kîskiswâyahkwâwi', 'kîskiswâyêkwâwi', 'kîskisomaki', 'kîskisomaci', 'kîskisomâyâhki', 'kîskisomâyahko', 'kîskisomâyahki', 'kîskisomâyêko', 'kîskisoci', 'kîskisoski', 'kîskisokoyâhki', 'kîskisokoyahko', 'kîskisokoyahki', 'kîskisokoyêko', 'kîskisotwâwi', 'kîskisoskwâwi', 'kîskisokoyâhkwâwi', 'kîskisokoyahkwâwi', 'kîskisokoyêkwâwi', 'kîskisomici', 'kîskisomiski', 'kîskisokoyâhki', 'kîskisokoyahko', 'kîskisokoyahki', 'kîskisokoyêko', 'kîskiswâci', 'kîskiswâtwâwi', 'kîskiswâyici', 'kîskisomâci', 'kîskisomâtwâwi', 'kîskisokoci', 'kîskisokotwâwi', 'kîskisokoyici',
    ]);
  });

  it('should display all imperative forms', function () {
    findAllWordforms([
      'kîskison', 'kîskisonân', 'kîskisonân', 'kîskisok', 'kîskisôhkan', 'kîskisôhkâhk', 'kîskisôhkâhk', 'kîskisôhkêk', 'kîskis', 'kîskisohk', 'kîskiswâtân', 'kîskisok', 'kîskisohkok', 'kîskiswâtânik', 'kîskiswâhkan', 'kîskiswâhkêk', 'kîskiswâhkahk', 'kîskiswâhkanik', 'kîskiswâhkêkok', 'kîskiswâhkahkok',
    ]);
  });

  it('should display all Prt, independent forms', function () {
    findAllWordforms([
      'kikî-kîskison', 'kikî-kîskisonân', 'kikî-kîskisonân', 'kikî-kîskisonâwâw', 'kikî-kîskisotin', 'kikî-kîskisotinân', 'kikî-kîskisotinân', 'kikî-kîskisotinâwâw',
    ]);
  });

  it('should display all Prt, conjunct forms', function () {
    findAllWordforms([
      'ê-kî-kîskisoyan', 'ê-kî-kîskisoyâhk', 'ê-kî-kîskisoyâhk', 'ê-kî-kîskisoyêk', 'ê-kî-kîskisotân', 'ê-kî-kîskisotâhk', 'ê-kî-kîskisotâhk', 'ê-kî-kîskisotakok',
    ]);
  });

  it('should display all Fut+Int, independent forms', function () {
    findAllWordforms([
      'kiwî-kîskison', 'kiwî-kîskisonân', 'kiwî-kîskisonân', 'kiwî-kîskisonâwâw', 'kiwî-kîskisotin', 'kiwî-kîskisotinân', 'kiwî-kîskisotinân', 'kiwî-kîskisotinâwâw',
    ]);
  });

  it('should display all Fut+Int, conjunct forms', function () {
    findAllWordforms([
      'ê-wî-kîskisoyan', 'ê-wî-kîskisoyâhk', 'ê-wî-kîskisoyâhk', 'ê-wî-kîskisoyêk', 'ê-wî-kîskisotân', 'ê-wî-kîskisotâhk', 'ê-wî-kîskisotâhk', 'ê-wî-kîskisotakok',
    ]);
  });

  it('should display all Fut+Def forms', function () {
    findAllWordforms([
      'kika-kîskison', 'kika-kîskisonân', 'kika-kîskisonân', 'kika-kîskisonâwâw', 'kika-kîskisotin', 'kika-kîskisotinân', 'kika-kîskisotinân', 'kika-kîskisotinâwâw',
    ]);
  });

  function findAllWordforms(forms) {
    for (let wordform of forms) {
      const paradigmTable = cy.get('table[data-type="full"]');
      paradigmTable.contains(wordform)
        .should('be.visible');
    }
  };
});
