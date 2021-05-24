@echo off

echo Welcome, this will run forsale.Test
:: Set amount of times to run from user input
set /P numToRun= Please enter how many times to run the program:

set /a numParam = 1000
set /a strParam = 1000

setlocal enabledelayedexpansion enableextensions

javac -d . Source/*.java Source/strategies/*.java
break>scores.txt
:: Start looping here while increasing the jar pars
:: Loop from 0 to numToRun
for /L %%i in (1 1 %numToRun%) do (
    set /a numParam = !numParam! * 2
    set /a strParam = !strParam! * 2
    java forsale.Test !numParam! !strParam!

    :: The two lines below are used for testing
    echo %numParam%  !numParam!
    echo %strParam%  !strParam!
)

@echo on
