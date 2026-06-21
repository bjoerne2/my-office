on run argv
    set currentScriptPath to POSIX path of (path to me)
    set currentDir to do shell script "dirname " & quoted form of currentScriptPath
    set targetScript to currentDir & "/applescript/accounts.applescript"

    return do shell script "osascript " & quoted form of targetScript
end run
