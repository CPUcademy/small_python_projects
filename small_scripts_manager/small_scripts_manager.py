from tkinter import *
import ast, os
from cryptography.fernet import Fernet

class SmallScriptsManager:
    def __init__(self):
        self.__root = Tk()
        self.__root.title("Small scripts manager")
        self.__root.geometry("585x388+100+100")
        self.__modules = set()
        self.__variables = {"max_width": 602, "button_padding": 10, "char_width": 7, "current_x": 0}
        Button(self.__root, text="Add a script", command=self.__addScript, bg="gray", fg="white").place(x=10, y=353)
        self.__generate_key()
        self.__displayScripts()
        self.__root.mainloop()

    def __generate_key(self):
        if not os.path.exists("secret.key"):
            key = Fernet.generate_key()
            with open("secret.key", "wb") as key_file:
                key_file.write(key)
        with open("secret.key", "rb") as key_file:
            self.__key = key_file.read()
        self.__cipher = Fernet(self.__key)

    def __encrypt_data(self, data):
        return self.__cipher.encrypt(data.encode()).decode()

    def __decrypt_data(self, data):
        return self.__cipher.decrypt(data.encode()).decode()

    def __addScript(self):
        t = Toplevel()
        t.title("Add a script")
        t.geometry(f"320x80+200+200")

        Label(t, text="Enter the name of the module:").place(x=10, y=10)
        entry = Entry(t)
        entry.place(x=180, y=10)
        
        def confirm():
            result = entry.get()
            if len(result) > 0:
                t.destroy()
                self.__modules.add(result)
                encrypted_data = self.__encrypt_data(str(list(self.__modules)))
                with open("programs.txt", "w") as w:
                    w.write(encrypted_data)
                globals()[result] = __import__(result)
                self.__refresh_scripts()

        button = Button(t, text="Confirm", command=lambda: confirm())
        button.place(x=135, y=40)
        self.__root.wait_window(t)

    def __refresh_scripts(self):
        for widget in self.toolsFrame.winfo_children():
            widget.destroy()
        self.__displayScripts()

    def __displayScripts(self):
        self.canvas = Canvas(self.__root, width=560, height=340)
        self.canvas.place(x=0, y=0)
        self.scrollbar = Scrollbar(self.__root, orient="vertical", command=self.canvas.yview)
        self.scrollbar.place(x=567, y=0, height=340)
        self.toolsFrame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.toolsFrame, anchor='nw')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        try:
            with open("programs.txt", "r") as r:
                encrypted_data = r.read()
                if encrypted_data:
                    self.__modules = set(ast.literal_eval(self.__decrypt_data(encrypted_data)))
        except (FileNotFoundError, SyntaxError, Exception):
            self.__modules = set()
        for x in self.__modules: globals()[x] = __import__(x)

        current_row_frame = Frame(self.toolsFrame)
        current_row_frame.pack(fill="x")
        
        for module in self.__modules:
            button_text = module
            button_length = len(button_text)
            button_width = button_length * self.__variables["char_width"] + self.__variables["button_padding"]
            if self.__variables["current_x"] + button_width > self.__variables["max_width"]:
                current_row_frame = Frame(self.toolsFrame)
                current_row_frame.pack(fill="x")
                self.__variables["current_x"] = 0

            button = Button(current_row_frame, text=button_text, command=lambda y=module: getattr(eval(y), y)())
            button.pack(side="left", padx=self.__variables["button_padding"] // 2, pady=5)
            self.__variables["current_x"] += button_width

        self.toolsFrame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        self.__root.bind_all("<MouseWheel>", self.__on_mouse_wheel)

    def __on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
