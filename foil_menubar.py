from Tkinter import *


class MenuBar(object):
    def __init__(self, controller, parent_view):
    	self.controller = controller
        self.parent_view = parent_view
        self.top = self.parent_view.winfo_toplevel()
        self.menuBar = Menu(self.top)
        self.top['menu'] = self.menuBar
        self.makeFormulaMenu()


    def makeFormulaMenu(self):
        self.sub_menu_formula_manage = Menu(self.menuBar)
        self.menuBar.add_cascade(label='Formulae', menu=self.sub_menu_formula_manage)
        self.sub_menu_formula_manage.add_command(label='NACA-00', command=self.controller.chooseNACA_00)
        self.sub_menu_formula_manage.add_command(label='NACA-63', command=self.controller.chooseNACA_63)
