function saveInvoiceAttachments() {

  const folderId = "1EFJU_q7SugjvFlQkdcQ-Wrs5s48HLHLQ";
  const folder = DriveApp.getFolderById(folderId);
  const doneLabel = GmailApp.getUserLabelByName("Done") || GmailApp.createLabel("Done");
  const threads = GmailApp.search('label:Buchführung -label:Done');
  threads.forEach(thread => {
    let savedCount = 0;
    const messages = thread.getMessages();
    messages.forEach(message => {
      Logger.log(
        "E-Mail gefunden: Betreff='" + message.getSubject() +
        "', Von='" + message.getFrom() +
        "', Datum='" + message.getDate() + "'"
      );
      const attachments = message.getAttachments();
      attachments.forEach(att => {
        const contentType = att.getContentType();
        const fileName = att.getName();
        const isPdfAttachment = contentType === "application/pdf" ||
          (contentType === "application/octet-stream" && fileName.toLowerCase().endsWith(".pdf"));

        Logger.log(
          "Attachment gefunden: Name='" + fileName +
          "', Content-Type='" + contentType + "'"
        );
        if (isPdfAttachment) {
          folder.createFile(att);
          savedCount += 1;
          Logger.log("Gespeichert: " + fileName);
        }
      });
    });

    thread.addLabel(doneLabel);
    Logger.log("Thread als Done markiert. Gespeicherte PDFs: " + savedCount);
  });
}
