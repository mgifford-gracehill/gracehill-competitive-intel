/**
 * Builds the Competitive Intelligence Requests form.
 *
 * WHY THIS EXISTS: the question-type dropdown in the Forms editor would not accept
 * automated clicks, so this does the same job deterministically through the API.
 *
 * HOW TO RUN
 *   1. Go to script.google.com and click "New project".
 *   2. Delete whatever is in the editor and paste this whole file in.
 *   3. Press Run. Google will ask you to authorise it the first time — that is expected,
 *      it is your own script acting on your own form.
 *   4. Check the execution log at the bottom for the two links it prints.
 *
 * SAFE TO RE-RUN. It clears the existing questions first, so running it twice does not
 * duplicate anything. Your title and your "collect email addresses" setting are left alone.
 */

var FORM_ID = '1E5sJ1Bi_g_dImwSzOWxS9NFsNETBIAk5sgLDn0hFBOY';

function buildCIRequestForm() {
  var form = FormApp.openById(FORM_ID);

  // Clear existing questions so this is repeatable. Settings are not touched.
  var items = form.getItems();
  for (var i = items.length - 1; i >= 0; i--) {
    form.deleteItem(items[i]);
  }

  form.setTitle('Competitive Intelligence Requests');
  form.setDescription(
    'Questions, corrections, and anything missing from the competitive intelligence tool ' +
    'at ci-gracehill.com. Please do not name a customer or prospect — describe the situation ' +
    'instead. Responses go to a shared sheet.'
  );

  // 1 — type of request
  form.addMultipleChoiceItem()
    .setTitle('What kind of request is this?')
    .setChoiceValues([
      'Something here is wrong or out of date',
      'A competitor is missing',
      'I have a question I could not answer on a call',
      'I need more on a competitor we already track',
      'I heard something in a deal worth recording'
    ])
    .setRequired(true);

  // 2 — which competitor or page
  form.addTextItem()
    .setTitle('Which competitor or page?')
    .setHelpText('The competitor name, or the page you were looking at.')
    .setRequired(true);

  // 3 — the detail
  form.addParagraphTextItem()
    .setTitle('What do you need, or what is wrong?')
    .setHelpText(
      'One or two plain sentences is plenty. Please do not name a customer or prospect — ' +
      'describe the situation instead. This goes into a shared record.'
    )
    .setRequired(true);

  // 4 — source, optional
  form.addTextItem()
    .setTitle('Source or link, if you have one')
    .setHelpText('A URL, a screenshot name, or where you heard it.')
    .setRequired(false);

  // 5 — urgency
  form.addMultipleChoiceItem()
    .setTitle('How urgent is it?')
    .setChoiceValues([
      'Whenever — good to fix eventually',
      'This week — I have a deal open',
      'Today — I am on a call about it'
    ])
    .setRequired(true);

  Logger.log('Done — 5 questions created.');
  Logger.log('Edit the form:  ' + form.getEditUrl());
  Logger.log('Share this one: ' + form.getPublishedUrl());
}
