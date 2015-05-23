import sys

class player:
    name=""
    def read_from_file(self,f):
        self.name=f.readline().rstrip('\n')
        
    def write_to_file(self,f):
        f.write("player\n")
        f.write(self.name+'\n')
        
    def get_name(self):
        return self.name
    
    def set_name(self,new_name=""):
        self.name=new_name

    def print_me(self):
        return self.name

def read_data():
    global name
    global players
    players=[]
    f=open('data.cbn','r')
    name=f.readline().rstrip('\n')
    current="lol"
    while current!='':
        current=f.readline().rstrip('\n')
        if current=='player':
            x=player()
            x.read_from_file(f)
            players.append(x)
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
    print("Hello, "+name+"!")

def help_me():
    #horrible help function
    global commands
    print("List of commands:",
          "\n".join(sorted([key for key in commands])),
          sep="\n")

def add_player():
    global players
    new_name=input("Name: ").lower()
    x=player()
    x.set_name(new_name)
    players.append(x)

def player_exists():
    global players
    new_name=input("Name: ").lower()
    for x in players:
        if x.get_name()==new_name:
            print("He or she exists")
            break
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
    new_name=input("Name: ").lower()
    players2=[x for x in players if x.get_name()!=new_name]
    if len(players2)==len(players):
       print("Sorry, can't find him or her.")
    else:
        players=players2
        print("Done!")

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
        'delete':delete_forever}
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
