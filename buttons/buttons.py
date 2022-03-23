from tkinter import PhotoImage, Button


class MenuButton:

    def __init__(self, parent, art: str, relx: float = 0, rely: float = 0):
        self.parent = parent
        self.width = parent.winfo_width()
        self.height = parent.winfo_width()

        self.image = PhotoImage(file=art)

        self.button = Button(self.parent, command=self.behavior)
        self.button.config(image=self.image)
        self.button.place(relx=relx, rely=rely)

    def behavior(self):
        raise NotImplementedError("MenuButtons must implement behavior method.")


class BackButton(MenuButton):

    def __init__(self, parent, art: str = r"buttons\Back.gif", relx: float = 0, rely: float = 0):
        super().__init__(parent=parent, art=art, relx=relx, rely=rely)

    def behavior(self):
        self.parent.destroy()


class PopupButton:

    def __init__(self, parent, art: str, relx: float = 0, rely: float = 0):
        self.parent = parent
        self.width = parent.popUpFrame.winfo_width()
        self.height = parent.popUpFrame.winfo_height()

        self.image = PhotoImage(file=art)
        self.button = Button(parent.popUpFrame, command=self.behavior)
        self.button.config(image=self.image)
        self.button.place(relx=relx, rely=rely)

    def behavior(self):
        raise NotImplementedError("PopupButtons must implement behavior method.")


class YesButton(PopupButton):

    def __init__(self, parent, art: str = r"buttons\yes.gif", relx: float = 0, rely: float = 0):
        super().__init__(parent=parent, art=art, relx=relx, rely=rely)

    def behavior(self):
        pass


class NoButton(PopupButton):

    def __init__(self, parent, art: str = r"buttons\no.gif", relx: float = 0, rely: float = 0):
        super().__init__(parent=parent, art=art, relx=relx, rely=rely)

    def behavior(self):
        self.parent.popUpFrame.destroy()


