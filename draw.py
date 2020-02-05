from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageFile
import os

def draw_preview(template_file, max_size, draw_infos=None,  font=None):
    with Image.open(template_file) as im:
        #draw preview text
        if(draw_infos != None and font != None):
            for k in draw_infos:
                draw_text(im,draw_infos[k]['largest'],draw_infos[k]['rgb'],
                          draw_infos[k]['coords'],font,draw_infos[k]['font_size'])
        #readjust img to fit preview frame
        width, height = im.size
        if(width > max_size or height > max_size):
            if(width > height):
                img_ratio = height/width
                new_height = max_size * img_ratio
                im = im.resize((max_size, round(new_height)))
            else:
                img_ratio = width/height
                new_width = max_size * img_ratio
                im = im.resize((round(new_width), max_size))
        im.save('temp.gif','GIF')

def draw_text(img, txt, rgb=(0,0,0), coords=(0,0), font=None,font_size=1):
    select_font = ImageFont.truetype(font, size = font_size)
    draw = ImageDraw.Draw(img)
    
    txt_offset = select_font.getoffset(txt)
    largura_txt, altura_txt = draw.textsize(txt,font=select_font)

    pos_x = coords[0] - txt_offset[0] - (largura_txt/2)
    pos_y = coords[1] - txt_offset[1] - (altura_txt/2)
    
    draw.text((pos_x,pos_y), txt, rgb, font=select_font)
    #img.save('certificados/'+nome_arq+linhas[0].replace(' ','')+'.pdf','PDF', resolution=100)

def generate_multiples(template_file,draw_infos,font,name_template,header_ID,output_directory):
    with Image.open(template_file) as im:
        num_rows = len(list(draw_infos.items())[0][1]['texts'])
        IDs = []#list of UNIQUE file name ids
        count = 2
        for i in range(num_rows):
            with im.copy() as img_copy:
                #prints to one document
                for k in draw_infos:
                    if(k == header_ID):
                        ID = draw_infos[k]['texts'][i]
                        if(ID in IDs):
                            ID += str(count)
                            count += 1
                        else:
                            IDs.append(ID)
                    draw_text(img_copy,draw_infos[k]['texts'][i],draw_infos[k]['rgb'],
                              draw_infos[k]['coords'],font,draw_infos[k]['font_size'])
                file_path = os.path.join(output_directory,name_template+'_'+ID+'.pdf')
                img_copy.save(file_path,'PDF', resolution=100)
