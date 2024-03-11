import cmd


class Echo(cmd.Cmd):
    '''Dund echo comand REPL'''
    prompt = ':->'
    words = 'one', 'two', 'three', 'four', 'five'
    
    def do_echo(self, args):
        print(args)
    
    def complete_echo(self, text, line, begidx, endidx):
        return [c for c in self.words if c.startswith(text)]
    
    def do_EOF(self, args):
        return True
    
    def emptyline(self) -> bool:
        pass


def main():
    Echo().cmdloop()    


if __name__ == '__main__':
    main()
