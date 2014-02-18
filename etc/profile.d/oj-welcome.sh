#http://ubuntuforums.org/showthread.php?t=2028113&p=12110679#post12110679
echo_c()
{
  w=$(stty size | cut -d" " -f2)       # width of the terminal
  l=${#1}                              # length of the string
  printf "%"$((l+(w-l)/2))"s\n" "$1"   # print string padded to proper width (%Ws)
}
echo_c_colored()
{
  w=$(stty size | cut -d" " -f2)       # width of the terminal
  l=${#1}                              # length of the string
  printf "%"$(((l+6)+(w-l)/2))"s\n" "$1"   # print string padded to proper width (%Ws)
}
echo
echo_c  "********************************************"
echo_c_colored  "** $(tput setaf 2)Welcome To Ojuba 35 (Aljazair) Terminal$(tput sgr0) **"
# FIXME: To use /etc/issue after Arabic support in terminal.
#echo_c_colored  "** $(tput setaf 2)wellcome $(cat /etc/issue | head -n1)$(tput sgr0) **"
echo_c  "********************************************"
echo
