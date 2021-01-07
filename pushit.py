from contextlib import ContextDecorator
from collections import deque
import os 

class pushit(ContextDecorator):

    q = deque()
    
    def __init__(self,*args, **kwargs): # init for cntxt mgr
        if isinstance(args, function): 
            self.fn = args
        else:
            pass
        self.q = pushit.q
        self.prev_dir = None
        super().__init__()
        print('Init: ', args)
        
    
    def __call__(self,*args, **kwargs):
        if args:
            if 'right' not in kwargs:
                for arg in args:
                    pushit.q.appendleft(arg)
            else:
                for arg in args:
                    pushit.q.append(arg)
        print('call: ',args)
    def __enter__(self):
        self.fn(file=None)
        return pushit.q

    def __exit__(self, *exc):
        print('out')
        if self.prev_dir:os.chdir(self.prev_dir)
        return False 
    
    def __repr__(self):
        for ix, obj in enumerate(pushit.q):
            print(ix,obj)
        return ''
    

@pushit 
def pushd(file): # 1st initializes func
    self.prev_dir = os.getcwd()
    print(self.prev_dir)
    if file: os.chdir(file)
    print('here: ', os.getcwd())
    pass

# pushd()
# pushd('test') # these are sent to __call__
# pushd('test/test1')
# pushd('test/test2', right=True)
# print('--Start--')
# print(pushd.q)

# print('\n--Context mgr--')
# print('CM--withoutargs')
# with pushit() as f:
#     print(f)
#     for obj in f:
#         print(obj)
#     print('dang\n') 

# print('\nC.M--With args')
# with pushit('who') as f:
#     print(f)
#     for obj in f:
#         print(obj)
#     print('dang') 