import sys

class player:
    
    states=['mo','mi','to','ti','bo','bi','mito','moti','tomi','timo','none']
    
    def __init__(self,name=""):
        self.name=name
        self.id=None
        self.fac=False
        self.slots=['none' for i in range(1,6)]

    def read_from_file(self,f):
        self.name=f.readline().rstrip('\n')
        self.id=int(f.readline().rstrip('\n'))
        self.fac=f.readline().rstrip('\n')=='True'
        self.slots=[f.readline().rstrip('\n') for i in range(1,6)]

    def write_to_file(self,f):
        f.write("player\n")
        f.write(self.name+'\n')
        f.write(str(self.id)+'\n')
        f.write(str(self.fac)+'\n')
        for i in self.slots:
            f.write(i+'\n')

    def print_me(self):
        all='Name: '+self.name+", Id: "+str(self.id)+", FAC: "+str(self.fac)
        all+=', Slots: ('+', '.join(self.slots)+').'
        return all

    def __hash__(self):
        return hash(self.name)

    def __eq__(self,other):
        try:
            return self.get_name()==other.get_name()
        except AttributeError:
            return NotImplemented

def read_data():
    global name
    global players
    players=set()
    f=open('data.cbn','r')
    name=f.readline().rstrip('\n')
    current="lol"
    while current!='':
        current=f.readline().rstrip('\n')
        if current=='player':
            x=player()
            x.read_from_file(f)
            players.add(x)
    f.close()

def first_time():
    set_name()

def save():
    f=open('data.cbn','w')
    f.write(name+'\n')
    for x in players:
        x.write_to_file(f)
    f.close()
    print("All data was saved!")

def exit_all():
    save()
    print("Goodbye!")
    sys.exit()

def get_player(name):
    #Get the object of the player
    #UnPythonic hack, but it's the only way i know
    global players
    class grab:
        def __init__(self,value):
            self.value=value
        def __hash__(self):
            return hash(self.value)
        def __eq__(self,other):
            if self.value.name==other.name:
                self.real_value=other
                return True
            return False
    x=grab(player(name))
    if x in players:
        return x.real_value
    return None

#commands
def set_name():
    global name
    name=input("Your name is: ")

def all_commands():
    global commands
    print("List of commands:",
          ", ".join([key for key in commands]),
          sep="\n")

def add_player():
    global players
    s=input("Name: ").lower()
    x=get_player(s)
    if x != None:
        print("Player already exists!")
    else:
        x=player(s)
        while x.id==None:
            try:
                x.id=int(input("Id: "))
            except ValueError:
                print("Id needs to be a number!")
        players.add(x)

def player_exists():
    global players
    x=get_player(input("Name: ").lower())
    if x != None:
        print(x.print_me())
    else:
        print("Sorry, can't find player.")

def list_all():
    global players
    if len(players)==0:
        print("You have added no users yet!")
        return
    for x in players:
        print(x.print_me())

def delete_forever():
    global players
    response=input("Are you sure you want to permanently delete a "+
                   "player? Say 'yes' if so: ").lower()
    if response!='yes':
        return
    x=get_player(input("Name: ").lower())
    if x == None:
        print("Sorry, can't find player.")
        return
    players.remove(x)
    print("Done!")

def change_id():
    global players
    x=get_player(input("Name: ").lower())
    if x==None:
        print("Player not found")
        return
    original_id=x.id
    while original_id==x.id:
        try:
            x.id=int(input("Id: "))
        except ValueError:
            print("Id needs to be a number!")

def change_fac():
    global players
    x=get_player(input("Name: ").lower())
    if x==None:
        print("Player not found")
        return
    response=input("Does player have FAC (yes/no): ").lower()
    while response != "yes" and response != "no":
        response=input("Does player have FAC (yes/no): ").lower()
    if response=="yes":
        x.fac=True
    else:
        x.fac=False

def change_slots():
    global players
    x=get_player(input("Name: ").lower())
    if x==None:
        print("Player not found")
        return
    for i in range(5):
        name=input("Slot #"+str(i+1)+": ")
        while not name in player.states and len(name)>0:
            print("Invalid state.")
            name=input("Slot #"+str(i+1)+": ")
        if len(name) == 0:
            continue
        x.slots[i]=name

def main():
    global commands
    global name
    commands={
        'exit':exit_all,
        'commands':all_commands,
        'name':set_name,
        'add':add_player,
        'save':save,
        'check':player_exists,
        'list':list_all,
        'delete':delete_forever,
        'id':change_id,
        'fac':change_fac,
        'slots':change_slots}
    try:
        read_data()
    except FileNotFoundError:
        first_time()
    print("Welcome back, "+name+"!")
    while 1:
        s=input("Command: ").lower()
        if s=='':
            continue
        proc=commands.get(s)
        if proc != None: proc()
        else: print("Command not found. Plese try again.",
                    "Write 'commands' for a list of commands.")

if __name__ == '__main__':
    main()
