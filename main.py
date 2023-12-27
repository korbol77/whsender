import sys
import requests
import os
import base64
import json

ALL_COMMANDS = ("\n  Commands:\n"
"  $send <message> = Sends the specified message via webhook\n"
"  $modify-name <name> = Changes the webhook name to the specified one\n"
"  $commands = Displays all available commands\n"
"  $delete = Deletes webhook\n"
"  $clear = Clears the console\n"
"  $exit = Returns to main panel")

class Colors:
  RED = "\u001b[31m"
  BRIGHT_RED = "\u001b[91m"
  GREEN = "\u001b[32m"
  BRIGHT_BLUE = "\u001b[94m"
  WHITE = "\u001b[37m"
  RESET = "\u001b[0m"

WHSENDER_LOGO = rf"""
{Colors.BRIGHT_RED}   _ _ _ _____ {Colors.BRIGHT_BLUE} _____ _____ _____ ____  _____ _____ 
{Colors.BRIGHT_RED}  | | | |  |  |{Colors.BRIGHT_BLUE}|   __|   __|   | |    \|   __| __  |
{Colors.BRIGHT_RED}  | | | |     |{Colors.BRIGHT_BLUE}|__   |   __| | | |  |  |   __|    -|
{Colors.BRIGHT_RED}  |_____|__|__|{Colors.BRIGHT_BLUE}|_____|_____|_|___|____/|_____|__|__|  by korbol77""" + Colors.RESET

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
    command_args = command.split(command_type + " ")

    match(command_type):
      case "$send":
        if len(command_args) == 2:
          r = requests.post(webhook_url, data={"content": command_args[1]})
          if r.status_code == 204:
            print(Commands.success("Command succeeded"))
          else:
            print(Commands.error("Command failed!"))
        else:
          print(Commands.error("The \"send\" command requires the <message> argument!"))

      case "$modify-name":
        if len(command_args) == 2:
          r = requests.patch(webhook_url, json={"name": command_args[1]}, headers={"Content-Type": "application/json"})
          if r.status_code == 200:
            print(Commands.success("Command succeeded"))
          else:
            print(Commands.error("Command failed!"))
        else:
          print(Commands.error("The \"modify-name\" command requires the <name> argument!"))

      case "$modify-avatar":
        if len(command_args) == 2:
          def get_b64_from_image_url(url):
            r = requests.get(url).content
            r_b64 = base64.b64encode(r)
            return r_b64

          image_b64 = "data:image/jpeg;base64," + get_b64_from_image_url(command_args[1]).decode("utf-8")
          r = requests.patch(webhook_url, json={"avatar": image_b64}, headers={"Content-Type": "application/json"})
          if r.status_code == 200:
            print(Commands.success("Command succeeded"))
          else:
            print(Commands.error("Command failed!"))
        else:
          print(Commands.error("The \"modify-avatar\" command requires the <avatar_url> argument!"))

      case "$webhook-details":
        r = requests.get(webhook_url)
        if r.status_code == 200:
          webhook_details = json.loads(r.text)
          print(f"\n  Webhook Info:\n    Name: {webhook_details['name']}\n\n  Webhook Owner Info:\n    Name: {webhook_details['user']['username']}")
        else:
          print(Commands.error("Command failed!"))

      case "$commands":
        print(ALL_COMMANDS)

      case "$delete":
        r = requests.delete(webhook_url)
        if r.status_code == 204:
          print(Commands.success("Command succeeded"))
        else:
          print(Commands.error("Command failed!"))

      case "$clear":
        os.system("clear")

  while True:
    print(WHSENDER_LOGO)
    option = input(Colors.BRIGHT_BLUE + "\n  1) Webhook Console\n  2) Help\n  3) Exit\n  > " + Colors.RESET)

    match(option):
      case "1":
        os.system("clear")

        while True:
          command = input("\n  Command > ")

          if command == "$exit":
            os.system("clear")
            break
          else:
            get_command(command)

      case "2":
        os.system("clear")
        print(ALL_COMMANDS)

      case "3":
        sys.exit()

      case _:
        os.system("clear")
        print("\n" + Commands.error("Invalid choice!"))

else:
  print("Usage:\npython3 main.py <webhook_url>")