// Backup for form submissions: paste into a Google Sheet's Extensions > Apps Script,
// then Deploy > New deployment > Web app (Execute as: Me, Who has access: Anyone).
// Put the web app URL in the Worker secret SHEET_WEBHOOK_URL.
function doPost(e) {
  var d = JSON.parse(e.postData.contents);
  var name = [d.first_name, d.last_name].filter(Boolean).join(" ") || d.name || "Someone";
  var known = { form: 1, page: 1, name: 1, first_name: 1, last_name: 1, email: 1, message: 1, submittedAt: 1, site: 1 };
  var extras = Object.keys(d).filter(function (k) { return !known[k]; })
    .map(function (k) { return k + ": " + d[k]; }).join("\n");

  SpreadsheetApp.getActiveSpreadsheet().getSheets()[0]
    .appendRow([d.submittedAt, d.form, d.page, name, d.email, d.message, extras]);

  MailApp.sendEmail({
    to: Session.getEffectiveUser().getEmail(),
    replyTo: d.email,
    subject: name + " wrote in on " + d.site,
    body: (d.message || "(no message)") + "\n\n---\n" + d.email + "\n" + d.form + " on " + d.page + (extras ? "\n" + extras : ""),
  });
  return ContentService.createTextOutput("ok");
}
