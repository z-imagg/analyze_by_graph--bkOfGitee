#!/usr/bin/env python
# -*- coding: utf-8 -*-

#【术语】 abs==abstract==抽象
import typing
T = typing.TypeVar('T')
from abc import abstractmethod,ABC
class TraverseAbs(ABC):
    def V(self,RE):
        self.bz(None,None,None,None,None)
        pass

    @abstractmethod
    def bz(self,RE,RL,isLeaf,S,C):
        raise Exception("你的抽象方法书写的不对，因为py应该自己确保不能调用此抽象方法，而不是靠我这个异常来确保")

class BzDeepth(TraverseAbs):
    def bz(self,RE,RL,isLeaf,deepth_ls,_):
        pass

class BzWriteDeepth(TraverseAbs):
    def bz(self,RE,RL,isLeaf,deepth_ls,_):
        pass

class BzWriteWidth(TraverseAbs):
    def bz(self,RE,RL,isLeaf,_,childLs):
        pass

class BzWrite成份(TraverseAbs):
    def bz(self,RE,RL,isLeaf,S,_):
        pass



if __name__=="__main__":
    BzDeepth().V(None)
    BzWriteDeepth().V(None)
    BzWriteWidth().V(None)
    BzWrite成份().V(None)
    
    TraverseAbs()#有抽象方法的类 不能被实例化，报错如下 
    #TypeError: Can't instantiate abstract class Traverse with abstract method bz

