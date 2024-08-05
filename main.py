#start
import tkinter as tk
from tkinter import scrolledtext 
import sys
import os

if getattr(sys, 'frozen', False):
    directory_name = os.path.dirname(sys.executable)
elif __file__:
    directory_name= os.path.dirname(__file__)

os.chdir(directory_name)

acm="00000000"
values=[]
addrs=[]
gets=[]

def logw(string):
    log['state']=tk.NORMAL
    log.insert('end', string + '\n')
    log['state']=tk.DISABLED

def execute(instruction, value):
    global addrs, values , acm , index
    if instruction=="000":
        for i in range(len(addrs)):
            if addrs[i]["text"]==value:
                a=i
        logw("Loaded "+ values[a]["text"] + "   (" + str(int(values[a]["text"], 2)) + ")")
        acm=values[a]["text"]
        index=index+1
        return True
    if instruction=="001":
        for i in range(len(addrs)):
            if addrs[i]["text"]==value:
                values[i]["text"]=acm
        logw("Stored "+ acm + "(" + str(int(acm, 2)) + ")" + " at " + value)
        index=index+1
        return True
    if instruction=="010":
        for i in range(len(addrs)):
            if addrs[i]["text"]==value:
                a=i
        added=int(acm, 2)+int(values[a]["text"], 2)
        added=str(format(added, "08b"))
        logw("Added "+ values[a]["text"] + "(" + str(int(values[a]["text"], 2)) + ")" + " to " + acm + "(" + str(int(acm, 2)) + ")   -> " + added + "(" + str(int(added, 2)) + ")")
        acm=added
        index=index+1
        return True
    if instruction=="011":
        for i in range(len(addrs)):
            if addrs[i]["text"]==value:
                a=i
        added=int(acm, 2)-int(values[a]["text"], 2)
        added=str(format(added, "08b"))
        logw("substracted "+ values[a]["text"] + "(" + str(int(values[a]["text"], 2)) + ")" + " from " + acm + "(" + str(int(acm, 2)) + ")   -> " + added + "(" + str(int(added, 2)) + ")")
        acm=added
        index=index+1
        return True
    if instruction=="100":
        for i in range(len(addrs)):
            if addrs[i]["text"]==value:
                if int(acm, 2)==0:
                    index=i
                    logw("Branching to " + value)
                else:
                    logw("Unable to branch: Stored number is not equal to 0. Passing")
                    index=index+1
        return True
    if instruction=="101":
        for i in range(len(addrs)):
            if addrs[i]["text"]==value:
                if int(acm, 2)>0:
                    index=i
                    logw("Branching to " + value)
                else:
                    logw("Unable to branch: Stored number is not positive. Passing")
                    index=index+1
        return True
    if instruction=="110":
        for i in range(len(addrs)):
            if addrs[i]["text"]==value:
                acm=values[i]["text"]
        logw("=====================")
        logw("Printing: " + acm + "   (" + str(int(acm, 2)) + ")")
        logw("=====================")
        index=index+1
        return True
    if instruction=="111":
        logw("Program halted")
        return False

def start():
    global addrs, values , index
    try:
        v=values[index]["text"]
        a=addrs[index]["text"]
        instr=v[0]+v[1]+v[2]
        cont=v[3]+v[4]+v[5]+v[6]+v[7]
        if execute(instr, cont):
            start()
    except Exception as e:
        logw(str(e))
        logw("U wrote a shitty program so try again")

def run():
    global addrs, values , index
    for i in range(len(values)):
        if len(values[i]["text"])!=8:
            swap_view(i)

    with open("mem_vis.txt", "w") as txt_file:
        for i in range(len(addrs)):
            txt_file.write(addrs[i]["text"] + ":" + values[i]["text"]+"\n")
        txt_file.close()
    index=0
    start()

def load_from_txt():
    global addrs, values , gets 
    with open("mem_vis.txt", "r") as txt_file:
        index=0
        for line in txt_file:
            adress, adress_value = line.split(":")
            adress_value=adress_value.strip()
            values[index]["text"]=adress_value
            gets[index].delete(0, tk.END)
            gets[index].insert(tk.END, adress_value)
            index=index+1
        txt_file.close()

def convert():
    try:
        number=dec_entry.get()
        bin_number=format(int(number), '08b')
        bin_entry.delete(0, tk.END)
        bin_entry.insert(0, bin_number)
    except Exception as e:
        logw(str(e))

def check_pos(index):
    global values
    comparable=32
    for i in range(len(values)):
        if values[i]["text"]=="11111111" or values[i]["text"]=="Halt":
            comparable=i
    if index<comparable:
        return True
    else:
        return False

def get_inst(string):
    if (string=="000"):
        return "Load   "
    
    if (string=="001"):
        return "Store  "
    
    if (string=="010"):
        return "Add    "
    
    if (string=="011"):
        return "Subs   "
    
    if (string=="100"):
        return "Br_eq0 "
    
    if (string=="101"):
        return "Br_ps  "
    
    if (string=="110"):
        return "Print  "
    
    if (string=="111"):
        return "Halt   "

def get_reverse_instr(string):
    if (string=="Load   "):
        return "000"
    
    if (string=="Store  "):
        return "001"
    
    if (string=="Add    "):
        return "010"
    
    if (string=="Subs   "):
        return "011"
    
    if (string=="Br_eq0 "):
        return "100"
    
    if (string=="Br_ps  "):
        return "101"
    
    if (string=="Print  "):
        return "110"
    
    if (string=="Halt   "):
        return "111"

def write_in_matrix(index):
    global values, gets
    number=gets[index].get()
    values[index]["text"]=number
    done=0

def swap_view(index):
    global values
    current_value=values[index]["text"]

    if check_pos(index):
        if len(current_value)==8:
            values[index]["text"]=get_inst(current_value[0]+current_value[1]+current_value[2]) + str(current_value[3]+current_value[4]+current_value[5]+current_value[6]+current_value[7])
        else:
            values[index]["text"]=get_reverse_instr(current_value[0]+current_value[1]+current_value[2]+current_value[3]+current_value[4]+current_value[5]+current_value[6]) + str(current_value[7]+current_value[8]+current_value[9]+current_value[10]+current_value[11])
    else:
        if current_value=="11111111":
            values[index]["text"]="Halt"
        if current_value=="Halt":
            values[index]["text"]="11111111"
        if current_value!="11111111" and current_value!="Halt":
            if len(current_value)==8:
                values[index]["text"]=str(int(current_value, 2))
            else:
                values[index]["text"]=format(int(current_value), "08b")

############################################################################################################
#gui start
gui_default_width= 1920
gui_default_height= 1090

root = tk.Tk(className = 'mif simulation')
root.geometry(str(gui_default_width) + 'x' + str(gui_default_height))
root.wm_state('zoomed')

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=3)
root.grid_columnconfigure(1, weight=1)

frame84=tk.LabelFrame(root, text='Memory', bg='#BCA9F5', highlightthickness=1, highlightbackground='black')
frame84.grid(row=0, column=0, sticky='nsew')
frame84.grid_columnconfigure(0, weight=3)
frame84.grid_columnconfigure(1, weight=1)
frame84.grid_rowconfigure(0, weight=1)

memxx=tk.LabelFrame(frame84, text="Matrix representaion", bg='#BCA9F5', highlightthickness=1, highlightbackground='black')
memxx.grid(row=0, column=0, sticky="nsew")

for i in range(0, 10):
    memxx.grid_columnconfigure(i, weight=1)
for i in range(0, 12):
    memxx.grid_rowconfigure(i, weight=1)

i=1
j=1
counter=0

while (i<9 and j<8):
    addr=tk.Label(memxx, bg='#BCA9F5', text=format(counter, '05b'))
    addr.grid(row=j, column=i, sticky="s")
    addrs.append(addr)

    value=tk.Button(memxx, text="00000000", height=1, width=10,  command= lambda counter=counter: swap_view(counter))
    value.grid(row=j+1, column=i, sticky="n")
    values.append(value)

    if i<8:
        i+=1
    else:
        i=1
        j+=2
    counter+=1
    
memy=tk.LabelFrame(frame84, text="Workspace", bg='#BCA9F5', highlightthickness=1, highlightbackground='black')
memy.grid(row=0, column=1, sticky="nsew")

memy.grid_columnconfigure(0, weight=1)
memy.grid_columnconfigure(1, weight=1)
memy.grid_columnconfigure(2, weight=1)
for i in range(33):
    memy.grid_rowconfigure(i, weight=1)

i=1
j=1
counter=0
while (i<9 and j<8):
    a=tk.Label(memy, bg='#BCA9F5', text=format(counter, '05b'))
    a.grid(row=counter, column=0)

    b=tk.Entry(memy)
    b.grid(row=counter, column=1)
    gets.append(b)

    c=tk.Button(memy, text="Push", command= lambda c=counter : write_in_matrix(c))
    c.grid(row=counter, column=2)

    if i<8:
        i+=1
    else:
        i=1
        j+=2
    counter+=1

run_button=tk.Button(memxx, text="Run", bg='#BCA9F5', command= lambda: run()) 
run_button.grid(row=10, column=4, sticky="sew")
load_txt=tk.Button(memxx, text="Load from txt", bg='#BCA9F5', command= lambda: load_from_txt())
load_txt.grid(column=5, row=10, sticky="sew")

##############################################################################################################
frame2=tk.LabelFrame(root, text='Others', bg='#BCA9F5', highlightthickness=1, highlightbackground='black')
frame2.grid(row=0, column=1, sticky='nsew')
frame2.grid_columnconfigure(0, weight=1)
frame2.grid_rowconfigure(0, weight=1)
frame2.grid_rowconfigure(1, weight=1)
frame2.grid_rowconfigure(2, weight=3)

instructions_frame=scrolledtext.ScrolledText(frame2, state='disabled', width=1, height=1)
instructions_frame.grid(row=0, column=0, sticky="nsew")
instructions_frame['state']=tk.NORMAL
instructions_frame.insert('end', "Available instructions:" + '\n')
instructions_frame.insert('end', "000 -- Load" + '\n')
instructions_frame.insert('end', "001 -- Store" + '\n')
instructions_frame.insert('end', "010 -- Add" + '\n')
instructions_frame.insert('end', "011 -- Substract" + '\n')
instructions_frame.insert('end', "100 -- Branch if 0" + '\n')
instructions_frame.insert('end', "101 -- Branch if pos" + '\n')
instructions_frame.insert('end', "110 -- Output" + '\n')
instructions_frame.insert('end', "111 -- Halt" + '\n')
instructions_frame['state']=tk.DISABLED


convert_frame=tk.LabelFrame(frame2, bg='#BCA9F5', highlightthickness=1, highlightbackground='black')
convert_frame.grid(row=1, column=0)

convert_frame.grid_columnconfigure(0, weight=1)
convert_frame.grid_columnconfigure(1, weight=1)
convert_frame.grid_rowconfigure(0, weight=1)
convert_frame.grid_rowconfigure(1, weight=1)
convert_frame.grid_rowconfigure(2, weight=1)

dec_label=tk.Label(convert_frame, bg='#BCA9F5', text="Dec. number:")
dec_label.grid(column=0, row=0)
dec_entry=tk.Entry(convert_frame)
dec_entry.grid(row=0, column=1)

bin_label=tk.Label(convert_frame, bg='#BCA9F5', text="Bin. number:")
bin_label.grid(column=0, row=1)
bin_entry=tk.Entry(convert_frame)
bin_entry.grid(row=1, column=1)

convert_btn=tk.Button(convert_frame, bg='#BCA9F5', text="Convert", command=lambda: convert())
convert_btn.grid(row=2, column=1)

log_frame=tk.LabelFrame(frame2, text="Log")
log_frame.grid(row=2, column=0, sticky="nsew")
log_frame.grid_columnconfigure(0, weight=1)
log_frame.grid_rowconfigure(0, weight=1)
log=scrolledtext.ScrolledText(log_frame, state='disabled', width=1, height=1)
log.grid(row=0, column=0, sticky='nsew')

root.mainloop()