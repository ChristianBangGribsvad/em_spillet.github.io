function createForm() {
  var form = FormApp.create('FIFA World Cup 2026 - Forudsigelser');
  form.setDescription('Udfyld dine forudsigelser inden turneringen starter den 11. juni 2026.');

  var GOALS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];

  function addMatch(homeTitle, homeHelp, awayTitle, awayHelp) {
    var hq = form.addListItem();
    hq.setTitle(homeTitle).setHelpText(homeHelp)
      .setChoices(GOALS.map(function(g) { return hq.createChoice(g); }))
      .setRequired(true);
    var aq = form.addListItem();
    aq.setTitle(awayTitle).setHelpText(awayHelp)
      .setChoices(GOALS.map(function(g) { return aq.createChoice(g); }))
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
      tq.createChoice('European Sperm Bank'),
      tq.createChoice('Frederiksborg Gymnasium'),
      tq.createChoice('Friends and Family'),
      tq.createChoice('GeH Fys'),
      tq.createChoice('Quantum and Laser Photonics DTU'),
    ])
    .setRequired(true);

  // ── Group stage predictions ─────────────────────────────────────────
  form.addSectionHeaderItem().setTitle('Group A');
  addMatch('Group A Predictions [Mexico - South Africa] (home)', 'Mexico goals', 'Group A Predictions [Mexico - South Africa] (away)', 'South Africa goals');
  addMatch('Group A Predictions [South Korea - Czechia] (home)', 'South Korea goals', 'Group A Predictions [South Korea - Czechia] (away)', 'Czechia goals');
  addMatch('Group A Predictions [Czechia - South Africa] (home)', 'Czechia goals', 'Group A Predictions [Czechia - South Africa] (away)', 'South Africa goals');
  addMatch('Group A Predictions [Mexico - South Korea] (home)', 'Mexico goals', 'Group A Predictions [Mexico - South Korea] (away)', 'South Korea goals');
  addMatch('Group A Predictions [Czechia - Mexico] (home)', 'Czechia goals', 'Group A Predictions [Czechia - Mexico] (away)', 'Mexico goals');
  addMatch('Group A Predictions [South Africa - South Korea] (home)', 'South Africa goals', 'Group A Predictions [South Africa - South Korea] (away)', 'South Korea goals');

  form.addSectionHeaderItem().setTitle('Group B');
  addMatch('Group B Predictions [Canada - Bosnia-Herzegovina] (home)', 'Canada goals', 'Group B Predictions [Canada - Bosnia-Herzegovina] (away)', 'Bosnia-Herzegovina goals');
  addMatch('Group B Predictions [Qatar - Switzerland] (home)', 'Qatar goals', 'Group B Predictions [Qatar - Switzerland] (away)', 'Switzerland goals');
  addMatch('Group B Predictions [Switzerland - Bosnia-Herzegovina] (home)', 'Switzerland goals', 'Group B Predictions [Switzerland - Bosnia-Herzegovina] (away)', 'Bosnia-Herzegovina goals');
  addMatch('Group B Predictions [Canada - Qatar] (home)', 'Canada goals', 'Group B Predictions [Canada - Qatar] (away)', 'Qatar goals');
  addMatch('Group B Predictions [Switzerland - Canada] (home)', 'Switzerland goals', 'Group B Predictions [Switzerland - Canada] (away)', 'Canada goals');
  addMatch('Group B Predictions [Bosnia-Herzegovina - Qatar] (home)', 'Bosnia-Herzegovina goals', 'Group B Predictions [Bosnia-Herzegovina - Qatar] (away)', 'Qatar goals');

  form.addSectionHeaderItem().setTitle('Group C');
  addMatch('Group C Predictions [Brazil - Morocco] (home)', 'Brazil goals', 'Group C Predictions [Brazil - Morocco] (away)', 'Morocco goals');
  addMatch('Group C Predictions [Haiti - Scotland] (home)', 'Haiti goals', 'Group C Predictions [Haiti - Scotland] (away)', 'Scotland goals');
  addMatch('Group C Predictions [Scotland - Morocco] (home)', 'Scotland goals', 'Group C Predictions [Scotland - Morocco] (away)', 'Morocco goals');
  addMatch('Group C Predictions [Brazil - Haiti] (home)', 'Brazil goals', 'Group C Predictions [Brazil - Haiti] (away)', 'Haiti goals');
  addMatch('Group C Predictions [Morocco - Haiti] (home)', 'Morocco goals', 'Group C Predictions [Morocco - Haiti] (away)', 'Haiti goals');
  addMatch('Group C Predictions [Scotland - Brazil] (home)', 'Scotland goals', 'Group C Predictions [Scotland - Brazil] (away)', 'Brazil goals');

  form.addSectionHeaderItem().setTitle('Group D');
  addMatch('Group D Predictions [United States - Paraguay] (home)', 'United States goals', 'Group D Predictions [United States - Paraguay] (away)', 'Paraguay goals');
  addMatch('Group D Predictions [Australia - Turkey] (home)', 'Australia goals', 'Group D Predictions [Australia - Turkey] (away)', 'Turkey goals');
  addMatch('Group D Predictions [United States - Australia] (home)', 'United States goals', 'Group D Predictions [United States - Australia] (away)', 'Australia goals');
  addMatch('Group D Predictions [Turkey - Paraguay] (home)', 'Turkey goals', 'Group D Predictions [Turkey - Paraguay] (away)', 'Paraguay goals');
  addMatch('Group D Predictions [Turkey - United States] (home)', 'Turkey goals', 'Group D Predictions [Turkey - United States] (away)', 'United States goals');
  addMatch('Group D Predictions [Paraguay - Australia] (home)', 'Paraguay goals', 'Group D Predictions [Paraguay - Australia] (away)', 'Australia goals');

  form.addSectionHeaderItem().setTitle('Group E');
  addMatch('Group E Predictions [Germany - Curaçao] (home)', 'Germany goals', 'Group E Predictions [Germany - Curaçao] (away)', 'Curaçao goals');
  addMatch('Group E Predictions [Ivory Coast - Ecuador] (home)', 'Ivory Coast goals', 'Group E Predictions [Ivory Coast - Ecuador] (away)', 'Ecuador goals');
  addMatch('Group E Predictions [Germany - Ivory Coast] (home)', 'Germany goals', 'Group E Predictions [Germany - Ivory Coast] (away)', 'Ivory Coast goals');
  addMatch('Group E Predictions [Ecuador - Curaçao] (home)', 'Ecuador goals', 'Group E Predictions [Ecuador - Curaçao] (away)', 'Curaçao goals');
  addMatch('Group E Predictions [Ecuador - Germany] (home)', 'Ecuador goals', 'Group E Predictions [Ecuador - Germany] (away)', 'Germany goals');
  addMatch('Group E Predictions [Curaçao - Ivory Coast] (home)', 'Curaçao goals', 'Group E Predictions [Curaçao - Ivory Coast] (away)', 'Ivory Coast goals');

  form.addSectionHeaderItem().setTitle('Group F');
  addMatch('Group F Predictions [Netherlands - Japan] (home)', 'Netherlands goals', 'Group F Predictions [Netherlands - Japan] (away)', 'Japan goals');
  addMatch('Group F Predictions [Sweden - Tunisia] (home)', 'Sweden goals', 'Group F Predictions [Sweden - Tunisia] (away)', 'Tunisia goals');
  addMatch('Group F Predictions [Netherlands - Sweden] (home)', 'Netherlands goals', 'Group F Predictions [Netherlands - Sweden] (away)', 'Sweden goals');
  addMatch('Group F Predictions [Tunisia - Japan] (home)', 'Tunisia goals', 'Group F Predictions [Tunisia - Japan] (away)', 'Japan goals');
  addMatch('Group F Predictions [Tunisia - Netherlands] (home)', 'Tunisia goals', 'Group F Predictions [Tunisia - Netherlands] (away)', 'Netherlands goals');
  addMatch('Group F Predictions [Japan - Sweden] (home)', 'Japan goals', 'Group F Predictions [Japan - Sweden] (away)', 'Sweden goals');

  form.addSectionHeaderItem().setTitle('Group G');
  addMatch('Group G Predictions [Belgium - Egypt] (home)', 'Belgium goals', 'Group G Predictions [Belgium - Egypt] (away)', 'Egypt goals');
  addMatch('Group G Predictions [Iran - New Zealand] (home)', 'Iran goals', 'Group G Predictions [Iran - New Zealand] (away)', 'New Zealand goals');
  addMatch('Group G Predictions [Belgium - Iran] (home)', 'Belgium goals', 'Group G Predictions [Belgium - Iran] (away)', 'Iran goals');
  addMatch('Group G Predictions [New Zealand - Egypt] (home)', 'New Zealand goals', 'Group G Predictions [New Zealand - Egypt] (away)', 'Egypt goals');
  addMatch('Group G Predictions [New Zealand - Belgium] (home)', 'New Zealand goals', 'Group G Predictions [New Zealand - Belgium] (away)', 'Belgium goals');
  addMatch('Group G Predictions [Egypt - Iran] (home)', 'Egypt goals', 'Group G Predictions [Egypt - Iran] (away)', 'Iran goals');

  form.addSectionHeaderItem().setTitle('Group H');
  addMatch('Group H Predictions [Spain - Cape Verde Islands] (home)', 'Spain goals', 'Group H Predictions [Spain - Cape Verde Islands] (away)', 'Cape Verde Islands goals');
  addMatch('Group H Predictions [Saudi Arabia - Uruguay] (home)', 'Saudi Arabia goals', 'Group H Predictions [Saudi Arabia - Uruguay] (away)', 'Uruguay goals');
  addMatch('Group H Predictions [Spain - Saudi Arabia] (home)', 'Spain goals', 'Group H Predictions [Spain - Saudi Arabia] (away)', 'Saudi Arabia goals');
  addMatch('Group H Predictions [Uruguay - Cape Verde Islands] (home)', 'Uruguay goals', 'Group H Predictions [Uruguay - Cape Verde Islands] (away)', 'Cape Verde Islands goals');
  addMatch('Group H Predictions [Uruguay - Spain] (home)', 'Uruguay goals', 'Group H Predictions [Uruguay - Spain] (away)', 'Spain goals');
  addMatch('Group H Predictions [Cape Verde Islands - Saudi Arabia] (home)', 'Cape Verde Islands goals', 'Group H Predictions [Cape Verde Islands - Saudi Arabia] (away)', 'Saudi Arabia goals');

  form.addSectionHeaderItem().setTitle('Group I');
  addMatch('Group I Predictions [France - Senegal] (home)', 'France goals', 'Group I Predictions [France - Senegal] (away)', 'Senegal goals');
  addMatch('Group I Predictions [Iraq - Norway] (home)', 'Iraq goals', 'Group I Predictions [Iraq - Norway] (away)', 'Norway goals');
  addMatch('Group I Predictions [France - Iraq] (home)', 'France goals', 'Group I Predictions [France - Iraq] (away)', 'Iraq goals');
  addMatch('Group I Predictions [Norway - Senegal] (home)', 'Norway goals', 'Group I Predictions [Norway - Senegal] (away)', 'Senegal goals');
  addMatch('Group I Predictions [Norway - France] (home)', 'Norway goals', 'Group I Predictions [Norway - France] (away)', 'France goals');
  addMatch('Group I Predictions [Senegal - Iraq] (home)', 'Senegal goals', 'Group I Predictions [Senegal - Iraq] (away)', 'Iraq goals');

  form.addSectionHeaderItem().setTitle('Group J');
  addMatch('Group J Predictions [Argentina - Algeria] (home)', 'Argentina goals', 'Group J Predictions [Argentina - Algeria] (away)', 'Algeria goals');
  addMatch('Group J Predictions [Austria - Jordan] (home)', 'Austria goals', 'Group J Predictions [Austria - Jordan] (away)', 'Jordan goals');
  addMatch('Group J Predictions [Argentina - Austria] (home)', 'Argentina goals', 'Group J Predictions [Argentina - Austria] (away)', 'Austria goals');
  addMatch('Group J Predictions [Jordan - Algeria] (home)', 'Jordan goals', 'Group J Predictions [Jordan - Algeria] (away)', 'Algeria goals');
  addMatch('Group J Predictions [Jordan - Argentina] (home)', 'Jordan goals', 'Group J Predictions [Jordan - Argentina] (away)', 'Argentina goals');
  addMatch('Group J Predictions [Algeria - Austria] (home)', 'Algeria goals', 'Group J Predictions [Algeria - Austria] (away)', 'Austria goals');

  form.addSectionHeaderItem().setTitle('Group K');
  addMatch('Group K Predictions [Portugal - Congo DR] (home)', 'Portugal goals', 'Group K Predictions [Portugal - Congo DR] (away)', 'Congo DR goals');
  addMatch('Group K Predictions [Uzbekistan - Colombia] (home)', 'Uzbekistan goals', 'Group K Predictions [Uzbekistan - Colombia] (away)', 'Colombia goals');
  addMatch('Group K Predictions [Portugal - Uzbekistan] (home)', 'Portugal goals', 'Group K Predictions [Portugal - Uzbekistan] (away)', 'Uzbekistan goals');
  addMatch('Group K Predictions [Colombia - Congo DR] (home)', 'Colombia goals', 'Group K Predictions [Colombia - Congo DR] (away)', 'Congo DR goals');
  addMatch('Group K Predictions [Colombia - Portugal] (home)', 'Colombia goals', 'Group K Predictions [Colombia - Portugal] (away)', 'Portugal goals');
  addMatch('Group K Predictions [Congo DR - Uzbekistan] (home)', 'Congo DR goals', 'Group K Predictions [Congo DR - Uzbekistan] (away)', 'Uzbekistan goals');

  form.addSectionHeaderItem().setTitle('Group L');
  addMatch('Group L Predictions [England - Croatia] (home)', 'England goals', 'Group L Predictions [England - Croatia] (away)', 'Croatia goals');
  addMatch('Group L Predictions [Ghana - Panama] (home)', 'Ghana goals', 'Group L Predictions [Ghana - Panama] (away)', 'Panama goals');
  addMatch('Group L Predictions [England - Ghana] (home)', 'England goals', 'Group L Predictions [England - Ghana] (away)', 'Ghana goals');
  addMatch('Group L Predictions [Panama - Croatia] (home)', 'Panama goals', 'Group L Predictions [Panama - Croatia] (away)', 'Croatia goals');
  addMatch('Group L Predictions [Panama - England] (home)', 'Panama goals', 'Group L Predictions [Panama - England] (away)', 'England goals');
  addMatch('Group L Predictions [Croatia - Ghana] (home)', 'Croatia goals', 'Group L Predictions [Croatia - Ghana] (away)', 'Ghana goals');

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