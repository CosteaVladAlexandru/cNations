import sys

class player:
    def __init__(self,name=""):
        self.name=name
        self.id=None

    def read_from_file(self,f):
        self.name=f.readline().rstrip('\n')
        self.id=int(f.readline().rstrip('\n'))

    def write_to_file(self,f):
        f.write("player\n")
        f.write(self.name+'\n')
        f.write(str(self.id)+'\n')

    def get_name(self):
        return self.name

    def set_name(self,new_name=""):
        self.name=new_name

    def get_id(self):
        return self.id

    def set_id(self,id):
        self.id=id

    def print_me(self):
        return self.name+" "+str(self.id)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self,other):
        return self.get_name()==other.get_name()

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
    x=player(input("Name: ").lower())
    if x in players:
        print("Player already exists!")
    else:
        while x.get_id()==None:
            try:
                x.set_id(int(input("Id:")))
            except ValueError:
                print("Id needs to be a number!")
        players.add(x)

def player_exists():
    global players
    x=player(input("Name: ").lower())
    if x in players:
        print("He or she exists")
        return
    else:
        print("Sorry, can't find him or her.")

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
    x=player(input("Name: ").lower())
    if x in players:
        players.remove(x)
        print("Done!")
    else:
        print("Sorry, can't find him or her.")

def change_id():
    global players
    #TODO: reimplement this
    #It currently discards all info except name.
    #I only want to discard id
    x=player(input("Name: ").lower())
    if x in players:
        players.remove(x)
        while x.get_id()==None:
            try:
                x.set_id(int(input("Id:")))
            except ValueError:
                print("Id needs to be a number!")
        players.add(x)
    else:
        print("Sorry, can't find him or her.")

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
        'id':change_id}
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
