# -*- coding: utf-8 -*-
# @Time    : 2023/11/29 20:39
# @Author  : Yuzhii0718
# @File    : launcher.py
# @Software: PyCharm

import os


class ApplicationLauncher:
    def __init__(self):
        self.menu = {
            "1": self.fluent_designer,
            "2": self.gallery,
            "3": self.canery
        }

    def fluent_designer(self):
        os.system("start ../FluentDesigner_v1.3.3/FluentDesigner.exe")

    def gallery(self):
        #  python ../examples/gallery/login.py
        os.system("python ../examples/gallery/demo.py")

    def canery(self):
        # python ../Canery/gallery/login.py
        os.system("python ../Canery/gallery/main.py")

    def launch(self):
        print("1 -> Fluent Designer, 2 -> Gallery, 3 -> Canery")
        print("Press Ctrl+C to exit.")
        while True:
            try:
                choice = input("Enter your choice: ")
                if choice in self.menu:
                    self.menu[choice]()
                else:
                    print("Invalid input. Please try again.")
            except KeyboardInterrupt:
                print("\nBye.")
                break
            except ValueError:
                print("Invalid input. Please try again.")
            except Exception as e:
                print(e)
                break


if __name__ == "__main__":
    launcher = ApplicationLauncher()
    launcher.launch()
