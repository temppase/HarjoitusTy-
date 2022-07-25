# Tälläinen harjoitustyö kokeilu.... Ohjelmisto syntetisaattori.
# Päätin ihna mielenkiinnosta tutustua tkinteriin, 
# kun olen kuitenkin C#:lla tehnyt formeja ja WPF:ää
# Mikään huippu suoritus tästä ei tosiaan tullut, 
# mutta ainakin pääsin kokeilemaan.

# Tarvittavat importit jotta voidaan käyttää tkinteriä ja lukea json tiedostoja
from tkinter import *
import json
from tkinter.filedialog import asksaveasfile
from tkinter import filedialog as fd
# Luodaan formi olio ja annetaan sille muutamia määrityksi.
syna = Tk()
syna.title("Syna")
w = 850
h = 800
syna.geometry(f"{w}x{h}+20+20")
syna.config(bg='#114452')
syna.minsize(715,680)
# Polkuja joita käytetään tiedostoihin kirjoitukseen tai lukemiseen.
param_path = 'C:/Users/tempp/Desktop/ttc2030/HarjoitusTyö/appsettings/parameters.json'
lfo_path = 'C:/Users/tempp/Desktop/ttc2030/HarjoitusTyö/appsettings/lfo.json'
pre_path = 'C:/Users/tempp/Desktop/ttc2030/HarjoitusTyö/appsettings/preferences.json'
presets = 'C:/Users/tempp/Desktop/ttc2030/HarjoitusTyö/presets/'
defaults_path = 'C:/Users/tempp/Desktop/ttc2030/HarjoitusTyö/appsettings/defaultpreset.json'
# Metodi jolla printataan käyttäjälle tietoa tilasta.
def AppState():
    with open(pre_path, 'r') as p:
        p_state = json.load(p)
    with open(param_path, 'r') as set:
        s_state = json.load(set)
    statelist = []
    statelist.append("--- App setting ---")
    statelist.append(" ")
    statelist.append(f" Sample rate: {p_state['def'][0]}")
    statelist.append(f" Buffer size: {p_state['def'][1]}")
    statelist.append(" ")
    statelist.append("--- LFO mode's ---")
    statelist.append(" ")
    n = 1
    for x,y in s_state.items():
        if (x.__contains__("mode")):
            statelist.append(f" {n}: {y.capitalize()}")
            n += 1
    statelist.append(" ")
    statelist.append("--- Info ---")
    statelist.append(" ")
    statelist.append(" Double click sustain")
    statelist.append(" slider to make it obey")
    statelist.append(" note off's")
    lb_var = StringVar(value=statelist)
    list_frm = Frame()
    list_frm.config(padx=5,pady=5,bg='#114452')
    databox = Listbox(
        list_frm,
        height=20,
        bg="#7bc",
        listvariable=lb_var)
    databox.grid(column=0,row=0,sticky=N)
    list_frm.grid(column=2, row=0,sticky=N)
AppState()
# Tässä luokassa käsitellään parametrejä joita sovelluksessa käytetään.
class Parameters:
    # Min arvot
    with open(defaults_path, 'r') as defaults:
        def_pm = json.load(defaults)
    with open(pre_path, 'r') as preferences:
        a_set = json.load(preferences)
    with open(param_path, 'r') as parameters:
        pm_set = json.load(parameters)
    sld = {
        "adsr":["A","D","S","R"], "wave":["Sine","Square","Saw","Triangle"],
        "depth":["1.","2.","3."],"speed":["1.","2.","3."]
    }
p = Parameters()

# Presetin tallennus metodi
def SavePreset():
    f = asksaveasfile(initialfile = 'Untitled.json',
        defaultextension=".json",filetypes=[("All Files","*.*"),("JSON file","*.json")])
    print(f.name)
    with open(f.name, "w") as s:
        json.dump(p.pm_set,s)

# Presetin lataus metodi (Tämä toimii, mutta en saanut ohjelmaan toimintoa,
# jolla olisi ottanut ladatut arvot käyttöön. Todennäköisesti, 
# jos olisin tehnyt widgetit aluksi erilailla tämänkin olisi saanut toimimaan kunnolla)
def LoadPreset():
    filetypes = (
        ("All Files","*.*"),
        ('JSON file', '*.json')
    )
    fname = fd.askopenfilename(
        title='Open a file',
        initialdir=presets,
        filetypes=filetypes)
    print(fname)
    with open(fname,"r") as load:
        l = json.load(load)
    p.pm_set = l
    with open(param_path,"w") as d:
        json.dump(l,d)
    AppState()

# Tallettaa säädetyt asetukset oletus asetuksiksi,
# Käynnistyessä latautuvat asetukset, jotka viimeksi on jääneet.
# Paitsi, jos lataat presetin ja käynnistät uudelleen niin silloin saat ne asetukset 
# oli tarkoitus tehdä vielä buttoni josta ne olisi saanut ladattua halutessan defaultit,
# mutta todennäköisesti siinä olisi ollu sama ongelma kuin presetin latauksessa.
# Koitin myös toimintoa joka olisi tuhonnut ja ladannut formin uudelleen,
# mutta avasi vain täysin tyhjän formin.   
def SaveDefault():
    with open(defaults_path, 'w') as save:
        json.dump(p.pm_set,save)

# Muutetaan näytteen otto taajuutta
def SampleRate(e):
    with open(pre_path, 'r') as preferences:
        print("\nChange sample rate")
        pre = json.load(preferences)
        pre['def'][0] = e
        with open(pre_path, 'w') as preferences:
            json.dump(pre, preferences)
    AppState()

# Muutetaan bufferin kokoa
def BufferSize(e):
    with open(pre_path, 'r') as preferences:
        print("\nChange buffer size")
        pre = json.load(preferences)
        pre['def'][1] = e
    with open(pre_path, 'w') as preferences:
        json.dump(pre, preferences)
    AppState()

# Muutetaan LFO:n aallon muotoja
def LFO(a,b):
    p.pm_set[f"{b}. mode"] = a
    with open(param_path, 'w') as lfo:
        json.dump(p.pm_set,lfo)
    AppState()

# Menu
class MenuBar:
    # Menu olio
    menubar = Menu(syna)
    syna.config(menu=menubar)
    # file menu olio
    file_menu = Menu(
    menubar,
    tearoff=0
    )
    # Tallennus komento
    file_menu.add_command(
    label='Save',
    command=SavePreset,
    )
    # LFO menu
    LFO_menu = Menu(
    menubar,
    tearoff=0
    )
    
    # Ali menut
    sub_menu0 = Menu(file_menu, tearoff=0)
    sub_menu1 = Menu(file_menu, tearoff=0)
    sub_menu2 = Menu(file_menu, tearoff=0)
    lfo_menu1 = Menu(LFO_menu, tearoff=0)
    lfo_menu2 = Menu(LFO_menu, tearoff=0)
    lfo_menu3 = Menu(LFO_menu, tearoff=0)
    


    # LFO menun ali menut
    LFO_menu.add_cascade(
    label='LFO 1',
    menu=lfo_menu1
    )
    LFO_menu.add_cascade(
    label='LFO 2',
    menu=lfo_menu2
    )
    LFO_menu.add_cascade(
    label='LFO 3',
    menu=lfo_menu3
    )
    # Tallennetaan oletusasetukset
    file_menu.add_command(
    label='Save as default',
    command=SaveDefault,
    )
    # Ladataan presetti
    file_menu.add_command(
    label='Load',
    command=LoadPreset,
    )
    # Erotin
    file_menu.add_separator()
    # Asetukset
    file_menu.add_cascade(
    label="Preferences",
    menu=sub_menu0
    )
    # Näytteenottotaajuus ja bufferin koko valikko
    sub_menu0.add_cascade(
    label="Sample rate",
    menu=sub_menu1
    )
    sub_menu0.add_cascade(
    label="Buffer size",
    menu=sub_menu2
    )
    # Nämä check buttonit olisin halunnut tehdä myös paremmin
    # Toimivat nyt auttavasti, mutta eivät osaa haistella muutosta oikein,
    # tai pikemminkin eivät osaa hakea oletusarvoa.
    # Koitin lisätä sellaisen toiminnon, mutta en saanut toimimaan oikein.
    # Nyt aallon muodot näkyvät printissä, joka käyttäjälle tulostetaan.  
    lfo_menu1.add_checkbutton(
        label="1. Sin",
        onvalue=1,
        offvalue=0,
        command=lambda a = "Sine":LFO(a,b=1)
        )
    lfo_menu1.add_checkbutton(
        label="1. Squ",
        onvalue=1,
        offvalue=0,
        command=lambda a = "Square":LFO(a,b=1)
        )
    lfo_menu1.add_checkbutton(
        label="1. Saw",
        onvalue=1,
        offvalue=0,
        command=lambda a = "Saw":LFO(a,b=1)
        )
    lfo_menu1.add_checkbutton(
        label="1. Tri",
        onvalue=1,
        offvalue=0,
        command=lambda a = "Triangle":LFO(a,b=1)
        )
    lfo_menu2.add_checkbutton(
        label="2. Sin",
        onvalue=1,
        offvalue=0,
        command=lambda a = "Sine":LFO(a,b=2)
        )
    lfo_menu2.add_checkbutton(
        label="2. Squ",
        onvalue=1,
        offvalue=0,
        command=lambda a = "Square":LFO(a,b=2)
        )
    lfo_menu2.add_checkbutton(
        label="2. Saw",
        onvalue=1,
        offvalue=0, 
        command=lambda a = "Saw":LFO(a,b=2)
        )
    lfo_menu2.add_checkbutton(
        label="2. Tri",
        onvalue=1,
        offvalue=0, 
        command=lambda a = "Triangle":LFO(a,b=2)
        )
    lfo_menu3.add_checkbutton(
        label="3. Sin",
        onvalue=1,
        offvalue=0,
        command=lambda a = "Sine":LFO(a,b=3)
        )
    lfo_menu3.add_checkbutton(
        label="3. Squ",
        onvalue=1,
        offvalue=0, 
        command=lambda a = "Square":LFO(a,b=3)
        )
    lfo_menu3.add_checkbutton(
        label="3. Saw",
        onvalue=1,
        offvalue=0,
        command=lambda a = "Saw":LFO(a,b=3)
        )
    lfo_menu3.add_checkbutton(
        label="3. Tri",
        onvalue=1,
        offvalue=0, 
        command=lambda a = "Triangle":LFO(a,b=3)
        )
    # Näytteenotto taajuuden ja bufferin koon arvot
    # sain toimimaan loopissakin. 
    for sb in range(3):
        sub_menu1.add_command(label=p.a_set["s"][sb],command=lambda a = sb: SampleRate(p.a_set["s"][a]))
        sub_menu2.add_command(label=p.a_set["b"][sb],command=lambda a = sb: BufferSize(p.a_set["b"][a]))
    
    # File menu jatkuu, ohjelman sulkeminen
    file_menu.add_separator()
    file_menu.add_command(
    label='Exit',
    command=syna.destroy,
    )
    menubar.add_cascade(
    label="File",
    menu=file_menu
    )
    menubar.add_cascade(
    label="LFO's",
    menu=LFO_menu
    )

# Attack, Decay, Sustain ja Release widget
class ADSR_sliders:
    global ADSR_mon
    ADSR_freme = Frame(syna, width=400, height=120,bg='#39a')
    ADSR_lbl = Label(ADSR_freme,text="ADSR",bg='#39a')
    ADSR_lbl.pack(anchor=N)
    ADSR_mon = Canvas(ADSR_freme,bg="#eee",width=400,height=200)
    ADSR_mon.pack(anchor=N,side="top",padx=5)
    ADSR_mon.delete("all")
    a = int(p.pm_set["attack"])/10
    ad = a + int(p.pm_set["decay"])/10
    ads = ad +int(p.pm_set["sustain"])/10
    adsr = ads+int(p.pm_set["release"])/10
    ADSR_mon.create_line(0,200, a,0, fill="red", width=2)
    ADSR_mon.create_line(a,0,ad,100, fill="blue", width=2)
    ADSR_mon.create_line(ad,100,ads,100, fill="green", width=2)
    ADSR_mon.create_line(ads,100,adsr,200, fill="pink", width=2)
    def Draw_lines(e):
        ADSR_mon.delete("all")
        a = int(p.pm_set["attack"])/10
        ad = a + int(p.pm_set["decay"])/10
        ads = ad +int(p.pm_set["sustain"])/10
        adsr = ads+int(p.pm_set["release"])/10
        ADSR_mon.create_line(0,200, a,0, fill="red", width=2)
        ADSR_mon.create_line(a,0,ad,100, fill="blue", width=2)
        ADSR_mon.create_line(ad,100,ads,100,  fill="green", width=2)
        ADSR_mon.create_line(ads,100,adsr,200, fill="pink", width=2)
    def AVal(e):
        p.pm_set["attack"] = e
        with open(param_path, 'w') as a:
                json.dump(p.pm_set,a)
    def DVal(e):
        p.pm_set["decay"] = e
        with open(param_path, 'w') as d:
                json.dump(p.pm_set,d)
    def SVal(e):
        p.pm_set["sustain"] = e
        with open(param_path, 'w') as s:
                json.dump(p.pm_set,s)
    def RVal(e):
        p.pm_set["release"] = e
        with open(param_path, 'w') as r:
                json.dump(p.pm_set,r)
        
    def isChecked(e):
        if p.pm_set["obey key"] == False:
            p.pm_set["obey key"] = True
            p.pm_set["state"] = "disabled"
            p.pm_set["bg"] = "#968"

            with open(param_path, 'w') as obey:
                json.dump(p.pm_set,obey)
            p.sld["adsr"][2]["state"] = DISABLED
            p.sld["adsr"][2]["bg"] = '#968'
        else:
            p.pm_set["obey key"] = False
            p.pm_set["state"] = "normal"
            p.pm_set["bg"] = "#557"
            with open(param_path, 'w') as obey:
                json.dump(p.pm_set,obey)
            p.sld["adsr"][2]["state"] = NORMAL
            p.sld["adsr"][2]["bg"] = '#557'

    p.sld["adsr"][0] = Scale(
        ADSR_freme,
        orient= HORIZONTAL,
        sliderlength=10, 
        from_=5, 
        to=1000, 
        width=7,
        length=400, 
        label="Attack",
        bg='#167',
        fg='#abd',
        command=AVal
        )
    p.sld["adsr"][0].set(p.pm_set["attack"])
    p.sld["adsr"][0].bind("<Motion>",Draw_lines)
    p.sld["adsr"][0].pack(
        ipadx=0,
        ipady=0,
        expand=False,    
    )
    p.sld["adsr"][1] = Scale(
        ADSR_freme,
        orient= HORIZONTAL,
        sliderlength=10, 
        from_=5, 
        to=1000, 
        width=7,
        length=400, 
        label="Decay", 
        bg='#375',
        fg='#abd',
        command=DVal
        )
    p.sld["adsr"][1].set(p.pm_set["decay"])
    p.sld["adsr"][1].bind("<Motion>",Draw_lines)
    p.sld["adsr"][1].pack(
        ipadx=0,
        ipady=0,
        expand=False,
    )
    p.sld["adsr"][2] = Scale(
        ADSR_freme,
        orient= HORIZONTAL,
        sliderlength=10, 
        from_=5, 
        to=1000,
        width=7,
        length=400,
        state=p.pm_set["state"], 
        label="Sustain", 
        bg=p.pm_set["bg"],
        fg='#abd',
        command=SVal
        )
    p.sld["adsr"][2].set(p.pm_set["sustain"])
    p.sld["adsr"][2].bind("<Motion>",Draw_lines)
    p.sld["adsr"][2].bind("<Double-Button-1>",isChecked)
    p.sld["adsr"][2].pack(
        ipadx=0,
        ipady=0,
        expand=False,
    )
    p.sld["adsr"][3] = Scale(
        ADSR_freme,
        orient= HORIZONTAL,
        sliderlength=10, 
        from_=5, 
        to=1000, 
        width=7,
        length=400,
        label="Release", 
        bg='#755',
        fg='#abd',
        command=RVal
        )
    p.sld["adsr"][3].set(p.pm_set["release"])
    p.sld["adsr"][3].bind("<Motion>",Draw_lines)
    p.sld["adsr"][3].pack(
        ipadx=0,
        ipady=0,
        expand=False,
    )
    ADSR_freme.grid(row=0,column=0,padx=10,pady=10)

# Eri aaltojen äänen voimakkuus
class Wave_Sliders:
    # arvot prosentuaalisia säätimissä
    Wave_freme = Frame(syna, width=275, height=100,bg='#39a')
    Wave_lbl = Label(Wave_freme,text="Waves",bg='#39a')
    Wave_lbl.pack(anchor=N)
    def SineVal(e):
        p.pm_set["sin vol"] = e
        with open(param_path, 'w') as sin:
                json.dump(p.pm_set,sin)
    def SquareVal(e):
        p.pm_set["sin vol"] = e
        with open(param_path, 'w') as squ:
                json.dump(p.pm_set,squ)
    def SawVal(e):
        p.pm_set["sin vol"] = e
        with open(param_path, 'w') as saw:
                json.dump(p.pm_set,saw)
    def TriangleVal(e):
        p.pm_set["sin vol"] = e
        with open(param_path, 'w') as tri:
                json.dump(p.pm_set,tri)
    # from_ ja to arvot tulevat vielä muuttumaan...
    p.sld["wave"][0] = Scale(
        Wave_freme,
        length=400,
        sliderlength=20,
        from_=0, 
        to=100, 
        width=7, 
        label="Sine", 
        bg='#167',
        fg='#abd',
        orient=HORIZONTAL, 
        command=SineVal
        )
    p.sld["wave"][0].set(p.pm_set["sin vol"])
    p.sld["wave"][0].pack(ipadx=0,ipady=0,expand=True)
    p.sld["wave"][1] = Scale(
        Wave_freme,
        length=400,
        sliderlength=20, 
        from_=0, 
        to=100, 
        width=7, 
        label="Square", 
        bg='#375',
        fg='#abd',
        orient=HORIZONTAL, 
        command=SquareVal
        )
    p.sld["wave"][1].set(p.pm_set["squ vol"])
    p.sld["wave"][1].pack(ipadx=0,ipady=0,expand=True)
    p.sld["wave"][2] = Scale(
        Wave_freme,
        length=400,
        sliderlength=20,
        from_=0, 
        to=100, 
        width=7, 
        label="Saw", 
        bg='#557',
        fg='#abd',
        orient=HORIZONTAL, 
        command=SawVal
        )
    p.sld["wave"][2].set(p.pm_set["saw vol"])
    p.sld["wave"][2].pack(ipadx=0,ipady=0,expand=True)
    p.sld["wave"][3] = Scale(
        Wave_freme,
        length=400,
        sliderlength=20, 
        from_=0, 
        to=100, 
        width=7, 
        label="Triangle", 
        bg='#755',
        fg='#abd',
        orient=HORIZONTAL, 
        command=TriangleVal
        )
    p.sld["wave"][3].set(p.pm_set["tri vol"])
    p.sld["wave"][3].pack(ipadx=0,ipady=0,expand=True)
    Wave_freme.grid(row=1,column=0,sticky=NW,padx=10,pady=10)

# Vola ja tempo widget
class VolumeTempo:
    vol_frm = Frame()
    vol_frm.config(bg="#4ab")
    def Change(e):
        p.pm_set["master"] = e
    def Tempo(e):
        p.pm_set["tempo"] = e
    vol = Scale(
        vol_frm,
        length=250,
        sliderlength=20, 
        from_=0, 
        to=100, 
        label="Master vol",
        bg='#39a',
        orient=HORIZONTAL, 
        command=Change
        )
    tempo = Scale(
        vol_frm,
        length=250,
        sliderlength=20, 
        from_=30, 
        to=360, 
        label="Master tempo",
        bg='#39a',
        orient=HORIZONTAL, 
        command=Change
        )
    vol.set(p.pm_set["master"])
    vol.pack()
    tempo.set(p.pm_set["tempo"])
    tempo.pack()
    vol_frm.grid(row=0,column=1,sticky=N,padx=5,pady=10)

# LFO widget
class LFOs:
    # Muuta metodeihin tallennukset.
    def Depth_1(e):
        p.pm_set["1. depht"] = e
        with open(param_path, 'w') as d1:
                json.dump(p.pm_set,d1)
    def Speed_1(e):
        p.pm_set["1. speed"] = e
        with open(param_path, 'w') as s1:
                json.dump(p.pm_set,s1)
    def Depth_2(e):
        p.pm_set["2. depht"] = e
        with open(param_path, 'w') as d2:
                json.dump(p.pm_set,d2)
    def Speed_2(e):
        p.pm_set["2. speed"] = e
        with open(param_path, 'w') as s2:
                json.dump(p.pm_set,s2)
    def Depth_3(e):
        p.pm_set["3. depht"] = e
        with open(param_path, 'w') as d3:
                json.dump(p.pm_set,d3)
    def Speed_3(e):
        p.pm_set["3. speed"] = e
        with open(param_path, 'w') as s3:
                json.dump(p.pm_set,s3)
    LFO_frm = Frame(bg='#4ab')
    #########
    p.sld["depth"][0] = Scale(
        LFO_frm, 
        label="LFO 1. depth",
        bg='#7ab',
        length=350,
        sliderlength=10,
        width=7,
        orient=HORIZONTAL,
        command=Depth_1
        )
    p.sld["depth"][0].set(p.pm_set["1. depht"])
    p.sld["depth"][0].pack()
    p.sld["speed"][0] = Scale(
        LFO_frm,
        label="LFO 1. speed",
        bg='#977',
        length=350,
        sliderlength=10,
        from_=0,to=1000,
        width=7,
        orient=HORIZONTAL,
        command=Speed_1
        )
    p.sld["speed"][0].set(p.pm_set["1. speed"])
    p.sld["speed"][0].pack()
     #########
    p.sld["depth"][1] = Scale(
        LFO_frm, 
        label="LFO 2. depth",
        bg='#7ab',
        length=350,
        sliderlength=10,
        width=7,
        orient=HORIZONTAL,
        command=Depth_2
        )
    p.sld["depth"][1].set(p.pm_set["2. depht"])
    p.sld["depth"][1].pack()
    p.sld["speed"][1] = Scale(
        LFO_frm,
        label="LFO 2. speed",
        bg='#977',
        length=350,
        sliderlength=10,
        from_=0,to=1000,
        width=7,
        orient=HORIZONTAL,
        command=Speed_2
        )
    p.sld["speed"][1].set(p.pm_set["2. speed"])
    p.sld["speed"][1].pack()
     #########
    p.sld["depth"][2] = Scale(
        LFO_frm, 
        label="LFO 3. depth",
        bg='#7ab',
        length=350,
        sliderlength=10,
        width=7,
        orient=HORIZONTAL,
        command=Depth_3
        )
    p.sld["depth"][2].set(p.pm_set["3. depht"])
    p.sld["depth"][2].pack()
    p.sld["speed"][2] = Scale(
        LFO_frm,
        label="LFO 3. speed",
        bg='#977',
        length=350,
        sliderlength=10,
        from_=0,to=1000,
        width=7,
        orient=HORIZONTAL,
        command=Speed_3
        )
    p.sld["speed"][2].set(p.pm_set["3. speed"])
    p.sld["speed"][2].pack()
    LFO_frm.grid(row=1,column=1,columnspan=2,sticky=EW,padx=5,pady=10)
# Käynnistetään formi
syna.mainloop()

# Muutama sana siitä miksi en ehkä onnistunut niin hyvin kuin toivoin.
# 1. Aiempi kokemus WinFormeista ja WPF:istä ei auttanut kovin paljon.
# 2. Projekti muuttui aikapaljon matkanvarrella ja se saattoi tehdä siitä sekavan.
# 3. Koitin korjailla joiltain osin, mutta se toi paikoin uusia ongelmia ja olisi vaatinut isompia muutoksia    