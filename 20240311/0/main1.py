import cmd
import calendar

class Calend(cmd.Cmd):
    '''Text calendar'''
    prompt = '>>>'
    
    def do_prmonth(self, args):
        '''Print a month’s calendar as returned by formatmonth().'''
        theyear, themonth = map(int, args.split())
        print(calendar.prmonth(themonth=themonth, theyear=theyear))
    
    
    
    def do_pryear(self, args):
        '''Print the calendar for an entire year as returned by formatyear().'''
        print(calendar.TextCalendar().pryear(theyear=int(args)))

if __name__ == '__main__':
    Calend().cmdloop()
    
