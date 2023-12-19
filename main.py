import sys
import requests
import os

class Colors:
  RED = "\u001b[31m"
  GREEN = "\u001b[32m"
  BLUE = "\u001b[34m"
  WHITE = "\u001b[37m"
  RESET = "\u001b[0m"

WHSENDER_LOGO = Colors.BLUE + r"""
  ___       _______  ______________________   __________________________ 
  __ |     / /__  / / /_  ___/__  ____/__  | / /__  __ \__  ____/__  __ \
  __ | /| / /__  /_/ /_____ \__  __/  __   |/ /__  / / /_  __/  __  /_/ /
  __ |/ |/ / _  __  / ____/ /_  /___  _  /|  / _  /_/ /_  /___  _  _, _/ 
  ____/|__/  /_/ /_/  /____/ /_____/  /_/ |_/  /_____/ /_____/  /_/ |_|""" + Colors.RESET


class Commands:
  def error(text):
    return Colors.RED + "  [" + Colors.WHITE + "!" + Colors.RED + f"] {text}" + Colors.RESET
  def success(text):
    return Colors.GREEN + "  [" + Colors.WHITE + "+" + Colors.GREEN + f"] {text}" + Colors.RESET

# os.system("title WHSENDER - Discord Webhook Sender")

if len(sys.argv) == 2:
  webhook_url = sys.argv[1]

  def get_command(command):
    command_type = command.split(" ")[0]

    match(command_type):
      case "$send":
        command_args = command.split(command_type + " ")

        if len(command_args) == 2:
          r = requests.post(webhook_url, data={"content": command_args[1]})
          if r.status_code == 204:
            print(Commands.success("Command succeeded"))
          else:
            print(Commands.error("Command failed!"))
        else:
          print(Commands.error("The \"send\" command requires the <message> argument!"))
      case "$delete":
        r = requests.delete(webhook_url)
        if r.status_code == 204:
          print(Commands.success("Command succeeded"))
        else:
          print(Commands.error("Command failed!"))

  while True:
    print(WHSENDER_LOGO)
    option = input(Colors.BLUE + "\n  a) Webhook Console\n  b) Help\n  c) Exit\n  > " + Colors.RESET)

    match(option):
      case "a":
        os.system("clear")

        while True:
          command = input("\n  Command > ")

          if command == "$exit":
            os.system("clear")
            break
          else:
            get_command(command)
      case "b":
        os.system("clear")
        print("\n  Commands:\n"
              "  $send <message> = Sends the specified message via webhook\n"
              "  $delete = Deletes webhook\n"
              "  $exit = Returns to main panel\n"
              "  Author: korbol77")
      case "c":
        sys.exit()
      case _:
        os.system("clear")
        print("\n" + Commands.error("Invalid choice!"))

else:
  print("Usage:\npython3 main.py <webhook_url>")