function createForm() {
  var form = FormApp.create('FIFA World Cup 2026 - Forudsigelser');
  form.setDescription('Udfyld dine forudsigelser inden turneringen starter den 11. juni 2026.');

  var scoreValidation = FormApp.createTextValidation()
    .requireTextMatchesPattern('^\\d+\\s*-\\s*\\d+$')
    .build();

  function addMatch(title, homeTeam, awayTeam) {
    form.addTextItem()
        .setTitle(title)
        .setHelpText(homeTeam + ' goals - ' + awayTeam + ' goals  (e.g. 2 - 1)')
        .setValidation(scoreValidation)
        .setRequired(true);
  }

  // ── Personal info ──────────────────────────────────────────────────
  form.addTextItem().setTitle('First name').setRequired(true);
  form.addTextItem().setTitle('Last name').setRequired(true);

  // ── Which team do you belong to? ───────────────────────────────────
  var tq = form.addCheckboxItem();
  tq.setTitle('Which team(s) do you belong to?')
    .setChoices([
      tq.createChoice('Danica Ejendomme'),
      tq.createChoice('Novo Nordisk'),
      tq.createChoice('Quantum and Laser Photonics DTU'),
      tq.createChoice('GeH Fys'),
      tq.createChoice('Frederiksborg Gymnasium'),
      tq.createChoice('Friends and Family'),
    ])
    .setRequired(true);

  // ── Group stage predictions ─────────────────────────────────────────
  form.addSectionHeaderItem().setTitle('Group A');
  addMatch('Group A Predictions [Mexico - South Africa]', 'Mexico', 'South Africa');
  addMatch('Group A Predictions [South Korea - Czechia]', 'South Korea', 'Czechia');
  addMatch('Group A Predictions [Czechia - South Africa]', 'Czechia', 'South Africa');
  addMatch('Group A Predictions [Mexico - South Korea]', 'Mexico', 'South Korea');
  addMatch('Group A Predictions [Czechia - Mexico]', 'Czechia', 'Mexico');
  addMatch('Group A Predictions [South Africa - South Korea]', 'South Africa', 'South Korea');

  form.addSectionHeaderItem().setTitle('Group B');
  addMatch('Group B Predictions [Canada - Bosnia-Herzegovina]', 'Canada', 'Bosnia-Herzegovina');
  addMatch('Group B Predictions [Qatar - Switzerland]', 'Qatar', 'Switzerland');
  addMatch('Group B Predictions [Switzerland - Bosnia-Herzegovina]', 'Switzerland', 'Bosnia-Herzegovina');
  addMatch('Group B Predictions [Canada - Qatar]', 'Canada', 'Qatar');
  addMatch('Group B Predictions [Switzerland - Canada]', 'Switzerland', 'Canada');
  addMatch('Group B Predictions [Bosnia-Herzegovina - Qatar]', 'Bosnia-Herzegovina', 'Qatar');

  form.addSectionHeaderItem().setTitle('Group C');
  addMatch('Group C Predictions [Brazil - Morocco]', 'Brazil', 'Morocco');
  addMatch('Group C Predictions [Haiti - Scotland]', 'Haiti', 'Scotland');
  addMatch('Group C Predictions [Scotland - Morocco]', 'Scotland', 'Morocco');
  addMatch('Group C Predictions [Brazil - Haiti]', 'Brazil', 'Haiti');
  addMatch('Group C Predictions [Morocco - Haiti]', 'Morocco', 'Haiti');
  addMatch('Group C Predictions [Scotland - Brazil]', 'Scotland', 'Brazil');

  form.addSectionHeaderItem().setTitle('Group D');
  addMatch('Group D Predictions [United States - Paraguay]', 'United States', 'Paraguay');
  addMatch('Group D Predictions [Australia - Turkey]', 'Australia', 'Turkey');
  addMatch('Group D Predictions [United States - Australia]', 'United States', 'Australia');
  addMatch('Group D Predictions [Turkey - Paraguay]', 'Turkey', 'Paraguay');
  addMatch('Group D Predictions [Turkey - United States]', 'Turkey', 'United States');
  addMatch('Group D Predictions [Paraguay - Australia]', 'Paraguay', 'Australia');

  form.addSectionHeaderItem().setTitle('Group E');
  addMatch('Group E Predictions [Germany - Curaçao]', 'Germany', 'Curaçao');
  addMatch('Group E Predictions [Ivory Coast - Ecuador]', 'Ivory Coast', 'Ecuador');
  addMatch('Group E Predictions [Germany - Ivory Coast]', 'Germany', 'Ivory Coast');
  addMatch('Group E Predictions [Ecuador - Curaçao]', 'Ecuador', 'Curaçao');
  addMatch('Group E Predictions [Ecuador - Germany]', 'Ecuador', 'Germany');
  addMatch('Group E Predictions [Curaçao - Ivory Coast]', 'Curaçao', 'Ivory Coast');

  form.addSectionHeaderItem().setTitle('Group F');
  addMatch('Group F Predictions [Netherlands - Japan]', 'Netherlands', 'Japan');
  addMatch('Group F Predictions [Sweden - Tunisia]', 'Sweden', 'Tunisia');
  addMatch('Group F Predictions [Netherlands - Sweden]', 'Netherlands', 'Sweden');
  addMatch('Group F Predictions [Tunisia - Japan]', 'Tunisia', 'Japan');
  addMatch('Group F Predictions [Tunisia - Netherlands]', 'Tunisia', 'Netherlands');
  addMatch('Group F Predictions [Japan - Sweden]', 'Japan', 'Sweden');

  form.addSectionHeaderItem().setTitle('Group G');
  addMatch('Group G Predictions [Belgium - Egypt]', 'Belgium', 'Egypt');
  addMatch('Group G Predictions [Iran - New Zealand]', 'Iran', 'New Zealand');
  addMatch('Group G Predictions [Belgium - Iran]', 'Belgium', 'Iran');
  addMatch('Group G Predictions [New Zealand - Egypt]', 'New Zealand', 'Egypt');
  addMatch('Group G Predictions [New Zealand - Belgium]', 'New Zealand', 'Belgium');
  addMatch('Group G Predictions [Egypt - Iran]', 'Egypt', 'Iran');

  form.addSectionHeaderItem().setTitle('Group H');
  addMatch('Group H Predictions [Spain - Cape Verde Islands]', 'Spain', 'Cape Verde Islands');
  addMatch('Group H Predictions [Saudi Arabia - Uruguay]', 'Saudi Arabia', 'Uruguay');
  addMatch('Group H Predictions [Spain - Saudi Arabia]', 'Spain', 'Saudi Arabia');
  addMatch('Group H Predictions [Uruguay - Cape Verde Islands]', 'Uruguay', 'Cape Verde Islands');
  addMatch('Group H Predictions [Uruguay - Spain]', 'Uruguay', 'Spain');
  addMatch('Group H Predictions [Cape Verde Islands - Saudi Arabia]', 'Cape Verde Islands', 'Saudi Arabia');

  form.addSectionHeaderItem().setTitle('Group I');
  addMatch('Group I Predictions [France - Senegal]', 'France', 'Senegal');
  addMatch('Group I Predictions [Iraq - Norway]', 'Iraq', 'Norway');
  addMatch('Group I Predictions [France - Iraq]', 'France', 'Iraq');
  addMatch('Group I Predictions [Norway - Senegal]', 'Norway', 'Senegal');
  addMatch('Group I Predictions [Norway - France]', 'Norway', 'France');
  addMatch('Group I Predictions [Senegal - Iraq]', 'Senegal', 'Iraq');

  form.addSectionHeaderItem().setTitle('Group J');
  addMatch('Group J Predictions [Argentina - Algeria]', 'Argentina', 'Algeria');
  addMatch('Group J Predictions [Austria - Jordan]', 'Austria', 'Jordan');
  addMatch('Group J Predictions [Argentina - Austria]', 'Argentina', 'Austria');
  addMatch('Group J Predictions [Jordan - Algeria]', 'Jordan', 'Algeria');
  addMatch('Group J Predictions [Jordan - Argentina]', 'Jordan', 'Argentina');
  addMatch('Group J Predictions [Algeria - Austria]', 'Algeria', 'Austria');

  form.addSectionHeaderItem().setTitle('Group K');
  addMatch('Group K Predictions [Portugal - Congo DR]', 'Portugal', 'Congo DR');
  addMatch('Group K Predictions [Uzbekistan - Colombia]', 'Uzbekistan', 'Colombia');
  addMatch('Group K Predictions [Portugal - Uzbekistan]', 'Portugal', 'Uzbekistan');
  addMatch('Group K Predictions [Colombia - Congo DR]', 'Colombia', 'Congo DR');
  addMatch('Group K Predictions [Colombia - Portugal]', 'Colombia', 'Portugal');
  addMatch('Group K Predictions [Congo DR - Uzbekistan]', 'Congo DR', 'Uzbekistan');

  form.addSectionHeaderItem().setTitle('Group L');
  addMatch('Group L Predictions [England - Croatia]', 'England', 'Croatia');
  addMatch('Group L Predictions [Ghana - Panama]', 'Ghana', 'Panama');
  addMatch('Group L Predictions [England - Ghana]', 'England', 'Ghana');
  addMatch('Group L Predictions [Panama - Croatia]', 'Panama', 'Croatia');
  addMatch('Group L Predictions [Panama - England]', 'Panama', 'England');
  addMatch('Group L Predictions [Croatia - Ghana]', 'Croatia', 'Ghana');

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

  var q = form.addListItem();
  q.setTitle('Who is going to be the top scorer throughout FIFA World Cup 2026? (20 points)')
   .setChoices([q.createChoice('Aleksandar Mitrovic'), q.createChoice('Alvaro Morata'), q.createChoice('Antoine Griezmann'), q.createChoice('Bukayo Saka'), q.createChoice('Christian Pulisic'), q.createChoice('Cody Gakpo'), q.createChoice('Darwin Nunez'), q.createChoice('Dusan Vlahovic'), q.createChoice('Erling Haaland'), q.createChoice('Ferran Torres'), q.createChoice('Florian Wirtz'), q.createChoice('Folarin Balogun'), q.createChoice('Harry Kane'), q.createChoice('Jude Bellingham'), q.createChoice('Julian Alvarez'), q.createChoice('Karim Benzema'), q.createChoice('Kylian Mbappe'), q.createChoice('Lamine Yamal'), q.createChoice('Lionel Messi'), q.createChoice('Mohamed Salah'), q.createChoice('Ollie Watkins'), q.createChoice('Pedri'), q.createChoice('Phil Foden'), q.createChoice('Raphinha'), q.createChoice('Richarlison'), q.createChoice('Robert Lewandowski'), q.createChoice('Romelu Lukaku'), q.createChoice('Serhou Guirassy'), q.createChoice('Victor Osimhen'), q.createChoice('Vinicius Junior')])
   .setRequired(true);

  var q = form.addListItem();
  q.setTitle('How many goals does the top scorer score? (10 points)')
   .setChoices([q.createChoice('1'), q.createChoice('2'), q.createChoice('3'), q.createChoice('4'), q.createChoice('5'), q.createChoice('6'), q.createChoice('7'), q.createChoice('8'), q.createChoice('9'), q.createChoice('10'), q.createChoice('11'), q.createChoice('12'), q.createChoice('13'), q.createChoice('14'), q.createChoice('15')])
   .setRequired(true);

  Logger.log('Form created: ' + form.getPublishedUrl());
  Logger.log('Edit URL:     ' + form.getEditUrl());
}