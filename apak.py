import sys, datetime, io, os

def __printerror(text):
  print('\033[0;31;49m{}\033[m'.format(text))
  sys.exit()

class packer(object):
  def __init__(self, filename):
    """ Opens the apak file and makes sure that the first 4 bytes are 'APAK' """
    with open('logfile', 'w') as openfile:
      openfile.write('')
    self.printlog = False
    self.__log('Starting packer...')
    self.filename = filename
    self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    try:
      with open(filename + '.apak', 'rb') as apakfile:
        self.__log(' - Checking APAK...')
        if apakfile.read(4) == b'\x41\x50\x41\x4B':
          self.__log(' - Checked')
        else:
          __printerror('FileError: That file is not an apak file!')
    except:
      self.__log(' - Creating APAK...')
      with open(filename + '.apak', 'wb') as apakfile:
        apakfile.write(b"APAK{ }")
      self.__log(' - APAK created')
    self.__log('Packer started')

  def __log(self, text):
    if self.printlog:
      print('\033[32m{}\033[m'.format(text))
    with open('logfile', 'a') as openfile:
      openfile.write(text + ' at ' + str(datetime.datetime.now()) + '\n')
  
  def clear(self):
    self.__log('Clearing apak...')
    with open(self.filename + '.apak', 'wb') as apakfile:
      apakfile.write(b"APAK{ }")
    self.__log('Cleared apak')

  def addfile(self, filename, name=False):
    if not name:
      name = filename
    self.__log('Adding file...')
    with open(filename, "rb") as readfile:
      self.__log(' - Reading file...')
      filecontence = readfile.read()
      self.__log(' - Read')
    with open(self.filename + '.apak', 'rb') as apakfile:
      self.__log(' - Loading APAK file...')
      apakfile.seek(4)
      apakdict = eval(apakfile.read())
      self.__log(' - Loaded')
    apakdict[name] = filecontence
    with open(self.filename + '.apak', 'wb') as apakwrite:
      self.__log(' - Saving...')
      apakwrite.write(b"APAK" + str(apakdict).encode('UTF-8'))
      self.__log(' - Saved')

  def addtext(self, apaktextobject):
    self.__log('Adding apak text object...')
    self.__log(' - Checking if apak text object...')
    try:
      if apaktextobject.type == 'apaktextobject':
        pass
      else:
        __printerror('TypeError: That object is not a apak text object!')
    except:
      __printerror('TypeError: That object is not a apak text object!')
    self.__log(' - Done')
    self.__log(' - Getting text...')
    name, filecontence = apaktextobject.read()
    self.__log(' - Got text')
    with open(self.filename + '.apak', 'rb') as apakfile:
      self.__log(' - Loading APAK file...')
      apakfile.seek(4)
      apakdict = eval(apakfile.read())
      self.__log(' - Loaded')
    apakdict[name] = filecontence.read()
    with open(self.filename + '.apak', 'wb') as apakwrite:
      self.__log(' - Saving...')
      apakwrite.write(b"APAK" + str(apakdict).encode('UTF-8'))
      self.__log(' - Saved')
  
  def config(self, **kwargs):
    for i in kwargs:
      if i == 'printlog':
        if type(kwargs[i]) == bool:
          self.printlog = kwargs[i]
        else:
          __printerror('ConfigError: Argument "printlog" is a bool, not ' + str(type(kwargs[i])))
      elif i == "root_dir":
        self.ROOT_DIR = kwargs[i]
      else:
        pass
  
  def listfiles(self):
    self.__log('Getting file list...')
    files = []
    with open(self.filename + '.apak', 'rb') as apakfile:
      self.__log(' - Loading APAK file...')
      apakfile.seek(4)
      apakdict = eval(apakfile.read())
      self.__log(' - Loaded')
    self.__log(' - Assembling list...')
    for item in apakdict:
      files.append(item)
    self.__log(' - List Assembled...')
    return files

  def __finddir(self, path, permpath):
    self.__log('Finding files in {}...'.format(path))
    for i in os.listdir(path):
      if os.path.isfile(os.path.join(path, i)):
        self.__log('Found file {}, adding...'.format(i))
        if path.replace(permpath, '') == '':
          self.addfile(os.path.join(path, i), path.replace(permpath, '/') + '/' + i)
        else:
          self.addfile(os.path.join(path, i), path.replace(permpath, '') + '/' + i)
      else:
        self.__log('Found directory, recursively searching...')
        self.__finddir(os.path.join(path, i), permpath)
  
  def adddir(self, path, recursive=True):
    self.directory = {}
    ROOT_DIR = os.path.join(self.ROOT_DIR, os.pardir)
    ROOT_DIR = self.ROOT_DIR
    PATH_DIR = os.path.join(ROOT_DIR, path)
    if recursive:
      self.__finddir(PATH_DIR, ROOT_DIR)
    else:
      self.__log('Finding files...')
      for i in os.listdir(PATH_DIR):
        if os.path.isfile(os.path.join(PATH_DIR, i)):
          self.__log('Found file {}, adding...'.format(i))
          self.addfile(os.path.join(PATH_DIR,i), PATH_DIR.replace(ROOT_DIR, '') + '/' + i)

  def getfile(self, filename, etype='bytes'):
    with open(self.filename + '.apak', 'rb') as apakfile:
      apakfile.seek(4)
      apakdict = eval(apakfile.read())
    if filename in apakdict:
      if etype == 'bytes':
        return io.BytesIO(apakdict[filename])
      elif etype == 'string':
        return io.StringIO(apakdict[filename].decode('UTF-8'))
      else:
        __printerror('TypeError: Type {} is not allowed.'.format(etype))
    else:
      __printerror('NotFoundError: File {} is not in apak.'.format(filename))
   
  def __mkdirs(self, path):
    dirpath = '/'.join(path.split('/')[:-1])
    try:
      os.makedirs(dirpath)
    except:
      pass
  
  def extract(self):
    ROOT_DIR = self.ROOT_DIR
    with open(self.filename + '.apak', 'rb') as apakfile:
      apakfile.seek(4)
      apakdict = eval(apakfile.read())
      for file in apakdict:
        files = ROOT_DIR + file
        self.__mkdirs(files)
        with open(files, 'wb') as temp_write_file:
          temp_write_file.write(apakdict[file])
  
  def removefile(self, name):
    self.__log('Removing file...')
    with open(self.filename + '.apak', 'rb') as apakfile:
      self.__log(' - Loading APAK file...')
      apakfile.seek(4)
      apakdict = eval(apakfile.read())
      self.__log(' - Loaded')
    self.__log(' - Checking if file exists...')
    if name in apakdict:
      self.__log(' - Erasing file...')
      del apakdict[name]
      self.__log(' - Erased')
    else:
      __printerror("NotFoundError: File {} is not in apak.".format(name))
    with open(self.filename + '.apak', 'wb') as apakwrite:
      self.__log(' - Saving...')
      apakwrite.write(b"APAK" + str(apakdict).encode('UTF-8'))
      self.__log(' - Saved')

class apaktextobject(object):
  def __init__(self, name, text, etype='bytes'):
    self.name = name
    self.text = text
    self.type = "apaktextobject"
    if etype == 'bytes':
      self.__etype = etype
    elif etype == 'string':
      self.__etype = etype
    else:
      __printerror('TypeError: Type {} is not allowed.'.format(etype))
  def read(self):
    if self.__etype == 'bytes':
      return (self.name, io.BytesIO(bytes(self.text, 'UTF-8')))
    elif self.__etype == 'string':
      return (self.name, io.StringIO(self.text))
    else:
      __printerror('TypeError: Type {} is not allowed.'.format(self.__etype))

class saver(object):
  def __init__(self, defultvalue):
    if type(defultvalue) != dict:
      __printerror('TypeError: "defultvalue" must be a dictionary not {}'.format(str(type(defultvalue))))
    else:
      self.__defult = defultvalue
      self.__save = defultvalue

  def __setitem__(self, key, item):
    self.__save[key] = item

  def __getitem__(self, key):
    return self.__save[key]
  
  def __repr__(self):
    return repr(self.__save)

  def __len__(self):
    return len(self.__save)

  def __delitem__(self, key):
    del self.__save[key]

  def clear(self):
    return self.__save.clear()

  def __contains__(self, item):
    return item in self.__save

  def __splitdata(self, data):
    keys = []
    datas = []
    for key in data:
      if type(data[key]) == dict:
        temp_keys, temp_datas = self.__splitdata(data[key])
        temp_keys.append(key)
        keys.append(temp_keys)
        datas.append(temp_datas)
      else:
        keys.append(key)
        datas.append(data[key])
    return keys, datas
  
  def __unsplitdata(self, keys, datas):
    bigdict = {}
    for key in range(len(keys)):
      if type(keys[key]) == list:
        bigdict[keys[key][-1]] = self.__unsplitdata(keys[key][:-1], datas[key])
      else:
        bigdict[keys[key]] = datas[key]
    return bigdict

  def __update(self, old, new):
    returndict = old.copy()
    for key in new:
      if key in old:
        if type(new[key]) == dict:
          returndict[key] = self.__update(old[key], new[key])
        else:
          pass
      else:
        returndict[key] = new[key]
    return returndict
  
  def save(self, name):
    keys, savedata = self.__splitdata(self.__save)
    with open(name + '.save', 'wb') as savefile:
      savefile.write(b"SAVE" + str(savedata).encode('UTF-8'))
    return keys
  
  def load(self, name, keys, update=True):
    try:
      with open(name + '.save', 'rb') as savefile:
        if savefile.read(4) == b'\x53\x41\x56\x45':
          tempsave = eval(savefile.read())
          if update:
            self.__save = self.__update(self.__unsplitdata(keys, tempsave), self.__defult)
        else:
          __printerror('FileError: File {} is not an save file'.format(name))
    except:
      __printerror('FileError: File {} does not exist'.format(name))

def __tkintergui():
  try:
    import tkinter as tk
    from tkinter import filedialog, messagebox
  except:
    __printerror("ImportError: Cannot import tkinter")
  
  filebtn = []
  removebtn = []

  def openew():
    root.destroy()
    __tkintergui()
  
  def clearask():
    if messagebox.askquestion("Confirm","Are you sure you want to clear this APAK?") == 'yes':
      pack.clear()

  def savenewtext(textobj, filename):
    pack.addtext(apaktextobject(filename, textobj.get("1.0",'end-1c')))
    messagebox.showinfo("Info", filename + "has been saved")

  def writetext(text, filename):
    with open(filename, "w") as fn:
      fn.write(text)
    messagebox.showinfo("Info", filename + " has been exported")

  def openfile(filename):
    newWindow = tk.Toplevel(root)
    newWindow.geometry('350x150')
    newWindow.title("File Viewer")
    scrollbar = tk.Scrollbar(newWindow)
    textwindow = tk.Text(newWindow)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    textwindow.pack(expand=1, fill=tk.BOTH)
    textwindow.tag_configure("red", foreground="red")
    scrollbar.config(command=textwindow.yview)
    textwindow.config(yscrollcommand=scrollbar.set)
    textwindow.insert(tk.END, pack.getfile(filename).read())
    menubar = tk.Menu(newWindow)
    menubar.add_command(label="Save", command=lambda textobj=textwindow, filename=filename: savenewtext(textwindow, filename))
    menubar.add_command(label="Export File", command=lambda filename=filename: writetext(pack.getfile(filename).read(), filename))
    menubar.add_command(label="Close", command=newWindow.destroy)
    newWindow.config(menu=menubar)

  def removefile(filename):
    if messagebox.askquestion("Confirm","Are you sure you want to remove " + filename + "?") == 'yes':
      pack.removefile(filename)
      scan()

  def addfile():
    path = filedialog.askopenfilename(initialdir=os.path.dirname(os.path.abspath(__file__)), title="Select file")
    if path in [' ', '', ()]:
      return
    pack.addfile(path, name=path.replace(os.path.dirname(os.path.abspath(__file__)), ''))
    scan()

  def extractfile():
    pack.extract()

  def scan():
    for item in range(len(filebtn)):
      filebtn[item-1].destroy()
      removebtn[item-1].destroy()
      del filebtn[item-1]
      del removebtn[item-1]
    for file in pack.listfiles():
      filebtn.append(tk.Button(root, text=file, command=lambda file=file: openfile(file)))
      removebtn.append(tk.Button(root, text="Remove", command=lambda file=file: removefile(file)))
    for item in range(len(filebtn)):
      filebtn[item].grid(column=0, row=item)
      removebtn[item].grid(column=1, row=item)

  root = tk.Tk()
  path = filedialog.askopenfilename(initialdir=os.path.dirname(os.path.abspath(__file__)), title="Select apak file", filetypes=(("apak file", "*.apak"),("all files", "*.*")))
  if path in [' ', '', ()]:
    return

  pack = packer('.'.join(path.split('.')[:-1]))

  root.geometry('350x150')

  root.title("APAK editor: " + path)

  scan()

  menubar = tk.Menu(root)
  filemenu = tk.Menu(menubar, tearoff=0)
  filemenu.add_command(label="Clear", command=clearask)
  filemenu.add_command(label="Open New", command=openew)
  filemenu.add_separator()
  filemenu.add_command(label="Exit", command=root.destroy)
  menubar.add_cascade(label="File", menu=filemenu)

  apakmenu = tk.Menu(menubar, tearoff=0)
  apakmenu.add_command(label="Add File", command=addfile)
  apakmenu.add_command(label="Extract", command=extractfile)
  menubar.add_cascade(label="APAK", menu=apakmenu)
  
  root.config(menu=menubar)

  root.mainloop()

def __runfile(plist):
  p = packer(plist[0])
  for i in range(len(plist[1:])):
    i += 1
    if plist[i][0] == '-':
      if plist[i][1:] == 'f':
        if plist[i+1][0] == '-':
          __printerror('ArgumentError: Command -f must have a valid file name')
        else:
          p.addfile(plist[i+1])
      elif plist[i][1:] == 'd':
        if plist[i+1][0] == '-':
          __printerror('ArgumentError: Command -d must have a valid directory name')
        else:
          p.adddir(plist[i+1], False)
      elif plist[i][1:] == 'dr':
        if plist[i+1][0] == '-':
          __printerror('ArgumentError: Command -dr must have a valid directory name')
        else:
          p.adddir(plist[i+1], True)
      elif plist[i][1:] == 'clear':
        p.clear()
      elif plist[i][1:] == 'ex':
        p.extract()
    else:
      pass

if __name__ == '__main__':
  if len(sys.argv) <= 1:
    print('Usage:')
    print('Visit https://cloudy-day-central.jackneils.repl.co/wiki/apak for more information')
    print('run [commandfile] -------- Runs apak command file')
    print('[apakname] [commands] ---- Runs the commands that were given')
    print('gui ---------------------- Runs the APAK GUI ( Requires tkinter )')
    sys.exit()
  if sys.argv[1] == 'run':
    try:
      with open(sys.argv[2], 'r') as apak_file:
        __runfile(apak_file.read().replace('\n','').split(' '))
    except:
      __printerror('FileError: Cannot open file given')
  elif sys.argv[1] == 'gui':
    __tkintergui()
  else:
    __runfile(sys.argv[1:])
