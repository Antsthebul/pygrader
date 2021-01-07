import os

from pathlib import Path
from contextlib import ContextDecorator
from collections import deque

# class Node:

#     def __init__(self, name):
#         self.actual = name 
    
#     def __repr__(self):
#         return self.actual.stem 
    

class pushit(ContextDecorator):
    home = os.environ['HOMEPATH']
    q = deque()
    
    def __init__(self,*args, **kwargs): # init for cntxt mgr
        # if args:
        #     if type(args[0])== 'function': 
        #         self.fn = args
        # else:
        #     pass
        self.q = pushit.q
        self.prev_dir = None
        super().__init__()
        print('Init: ', args)
        
    
    def __call__(self,file=None, ch_dir=True,**kwargs):
        if file:
            if '~' in file:
                file = Path(pushit.home) / file.lstrip('~/')
                # print(file)
                # print(str(file))
            else:
                file = Path(os.getcwd()) / file
            # file = Node(file)
            if 'right' not in kwargs:
                pushit.q.appendleft(file)
            else:
                pushit.q.append(file)
        print('call: ',file)
        if ch_dir and file:
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
    
    def __iter__(self): pass
@pushit 
def pushd(file): # 1st initializes func
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
                print('Pushd has no more dirs in queue')
        else:
            try:
                obj = pushit.q.pop()
            except ValueError:
                print(e)
                print('Pushd has no more dirs in queue')

    return obj
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
    for obj in f:
        print(obj)
    print('dang\n')

print('\n--Context mgr 2 levels--') 
with pushit() as f:
    with pushit() as f:
        print(repr(f))
    print('dang\n')
# print('\nC.M--With args')
# with pushit('who') as f:
#     print(f)
#     for obj in f:
#         print(obj)
#     print('dang') 