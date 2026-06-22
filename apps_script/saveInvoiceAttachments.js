function saveInvoiceAttachments() {

  const folderId = "1EFJU_q7SugjvFlQkdcQ-Wrs5s48HLHLQ";
  const folder = DriveApp.getFolderById(folderId);
  const threads = GmailApp.search('label:Buchführung');
  threads.forEach(thread => {
    const messages = thread.getMessages();
    messages.forEach(message => {
      const attachments = message.getAttachments();
      attachments.forEach(att => {
        if (att.getContentType() === "application/pdf") {
          folder.createFile(att);
          Logger.log("Gespeichert: " + att.getName());
        }
      });
    });
  });
}
