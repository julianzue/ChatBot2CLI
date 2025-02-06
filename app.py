from colorama import Fore, Style, init
import json
import time
import os


init()

y = Fore.LIGHTYELLOW_EX
c = Fore.LIGHTCYAN_EX
r = Fore.LIGHTRED_EX
re = Fore.RESET

dim = Style.DIM
res = Style.NORMAL


def addToHistory(time, question, answer):

    if not os.path.exists("history.json"):
        with open("history.json", "w") as f:
            json.dump([], f, indent=4)

    with open("history.json", "r") as f:
        history = json.load(f)

    history.append(
        {
            "time": time,
            "question": question,
            "answer": answer
        }
    )

    with open("history.json", "w") as f:
        json.dump(history, f, indent=4)


class Chat():
    def __init__(self):
        print("Menu")
        print("----")

        self.commands = [
            {
                "name": "chat",
                "info": "Starts a new Chat.",
                "func": self.chat
            },
            {
                "name": "history",
                "info": "Shows the histroy.",
                "func": self.history
            },
            {
                "name": "help",
                "info": "Shows the help.",
                "func": self.help
            },
            {
                "name": "exit",
                "info": "Closes this program.",
                "func": self.close
            }
        ]

        for command in self.commands:
            print(f"[*] {c}{'{:<10}'.format(command['name'])}{re}{command['info']}")

        self.prompt()


    def prompt(self):

        choose = input(f"{y}[+] {re}")

        not_found = True

        for command in self.commands:
            if choose == command["name"]:
                not_found = False
                print("")
                command["func"]()

        if not_found:
            print("")
            print(f"{r}[!]{re} Command {r}{choose}{re} not found. Please try again.")
            print("")
            self.prompt()



    def chat(self):
        prompt = input(f"{y}[+] Enter Prompt: {re}")   

        with open("data.json", "r") as f:
            data = json.load(f)

        t = time.strftime('%Y-%m-%d %H:%M:%S')
        output = []

        for question in data["questions"]:
            if prompt.lower() in question["question"].lower():
                print("")
                print(f"{dim}[*] {t}{res}")
                print(f"[*] {question["question"]}")
                print(f"{c}[*] {question["answer"]}{re}")
                output.append([question["question"], question["answer"]])

        print("")
        addToHistory(t, prompt, output)

        if prompt == "exit":
            print("Bye!")
            print("")
            self.prompt()
        else:
            self.chat()


    def history(self):
        with open("history.json", "r") as f:
            history = json.load(f)

        for index, query in enumerate(history, 1):
            if not index == 1:
                print("")
                
            print(f"{dim}{'{:03d}'.format(index)} {query['time']}{res}")
            print(f"{y}[+] Prompt: {query['question']}{re}")

            for i, answer in enumerate(query["answer"], 1):
                print(f"{dim}{'{:03d}'.format(i)}{res} {answer[0]} {c}{answer[1]}{re}")

        print("")

        self.prompt()


    def help(self):
        for command in self.commands:
            print(f"[*] {c}{'{:<10}'.format(command['name'])}{re}{command['info']}")

        print("")
        self.prompt()

    
    def close(self):
        print(f"{r}[!]{re} Bye.")


Chat()