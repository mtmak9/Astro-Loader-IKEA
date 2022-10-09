from concurrent.futures import thread
from inspect import signature
from turtle import left
from pyautogui import *
from tkinter import *
from tkinter import messagebox, filedialog
import time, os, ctypes, sys, easygui, pyautogui
from time import perf_counter
from PIL import ImageTk,Image 
import threading

root=Tk()
app_title = 'Astro Loader v1.0(beta)'
root.title(app_title)
root.iconbitmap('data\\icon.ico')
root.geometry("400x545")
root.configure(bg="#0454a0")
root.resizable(0,0)

my_menu = Menu(root)
root.config(menu=my_menu)

#file_path = StringVar.get()
shipment = StringVar()
seal = StringVar()
registration = StringVar()
trailer_id = StringVar()
global my_sign
my_sign = ('my_sign.png')

#saving settings
if os.path.isfile('output.txt'):
        with open('output.txt','r') as f:
            all_lines = f.read().split(',')
            shipment.set(all_lines[0])
            registration.set(all_lines[1])
            seal.set(all_lines[2])
            trailer_id.set(all_lines[3])

def signature_file():
    global my_sign
    root.my_sign = filedialog.askopenfilename()
    print(root.my_sign)

def is_capslock_on():
    if ctypes.WinDLL("User32.dll").GetKeyState(0x14) == True:
        messagebox.showwarning("Warning","Caps Lock is On!! Please switch Caps lock Off, and click Ok..")
        print("Caps Lock is On")
        if ctypes.WinDLL("User32.dll").GetKeyState(0x14) == True:
            messagebox.showwarning("Warning","Caps Lock is still! Script is stoped, application will be Close.")
            print("App will be close.")
            exit()           
    else:
        print("Caps Lock is Off")
        pass
    time.sleep(2)
    
def start():
    start_time = perf_counter()
#--- SAVE LAST DATA TO FILE----
    get_shipment = shipment.get()
    get_registration = registration.get()
    get_seal = seal.get()
    get_trailer = trailer_id.get()
    pList = [get_shipment,get_registration,get_seal,get_trailer]
    with open("output.txt", "w") as f:
        f.truncate(0)
        f.write(','.join(map(str,pList)))   
#--- SAVE DATA --- END LINE
    
    time.sleep(2)
    is_capslock_on()
    #---CHECK IF OFFLINE LOADS ARE ON "Include Cancelled, Finished"
    if pyautogui.locateOnScreen('images\\offline_loads_ON.png', confidence=0.8) == True:
        step_0 = pyautogui.locateOnScreen('images\\offline_loads_ON.png', confidence=0.8)
        pyautogui.moveTo(step_0)
        pyautogui.click(step_0, button='left')
        print('Offline Loads, are On, will switch Off first.')
          
    if pyautogui.locateOnScreen('images\\consigment_unactive.png', confidence=0.9) != None:
        step_1 = pyautogui.locateOnScreen('images\\consigment_unactive.png', confidence=0.9)
        pyautogui.moveTo(step_1)
        pyautogui.click(step_1, button='left')
        print('Go to Consigment')
    elif pyautogui.locateOnScreen('images\\consigment_active.png', confidence=0.9) != None:
        step_1 = pyautogui.locateOnScreen('images\\consigment_unactive.png', confidence=0.9)
        pyautogui.moveTo(step_1)
        pyautogui.click(step_1, button='left')
        print('Go to Consigment')
        
    if pyautogui.locateOnScreen('images\\consignment-shipment_active.png', confidence=0.9) != None:    
        step_2 = pyautogui.locateOnScreen('images\\consignment-shipment_active.png', confidence=0.9)
        pyautogui.moveTo(step_2)
        pyautogui.click(button='left')
        #pyautogui.move(0, 30)
    elif pyautogui.locateOnScreen('images\\consignment-shipment_unactive.png', confidence=0.9) != None:    
        step_2 = pyautogui.locateOnScreen('images\\consignment-shipment_unactive.png', confidence=0.9)
        pyautogui.moveTo(step_2)
        pyautogui.click(button='left')
        #pyautogui.move(0, 30)
        
    time.sleep(0.5)   
    pyautogui.hotkey('ctrl','f')
    print('Pressing CTRL+F')
    time.sleep(1)
    shipment_nr = shipment.get()
    pyautogui.write(shipment_nr)
    time.sleep(0.5)
    pyautogui.hotkey('enter')
    time.sleep(0.5)
    
    #---Check if Load are Finished
    if pyautogui.locateOnScreen('images\\50_outbound_empty.png', confidence=0.8) != None:
        print('Load is Not Ready, Status: "50 Outbound: Loaded"')
        Yes_No = messagebox.askyesno("Warning","Status: 50 Outbound, Load is not ready for Collection, program will close.")
        if Yes_No == False:
            print("Program will stop working..")
            #break function
        elif Yes_No == True:
            print(f"You choose continue with the process, even if Load {shipment_nr}, is not ready for collection...")
            time.sleep(1)
            pass
    elif pyautogui.locateOnScreen('images\\70_outbound_loaded.png', confidence=0.8) != None:
        print('Load is Ready for Collection, Status: "70 Outbound: Loaded", Continue work...')    
        pass
    else:
        print('Load not Exist, wrong number or Shipment is Gone...')
        messagebox.showwarning("Warning","Nothing was Found...")
        exit()
        #break function
        
    #---Check Loading Location on the Yard---#
    print('#-- Start MHA location --#')
    if pyautogui.locateOnScreen('images\\MHA.png', confidence=0.8) != None:
        MHA_loc = pyautogui.locateOnScreen('images\\MHA.png', confidence=0.8)
        pyautogui.moveTo(MHA_loc)
        pyautogui.click(MHA_loc, button='left')
        time.sleep(0.5)
        pyautogui.hotkey('ctrl','c')
        copied_MHA = root.clipboard_get()
        time.sleep(1)
        root.title(f'{copied_MHA}')
        print(copied_MHA)
        time.sleep(0.5)
    elif pyautogui.locateOnScreen('images\\MHA2.png', confidence=0.8) != None:    
        MHA_loc = pyautogui.locateOnScreen('images\\MHA2.png', confidence=0.8)
        pyautogui.moveTo(MHA_loc)
        pyautogui.click(MHA_loc, button='left')
        time.sleep(0.5)
        pyautogui.hotkey('ctrl','c')
        copied_MHA = root.clipboard_get()
        time.sleep(1)
        root.title(f'{copied_MHA}')
        print(copied_MHA)
        time.sleep(0.5)
        
#---Create location Audio File---Text-To-Speach---#
#-------------------------------------------------#
#---Text-To-Speach--------------------------------#
    
    #---Looking for shipment number
    if pyautogui.locateOnScreen('images\\001TSOS10000.png', confidence=0.8) != None:
        step_3 = pyautogui.locateOnScreen('images\\001TSOS10000.png', confidence=0.8)
        pyautogui.moveTo(step_3)
        pyautogui.click(step_3, button='left')
        time.sleep(0.5)
        pyautogui.hotkey('ctrl','c')
        #---- Copy Shipment number --- VISIBLE LOCATION AND TRAILR ID
        copied_shipment = root.clipboard_get()
        print(copied_shipment)
        
    elif pyautogui.locateOnScreen('images\\001TSOS10000.png', confidence=0.8) == None:
        messagebox.showinfo("Message", "I cant find shipment number: ", copied_shipment)
        os.system("pause")
    
    #---Go TO SQL QUERIES TAB
    if pyautogui.locateOnScreen('images\\sql_queries_published_queries.png', confidence=0.8) != None:
        step_4 = pyautogui.locateOnScreen('images\\sql_queries_published_queries.png', confidence=0.8)
        pyautogui.moveTo(step_4)
        pyautogui.click(step_4, button='left')
        print('Go to SQL Queries')
    elif pyautogui.locateOnScreen('images\\sql_queries_published_queries_active.png', confidence=0.8) != None:
        step_4 = pyautogui.locateOnScreen('images\\sql_queries_published_queries_active.png', confidence=0.8)
        pyautogui.moveTo(step_4)
        pyautogui.click(step_4, button='left')
        print('Go to SQL Queries')
    
    #---Open Despatch Paper
    if pyautogui.locateOnScreen('images\\despatch_paper_not_active.png', confidence=0.8) != None:
        step_4 = pyautogui.locateOnScreen('images\\despatch_paper_not_active.png', confidence=0.8)
        pyautogui.moveTo(step_4)
        pyautogui.doubleClick(step_4, button='left')
    elif pyautogui.locateOnScreen('images\\despatch_paper_active.png', confidence=0.8) != None:
        step_4 = pyautogui.locateOnScreen('images\\despatch_paper_active.png', confidence=0.8)
        pyautogui.moveTo(step_4)
        pyautogui.doubleClick(step_4, button='left')
    elif pyautogui.locateOnScreen('images\\booking_office_dir_not_active.png', confidence=0.8) != None:
        step_4 = pyautogui.locateOnScreen('images\\booking_office_dir_not_active.png', confidence=0.8)
        pyautogui.moveTo(step_4)
        pyautogui.doubleClick(step_4, button='left')
        if pyautogui.locateOnScreen('images\\despatch_paper_not_active.png', confidence=0.8) != None:
            step_4 = pyautogui.locateOnScreen('images\\despatch_paper_not_active.png', confidence=0.8)
            pyautogui.moveTo(step_4)
            pyautogui.doubleClick(step_4, button='left')
    print('Manage with Despatch paper procedure..')
    #---Paste Shipment number to Searchbar
    time.sleep(0.5)
    if pyautogui.locateOnScreen('images\\shipment_nr.png', confidence=0.8) != None:
        print('Shipment window located')
        pyautogui.typewrite(copied_shipment)
        time.sleep(0.5)
        if pyautogui.locateOnScreen('images\\001TSOS10000.png', confidence=0.8) == None:
            print("Didn't find Correct shipment number")
            messagebox.showwarning("Warning","Incorrect Shipment number, program will close.")
            sys.exit()
        
        print('Shipment Paste successfully')
    time.sleep(0.5)
    pyautogui.hotkey('enter')
    if pyautogui.locateOnScreen('images\\extended_shp_unactive.png', confidence=0.9) != None:
        step_5  = pyautogui.locateOnScreen('images\\extended_shp_unactive.png', confidence=0.9)
        time.sleep(0.5)
    elif pyautogui.locateOnScreen('images\\extended_shp_active.png', confidence=0.9) != None:
        step_5 = pyautogui.locateOnScreen('images\\extended_shp_active.png', confidence=0.9)
    pyautogui.moveTo(step_5)
    pyautogui.click(step_5, button='left')
    pyautogui.hotkey('ctrl', 'r')
    time.sleep(1)
    step_6 = pyautogui.locateOnScreen('images\\show_button.png', confidence=0.8)
    pyautogui.moveTo(step_6)
    pyautogui.click(step_6, button='left')
    time.sleep(1)
    #--- Waiting for button SHOW to reaction
    step_7 = pyautogui.locateOnScreen('images\\file.png', confidence=0.8)
    pyautogui.moveTo(step_7)
    pyautogui.click(step_7, button='left')
    time.sleep(0.3)
    step_8 = pyautogui.locateOnScreen('images\\export_document.png', confidence=0.8)
    pyautogui.moveTo(step_8)
    pyautogui.click(step_8, button='left')
    time.sleep(0.3)
    step_9 = pyautogui.locateOnScreen('images\\button_ok_pdf_export_options.png', confidence=0.8)
    pyautogui.moveTo(step_9)
    pyautogui.click(step_9, button='left')
    time.sleep(0.3)
    #----PASTE SHIPMENT NUMBER
    pyautogui.typewrite(copied_shipment)
    step_10 = pyautogui.locateOnScreen('images\\save_button_despatch_confirm.png', confidence=0.75)
    pyautogui.moveTo(step_10)
    pyautogui.click(step_10, button='left')
    time.sleep(0.3)
    
    #---CHECKING DOCUMENTS EXISTING IN SYSTEM 'DESPATCH FOLDER'
    if pyautogui.locateOnScreen('images\\load_allready_exist.png', confidence=0.8) != None:
        print('Load documents, allready exist in the system, Shipment is propably Gone... program stop working.')
        despatch_folder_load = messagebox.askyesno("Warning",f"Documents allready exist for Load: {copied_shipment}, Do you want Replace current load? ")
        if despatch_folder_load == True:
            confirm_exchange = pyautogui.locateOnScreen('images\\exchange_load_in_despatch_folder.png', confidence=0.8)
            pyautogui.moveTo(confirm_exchange)
            pyautogui.click(confirm_exchange, button='left')
            time.sleep(1)
            print('Load Documents has been Exchanged, successfully.')
            time.sleep(2)
            
        elif despatch_folder_load == False:
            print('You choose Not to continue process, program will close.')
            sys.exit()
        
    step_11 = pyautogui.locateOnScreen('images\\yes_button.png', confidence=0.8)
    pyautogui.moveTo(step_11)
    pyautogui.click(step_11, button='left')
    time.sleep(2)
    #
    #--------PDF EDITOR WORK---------#
    pyautogui.hotkey('ctrl','-')
    pyautogui.hotkey('ctrl','-')
    pyautogui.hotkey('ctrl','-')
    step_12 = pyautogui.locateOnScreen('images\\fill_and_sign.png', confidence=0.8)
    pyautogui.moveTo(step_12)
    pyautogui.click(step_12, button='left')
    time.sleep(2.5)
    while pyautogui.locateOnScreen('images\\registration_number.png', confidence=0.8) == None:
        time.sleep(1)

    #--------FETCH DATA---------
    reg_nr = registration.get()
    seal_nr = seal.get()
    trailer_nr = trailer_id.get()
    #--------PDF EDITOR WORK---------#
    #
    #---TYPE REGISTRATION ON PDF_1
    step_13 = pyautogui.locateCenterOnScreen('images\\registration_number.png', confidence=0.8)
    pyautogui.moveTo(step_13)
    pyautogui.move(0,25)
    pyautogui.click(button='left')
    pyautogui.typewrite(reg_nr)
    print('Registration - Done')
    pyautogui.move(150,0)
    pyautogui.click(button='left')
    #---TYPE SEAL NUMBER ON PDF_1
    time.sleep(0.5)
    step_14 = pyautogui.locateCenterOnScreen('images\\seal_number.png', confidence=0.8)
    pyautogui.moveTo(step_14)
    pyautogui.move(0,25)
    pyautogui.doubleClick(button='left')
    pyautogui.typewrite(seal_nr)
    print('Seal number - Done')
    #---SCROLL DOWN---
    pyautogui.hotkey('pgdn')
    time.sleep(0.3)
    #---TYPE SEAL NUMBER ON GATEPASS
    step_15 = pyautogui.locateCenterOnScreen('images\\seal_nr_gatepass.png', confidence=0.8)
    pyautogui.moveTo(step_15)
    pyautogui.move(180,0)
    pyautogui.doubleClick(button='left')
    time.sleep(0.3)
    pyautogui.typewrite(seal_nr)
    print(f'{seal_nr} , correct applied to Gatepass')
    time.sleep(0.3)
    step_16 = pyautogui.locateCenterOnScreen('images\\vehicle_reg_gatepass.png', confidence=0.85)
    pyautogui.moveTo(step_16)
    pyautogui.move(185,0)
    pyautogui.doubleClick(button='left')
    pyautogui.typewrite(reg_nr)
    print(f'{reg_nr} , correct applied to Gatepass')
    pyautogui.move(185,0)
    pyautogui.click(button='left')
    #---TYPE TRAILER IN NR ON GATEPASS
    step_17 = pyautogui.locateCenterOnScreen('images\\trailer_nr_in.png', confidence=0.8)
    pyautogui.moveTo(step_17)
    time.sleep(0.3)
    pyautogui.move(210,0)
    pyautogui.doubleClick(button='left')
    pyautogui.typewrite(trailer_nr)
    print(f'{trailer_nr}, correct applied to Gatepass')
    time.sleep(0.2)
    #---ISSUED BY: .......... (GATEPASS)
    step_18 = pyautogui.locateCenterOnScreen('images\\sign_co_worker.png', confidence=0.8)
    pyautogui.moveTo(step_18)
    pyautogui.click(button='left')
    print('Co-Worker Signature, has been correct applied to Gatepass')
    time.sleep(0.2)
    step_19 = pyautogui.locateOnScreen(my_sign, confidence=0.8)
    pyautogui.moveTo(step_19)
    pyautogui.click(button='left')
    time.sleep(0.2)
    #---SIGN WAREHOUSE SIGN
    step_20 = pyautogui.locateCenterOnScreen('images\\warehouse_sign.png', confidence=0.8)
    pyautogui.moveTo(step_20)
    #pyautogui.move(0,0)
    time.sleep(0.2)
    pyautogui.click(button='left')
    time.sleep(0.2)
    step_21 = pyautogui.locateCenterOnScreen('images\\sign_co_worker.png', confidence=0.8)
    pyautogui.moveTo(step_21)
    pyautogui.click(step_21, button='left')
    time.sleep(0.2)
    step_22 = pyautogui.locateOnScreen(my_sign, confidence=0.8)
    pyautogui.moveTo(step_22)
    pyautogui.click(step_22, button='left')
    time.sleep(0.2)
    
    step_23 = pyautogui.locateCenterOnScreen('images\\issued_by_sign.png', confidence=0.85)
    pyautogui.moveTo(step_23)
    time.sleep(0.5)
    pyautogui.move(220,0)
    pyautogui.click(button='left')
    print('Signatures, has been correct applied to Gatepass')
    
#----Counting Time finish----
    end_time = perf_counter()
    finish_time = perf_counter()
    print(f'It took {end_time- start_time :0.2f} second(s) to complete.')
    root.title(f'{app_title}')
    
    #--- BETA TEST - WARNING FOR SIGN UP ---#
    #beta_test = messagebox.askyesno("Warning","Do you want to continue with Certification Sign process?")
    #if beta_test == False:
    #    exit()
    
    #---- CERTIFICATE DRIVER SIGN---#
    print('Start Certificate process, for Get Driver Sign...')
    time.sleep(2)
    step_24 = pyautogui.locateOnScreen('images\\tools.png', confidence=0.8)
    pyautogui.moveTo(step_24)
    pyautogui.click(step_24, button='left')
    time.sleep(1.5)
    print('Tools')

    step_25 = pyautogui.locateOnScreen('images\\certificate_sign.png', confidence=0.8)
    pyautogui.moveTo(step_25)
    pyautogui.click(step_25, button='left')
    time.sleep(1)
    print('Certificates')

    step_26 = pyautogui.locateOnScreen('images\\digitally_sign.png', confidence=0.8)
    pyautogui.moveTo(step_26)
    pyautogui.click(step_26, button='left')
    time.sleep(1)
    pyautogui.hotkey('pgdn')
    time.sleep(1)
    print('Digitally Sign')

    #---1st SIGNATURE DRIVER'S
    step_27 = pyautogui.locateOnScreen('images\\carrier_start_signature.png', confidence=0.8)
    pyautogui.moveTo(step_27)
    time.sleep(1)
    pyautogui.move(-30, -10)
    pyautogui.drag(250, 50, 0.3, button='left')
    print('Waiting for driver Signature')
    time.sleep(3)

    #--CHECK IF DRIVER MADE 1st SIGN--#
    step_28 = pyautogui.locateOnScreen('images\\signature_recognision_sign.png', confidence=0.8)
    while step_28 != None:
        print('Waiting for Driver Signature...')
        time.sleep(2)
        step_28 = pyautogui.locateOnScreen('images\\signature_recognision_sign.png', confidence=0.8)

    step_29 = pyautogui.locateOnScreen('images\\digitally_sign.png', confidence=0.8)
    pyautogui.moveTo(step_29)
    pyautogui.click(step_29, button='left')
    time.sleep(0.5)
    pyautogui.hotkey('pgdn')
    time.sleep(1)

    #---2nd SIGNATURE DRIVER'S
    step_30 = pyautogui.locateOnScreen('images\\carrier_start_signature.png', confidence=0.8)
    pyautogui.moveTo(step_30)
    pyautogui.move(-40, 60)
    pyautogui.drag(255, 50, 0.3, button='left')
    time.sleep(3)
    print('Waiting for driver Signature')

    #--CHECK IF DRIVER MADE 2nd SIGN--#
    step_31 = pyautogui.locateOnScreen('images\\signature_recognision_sign.png', confidence=0.8)
    while step_31 != None:
        print('Waiting for Driver Signature...')
        time.sleep(2)
        step_31 = pyautogui.locateOnScreen('images\\signature_recognision_sign.png', confidence=0.8)

    print('Process completed')
    
    step_32 = pyautogui.locateOnScreen('images\\print_icon.png', confidence=0.8)
    pyautogui.moveTo(step_32)
    pyautogui.click(step_32, button='left')
    time.sleep(2)
    
    step_33 = pyautogui.locateOnScreen('images\\printer_arrow_up.png', confidence=0.8)
    pyautogui.moveTo(step_33)
    pyautogui.click(step_33, button='left')
    time.sleep(1)
    
#----Counting Time finish----
    #end_time = perf_counter()
    #print(f'It took {end_time- start_time :0.2f} second(s) to complete.')    
    
    #--- PYAUTOGUI IF YES:
    #--- IF YES ---
    
    step_34 = pyautogui.locateOnScreen('images\\print_button.png', confidence=0.8)
    pyautogui.moveTo(step_34)
    pyautogui.click(step_34, button='left')
    time.sleep(2)

    #MESSAGE FROM TKINTER CONFIRMATION PROCES.
    print('Koniec, pracy')
    print(f'It took {finish_time- start_time :0.2f} second(s) to complete.')  
    
def stop():
    start_button.config(state=NORMAL)
    exit()
    #os._exit(0)
    
def threading_1():
    start_button.config(state=DISABLED)
    print('Program will start working...')
    threading.Thread(target=start).start()
    start_button.config(state=NORMAL)

    
def check_sign():
    #New window configuration
    new_window = Toplevel()
    new_window.iconbitmap('data\\icon.ico')
    new_window.configure(bg="#0454a0")
    new_window.resizable(0,0)
    new_window.geometry("300x300")
    new_window.title("Your signature image")
    
    my_image = ImageTk.PhotoImage(Image.open('Astro-Loader\my_sign.png'))
    
    my_image_label = Label(new_window, image=my_image)
    my_image_label.pack(padx=10,pady=10)
    
#Create a menu item
file_menu = Menu(my_menu)
my_menu.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Sign', command=signature_file)
file_menu.add_command(label='Check your sign', command=check_sign)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

#---IKEA image
img = PhotoImage(file='data/ikea.png')
Label(root,image=img).pack(padx=10,pady=10, side='top')

#---Main Frame
all_fonts = ('Calibri',11, 'bold')
main_frame = LabelFrame(root, text='Astro Loader',fg='#eacb14', bg="#0454a0", labelanchor=N, padx=40, font=('Calibri',13, 'bold'))
main_frame.pack(pady=10,padx=15)

#Shipment Frame & Label
shipment_frame = LabelFrame(main_frame, text='Shipment:',fg='#eacb14', bg="#0454a0",  labelanchor=N, font=all_fonts)
shipment_frame.pack(pady=10,padx=15)

#Shipment number Get
shipment_nr = Entry(shipment_frame, textvariable=shipment)
shipment_nr.pack(pady=10,padx=15)

#Registration Frame & Label
registration_frame = LabelFrame(main_frame, text='Registration:',fg='#eacb14', bg="#0454a0", labelanchor=N, font=all_fonts)
registration_frame.pack(pady=10,padx=15)

#Vehicle Registration Get
registration_nr = Entry(registration_frame, textvariable=registration)
registration_nr.pack(pady=10,padx=15)

#Seal Number Frame & Label
seal_frame = LabelFrame(main_frame, text='Seal Nr:',fg='#eacb14', bg="#0454a0", labelanchor=N, font=all_fonts)
seal_frame.pack(pady=10,padx=15)

#Seal number Get
seal_nr = Entry(seal_frame, textvariable=seal)
seal_nr.pack(pady=10,padx=15)

#Trailer ID Frame & Label
trailer_frame = LabelFrame(main_frame, text='Trailer ID:',fg='#eacb14', bg="#0454a0", labelanchor=N, font=all_fonts)
trailer_frame.pack(padx=15,pady=10)

#Trailer ID Get
trailer_nr = Entry(trailer_frame, textvariable=trailer_id)
trailer_nr.pack(pady=10,padx=15)

#Button Start
start_button = Button(main_frame, text='Start', command=threading_1, bg='#39D38D', width='10', state=NORMAL)
start_button.pack(padx=10,pady=10, side='right')

#Button Stop
stop_button = Button(main_frame, text='Stop', command=stop, bg='#f44336', width='10')
stop_button.pack(padx=10,pady=10, side='left')

#sign_button = Button(root, text='Your Sign', command=signature_file, bg='#F9D62E', font=all_fonts)
#start_button.pack(pady=10)

#Button Stop
#stop_button = Button(root, text='  Stop  ', command=stop, bg='#f44336')
#stop_button.pack(pady=10)
#Author Label
mtmak9 = Label(root, text='Cre@ted by MTMAK9', font=('Comic Sans MS', 8, 'bold'), fg='#eacb14', bg="#0454a0")
mtmak9.pack(pady=5,padx=5, side='right')

root.mainloop()

