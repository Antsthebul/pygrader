import os

from pathlib import Path
from contextlib import ContextDecorator
from collections import deque

    

class pushit(ContextDecorator):
    ''' Allows the'''
    home = os.environ['HOMEPATH']
    q = deque()
    
    def __init__(self,*args, **kwargs): # init for cntxt mgr calls
        self.q = pushit.q
        self.prev_dir = None
        super().__init__()
        
    
    def __call__(self,file=None, chdir=True,**kwargs):
        ''' Default is to change to dir that is added to queue. 
        Passing chdir=False allows to remain in current dir, 
        while adding to the queue'''
        if file:
            if '~' in file:
                file = Path(pushit.home) / file.lstrip('~/')
            else:
                file = Path(os.getcwd()) / file
            if 'right' not in kwargs:
                pushit.q.appendleft(file)
            else:
                pushit.q.append(file)
        print('call: ',file)
        if chdir and file:
            os.chdir(file)
    
    def __enter__(self, file=None):
        print('__enter__')
        self.prev_dir = os.getcwd()
        print(self.prev_dir)
        if file:
            route = popd(file)
        else:
            route = popd()
        os.chdir(route)
        print('Now here: ', os.getcwd())
        return self

    def __exit__(self, *exc):
        print('__exiting__')
        if self.prev_dir:os.chdir(self.prev_dir)
        print('We exited: ', self.prev_dir) # this should be where we intiaiily started
        return False 
    
    def __repr__(self):
        current = os.getcwd()
        if not pushit.q:
            print('0 {};'.format(current))

        for ix, obj in enumerate(pushit.q):
            if  ix== 0:
                print(current)
            print(ix,obj.stem)
        return ''
    
    def __iter__(self):
        for obj in pushit.q:
            yield obj.stem
@pushit 
def pushd(file): # __init__ this is wut intializes the pushd as a
                # context deco 1st.
    pass

def popd(file=None, left=True):
    if file:
        try:
            pushit.q.remove(file)
        except ValueError:
            print(e)
            print('Unable to remove " %s" Pushd has no more dirs in queue' % file)
    else:
        if left:
            try:
                obj = pushit.q.popleft()
            except ValueError:
                print(e)
                print('Pushd does not contin any dirs')
        else:
            try:
                obj = pushit.q.pop()
            except ValueError:
                print(e)
                print('Pushd does not contain any dirs')

    return obj

# Tests
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

print('Append right:')
pushd('test2', right=True)
print('Echo:\n',pushd)
print('-'*50)

print('From home dir')
pushd('~/anaconda3')
print('Echo:\n',pushd)

print('-'*50)
print('--Start--')
# print(pushd.q)

print('\n--Context mgr--')
print('CM--withoutargs')
with pushit() as f:
    print('Begin for loop')
    for obj in f:
        print('No arg: ',obj)

print('Echo: ', pushd)
print('\n--Context mgr 2 levels--') 
with pushit() as f:
    with pushit() as f:
        print(f)
# print('\nC.M--With args')
# with pushit('who') as f:
#     print(f)
#     for obj in f:
#         print(obj)
#     print('dang') 