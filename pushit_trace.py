import os
import sys 

from pathlib import Path
from contextlib import ContextDecorator
from collections import deque

    

class pushit(ContextDecorator):
    ''' A mix between a queue and a context manager.If used as a context manager, pushit will always
    return to PWD.'''
    home = os.environ['HOMEPATH'] if sys.platform[:3] == 'win' else os.environ['HOME']
    q = deque()

    def __init__(self,*args, **kwargs): # init for cntxt mgr calls, and funs @ startup
        # This runs twice in that 1st time @ startup nd then when using with statement
        super().__init__()
        self.q = pushit.q
        self.prev_dir = None
        self.main = Path(os.getcwd())
        if args and (type(args[0]) ==str):
            self.thispath = args[0] 
        elif args and (type(args[0]) != str):
            self.fn = args[0]
        else:
            self.thispath = None
    
    def __call__(self,path=None, chdir=True,**kwargs): # As function
        ''' Default for pushd is to change to dir when called, and add to queue. 
        Passing chdir=False remains in current dir, 
        while still adding to queue'''
        if not pushit.q:
            pushit.q.append(self.main) # always start queue with cwd @ function call w or w/ args
        if path:
            path = self.clean_path(path)
            if 'right' not in kwargs:
                pushit.q.appendleft(path)
            else:
                pushit.q.append(path)
        # print('Called with: ',path)
        if chdir and path:
            os.chdir(path)
        return self.fn(path)
    
    def __enter__(self):
        print('Enter: ', end='')
        self.prev_dir = os.getcwd()
        print(self.prev_dir)
        if self.thispath:
            os.chdir(self.clean_path(self.thispath)) # Just head to dir
        else:
            os.chdir(popd(left=True))  # or use queue, LIFO mode
        print('We now switched to here: ', os.getcwd())
        print('Enter body...\n')
        return self # to be used by context MGR

    def __exit__(self, *exc):
        print('__exiting__')
        print('Still in: ', os.getcwd())
        if self.prev_dir and (self.prev_dir != os.getcwd()):
            os.chdir(self.prev_dir)
            print('We exited to: ', self.prev_dir) # this should be where we intiaiily started
        return False 
    
    def __repr__(self):
        current = os.getcwd()
        print('- {};'.format(current))
        for ix, obj in enumerate(pushit.q):
                print(ix,obj.stem)
      
        return ''
    
    def __iter__(self):
        ''' Path objects have .stem() if names should be
        displayed instead'''
        for obj in pushit.q:
            yield obj
    
    def clean_path(self, path):
        if '~' in path:
            path = Path(pushit.home) / path.lstrip('~/')
        else:
            path = Path(os.getcwd()) / path
        if '.' in str(path):
            path = path.resolve()
        if path.is_dir():
            return path
        raise FileNotFoundError(f'FileNotFoundError: Unable to locate path specified "{path}".')

    def clear(self):
        '''Start fresh from original call location '''
        pushit.q.clear()
        os.chdir(self.main)
        
@pushit 
def pushd(file):
    print('I run')
    pass

def popd(path=None, left=None, save=False):
    '''If path is specifed, path will be removed
    save kwarg is for when popd shoud 'echo' the dir instead of
    remove it'''
    obj = None
    if path:
        try:
            pushit.q.remove(path)
        except ValueError:
            print('Unable to locate "%s" ' % path)
    else:
        if left:
            left = False
            try:
                obj = pushit.q.popleft()
            except IndexError:
                print('Pushd does not contin any dirs')
            else:
                left = True
        else:
            right = False
            try:
                obj = pushit.q.pop()
            except IndexError:
                print('Pushd does not contain any dirs')
            else:
                right = True
    obj = str(obj)
    if save and left:
        pushd(obj)
    elif save and right:
        pushd(obj, right=True) 
    return obj

