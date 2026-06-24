on run argv
    if (count of argv) is not 3 then error "Usage: osascript transactions.applescript <account-name> <from-date> <to-date>"

    set accountName to item 1 of argv
    set fromDate to item 2 of argv
    set toDate to item 3 of argv

    tell application "MoneyMoney"
        return export transactions from account accountName from date fromDate to date toDate as "csv"
    end tell
end run

