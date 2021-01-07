import os

from pathlib import Path
from contextlib import ContextDecorator
from collections import deque



class pushit(ContextDecorator):
    home = os.environ['HOMEPATH']
    q = deque()
    
    def __init__(self,*args, **kwargs): # init for cntxt mgr
        if args:
            if type(args[0])== 'function': 
                self.fn = args
        else:
            pass
        self.q = pushit.q
        self.prev_dir = None
        super().__init__()
        print('Init: ', args)
        
    
    def __call__(self,file=None, ch_dir=True,**kwargs):
        if file:
            if '~' in file:
                file = Path(pushit.home) / file.lstrip('~/')
            if 'right' not in kwargs:
                pushit.q.appendleft(file)
            else:
                pushit.q.append(file)
        print('call: ',file)
        if ch_dir and file:
            os.chdir(file)
    
    def __enter__(self, file=None):
        self.prev_dir = os.getcwd()
        print(self.prev_dir)
        if file: 
            route = pop(file)
            os.chdir(route)
        print('here: ', os.getcwd())
        return pushit.q

    def __exit__(self, *exc):
        print('out')
        if self.prev_dir:os.chdir(self.prev_dir)
        return False 
    
    def __repr__(self):
        current = os.getcwd()
        if not pushit.q:
            print('0 {};'.format(current))

        for ix, obj in enumerate(pushit.q):
            if  ix== 0:
                print('{} {};'.format(current))
            print(ix,obj)
        return ''
    

@pushit 
def pushd(file): # 1st initializes func
    pass

def popd(file=None):
    if file:
        try:
            pushit.q.remove(file)
        except ValueError:
            print(e)
            print('Unable to remove " %s" Pushd has no more dirs in queue' % file)
    else:
        try:
            pushit.q.popleft()
        except ValueError:
            print(e)
            print('Pushd has no more dirs in queue')

# dirs can be traced from home or by cwd only
print('Echo:\n',pushd)
print('-' * 50)
print('Empty call:\n',pushd())
print('-' * 50)

print('Single file addition:')
pushd('test') # these are sent to __call__
print('Echo:\n',pushd)
print('-' * 50)

print('Single file addition:')
pushd('test1') # 
print('Echo:\n',pushd)
print('-'*50)

print('Append right: ', pushd('test2', right=True))
print('Echo:\n',pushd)
print('-'*50)
print('From home dir', pushd('~/anaconda3'))
print('Echo:\n',pushd)

print('-'*50)
print('--Start--')
# print(pushd.q)

print('\n--Context mgr--')
print('CM--withoutargs')
with pushit() as f:
    print(f)
    for obj in f:
        print(obj)
    print('dang\n') 

# print('\nC.M--With args')
# with pushit('who') as f:
#     print(f)
#     for obj in f:
#         print(obj)
#     print('dang') 