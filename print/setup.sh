#!/usr/bin/bash

PPD_FILE="./Sharp-MX-C304W-ps.ppd"
TEST_FILE="./TESTPRINT.pdf"

# Function to URL-encode strings (for passwords with #, @, etc.)
urlencode() {
    local string="${1}"
    local strlen=${#string}
    local encoded=""
    local pos c o

    for (( pos=0 ; pos<strlen ; pos++ )); do
       c=${string:$pos:1}
       case "$c" in
          [-_.~a-zA-Z0-9] ) o="${c}" ;; # Safe characters
          * )               printf -v o '%%%02x' "'$c" ;; # Hex encode everything else
       esac
       encoded+="${o}"
    done
    echo "${encoded}"
}

# 1. Check if PPD exists before starting
if [[ ! -f "$PPD_FILE" ]]; then
    echo "Error: PPD file ($PPD_FILE) not found in current directory."
    exit 1
fi

# 1. Check if PPD exists before starting
if [[ ! -f "$TEST_FILE" ]]; then
    echo "Error: Test document ($TEST_FILE) not found in current directory."
    exit 1
fi

# credits for a double sided color print
creds="3.0" # i think it was 3.0, but it could be something like 1.5 or 2.0

while true; do
    read -r -p "Select Printer:
1) Lied Media
2) Library Printer 1 (WIP)
3) Library Printer 2 (WIP)
4) 24/7 Library Printer (WIP)
5) Other

Selection: " printer

    case "$printer" in
        "1")
        PRINTER="LiedMedia"
        break
        ;;

        "2")
        echo "This printer option is a placeholder!"
        exit
        ;;

        "3")
        echo "This printer option is a placeholder!"
        exit
        ;;

        "4")
        echo "This printer option is a placeholder!"
        exit
        ;;

        "5")
        read -r -p "Input the internal name of the printer
Ex: Lied Media -> LiedMedia: " PRINTER
        break
        ;;


        *)
        echo "Invalid input"
        ;;
    esac
done

read -r -p "Enter Doane Username (first.last): " USERNAME

read -r -s -p "Enter Doane Password (input hidden): " PASSWORD

ENCODED_PASS=$(urlencode "$PASSWORD")
ENCODED_USER=$(urlencode "$USERNAME")

echo "
" # newline since s also hides the newline? 

echo "---
Configuring CUPS... (You may be prompted for $USER@$HOSTNAME's password)
---
"


sudo systemctl start cups.service > /dev/null # in case user doesn't have it set to autorun

if sudo lpadmin -p "$PRINTER" -v "smb://$ENCODED_USER:$ENCODED_PASS@crete/ob2/$PRINTER" -E -P "$PPD_FILE" > /dev/null; then
    echo "
Successfully added $PRINTER!
    "
else
    echo "Failed to add printer. Check your credentials."
    exit 1
fi



read -r -p "
Would you like to print a test file? Est. $creds credits! (y/N): " confirmation

if [[ "$confirmation" =~ ^[Yy]$ ]]; then
    echo "Sending 2-page duplex test..."

    lp -d "$PRINTER" -o sides=two-sided-long-edge -o Duplex=DuplexNoTumble "$TEST_FILE"

    echo "Sent! The print may take up to a minute to register on the printer, please be patient!"
fi


echo "
Note: Your credentials are saved in /etc/cups/printers.conf!"