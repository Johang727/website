#!/usr/bin/bash

TEST_FILE="./TESTPRINT.pdf"

custom_ppd="false"

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

# credits for a double sided color print
creds="3.0" # i think it was 3.0, but it could be something like 1.5 or 2.0

echo "Note: Your credentials will be saved in /etc/cups/printers.conf! This file is read protected by root."
echo "Continuing is not recommended on a shared device! I am not responsible for leaked passwords."

read -r -p "Would you like to proceed? (y/N): " confirmation
if [[ "$confirmation" =~ ^[Nn]$ ]]; then
    exit 0
fi

while true; do
    read -r -p "Select Printer:
1) Lied Media
2) Library Printer 1 (Inconsistent)
3) Library Printer 2 (Inconsistent)
4) 24/7 Library Printer
5) Other

Selection: " printer

    case "$printer" in
        "1")
        PRINTER="LiedMedia"
        PPD_FILE="./Sharp-MX-C304W-ps.ppd"
        break
        ;;

        "2")
        PRINTER="Lib1Sharp"
        PPD_FILE="./Sharp-MX-5071-ps.ppd"
        break
        ;;

        "3")
        PRINTER="Lib2Sharp"
        PPD_FILE="./Sharp-MX-M5071-ps.ppd"
        echo "Note: This is a Black/White only printer."
        break
        ;;

        "4")
        PRINTER="Lib247Color"
        PPD_FILE="./Sharp-MX-4071-ps.ppd"
        break
        ;;

        "5")
        read -r -p "Input the internal name of the printer
Ex: LiedMedia: " PRINTER
        while true; do
            read -r -p "Select Model:
1) Sharp MX C304W
2) Sharp-MX-5071
3) Sharp-MX-M5071
4) Sharp-MX-4071
5) Provide Own PPD

Selection: " model


            case "$model" in
                "1")
                PPD_FILE="./Sharp-MX-C304W-ps.ppd"
                break
                ;;

                "2")
                PPD_FILE="./Sharp-MX-5071-ps.ppd"
                break
                ;;

                "3")
                PPD_FILE="./Sharp-MX-M5071-ps.ppd"
                break
                ;;

                "4")
                PPD_FILE="./Sharp-MX-4071-ps.ppd"
                break
                ;;

                "5")
                read -r -p "Enter the path to the PPD file
Ex: ./Sharp-MX-4071-ps.ppd: " PPD_FILE
                custom_ppd="true"
                break
                ;;

                *)
                echo "Invalid input"
                ;;
            esac
        done
        break
        ;;


        *)
        echo "Invalid input"
        ;;
    esac
done


if [[ ! -f "$PPD_FILE" ]]; then
    if [ "$custom_ppd" = "true" ]; then
        echo "File ($PPD_FILE) not found! Check the path and try again"
        exit 1
    fi
    echo "Error: PPD file ($PPD_FILE) not found in current directory."
    read -r -p "Would you like to download it? (y/N): " confirmation
    if [[ "$confirmation" =~ ^[Yy]$ ]]; then
        curl -fsSL "https://raw.githubusercontent.com/Johang727/website/master/print/$PPD_FILE" -o "$PPD_FILE" || {
            echo "Download failed. Check your connection or grab it manually from the Sharp website."
            exit 1
        }
    else
        echo "PPD file ($PPD_FILE) is needed to complete setup. Exiting."
        exit 1
    fi
fi


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
    if [[ ! -f "$TEST_FILE" ]]; then
        echo "Test document ($TEST_FILE) not found in current directory."
        read -r -p "Would you like to download it? (y/N): " confirmation
        if [[ "$confirmation" =~ ^[Yy]$ ]]; then
            curl -fsSL "https://raw.githubusercontent.com/Johang727/website/master/print/$TEST_FILE" -o "$TEST_FILE" || {
                echo "Download failed. Check your connection or grab it manually at print.johang.dev"
                exit 1
            }
        else
            echo "Printing test file will be omitted."
        fi
    fi

    if [[ -f "$TEST_FILE" ]]; then
        echo "Sending 2-page duplex test..."
        lp -d "$PRINTER" -o sides=two-sided-long-edge -o Duplex=DuplexNoTumble "$TEST_FILE"
        echo "Sent! The print may take up to a minute to register on the printer, please be patient!"
    fi
fi


echo "
For the most consistent printing, use the CLI directly:
lp -d $PRINTER -o sides=two-sided-long-edge -o Duplex=DuplexNoTumble <file.pdf>

Note: Print jobs on the printer will be under $USER rather than $ENCODED_USER. Regardless, $ENCODED_USER will be charged."

