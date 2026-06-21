on run argv
    if (count of argv) is not 2 then error "Usage: osascript transactions.applescript <from-date> <to-date>"

    set fromDate to item 1 of argv
    set toDate to item 2 of argv

    tell application "MoneyMoney"
        return export transactions from account "DKB-Business" from date fromDate to date toDate as "csv"
    end tell
end run

