function createForm() {
  var form = FormApp.create('FIFA World Cup 2026 - Forudsigelser');
  form.setDescription('Udfyld dine forudsigelser inden turneringen starter den 11. juni 2026.');

  var SCORES = ['0 - 0', '0 - 1', '1 - 0', '0 - 2', '1 - 1', '2 - 0', '0 - 3', '1 - 2', '2 - 1', '3 - 0', '0 - 4', '1 - 3', '2 - 2', '3 - 1', '4 - 0', '0 - 5', '1 - 4', '2 - 3', '3 - 2', '4 - 1', '5 - 0', '1 - 5', '2 - 4', '3 - 3', '4 - 2', '5 - 1', '2 - 5', '3 - 4', '4 - 3', '5 - 2', '3 - 5', '4 - 4', '5 - 3', '4 - 5', '5 - 4', '5 - 5'];

  function addMatch(title) {
    var q = form.addListItem();
    q.setTitle(title)
     .setChoices(SCORES.map(function(s) { return q.createChoice(s); }))
     .setRequired(true);
  }

  // ── Personal info ──────────────────────────────────────────────────
  form.addTextItem().setTitle('First name').setRequired(true);
  form.addTextItem().setTitle('Last name').setRequired(true);

  // ── Which team do you belong to? ───────────────────────────────────
  var tq = form.addCheckboxItem();
  tq.setTitle('Which team(s) do you belong to?')
    .setChoices([
      tq.createChoice('European Sperm Bank'),
      tq.createChoice('Frederiksborg Gymnasium'),
      tq.createChoice('Friends and Family'),
      tq.createChoice('GeH Fys'),
      tq.createChoice('Next11'),
      tq.createChoice('Quantum and Laser Photonics DTU'),
    ])
    .setRequired(true);

  // ── Group stage predictions ─────────────────────────────────────────
  form.addSectionHeaderItem().setTitle('Group A');
  addMatch('Group A Predictions [Mexico - South Africa]');
  addMatch('Group A Predictions [South Korea - Czechia]');
  addMatch('Group A Predictions [Czechia - South Africa]');
  addMatch('Group A Predictions [Mexico - South Korea]');
  addMatch('Group A Predictions [Czechia - Mexico]');
  addMatch('Group A Predictions [South Africa - South Korea]');

  form.addSectionHeaderItem().setTitle('Group B');
  addMatch('Group B Predictions [Canada - Bosnia-Herzegovina]');
  addMatch('Group B Predictions [Qatar - Switzerland]');
  addMatch('Group B Predictions [Switzerland - Bosnia-Herzegovina]');
  addMatch('Group B Predictions [Canada - Qatar]');
  addMatch('Group B Predictions [Switzerland - Canada]');
  addMatch('Group B Predictions [Bosnia-Herzegovina - Qatar]');

  form.addSectionHeaderItem().setTitle('Group C');
  addMatch('Group C Predictions [Brazil - Morocco]');
  addMatch('Group C Predictions [Haiti - Scotland]');
  addMatch('Group C Predictions [Scotland - Morocco]');
  addMatch('Group C Predictions [Brazil - Haiti]');
  addMatch('Group C Predictions [Morocco - Haiti]');
  addMatch('Group C Predictions [Scotland - Brazil]');

  form.addSectionHeaderItem().setTitle('Group D');
  addMatch('Group D Predictions [United States - Paraguay]');
  addMatch('Group D Predictions [Australia - Turkey]');
  addMatch('Group D Predictions [United States - Australia]');
  addMatch('Group D Predictions [Turkey - Paraguay]');
  addMatch('Group D Predictions [Turkey - United States]');
  addMatch('Group D Predictions [Paraguay - Australia]');

  form.addSectionHeaderItem().setTitle('Group E');
  addMatch('Group E Predictions [Germany - Curaçao]');
  addMatch('Group E Predictions [Ivory Coast - Ecuador]');
  addMatch('Group E Predictions [Germany - Ivory Coast]');
  addMatch('Group E Predictions [Ecuador - Curaçao]');
  addMatch('Group E Predictions [Ecuador - Germany]');
  addMatch('Group E Predictions [Curaçao - Ivory Coast]');

  form.addSectionHeaderItem().setTitle('Group F');
  addMatch('Group F Predictions [Netherlands - Japan]');
  addMatch('Group F Predictions [Sweden - Tunisia]');
  addMatch('Group F Predictions [Netherlands - Sweden]');
  addMatch('Group F Predictions [Tunisia - Japan]');
  addMatch('Group F Predictions [Tunisia - Netherlands]');
  addMatch('Group F Predictions [Japan - Sweden]');

  form.addSectionHeaderItem().setTitle('Group G');
  addMatch('Group G Predictions [Belgium - Egypt]');
  addMatch('Group G Predictions [Iran - New Zealand]');
  addMatch('Group G Predictions [Belgium - Iran]');
  addMatch('Group G Predictions [New Zealand - Egypt]');
  addMatch('Group G Predictions [New Zealand - Belgium]');
  addMatch('Group G Predictions [Egypt - Iran]');

  form.addSectionHeaderItem().setTitle('Group H');
  addMatch('Group H Predictions [Spain - Cape Verde Islands]');
  addMatch('Group H Predictions [Saudi Arabia - Uruguay]');
  addMatch('Group H Predictions [Spain - Saudi Arabia]');
  addMatch('Group H Predictions [Uruguay - Cape Verde Islands]');
  addMatch('Group H Predictions [Uruguay - Spain]');
  addMatch('Group H Predictions [Cape Verde Islands - Saudi Arabia]');

  form.addSectionHeaderItem().setTitle('Group I');
  addMatch('Group I Predictions [France - Senegal]');
  addMatch('Group I Predictions [Iraq - Norway]');
  addMatch('Group I Predictions [France - Iraq]');
  addMatch('Group I Predictions [Norway - Senegal]');
  addMatch('Group I Predictions [Norway - France]');
  addMatch('Group I Predictions [Senegal - Iraq]');

  form.addSectionHeaderItem().setTitle('Group J');
  addMatch('Group J Predictions [Argentina - Algeria]');
  addMatch('Group J Predictions [Austria - Jordan]');
  addMatch('Group J Predictions [Argentina - Austria]');
  addMatch('Group J Predictions [Jordan - Algeria]');
  addMatch('Group J Predictions [Jordan - Argentina]');
  addMatch('Group J Predictions [Algeria - Austria]');

  form.addSectionHeaderItem().setTitle('Group K');
  addMatch('Group K Predictions [Portugal - Congo DR]');
  addMatch('Group K Predictions [Uzbekistan - Colombia]');
  addMatch('Group K Predictions [Portugal - Uzbekistan]');
  addMatch('Group K Predictions [Colombia - Congo DR]');
  addMatch('Group K Predictions [Colombia - Portugal]');
  addMatch('Group K Predictions [Congo DR - Uzbekistan]');

  form.addSectionHeaderItem().setTitle('Group L');
  addMatch('Group L Predictions [England - Croatia]');
  addMatch('Group L Predictions [Ghana - Panama]');
  addMatch('Group L Predictions [England - Ghana]');
  addMatch('Group L Predictions [Panama - Croatia]');
  addMatch('Group L Predictions [Panama - England]');
  addMatch('Group L Predictions [Croatia - Ghana]');

  // ── Group winners ───────────────────────────────────────────────────
  form.addSectionHeaderItem().setTitle('Group winners');
  var q = form.addListItem();
  q.setTitle('Group A 1st place').setChoices([q.createChoice('Czechia'), q.createChoice('Mexico'), q.createChoice('South Africa'), q.createChoice('South Korea')]).setRequired(true);
  var q = form.addListItem();
  q.setTitle('Group A 2nd place').setChoices([q.createChoice('Czechia'), q.createChoice('Mexico'), q.createChoice('South Africa'), q.createChoice('South Korea')]).setRequired(true);
  var q = form.addListItem();
  q.setTitle('Group B 1st place').setChoices([q.createChoice('Bosnia-Herzegovina'), q.createChoice('Canada'), q.createChoice('Qatar'), q.createChoice('Switzerland')]).setRequired(true);
  var q = form.addListItem();
  q.setTitle('Group B 2nd place').setChoices([q.createChoice('Bosnia-Herzegovina'), q.createChoice('Canada'), q.createChoice('Qatar'), q.createChoice('Switzerland')]).setRequired(true);
  var q = form.addListItem();
  q.setTitle('Group C 1st place').setChoices([q.createChoice('Brazil'), q.createChoice('Haiti'), q.createChoice('Morocco'), q.createChoice('Scotland')]).setRequired(true);
  var q = form.addListItem();
  q.setTitle('Group C 2nd place').setChoices([q.createChoice('Brazil'), q.createChoice('Haiti'), q.createChoice('Morocco'), q.createChoice('Scotland')]).setRequired(true);
  var q = form.addListItem();
  q.setTitle('Group D 1st place').setChoices([q.createChoice('Australia'), q.createChoice('Paraguay'), q.createChoice('Turkey'), q.createChoice('United States')]).setRequired(true);
  var q = form.addListItem();
  q.setTitle('Group D 2nd place').setChoices([q.createChoice('Australia'), q.createChoice('Paraguay'), q.createChoice('Turkey'), q.createChoice('United States')]).setRequired(true);
  var q = form.addListItem();
  q.setTitle('Group E 1st place').setChoices([q.createChoice('Curaçao'), q.createChoice('Ecuador'), q.createChoice('Germany'), q.createChoice('Ivory Coast')]).setRequired(true);
  var q = form.addListItem();
  q.setTitle('Group E 2nd place').setChoices([q.createChoice('Curaçao'), q.createChoice('Ecuador'), q.createChoice('Germany'), q.createChoice('Ivory Coast')]).setRequired(true);
  var q = form.addListItem();
  q.setTitle('Group F 1st place').setChoices([q.createChoice('Japan'), q.createChoice('Netherlands'), q.createChoice('Sweden'), q.createChoice('Tunisia')]).setRequired(true);
  var q = form.addListItem();
  q.setTitle('Group F 2nd place').setChoices([q.createChoice('Japan'), q.createChoice('Netherlands'), q.createChoice('Sweden'), q.createChoice('Tunisia')]).setRequired(true);
  var q = form.addListItem();
  q.setTitle('Group G 1st place').setChoices([q.createChoice('Belgium'), q.createChoice('Egypt'), q.createChoice('Iran'), q.createChoice('New Zealand')]).setRequired(true);
  var q = form.addListItem();
  q.setTitle('Group G 2nd place').setChoices([q.createChoice('Belgium'), q.createChoice('Egypt'), q.createChoice('Iran'), q.createChoice('New Zealand')]).setRequired(true);
  var q = form.addListItem();
  q.setTitle('Group H 1st place').setChoices([q.createChoice('Cape Verde Islands'), q.createChoice('Saudi Arabia'), q.createChoice('Spain'), q.createChoice('Uruguay')]).setRequired(true);
  var q = form.addListItem();
  q.setTitle('Group H 2nd place').setChoices([q.createChoice('Cape Verde Islands'), q.createChoice('Saudi Arabia'), q.createChoice('Spain'), q.createChoice('Uruguay')]).setRequired(true);
  var q = form.addListItem();
  q.setTitle('Group I 1st place').setChoices([q.createChoice('France'), q.createChoice('Iraq'), q.createChoice('Norway'), q.createChoice('Senegal')]).setRequired(true);
  var q = form.addListItem();
  q.setTitle('Group I 2nd place').setChoices([q.createChoice('France'), q.createChoice('Iraq'), q.createChoice('Norway'), q.createChoice('Senegal')]).setRequired(true);
  var q = form.addListItem();
  q.setTitle('Group J 1st place').setChoices([q.createChoice('Algeria'), q.createChoice('Argentina'), q.createChoice('Austria'), q.createChoice('Jordan')]).setRequired(true);
  var q = form.addListItem();
  q.setTitle('Group J 2nd place').setChoices([q.createChoice('Algeria'), q.createChoice('Argentina'), q.createChoice('Austria'), q.createChoice('Jordan')]).setRequired(true);
  var q = form.addListItem();
  q.setTitle('Group K 1st place').setChoices([q.createChoice('Colombia'), q.createChoice('Congo DR'), q.createChoice('Portugal'), q.createChoice('Uzbekistan')]).setRequired(true);
  var q = form.addListItem();
  q.setTitle('Group K 2nd place').setChoices([q.createChoice('Colombia'), q.createChoice('Congo DR'), q.createChoice('Portugal'), q.createChoice('Uzbekistan')]).setRequired(true);
  var q = form.addListItem();
  q.setTitle('Group L 1st place').setChoices([q.createChoice('Croatia'), q.createChoice('England'), q.createChoice('Ghana'), q.createChoice('Panama')]).setRequired(true);
  var q = form.addListItem();
  q.setTitle('Group L 2nd place').setChoices([q.createChoice('Croatia'), q.createChoice('England'), q.createChoice('Ghana'), q.createChoice('Panama')]).setRequired(true);

  // ── Special predictions ─────────────────────────────────────────────
  form.addSectionHeaderItem().setTitle('Special predictions');
  var q = form.addListItem();
  q.setTitle('FIFA World Cup 2026 final winner').setChoices([q.createChoice('Algeria'), q.createChoice('Argentina'), q.createChoice('Australia'), q.createChoice('Austria'), q.createChoice('Belgium'), q.createChoice('Bosnia-Herzegovina'), q.createChoice('Brazil'), q.createChoice('Canada'), q.createChoice('Cape Verde Islands'), q.createChoice('Colombia'), q.createChoice('Congo DR'), q.createChoice('Croatia'), q.createChoice('Curaçao'), q.createChoice('Czechia'), q.createChoice('Ecuador'), q.createChoice('Egypt'), q.createChoice('England'), q.createChoice('France'), q.createChoice('Germany'), q.createChoice('Ghana'), q.createChoice('Haiti'), q.createChoice('Iran'), q.createChoice('Iraq'), q.createChoice('Ivory Coast'), q.createChoice('Japan'), q.createChoice('Jordan'), q.createChoice('Mexico'), q.createChoice('Morocco'), q.createChoice('Netherlands'), q.createChoice('New Zealand'), q.createChoice('Norway'), q.createChoice('Panama'), q.createChoice('Paraguay'), q.createChoice('Portugal'), q.createChoice('Qatar'), q.createChoice('Saudi Arabia'), q.createChoice('Scotland'), q.createChoice('Senegal'), q.createChoice('South Africa'), q.createChoice('South Korea'), q.createChoice('Spain'), q.createChoice('Sweden'), q.createChoice('Switzerland'), q.createChoice('Tunisia'), q.createChoice('Turkey'), q.createChoice('United States'), q.createChoice('Uruguay'), q.createChoice('Uzbekistan')]).setRequired(true);
  var q = form.addListItem();
  q.setTitle('FIFA World Cup 2026 final loser').setChoices([q.createChoice('Algeria'), q.createChoice('Argentina'), q.createChoice('Australia'), q.createChoice('Austria'), q.createChoice('Belgium'), q.createChoice('Bosnia-Herzegovina'), q.createChoice('Brazil'), q.createChoice('Canada'), q.createChoice('Cape Verde Islands'), q.createChoice('Colombia'), q.createChoice('Congo DR'), q.createChoice('Croatia'), q.createChoice('Curaçao'), q.createChoice('Czechia'), q.createChoice('Ecuador'), q.createChoice('Egypt'), q.createChoice('England'), q.createChoice('France'), q.createChoice('Germany'), q.createChoice('Ghana'), q.createChoice('Haiti'), q.createChoice('Iran'), q.createChoice('Iraq'), q.createChoice('Ivory Coast'), q.createChoice('Japan'), q.createChoice('Jordan'), q.createChoice('Mexico'), q.createChoice('Morocco'), q.createChoice('Netherlands'), q.createChoice('New Zealand'), q.createChoice('Norway'), q.createChoice('Panama'), q.createChoice('Paraguay'), q.createChoice('Portugal'), q.createChoice('Qatar'), q.createChoice('Saudi Arabia'), q.createChoice('Scotland'), q.createChoice('Senegal'), q.createChoice('South Africa'), q.createChoice('South Korea'), q.createChoice('Spain'), q.createChoice('Sweden'), q.createChoice('Switzerland'), q.createChoice('Tunisia'), q.createChoice('Turkey'), q.createChoice('United States'), q.createChoice('Uruguay'), q.createChoice('Uzbekistan')]).setRequired(true);

  form.addTextItem()
      .setTitle('Who is going to be the top scorer throughout FIFA World Cup 2026? (20 points)')
      .setRequired(true);

  var q = form.addListItem();
  q.setTitle('How many goals does the top scorer score? (10 points)')
   .setChoices([q.createChoice('1'), q.createChoice('2'), q.createChoice('3'), q.createChoice('4'), q.createChoice('5'), q.createChoice('6'), q.createChoice('7'), q.createChoice('8'), q.createChoice('9'), q.createChoice('10'), q.createChoice('11'), q.createChoice('12'), q.createChoice('13'), q.createChoice('14'), q.createChoice('15')])
   .setRequired(true);

  Logger.log('Form created: ' + form.getPublishedUrl());
  Logger.log('Edit URL:     ' + form.getEditUrl());
}