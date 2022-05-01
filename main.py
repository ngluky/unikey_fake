from time import sleep
from pynput import keyboard
from pynput.keyboard import Controller
from pynput import mouse
from dist_ import key_head_,dist
import win32api,win32con



string = ''
string_no = ''
caps_status = win32api.GetKeyState(win32con.VK_CAPITAL)
ctrl_status = False
shift_pressed = False
pass_backspace = 0
pass_text = ''
key_ = Controller()

def type_text(string_no,string):
    global pass_backspace, pass_text
    pass_backspace = len(string_no)
    pass_text = string
    for i in string_no:
        key_.press(keyboard.Key.backspace)
        sleep(0.0000001)
    string_no = string
    key_.type(string)
    return string_no

def on_press(event):
    global string , caps_status, ctrl_status , shift_pressed, string_no, pass_backspace , pass_text
    print('\r                                                 \r' , end='')
    print( string, string_no , caps_status, ctrl_status , end='' )

    # print(event)
    have = False
    try:
        char = event.char

        if caps_status:
            char = char.upper()
        had_pess = pass_text.startswith(char)
        if had_pess:
            pass_text = pass_text[1:]

        if not had_pess:
            string_no += char

        
        

        if (char in key_head_) and not had_pess and not ctrl_status:
            relace_ = dist[char.lower()]
            have = False
            if 'str' in str(type(relace_)):
                if caps_status:
                    relace_ = relace_.upper()
                relace_ = relace_.split(',')
                if relace_[1] in string:
                    string = string.replace(relace_[1] , relace_[0]) + char
                    # string_no = type_text(string_no,string)
                    have = True
                elif relace_[0] in string:
                    string = string.replace(relace_[0] , relace_[1])
                    have = True
                if have:
                    string_no = type_text(string_no,string)


            else:
                for i in relace_:
                    if caps_status:
                        i = i.upper()
                    relace_ = i.split(',')
                    if relace_[1] in string:
                        string = string.replace(relace_[1] , relace_[0])
                        string_no = type_text(string_no,string + char)
                        have = True

                        break
                    elif relace_[0] in string:
                        string = string.replace(relace_[0] , relace_[1])
                        string_no = type_text(string_no,string)
                        have = True

                        break
                    
        if not have and not had_pess:
            string += char
            
            
                
                

    except:
        key = event.name
        if  key == "'caps_lock'" :
            caps_lock = not caps_lock

        if pass_backspace !=0:
            pass_backspace -= 1
        elif key == keyboard.Key.backspace.name:
            string = string[:-1]
            string_no = string_no[:-1]

        elif event == keyboard.Key.space:
            string = ''
            string_no = ''

        if key == keyboard.Key.ctrl_l.name or key == keyboard.Key.ctrl_r.name:
            ctrl_status = True
        
        if event == keyboard.Key.shift_l or event == keyboard.Key.shift_r:
            shift_pressed = True

    


def on_release(event):
    global string , caps_status, ctrl_status, shift_pressed, string_no
    if event == keyboard.Key.ctrl or event == keyboard.Key.ctrl_l:
            ctrl_status = False

    if event == keyboard.Key.shift_l or event == keyboard.Key.shift_r:
            shift_pressed = False
    
    try:
        event.char
    except:
        if  event == keyboard.Key.shift_l or event == keyboard.Key.shift_r\
                or event == keyboard.Key.ctrl \
                    or event == keyboard.Key.ctrl_l:

            pass
        else:
            string_no = string = ''

def click(x, y, button, pressed):
    global string , string_no
    string = string_no = ''


listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release
    )
listener.start()

listener_moused = mouse.Listener(
    on_click=click
)

listener_moused.run()
