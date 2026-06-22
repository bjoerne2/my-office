function saveInvoiceAttachments() {

  const folderId = "1EFJU_q7SugjvFlQkdcQ-Wrs5s48HLHLQ";
  const folder = DriveApp.getFolderById(folderId);
  const doneLabel = GmailApp.getUserLabelByName("Done") || GmailApp.createLabel("Done");
  const threads = GmailApp.search('label:Buchführung -label:Done');
  threads.forEach(thread => {
    let savedCount = 0;
    const messages = thread.getMessages();
    messages.forEach(message => {
      const attachments = message.getAttachments();
      attachments.forEach(att => {
        if (att.getContentType() === "application/pdf") {
          folder.createFile(att);
          savedCount += 1;
          Logger.log("Gespeichert: " + att.getName());
        }
      });
    });

    thread.addLabel(doneLabel);
    Logger.log("Thread als Done markiert. Gespeicherte PDFs: " + savedCount);
  });
}
