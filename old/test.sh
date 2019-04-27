#!/bin/bash
# Unter Theke -   1 Streifen
# Kabel   Sw      Grau    Blau      Rot
# LEDband Masse   Rot#    Blau      Gruen
# GPIO            15      11       16
# BCM             8       26       10
#
# Ueber Theke      3 Streifen
# Kabel   sw      Rot     Weiss    Gelb
# LEDband Masse   Rot     Blau     Gruen#(LAngsam an aus)
# GPIO            7       1        2
# BCM             7       12       13
#
# Fensterbank -   2 Streifen
# Kabel   Sw      Gelb    Weiss    Rot
# LEDband Masse   Rot     Blau     Gruen
# GPIO            8       10       0
# BCM             3       24       11

function e {
   read -n1 -r -p "Press for $2 on" key
   gpio mode $1 out
   gpio write $1 1
   read -n1 -r -p "Press any key to turn off..." key
   gpio write $1 0
   read -n1 -r -p "Press any key to move to next..." key
}

e 7 "UT R"
e 1 "UT B"
e 2 "UT G"