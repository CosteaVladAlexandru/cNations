import sys

class player:
    def __init__(self,name=""):
        self.name=name
        self.id=None
        self.fac=False

    def read_from_file(self,f):
        self.name=f.readline().rstrip('\n')
        self.id=int(f.readline().rstrip('\n'))
        self.fac=f.readline().rstrip('\n')=='True'

    def write_to_file(self,f):
        f.write("player\n")
        f.write(self.name+'\n')
        f.write(str(self.id)+'\n')
        f.write(str(self.fac)+'\n')

    def print_me(self):
        return self.name+" "+str(self.id)+" Fac="+str(self.fac)

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

def help_me():
    #horrible help function
    global commands
    print("List of commands:",
          "\n".join([key for key in commands]),
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
        print("Player exists")
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
    response=input("Does player have FAC (yes/no): ").lower()
    while response != "yes" and response != "no":
        response=input("Does player have FAC (yes/no): ").lower()
    if response=="yes":
        x.fac=True
    else:
        x.fac=False

def main():
    global commands
    global name
    commands={
        'exit':exit_all,
        'help':help_me,
        'name':set_name,
        'add':add_player,
        'save':save,
        'check':player_exists,
        'list':list_all,
        'delete':delete_forever,
        'id':change_id,
        'fac':change_fac}
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
                    "Write 'help' for a list of commands.")

if __name__ == '__main__':
    main()
