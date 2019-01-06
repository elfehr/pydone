#!/usr/bin/python
# gitlab.com/eyuku/pydone


from tkinter import *
import sys

# Define filename and make sure it exists
if len(sys.argv)>1:
	filename = sys.argv[1]
	open(filename,'a').close()
else:
	# Choose the default name and make sure the file is empty
	filename = "pydone_default"
	open(filename,'w+').close()


# Fields definition
# Window
top = Tk()
ico = PhotoImage(file='PyDone.png')
top.iconphoto(True, ico)
# Scrollbar
s = Scrollbar(top)
s.pack(side=RIGHT,fill=Y)
# Text field
f = Text(top,bg='white',fg='black',wrap=WORD,undo=FALSE,font=("Latin Modern Mono",12),selectbackground="SlateGray2",yscrollcommand=s.set)
f.pack(expand=TRUE,fill=BOTH)
s.config(command=f.yview)
# Status bar
s = Label(top,text="save&refresh: Ctrl+s; toggle status: Ctrl+space; add under/child: Alt+a/c; tab+/-: Alt+t/T",bg='gray20',fg='white',bd=0) # status bar
s.pack(side=BOTTOM,fill=X)
# Column index chosen to mean end of line
colMax = 999


# Formatting, by lowest priority
f.tag_config("definition",font=("Latin Modern Mono",10),foreground="gray80")
f.tag_config("title",underline=0,font=("Latin Modern Mono Caps",15))
f.tag_config("todo",foreground="black",overstrike=0,underline=0,background="white",selectbackground="SlateGray2")
f.tag_config("important",foreground="orange")
f.tag_config("urgent",foreground="orange red")
f.tag_config("deadly",foreground="red2",underline=1)
f.tag_config("hidden",foreground="gray80")
f.tag_config("tag",background="orange",foreground="black",selectbackground="SlateGray2")
f.tag_config("date",background="MediumPurple4",foreground="white",selectbackground="SlateGray2")
f.tag_config("done",foreground="gray80",overstrike=0,underline=0,background="white",selectbackground="SlateGray2")


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
	nbLines = int(f.index(END).split('.')[0])
	# First passage to count tabs
	tabs = [-1]
	for i in range(1,nbLines):
		line = f.get(str(i)+".0",str(i)+'.'+str(colMax))
		tabs.append(line.count('\t'))
	
	# Recond passage to act
	for i in range(1,nbLines): # line to be hidden
		visible = TRUE
		j = 1
		while i+j<=nbLines-1:
			# Break if line i+j is not a child or if one todo was found
			if tabs[i+j]<=tabs[i]:
				break
			elif tabs[i+j]==tabs[i]+1 and 'todo' in tagsOnLine(i+j):
				visible = FALSE
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
	l  = open(filename,'r')
	tagCol = [] # empty custom tags
	tagDef = []
	
	for line in l:
		# Add line
		startLine = f.index("insert")
		startLine = startLine[:-1]+'0'
		endLine = startLine[:-1]+str(colMax)
		f.insert(INSERT,line)
		
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
			f.tag_config(tagDef[i],background=tagCol[i],foreground="black",selectbackground="SlateGray2")
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
	l = open(filename,'w')
	l.write(f.get("1.0",'end-1c'))
	l.close()
	# Remove all tags
	tagList = f.tag_names()
	for tag in tagList:
		f.tag_remove(tag,1.0)
	# Empty and refresh, saving cursor position
	cursor = f.index(INSERT)
	f.delete('1.0', END)
	refreshField()
	f.mark_set(INSERT,cursor)
	# Reset window title
	top.wm_title(filename+" -- PyDone")
f.bind("<Control-s>", save)


# Toggle todo/done status
def toggle(event):
	cursor = f.index(INSERT)
	line=f.get("insert linestart","insert lineend")
	startBox = line.find('[')
	f.mark_set(INSERT,cursor.split('.')[0]+'.'+str(startBox))
	f.tag_remove("hidden",INSERT,"insert lineend")
	if line[startBox+1]==']':
		f.delete(INSERT,"insert+2c")
		f.insert(INSERT,"[x]")
		f.tag_remove("todo","insert linestart","insert lineend")
		f.tag_add("done","insert linestart","insert lineend")
		f.mark_set(INSERT,cursor.split('.')[0]+'.'+str(cursor.split('.')[1]+1))
	elif line[startBox+1:startBox+3]==' ]':
		f.delete(INSERT,"insert+3c")
		f.insert(INSERT,"[x]")
		f.tag_remove("todo","insert linestart","insert lineend")
		f.tag_add("done","insert linestart","insert lineend")
		f.mark_set(INSERT,cursor.split('.')[0]+'.'+cursor.split('.')[1])
	elif line[startBox+1:startBox+3]=='x]':
		f.delete(INSERT,"insert+3c")
		f.insert(INSERT,"[ ]")
		f.tag_remove("done","insert linestart","insert lineend")
		f.tag_add("todo","insert linestart","insert lineend")
		f.mark_set(INSERT,cursor.split('.')[0]+'.'+cursor.split('.')[1])
	toggleHidden()
	top.wm_title(filename+" * -- PyDone")
f.bind("<Control-space>", toggle)


# Add new tasks
def add(event):
	# Count tabs
	line=f.get("insert linestart","insert lineend")
	tabs = line.count('\t')
	# Move and insert tabs and box
	f.mark_set(INSERT,"insert+1l linestart")
	f.insert(INSERT,'\t'*tabs+'[ ] \n',"todo")
	f.mark_set(INSERT,"insert-1c")
	toggleHidden()
	top.wm_title(filename+" * -- PyDone")
f.bind("<Alt-a>",add)
def addChild(event):
	# Count tabs
	line=f.get("insert linestart","insert lineend")
	tabs = line.count('\t')
	# Move and insert tabs and box
	f.mark_set(INSERT,"insert+1l linestart")
	f.insert(INSERT,'\t'*tabs+'\t[ ] \n',"todo")
	f.mark_set(INSERT,"insert-1c")
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
		f.delete(f.index(INSERT).split('.')[0]+'.'+str(tab))
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
f.configure(undo=TRUE) # Allows undo/redo now
top.mainloop()
