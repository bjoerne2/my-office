function saveInvoiceAttachments() {

  const folderId = "1EFJU_q7SugjvFlQkdcQ-Wrs5s48HLHLQ";
  const baseFolder = DriveApp.getFolderById(folderId);
  const doneLabel = GmailApp.getUserLabelByName("Done") || GmailApp.createLabel("Done");
  const labelConfigs = [
    { gmailLabel: "Buchführung/AWS", driveFolderName: "AWS" },
    { gmailLabel: "Buchführung/GitHub", driveFolderName: "GitHub" },
    { gmailLabel: "Buchführung/Google", driveFolderName: "Google" },
    { gmailLabel: "Buchführung/hosting.de", driveFolderName: "hosting.de" }
  ];

  labelConfigs.forEach(config => {
    const targetFolder = getOrCreateSubFolder(baseFolder, config.driveFolderName);
    const threads = GmailApp.search('label:"' + config.gmailLabel + '" -label:Done');

    Logger.log(
      "Verarbeite Label '" + config.gmailLabel + "' in Drive-Unterordner '" +
      config.driveFolderName + "'. Gefundene Threads: " + threads.length
    );

    threads.forEach(thread => {
      let savedCount = 0;
      const messages = thread.getMessages();
      messages.forEach(message => {
        Logger.log(
          "E-Mail gefunden: Label='" + config.gmailLabel +
          "', Betreff='" + message.getSubject() +
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
            "Attachment gefunden: Label='" + config.gmailLabel +
            "', Name='" + fileName +
            "', Content-Type='" + contentType + "'"
          );
          if (isPdfAttachment) {
            const existingFiles = targetFolder.getFilesByName(fileName);
            if (existingFiles.hasNext()) {
              Logger.log(
                "Übersprungen, Datei existiert bereits in Drive-Unterordner '" +
                config.driveFolderName + "': " + fileName
              );
            } else {
              targetFolder.createFile(att);
              savedCount += 1;
              Logger.log(
                "Gespeichert in '" + config.driveFolderName + "': " + fileName
              );
            }
          }
        });
      });

      thread.addLabel(doneLabel);
      Logger.log(
        "Thread für Label '" + config.gmailLabel +
        "' als Done markiert. Gespeicherte PDFs: " + savedCount
      );
    });
  });
}

function getOrCreateSubFolder(parentFolder, folderName) {
  const folders = parentFolder.getFoldersByName(folderName);
  if (folders.hasNext()) {
    return folders.next();
  }

  Logger.log("Drive-Unterordner wird erstellt: " + folderName);
  return parentFolder.createFolder(folderName);
}
