# function for print personalized messages
function printMessage() {
  echo -e "\n\e[1;32m$(printf '%*s' "${COLUMNS:-$(tput cols)}" '' | tr ' ' '-')\e[0m"
  echo -e "\n\e[1;32m$1\e[0m\n"
  echo -e "\e[1;32m$(printf '%*s' "${COLUMNS:-$(tput cols)}" '' | tr ' ' '-')\e[0m\n"
}

# Verifica o usário para as permissões de instalação
function verifyUser() {
  testuser=2
  if [ $# -ge 1 ]; then
    while [ $testuser -ge 2 ]; do
      user=$1
      getent passwd $user >/dev/null
      testuser=$?
      if [ $testuser -eq 0 ]; then
        printMessage "Installing with user $user"
      else
        printMessage "The user does not exist, try again"
        verifyUser
      fi
    done
  else
    echo -n "User: "
    read user
    verifyUser $user
  fi
}