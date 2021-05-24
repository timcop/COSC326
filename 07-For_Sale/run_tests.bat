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
    java forsale.Test
)

@echo on
