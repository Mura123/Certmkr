import csv
import os
import draw
#Dependencies
from appJar import gui

MAX_IMAGE_SIZE = 700

option_frames = None
current_option_frame_idx = None

infos = {'headers':None,'csv_file':None,
         'template_file':None,'output_directory':None,
         'font':None,'columns':None}

draw_infos = {}

def press(btn):
    global infos
    global current_option_frame_idx
    if(btn=='select_columns'):
        second_screen()
    elif(btn=='adjust_to_template'):
        third_screen()
    elif(btn=='Next'):
        get_option_frame_data()
        if(current_option_frame_idx < len(option_frames)-1):
            current_option_frame_idx += 1
            regui_option_frame(current_option_frame_idx)
    elif(btn=='Prev'):
        get_option_frame_data()
        if(current_option_frame_idx > 0):
            current_option_frame_idx -= 1
            regui_option_frame(current_option_frame_idx)
    elif(btn=='Preview'):
        get_option_frame_data()
        regui_preview_frame(infos['template_file'], draw_text=True)
    elif(btn=='Done!'):
        get_option_frame_data()
        fourth_screen()
    elif(btn=='PRINT!'):
        name_template = app.getEntry('File_Name_Template')
        header_ID = app.getOptionBox('Column to use to differentiate file names:')
        draw.generate_multiples(infos['template_file'],draw_infos,infos['font'],
                                name_template,header_ID,infos['output_directory'])
        app.stop()

def get_option_frame_data():
    header = option_frames[current_option_frame_idx]
    x = int(app.getEntry('X:'))
    y = int(app.getEntry('Y:'))
    fs = int(app.getEntry('Font size:'))
    r = int(app.getEntry('R:'))
    g = int(app.getEntry('G:'))
    b = int(app.getEntry('B:'))
    draw_infos[header]['coords'] = (x,y)
    draw_infos[header]['font_size'] = fs
    draw_infos[header]['rgb'] = (r,g,b)

def gui_option_frame(i):
    header = option_frames[current_option_frame_idx]
    with app.labelFrame('Options',row=0,column=0,sticky='ew'):
        app.addLabel(header,row=0)
        app.addLabelNumericEntry('X:',row=1)
        app.setEntry('X:',draw_infos[header]['coords'][0])
        app.addLabelNumericEntry('Y:',row=2)
        app.setEntry('Y:',draw_infos[header]['coords'][1])
        app.addLabelNumericEntry('Font size:')
        app.setEntry('Font size:',draw_infos[header]['font_size'])
        for num,c in enumerate(['R:','G:','B:']):
            app.addLabelNumericEntry(c)
            app.setEntry(c,draw_infos[header]['rgb'][num])
        app.addButtons(['Prev','Next'],press)

def regui_option_frame(i):
    app.emptyLabelFrame('Options')
    gui_option_frame(i)

def gui_preview_frame(template, draw_text=False):
    if(draw_text):
        #draw largest texts from each used header to preview screen
        draw.draw_preview(template,MAX_IMAGE_SIZE,draw_infos,infos['font'])
    else:
        draw.draw_preview(template,MAX_IMAGE_SIZE)
    with app.labelFrame('Preview',row=0,column=1,sticky='news',rowspan=3):
        with app.frame('img', bg='grey'):
            app.addImage('testimg','temp.gif')

def regui_preview_frame(template, draw_text=False):
    app.emptyLabelFrame('Preview')
    gui_preview_frame(template,draw_text)

def first_screen():
    app.addLabel('Select CSV File',row=0,column=0)
    app.addFileEntry('Input_CSV',row=0,column=1)
    app.addLabel('Select template image (PNG, PSD)',row=1,column=0)
    app.addFileEntry('Input_Template',row=1,column=1)
    app.addLabel('Select output directory',row=2,column=0)
    app.addDirectoryEntry('Output_Directory',row=2,column=1)
    app.addLabel('Select font',row=3,column=0)
    with os.scandir(os.path.join(os.getcwd(),'fonts')) as entries:
        app.addAutoEntry('Input_Font',words=[entry.name for entry in entries],row=3,column=1)
    app.addNamedButton('Next','select_columns',press,row=4,column=1)

def second_screen():
    # Processing first screen
    infos['csv_file'] = app.getEntry('Input_CSV')
    infos['template_file'] = app.getEntry('Input_Template')
    infos['output_directory'] = app.getEntry('Output_Directory')
    infos['font'] = os.path.join(os.getcwd(),'fonts',app.getEntry('Input_Font'))
    
    with open(infos['csv_file'], 'r', encoding='utf-8', newline='') as arq:
        d_reader = csv.DictReader(arq)
        infos['headers'] = d_reader.fieldnames
    
    # Creating second screen
    app.emptyFrame('main')
    with app.frame('main'):
        app.addLabel('Which columns to use?')
        count=0
        for h in infos['headers']:
            app.addCheckBox(count,name=h)
            count+=1
        app.addNamedButton('Next','adjust_to_template',press)

def third_screen():
    global option_frames
    global current_option_frame_idx
    # Processing second screen
    infos['columns'] = app.getAllCheckBoxes()
    option_frames = [infos['headers'][k] for k in infos['columns'] if infos['columns'][k]]
    with open(infos['csv_file'], 'r', encoding='utf-8', newline='') as arq:
        d_reader = csv.DictReader(arq)
        for o in option_frames:
            draw_infos[o] = {'coords':(0,0), 'font_size':1, 'rgb':(0,0,0), 'texts':[], 'largest':''}
        for row in d_reader:
            for o in option_frames:
                draw_infos[o]['texts'].append(row[o])
                if(len(row[o]) > len(draw_infos[o]['largest'])):
                    draw_infos[o]['largest'] = row[o]
    # Creating third screen
    app.setSize('1000x800')
    app.emptyFrame('main')
    with app.frame('main'):
        # Options Frame
        current_option_frame_idx = 0
        gui_option_frame(current_option_frame_idx)
        app.addButton('Preview',press)
        app.addButton('Done!',press)
        # Preview Frame
        gui_preview_frame(infos['template_file'])

def fourth_screen():
    app.setSize('600x300')
    app.emptyFrame('main')
    with app.frame('main'):
        app.addLabel('Please enter a name template for you files below')
        app.addEntry('File_Name_Template')
        app.addLabelOptionBox('Column to use to differentiate file names:',option_frames)
        app.addButton('PRINT!',press)

### Start GUI ###
with gui('CERTMKR 0.00001','600x300',sticky='news', stretch='both') as app:
    app.setPadding(20,20)
    app.setInPadding(20,60)
    with app.frame('main'):
        first_screen()
