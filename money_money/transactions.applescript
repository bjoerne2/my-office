on run argv
    set currentScriptPath to POSIX path of (path to me)
    set currentDir to do shell script "dirname " & quoted form of currentScriptPath
    set targetScript to currentDir & "/applescript/transactions.applescript"

    set shellArgs to ""
    repeat with currentArg in argv
        set shellArgs to shellArgs & " " & quoted form of (currentArg as text)
    end repeat

    return do shell script "osascript " & quoted form of targetScript & shellArgs
end run
