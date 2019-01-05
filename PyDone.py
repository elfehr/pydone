#!/usr/bin/python
# Use:  python3 todoeditor.py file

### EXAMPLE FILE
#Category
#[ ] Project
#	[ ] Subproject
#	[ ] Subproject --tag //deadline
#		[x] Subsubproject
#		[ ] ! Important subsubproject //deadline
#		[ ] Urgent subsubproject !! --tag
#			[ ] !!! Very very important subsubsubproject
#		[x] Subsubproject
#	[ ] Subproject //deadline --custom tag
#--custom tag = red

from tkinter import *
import sys

# Fields definition
# Window
top = Tk()
# Scrollbar
s = Scrollbar(top)
s.pack(side=RIGHT,fill=Y)
# Text field
top.wm_title("To do list")
f = Text(top,bg='white',fg='black',wrap=WORD,font=("Latin Modern Mono",12),selectbackground="SlateGray2",yscrollcommand=s.set)
f.pack(expand=TRUE,fill=BOTH)
s.config(command=f.yview)
# Status bar
s = Label(top,text="save&refresh: <ctrl-s>; toggle status: <ctrl-space>; add under: <ctrl-a>",bg='gray20',fg='white',bd=0) # status bar
s.pack(side=BOTTOM,fill=X)


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


# Inserts file and formatting line by line
def refreshField():
	l  = open(sys.argv[1],'r')
	tagCol = [] # empty custom tags
	tagDef = []
	tabs = [-1] # empty indentation list
	for line in l:
		# Add line
		startLine = f.index("insert")
		startLine = startLine[:-1]+'0'
		endLine = startLine[:-1]+'999'
		f.insert(INSERT,line)
		
		# Read the tag definitions, right to left
		if line.startswith("--"):
			while line.count("--")>0:
				f.tag_add("definition",startLine,endLine)
				if line.rfind('=')>line.rfind('--'): # if there is an equal sign only
					tagCol.append(line[line.rfind('=')+1:].strip())
					tagDef.append(line[line.rfind('--')+2:line.rfind('=')].strip())
				line = line[:line.rfind('--')]
		
		# Count indentation
		tabs.append(line.count('\t'))
		
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
		endTag = 999
		while line.count('--')+line.count('//')>0:
			startTag = max(line.rfind('--'),line.rfind('//'))
			if line.rfind('--')>line.rfind('//'):
				f.tag_add("tag",startLine[:-1]+str(startTag),startLine[:-1]+str(endTag))
			else:
				f.tag_add("date",startLine[:-1]+str(startTag),startLine[:-1]+str(endTag))
			endTag = startTag-1
			line = line[:endTag].rstrip()
	l.close()
	
	
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
	
	
	# Tasks to be hidden
	print(tabs)
	for i in range(1,len(tabs)-1): # line to be hidden
		print(i)
		visible = TRUE
		j = 1
		while i+j<=len(tabs)-1:
			print('\t'*tabs[i+j],i+j)
			if tabs[i+j]<=tabs[i]:
				print('\t'*tabs[i+j],'not child')
				break
			if tabs[i+j]==tabs[i]+1:
				print('\t'*tabs[i+j],'correct indentation')
				if 'todo' in f.tag_names(str(i+j)+'.0'):
					print('\t'*tabs[i+j],'FALSE')
					visible = FALSE
					break
			j += 1
		# Toggle visibility
		if visible:
			f.tag_remove("hidden",str(i)+'.0',str(i)+'.999')
		else:
			f.tag_add("hidden",str(i)+'.0',str(i)+'.999')
	
	return



# Save and refresh formatting
def save(event):
	# Save to file
	l = open(sys.argv[1],'w')
	l.write(f.get("1.0",'end-1c'))
	l.close()
	print('saved')
	# Remove all tags
	tagList = f.tag_names()
	for tag in tagList:
		f.tag_remove(tag,1.0)
	# Empty and refresh, saving cursor position
	cursor = f.index(INSERT)
	f.delete('1.0', END)
	refreshField()
	f.mark_set(INSERT,cursor)
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
		f.tag_remove("todo",INSERT,"insert lineend")
		f.tag_add("done",INSERT,"insert lineend")
		f.mark_set(INSERT,cursor.split('.')[0]+'.'+cursor.split('.')[1]+1)
	elif line[startBox+1:startBox+3]==' ]':
		f.delete(INSERT,"insert+3c")
		f.insert(INSERT,"[x]")
		f.tag_remove("todo",INSERT,"insert lineend")
		f.tag_add("done",INSERT,"insert lineend")
		f.mark_set(INSERT,cursor.split('.')[0]+'.'+cursor.split('.')[1])
	elif line[startBox+1:startBox+3]=='x]':
		f.delete(INSERT,"insert+3c")
		f.insert(INSERT,"[ ]")
		f.tag_remove("done",INSERT,"insert lineend")
		f.tag_add("todo",INSERT,"insert lineend")
		f.mark_set(INSERT,cursor.split('.')[0]+'.'+cursor.split('.')[1])
f.bind("<Control-space>", toggle)


# Add new task
def add(event):
	# Count tabs
	line=f.get("insert linestart","insert lineend")
	tabs = line.count('\t')
	# Move and insert tabs and box
	f.mark_set(INSERT,"insert+1l linestart")
	f.insert(INSERT,'\t'*tabs+'[ ] \n',"todo")
	f.mark_set(INSERT,"insert-1c")
f.bind("<Alt-a>", add)


# Start UI
refreshField()
top.mainloop()
