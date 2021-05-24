echo Welcome, this will run forsale.Test

# Set amount of times to run from user input
read -p "Please enter how many times to run the program: " numToRun

javac -d . Source/*.java Source/strategies/*.java

# Loop from 0 to numToRun
for i in 0...$numToRun
do
    java forsale.Test > scores.txt
done

exit 0