"""
Music Player

This is the simple music player written in python . it also has a small txt database to add music . it can add, delete, loop, play ,pause music. this script depends on pygame. incase you don't have make sure to install it first.
pip install pygame

Feel free to copy,reuse,edit this game anywhere!


"""



from tkinter import *
from tkinter import messagebox,filedialog,ttk
import pygame


class App:
    def __init__(self,root):

        self.root=root
        self.root.title("Music Player")
        self.root.geometry("706x356")
        self.root.configure(background="#d9d9d9")
        pygame.mixer.init()

        self.data=easy_dict(read_data())

        self.playing_tract=None
        self.is_player_stopped=False

        self.volumes=list(range(10))
        self.variable = StringVar(self.root)
        self.variable.set(str(int(pygame.mixer.music.get_volume()*10)))

        self.list_box=Listbox(self.root,selectmode=SINGLE,width=70,height=15,background="#ffffff", borderwidth="2", disabledforeground="#a3a3a3",font=font1, foreground="#000000", justify=LEFT)
        self.play_button=Button(self.root,text="Play",command=lambda:self.play(),**dic)
        self.delete_button=Button(self.root,text="Delete",command=lambda:self.delete(),**dic)
        self.delete_all=Button(self.root,text='Clear',command=lambda:self.clear(),**dic)
        self.loop_button=Button(self.root,text='Loop',command=lambda:self.play(loop=True),**dic)
        self.add_button=Button(self.root,text='Add',command=lambda:self.add(),**dic)
        self.stop_button=Button(self.root,text='Stop',command=lambda:self.stop(),**dic)
        self.option_menu = ttk.OptionMenu(self.root, self.variable, *self.volumes,command=self.set_vol)

        self.positions=[(0,0),(2,320),(50,320),(103,320),(149,320),(195,320),(260,320),(660,328)]
        self.elements=[self.list_box,self.play_button,self.loop_button,self.add_button,self.stop_button,self.delete_button,self.delete_all,self.option_menu]

        self.place_elements()
        self.redisplay()

    def place_elements(self):
        for i in range(len(self.positions)):
            self.elements[i].place(x=self.positions[i][0],y=self.positions[i][1])


    def redisplay(self):
        write_data([self.data[i] for i in self.data])
        self.list_box.delete(0,END)
        for i in sorted(self.data):
            self.list_box.insert(END,i)

    def delete(self):
        song=self.return_selected()
        if song and song !=self.playing_tract:
            del self.data[song]
            self.redisplay()
        else:
            messagebox.showerror("ERROR", "Currently This song is playing")

    def play(self,loop=False):
        song=self.return_selected()
        if not self.is_player_stopped:
            if song is not None:
                path=self.data[song]
                pygame.mixer.music.load(path)
                self.playing_tract=song
                if loop:
                    pygame.mixer.music.play(-1)
                    return
                pygame.mixer.music.play(0)
        else:
            self.resume(loop)
            if song !=self.playing_tract:
                self.play()



    def return_selected(self):
        selected_song_index=self.list_box.curselection()
        if len(selected_song_index)<=0:
            messagebox.showerror("ERROR", "NO SONG SELECTED")
        else:
            return self.list_box.get(selected_song_index)

    def clear(self):
        if self.playing_tract is not None:
            self.data={self.playing_tract:self.data[self.playing_tract]}
        else:
            self.data={}
        self.redisplay()

    def add(self):
        filename = filedialog.askopenfilename(filetypes=types_list())
        if scan_file(filename):
            self.data[filename.split('/')[-1]]=filename
            self.redisplay()

    def stop(self):
        self.is_player_stopped=True
        pygame.mixer.music.pause()

    def resume(self,loop):
        self.is_player_stopped=False
        pygame.mixer.music.unpause()

    def set_vol(self,value):
        pygame.mixer.music.set_volume(int(value)/10)

font13 = "-family {Segoe UI} -size 12 -weight bold -slant "  \
"roman -underline 0 -overstrike 0"
font1="-family {Microsoft Sans Serif} -size 12 -weight bold"  \
" -slant roman -underline 0 -overstrike 0"
dic={'activebackground':"#d9d9d9",'activeforeground':"#000000",'background':"#ffffff",'borderwidth':"2",'disabledforeground':"#a3a3a3",'font':font13,'foreground':"#000000",'highlightbackground':"#d9d9d9",'highlightcolor':"black",'pady':"0"}

def scan_file(file):
    return any(file[len(file)-len(i):]==i for i in file_types)

def read_data():
    with open(database_file,'r') as file:
        original_list=[i[0:len(i)-1]  for i in file.readlines()]
    scanned_list=list(set(list(filter(scan_file,original_list))))
    return scanned_list if scanned_list==original_list else write_data(scanned_list)

def write_data(lis):
    with open(database_file,'w') as file:
        file.writelines([i+'\n' for i in lis])
    return lis

def easy_dict(lis):
    return {i.split('/')[-1]:i for i in lis}

def types_list():
    return tuple([(i.upper()+' file','*.{}'.format(i)) for i in file_types]+[("All Files", '*.*')])



database_file='database.txt'
file_types=['mp3','mp4','wav','ogg']


def main():
    app=Tk()
    app.resizable(0, 0)
    App(app)
    app.mainloop()


if __name__=="__main__":
    main()
