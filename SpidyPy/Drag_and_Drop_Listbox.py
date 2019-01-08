# Version 0.1
# Aus 'stackoverflow.com' 'tkinter listbox drag and drop with python'
# https://stackoverflow.com/questions/14459993/tkinter-listbox-drag-and-drop-with-python/39300853#39300853
# Danke 'Moshe'
# Vielen Dank 'Jarad' für die auf Selectmode 'MULTIPLE' umgeschriebene Fassung

# Wenn 'name' angegeben wird, wird die Reihenfolge und der Inhalt als CSV gespeichert.
#   Filename ist dann name.csv
import tkinter as tk
import csv


class Drag_and_Drop_Listbox(tk.Listbox):
  """ A tk listbox with drag'n'drop reordering of entries. """
  def __init__(self, master,name=None, **kw):
    kw['selectmode'] = tk.MULTIPLE
    kw['activestyle'] = 'none'
    tk.Listbox.__init__(self, master, kw)
    self.bind('<Button-1>', self.getState, add='+')
    self.bind('<Button-1>', self.setCurrent, add='+')
    self.bind('<B1-Motion>', self.shiftSelection)
    self.bind('<<ListboxSelect>>', self.save)
    self.curIndex = None
    self.curIndex3 = None
    self.curState = None
    self.name = name
  def setCurrent(self, event):
    ''' gets the current index of the clicked item in the listbox '''
    self.curIndex = self.nearest(event.y)
  def getState(self, event):
    ''' checks if the clicked item in listbox is selected '''
    i = self.nearest(event.y)
    self.curState = self.selection_includes(i)
  def shiftSelection(self, event):
    ''' shifts item up or down in listbox '''
    i = self.nearest(event.y)
    if self.curState == 1:
      self.selection_set(self.curIndex)
    else:
      self.selection_clear(self.curIndex)
    if i < self.curIndex:
      # Moves up
      x = self.get(i)
      selected = self.selection_includes(i)
      self.delete(i)
      self.insert(i+1, x)
      if selected:
        self.selection_set(i+1)
      self.curIndex = i   
    elif i > self.curIndex:
      # Moves down
      x = self.get(i)
      selected = self.selection_includes(i)
      self.delete(i)
      self.insert(i-1, x)
      if selected:
        self.selection_set(i-1)
      self.curIndex = i
    self.save(event)
  def save(self,event):
    print("Save Reihenfolge {}".format(self.name))
    print(self.get(0,tk.END))
    if(self.name):
      fieldnames = ['Index','Name','Selected']
      with open(self.name+'.csv',"w") as f:
        writer=csv.DictWriter(f,fieldnames=fieldnames)
        writer.writeheader()
        li=self.get(0,tk.END)
        for i,name in enumerate(li):    
          writer.writerow({'Index':i,'Name':name,'Selected':self.selection_includes(i)})

if __name__ == "__main__":
    # def printRightClickItem( event):
    #   ''' RK 14.12.18: gets the current text of the with the right button clicked item in the listbox '''
    #   curIndex = myListbox.nearest(event.y)
    #   print(f"Ausgewählt wurde: {myListbox.get(curIndex)}") 
    root = tk.Tk()
    #myListbox = Drag_and_Drop_Listbox(root,name="myListbox")
    myListbox = Drag_and_Drop_Listbox(root)
    for i,name in enumerate(['name'+str(i) for i in range(10)]):
        myListbox.insert(tk.END, name)
        if i % 2 == 0:
            myListbox.selection_set(i)
    myListbox.pack(fill=tk.BOTH, expand=True)
    #listbox.bind('<Button-3>', printRightClickItem)
    myListbox.bind('<Button-3>', lambda event: print("Ausgewählt wurde: {0}".format(myListbox.get(myListbox.nearest(event.y)))))
    root.mainloop()