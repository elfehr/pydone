#!/usr/bin/python
# gitlab.com/eyuku/pydone


import tkinter
import sys
from optparse import OptionParser
import io
#from tkinter import font


# Fields definition
# Window
top = tkinter.Tk()
ico = tkinter.PhotoImage(file='icon.png')
top.iconphoto(True, ico)
# Scrollbar
s = tkinter.Scrollbar(top)
s.pack(side=tkinter.RIGHT,fill=tkinter.Y)
# Text field
f = tkinter.Text(top,wrap=tkinter.WORD,undo=tkinter.FALSE,yscrollcommand=s.set)
f.pack(expand=tkinter.TRUE,fill=tkinter.BOTH)
s.config(command=f.yview)
# Status bar
s = tkinter.Label(top,text="save&refresh: Ctrl+s; toggle status: Ctrl+space; add under/child: Alt+a/c; tab+/-: Alt+t/T") # status bar
s.pack(side=tkinter.BOTTOM,fill=tkinter.X)
# Column index chosen to mean end of line
colMax = 999


# Read arguments
parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", default="pydone_default",
				help="write report to FILE")
parser.add_option("-t", "--theme", dest="themename", default="",
				help="theme help")
(options, args) = parser.parse_args()
filename = options.filename
themename = options.themename
if filename=="pydone_default" and len(args)>0:
	filename = args[0]

# Make sure the file exists and is empty if default
if filename=="pydone_default":
	open(filename,'w+').close()
else:
	open(filename,'a').close()


# Import color schemes and complete what is not user-defined
theme = {}
if themename != '':
	with open(themename,'r') as t:
		for line in t:
			line = line.split('#')[0]
			line = line.split('=',1)
			if len(line)==2:
				key = line[0].strip()
				value = line[1].strip()
				theme[key] = value

# General
if not 'color' in theme:
	theme['color'] = f.cget('fg')
if not 'selectionBackground' in theme:
	theme['selectionBackground'] = f.cget('selectbackground')
if not 'fieldBackground' in theme:
	theme['fieldBackground'] = f.cget('bg')
f.configure(fg=theme['color'],background=theme['fieldBackground'],selectbackground=theme['selectionBackground'])

# Status bar
if not 'statusFont' in theme:
	theme['statusFont'] = "TkTooltipFont"
if not 'statusColor' in theme:
	theme['statusColor'] = s.cget('fg')
if not 'statusBackground' in theme:
	theme['statusBackground'] = s.cget('bg')
s.configure(font=theme['statusFont'],fg=theme['statusColor'],background=theme['statusBackground'])

# Definitions
if not 'fontDefinition' in theme:
	theme['fontDefinition'] = "TkTooltipFont"
if not 'colorDefinition' in theme:
	theme['colorDefinition'] = "gray50"
if not 'highlightDefinition' in theme:
	theme['highlightDefinition'] = f.cget('background')
if not 'overstrikeDefinition' in theme:
	theme['overstrikeDefinition'] = False
if not 'underlineDefinition' in theme:
	theme['underlineDefinition'] = False
f.tag_config("definition",font=theme['fontDefinition'],foreground=theme['colorDefinition'],background=theme['highlightDefinition'],selectbackground=theme['selectionBackground'],overstrike=theme['overstrikeDefinition'],underline=theme['underlineDefinition'])

# Title
if not 'fontTitle' in theme:
	theme['fontTitle'] = "TkHeadingFont"
if not 'colorTitle' in theme:
	theme['colorTitle'] = f.cget('fg')
if not 'highlightTitle' in theme:
	theme['highlightTitle'] = f.cget('background')
if not 'overstrikeTitle' in theme:
	theme['overstrikeTitle'] = False
if not 'underlineTitle' in theme:
	theme['underlineTitle'] = False
f.tag_config("title",font=theme['fontTitle'],foreground=theme['colorTitle'],background=theme['highlightTitle'],selectbackground=theme['selectionBackground'],overstrike=theme['overstrikeTitle'],underline=theme['underlineTitle'])


# Todo
if not 'fontTodo' in theme:
	theme['fontTodo'] = "TkFixedFont"
if not 'colorTodo' in theme:
	theme['colorTodo'] = f.cget('fg')
if not 'highlightTodo' in theme:
	theme['highlightTodo'] = f.cget('background')
if not 'overstrikeTodo' in theme:
	theme['overstrikeTodo'] = False
if not 'underlineTodo' in theme:
	theme['underlineTodo'] = False
f.tag_config("todo",font=theme['fontTodo'],foreground=theme['colorTodo'],background=theme['highlightTodo'],selectbackground=theme['selectionBackground'],overstrike=theme['overstrikeTodo'],underline=theme['underlineTodo'])

# !
if not 'font!' in theme:
	theme['font!'] = "TkFixedFont"
if not 'color!' in theme:
	theme['color!'] = "DarkGoldenRod1"
if not 'highlight!' in theme:
	theme['highlight!'] = f.cget('background')
if not 'overstrike!' in theme:
	theme['overstrike!'] = False
if not 'underline!' in theme:
	theme['underline!'] = False
f.tag_config("important",font=theme['font!'],foreground=theme['color!'],background=theme['highlight!'],selectbackground=theme['selectionBackground'],overstrike=theme['overstrike!'],underline=theme['underline!'])

# !!
if not 'font!!' in theme:
	theme['font!!'] = "TkFixedFont"
if not 'color!!' in theme:
	theme['color!!'] = "OrangeRed2"
if not 'highlight!!' in theme:
	theme['highlight!!'] = f.cget('background')
if not 'overstrike!!' in theme:
	theme['overstrike!!'] = False
if not 'underline!!' in theme:
	theme['underline!!'] = False
f.tag_config("urgent",font=theme['font!!'],foreground=theme['color!!'],background=theme['highlight!!'],selectbackground=theme['selectionBackground'],overstrike=theme['overstrike!!'],underline=theme['underline!!'])

# !!!
if not 'font!!!' in theme:
	theme['font!!!'] = "TkFixedFont"
if not 'color!!!' in theme:
	theme['color!!!'] = "red"
if not 'highlight!!!' in theme:
	theme['highlight!!!'] = f.cget('background')
if not 'overstrike!!!' in theme:
	theme['overstrike!!!'] = False
if not 'underline!!!' in theme:
	theme['underline!!!'] = True
f.tag_config("deadly",font=theme['font!!!'],foreground=theme['color!!!'],background=theme['highlight!!!'],selectbackground=theme['selectionBackground'],overstrike=theme['overstrike!!!'],underline=theme['underline!!!'])

# Hidden
if not 'fontHidden' in theme:
	theme['fontHidden'] = "TkSmallCaptionFont"
if not 'colorHidden' in theme:
	theme['colorHidden'] = "gray50"
if not 'highlightHidden' in theme:
	theme['highlightHidden'] = f.cget('background')
if not 'overstrikeHidden' in theme:
	theme['overstrikeHidden'] = False
if not 'underlineHidden' in theme:
	theme['underlineHidden'] = False
f.tag_config("hidden",font=theme['fontHidden'],foreground=theme['colorHidden'],background=theme['highlightHidden'],selectbackground=theme['selectionBackground'],overstrike=theme['overstrikeHidden'],underline=theme['underlineHidden'])

# Tag
if not 'fontTag' in theme:
	theme['fontTag'] = "TkTextFont"
if not 'colorTag' in theme:
	theme['colorTag'] = f.cget('fg')
if not 'highlightTag' in theme:
	theme['highlightTag'] = "forest green"
if not 'overstrikeTag' in theme:
	theme['overstrikeTag'] = False
if not 'underlineTag' in theme:
	theme['underlineTag'] = False
f.tag_config("tag",font=theme['fontTag'],foreground=theme['colorTag'],background=theme['highlightTag'],selectbackground=theme['selectionBackground'],overstrike=theme['overstrikeTag'],underline=theme['underlineTag'])

# Date
if not 'fontDate' in theme:
	theme['fontDate'] = "TkTextFont"
if not 'colorDate' in theme:
	theme['colorDate'] = f.cget('fg')
if not 'highlightDate' in theme:
	theme['highlightDate'] = "DarkOrchid3"
if not 'overstrikeDate' in theme:
	theme['overstrikeDate'] = False
if not 'underlineDate' in theme:
	theme['underlineDate'] = False
f.tag_config("date",font=theme['fontDate'],foreground=theme['colorDate'],background=theme['highlightDate'],selectbackground=theme['selectionBackground'],overstrike=theme['overstrikeDate'],underline=theme['underlineDate'])

# Done
if not 'fontDone' in theme:
	theme['fontDone'] = "TkFixedFont"
if not 'colorDone' in theme:
	theme['colorDone'] = "gray50"
if not 'highlightDone' in theme:
	theme['highlightDone'] = f.cget('background')
if not 'overstrikeDone' in theme:
	theme['overstrikeDone'] = True
if not 'underlineDone' in theme:
	theme['underlineDone'] = False
f.tag_config("done",font=theme['fontDone'],foreground=theme['colorDone'],background=theme['highlightDone'],selectbackground=theme['selectionBackground'],overstrike=theme['overstrikeDone'],underline=theme['underlineDone'])



# Function returning list of tags on a line
def tagsOnLine(j):
	line = f.get(str(j)+".0",str(j)+'.'+str(colMax))
	tags = [] # empty list
	for c in range(0,len(line)):
		tag = f.tag_names(str(j)+'.'+str(c))
		for t in tag:
			if t not in tags:
				tags.append(t)
	return tags

# Function hiding tasks
def toggleHidden():
	nbLines = int(f.index(tkinter.END).split('.')[0])
	# First passage to count tabs
	tabs = [-1]
	for i in range(1,nbLines):
		line = f.get(str(i)+".0",str(i)+'.'+str(colMax))
		tabs.append(line.count('\t'))
	
	# Recond passage to act
	for i in range(1,nbLines): # line to be hidden
		visible = True
		j = 1
		while i+j<=nbLines-1:
			# Break if line i+j is not a child or if one todo was found
			if tabs[i+j]<=tabs[i]:
				break
			elif tabs[i+j]==tabs[i]+1 and 'todo' in tagsOnLine(i+j):
				visible = False
				break
			j += 1
		# Toggle visibility
		if visible:
			f.tag_remove("hidden",str(i)+'.0',str(i)+'.'+str(colMax))
		else:
			f.tag_add("hidden",str(i)+'.0',str(i)+'.'+str(colMax))
	return

# Function Inserting file and formatting line by line
def refreshField():
	l  = io.open(filename,'r',encoding='utf-8')
	tagCol = [] # empty custom tags
	tagDef = []
	
	for line in l:
		# Add line
		startLine = f.index("insert")
		startLine = startLine[:-1]+'0'
		endLine = startLine[:-1]+str(colMax)
		f.insert(tkinter.INSERT,line)
		
		# Read the tag definitions, right to left
		if line.startswith("--"):
			while line.count("--")>0:
				f.tag_add("definition",startLine,endLine)
				if line.rfind('=')>line.rfind('--'): # if there is an equal sign only
					tagCol.append(line[line.rfind('=')+1:].strip())
					tagDef.append(line[line.rfind('--')+2:line.rfind('=')].strip())
				line = line[:line.rfind('--')]
				
		# Search for checkbox
		if line.find('[]')>=0 or line.find('[ ]')>=0:
			f.tag_add("todo",startLine,endLine)
		elif line.find('[x]')>=0:
			f.tag_add("done",startLine,endLine)
		elif line!="":
			f.tag_add("title",startLine,endLine)
		
		# Counts !
		important = line.count('!')
		startTask = startLine.split('.')[0]+'.'+str(1+line.find(']'))
		if important==1:
			f.tag_add("important",startTask,endLine)
		elif important==2:
			f.tag_add("urgent",startTask,endLine)
		elif important>=3:
			f.tag_add("deadly",startTask,endLine)
		
		# Finds tags and dates, starting by the end
		endTag = colMax
		while line.count('--')+line.count('//')>0:
			startTag = max(line.rfind('--'),line.rfind('//'))
			if line.rfind('--')>line.rfind('//'):
				f.tag_add("tag",startLine[:-1]+str(startTag),startLine[:-1]+str(endTag))
			else:
				f.tag_add("date",startLine[:-1]+str(startTag),startLine[:-1]+str(endTag))
			endTag = startTag-1
			line = line[:endTag].rstrip()
	l.close()
	toggleHidden()
	
	# Defines the custom tags
	for i in range(0,len(tagDef)):
		try:
			f.tag_config(tagDef[i],background=tagCol[i],foreground="black",selectbackground=theme['selectionBackground'])
		except:
			continue
	f.tag_raise('done')
	# Go back to change them
	tagList = f.tag_ranges('tag')
	for i in range(0,len(tagList),2):
		tag = f.get(tagList[i],tagList[i+1]).lstrip('--')
		if tag in tagDef:
			f.tag_add(tag,tagList[i],tagList[i+1])
			f.tag_remove('tag',tagList[i],tagList[i+1])
	
	return



# Save and refresh formatting
def save(event):
	# Save to file
	try:
		with io.open(filename,'w',encoding='utf-8') as l:
			l.write(f.get("1.0",'end-1c'))
		# Remove all tags
		tagList = f.tag_names()
		for tag in tagList:
			f.tag_remove(tag,1.0)
		# Empty and refresh, saving cursor position
		cursor = f.index(tkinter.INSERT)
		f.delete('1.0', tkinter.END)
		refreshField()
		f.mark_set(tkinter.INSERT,cursor)
		# Reset window title
		top.wm_title(filename+" -- PyDone")
	except Exception as error:
		print("Error saving:",error)
f.bind("<Control-s>", save)


# Toggle todo/done status
def toggle(event):
	cursor = f.index(tkinter.INSERT)
	line=f.get("insert linestart","insert lineend")
	startBox = line.find('[')
	f.mark_set(tkinter.INSERT,cursor.split('.')[0]+'.'+str(startBox))
	f.tag_remove("hidden",tkinter.INSERT,"insert lineend")
	if line[startBox+1]==']':
		f.delete(tkinter.INSERT,"insert+2c")
		f.insert(tkinter.INSERT,"[x]")
		f.tag_remove("todo","insert linestart","insert lineend")
		f.tag_add("done","insert linestart","insert lineend")
		f.mark_set(tkinter.INSERT,cursor.split('.')[0]+'.'+str(cursor.split('.')[1]+1))
	elif line[startBox+1:startBox+3]==' ]':
		f.delete(tkinter.INSERT,"insert+3c")
		f.insert(tkinter.INSERT,"[x]")
		f.tag_remove("todo","insert linestart","insert lineend")
		f.tag_add("done","insert linestart","insert lineend")
		f.mark_set(tkinter.INSERT,cursor.split('.')[0]+'.'+cursor.split('.')[1])
	elif line[startBox+1:startBox+3]=='x]':
		f.delete(tkinter.INSERT,"insert+3c")
		f.insert(tkinter.INSERT,"[ ]")
		f.tag_remove("done","insert linestart","insert lineend")
		f.tag_add("todo","insert linestart","insert lineend")
		f.mark_set(tkinter.INSERT,cursor.split('.')[0]+'.'+cursor.split('.')[1])
	toggleHidden()
	top.wm_title(filename+" * -- PyDone")
f.bind("<Control-space>", toggle)


# Add new tasks
def add(event):
	# Count tabs
	line=f.get("insert linestart","insert lineend")
	tabs = line.count('\t')
	# Move and insert tabs and box
	f.mark_set(tkinter.INSERT,"insert+1l linestart")
	f.insert(tkinter.INSERT,'\t'*tabs+'[ ] \n',"todo")
	f.mark_set(tkinter.INSERT,"insert-1c")
	toggleHidden()
	top.wm_title(filename+" * -- PyDone")
f.bind("<Alt-a>",add)
def addChild(event):
	# Count tabs
	line=f.get("insert linestart","insert lineend")
	tabs = line.count('\t')
	# Move and insert tabs and box
	f.mark_set(tkinter.INSERT,"insert+1l linestart")
	f.insert(tkinter.INSERT,'\t'*tabs+'\t[ ] \n',"todo")
	f.mark_set(tkinter.INSERT,"insert-1c")
	toggleHidden()
	top.wm_title(filename+" * -- PyDone")
f.bind("<Alt-c>",addChild)


# Change identation
def addTab(event):
	f.insert("insert linestart",'\t')
	toggleHidden()
	top.wm_title(filename+" * -- PyDone")
f.bind("<Alt-t>",addTab)
def removeTab(event):
	tab = f.get("insert linestart","insert lineend").find('\t')
	if tab>=0:
		f.delete(f.index(tkinter.INSERT).split('.')[0]+'.'+str(tab))
	toggleHidden()
	top.wm_title(filename+" * -- PyDone")
f.bind("<Alt-T>",removeTab)


# Change window title if an alphanumeric character or a space is typed
def modified(event):
	if event.char.isalnum() or event.char.isspace():
		top.wm_title(filename+" * -- PyDone")
f.bind("<KeyPress>",modified)
# Refresh the screen if a modification is undone or redone
#def ifUndo(event):
#	print('cancelled')
#	toggleHidden()
#top.bind("<Control-z>",ifUndo)
#top.bind("<Control-Z>",ifUndo)
#top.bind("<Control-y>",ifUndo)


# Start UI
refreshField() # Initialize the field
top.wm_title(filename+" -- PyDone") # Reinitialize the window title
f.configure(undo=tkinter.TRUE) # Allows undo/redo now
top.mainloop()
