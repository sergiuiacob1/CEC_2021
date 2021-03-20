import math
from math import sin, cos
import operator
import random, time


class Algorithm:
    def __init__(self, func, optimumIsMinimum = True, precision = 5, dimensions = 2, steps = 1, doForever = 0, repeats = 1):
        self.func = func[0]
        self.dimRange = func[1]
        self.dimIntervalLength = self.dimRange[1] - self.dimRange[0]
        self.optimumIsMinimum = optimumIsMinimum
        if optimumIsMinimum:
            self.optInit = math.inf
            self.cmp = operator.lt
            self.getOpt = min
        else:
            self.optInit = -math.inf
            self.cmp = operator.gt
            self.getOpt = max
        self.dimensions = dimensions
        self.precision = precision
        self.steps = steps
        self.dimensionBitSize = math.ceil(
            math.log2(
                self.dimIntervalLength * 10**precision,
            )
        )
        self.candidateBitSize = self.dimensions * self.dimensionBitSize
        self.dimMaxInt = 2 ** self.dimensionBitSize - 1
        self.candidate = None
        self.be = self.optInit #best eval
        self.bb = None #bitstring
        self.bv = []   #values
        self.bstep = 0 #at which eval did we achieve this best
        self.br = 0 #repeat when best was found
        self.exploredPoints = []
        self.evals = 0
        self.repeats = repeats
        self.repCurr = 0
        self.doForever = doForever

    def __str__(self):
        return(self.getName() + ' ' + self.func.__doc__)
        
    def getName(self):
        return('Random Search Algorithm (Binary)')

    def gimmeSomeEval(self):
        c0 = [ self.dimRange[0] ] * self.dimensions
        c1 = [ self.dimRange[1] ] * self.dimensions
        c2 = [ self.dimRange[0] + (self.dimRange[1] - self.dimRange[0]) / 2 ] * self.dimensions
        e0 = self.func(c0)
        e1 = self.func(c1)
        e2 = self.func(c2)
        e = self.getOpt(e0, e1, e2)
        return(e)
        
    def getRepCurr(self):
        return(self.repCurr)

    def getRepMax(self):
        return(self.repeats)

    def getRepBest(self):
        return(self.br)
    
    def generateCandidate(self):
        candidate = [0] * self.candidateBitSize
        avBits = 0
        bitBlockSize = 64
        for ii in reversed( range(self.candidateBitSize) ):
            if avBits == 0:
                avBits = min(bitBlockSize, ii + 1)
                randBits = random.getrandbits(avBits)
            candidate[ii] = 1 & randBits
            randBits >>= 1
            avBits -= 1
        return(candidate)

    def decode(self, candidate):
        values = [0] * self.dimensions
        a0 = 0
        a1 = self.dimensionBitSize
        for ii in range(self.dimensions):
            values[ii] = self.decodeDimension( candidate[a0:a1] )
            a0 = a1
            a1 += self.dimensionBitSize
        return(values)

    def decodeDimension(self, dimensionBits):
        s = 0
        for b in dimensionBits:
            s = (s << 1) | b
        v = s / self.dimMaxInt * self.dimIntervalLength + self.dimRange[0]
        return(v)

    def eval(self, values):
        self.evals += 1
        e = self.func(values)
        self.exploredPoints.append([e, *values])
        return(e)

    def restart(self):
        self.candidate = None
        self.be = self.optInit #best eval
        self.bb = None #bitstring
        self.bv = []   #values
        self.bstep = 0 #at which eval did we achieve this best
        self.br = 0 #repeat when best was found
        self.exploredPoints = []
        self.evals = 0
        self.repCurr = 0

    def solveStep(self):
        if self.repCurr >= self.repeats:
            if self.doForever:
                self.restart()
            else:
                return()
        self.repCurr += 1
        self.candidate = self.generateCandidate()
        v = self.decode(self.candidate)
        e = self.eval(v)
        if self.cmp(e, self.be):
            self.br = self.repCurr - 1
            self.be = e
            self.bb = self.candidate[:]
            self.bv = v
            self.bstep = self.evals

    def run(self):
        self.exploredPoints = []
        for _ in range(self.steps):
            self.solveStep()
        return(self.exploredPoints)

class AlgorithmBihc(Algorithm):
    def __init__(self, func, optimumIsMinimum = True, precision = 5, dimensions = 2, steps = 1, repeats = 10000, doForever = 0):
        super().__init__(func, optimumIsMinimum, precision, dimensions, steps, doForever)
        self.repeats = repeats
        self.ce = 0 #current eval
        self.cv = [] #current values
        self.tbe = 0 #temp best eval, position
        self.tbp = 0

    def getName(self):
        return('Best Improvement Hill-Climbing Algorithm (Binary)')
        
    def restart(self):
        self.candidate = None
        self.be = self.optInit #best eval
        self.bb = None #bitstring
        self.bv = []   #values
        self.bstep = 0 #at which eval did we achieve this best
        self.br = 0 #repeat when best was found
        self.exploredPoints = []
        self.evals = 0
        self.repCurr = 0
        self.ce = 0
        self.cv = []


    def getBestMut(self, c):
        tbe = self.optInit
        tbp = -1
        tbv = []
        for ii in range( len(c) ):
            c[ii] = 1 - c[ii]
            tv = self.decode(c)
            te = self.eval(tv)
            if self.cmp(te, self.tbe):
                tbe = te
                tbp = ii
                tbv = tv
            c[ii] = 1 - c[ii] #reset the change
        return(tbe, tbp, tbv)
        
    def solveStep(self):
        if self.repCurr >= self.repeats and self.doForever == 0:
            return()
        if self.candidate == None:
            self.repCurr += 1
            self.candidate = self.generateCandidate()
            self.cv = self.decode(self.candidate)
            self.ce = self.eval(self.cv)
        self.tbe, self.tbp, self.tbv = self.getBestMut(self.candidate)
        if self.cmp(self.tbe, self.ce):
            self.ce = self.tbe
            self.cv = self.tbv
            self.candidate[self.tbp] = 1 - self.candidate[self.tbp]
        else:
            if self.cmp(self.ce, self.be):
                self.be = self.ce
                self.bb = self.candidate[:]
                self.bv = self.cv
                self.bstep = self.evals
                self.br = self.repCurr
            self.candidate = None

class AlgorithmGa(AlgorithmBihc):
    def __init__(self, func, optimumIsMinimum = True, precision = 5, dimensions = 2, steps = 1, popSize = 100, genNo = 1000, genGrace = 200, pm = 0.01, pcx = 0.2, selPressure = 1, doForever = 0):
        super().__init__(func, optimumIsMinimum, precision, dimensions, steps, 0, doForever)
        self.popSize = popSize
        self.genNo = genNo
        self.repeats = self.genNo
        self.genGrace = genGrace
        self.genCurr = 0
        self.pm = pm
        self.pcx = pcx
        self.pop = None
        self.popV = None #population decoded values: X
        self.popE = None #population evaluated values: f(X)
        self.popF = None #population fitnesses
        self.genMin = math.inf
        self.genMax = -math.inf
        self.selPressure = selPressure

    def getName(self):
        return('Genetic Algorithm (Binary), popSize = ' + str(self.popSize) + ' pm = ' + str(self.pm) + ' pcx = ' + str(self.pcx) + ' selPressureExponent = ' + str(self.selPressure) )
                
    def restart(self):
        self.genCurr = 0
        self.repeats = self.genNo
        self.pop = None
        self.br = 0
        self.be = self.optInit #best eval
        self.bb = None #bitstring
        self.bv = []   #values
        self.bstep = 0 #at which eval did we achieve this best
        self.br = 0 #repeat when best was found
        self.exploredPoints = []
        self.evals = 0
        self.repCurr = 0
        
    def solveStep(self):
        if self.genCurr >= self.repeats:
            if self.br > self.genCurr - self.genGrace:
                self.repeats += self.genGrace
            elif self.doForever == 1:
                self.restart()
            else:
                return()
        self.genCurr += 1
        self.repCurr = self.genCurr
        if self.pop == None or len(self.pop) == 0:
            self.pop = self.generatePop()
        self.mutation()
        self.crossOver()
        self.evalPop()
        self.pop = self.selection()

    def evalPop(self):
        self.popV = []
        self.popE = []
        self.genMin = math.inf
        self.genMax = -math.inf
        for c in self.pop:
            v = self.decode(c)
            e = self.eval(v)
            if e < self.genMin:
                self.genMin = e
            if e > self.genMax:
                self.genMax = e
            if self.cmp(e, self.be):
                self.be = e
                self.bb = c
                self.bv = v
                self.bstep = self.evals
                self.br = self.genCurr
            self.popV.append(v)
            self.popE.append(e)
        
    def selection(self):
        evalDistance = self.genMax - self.genMin
        if evalDistance == 0:
            evalDistance = 1
        epsilon = evalDistance * 0.01
        div = evalDistance / 2
        newPop = []
        self.popF = []
        if len(self.pop) == 0:
            return([])
        for e in self.popE:
            if self.optimumIsMinimum:
                f = (self.genMax - e + epsilon) / div
            else:
                f = (e - self.genMin + epsilon)  / div
            f = math.pow(f, self.selPressure)
            self.popF.append(f)
        self.partialSums = [ self.popF[0] ]
        for ii in range(1, len(self.popF) ):
            self.partialSums.append(self.partialSums[ii - 1] + self.popF[ii])
        selectVal = []
        for _ in range(self.popSize):
            val = random.random() * self.partialSums[-1]
            selectVal.append(val)
        selectVal.sort()
        lookStart = 0
        for ii, ps in enumerate(self.partialSums):
            for jj in range( lookStart, len(selectVal) ):
                if selectVal[jj] < ps:
                    newPop.append(self.pop[ii])
                    lookStart += 1
                else:
                    break
        return(newPop)

    def crossOver(self):
        cxScore = []
        for ii in range( len(self.pop) ):
            cxScore.append([ii, random.random()])
        cxScore.sort( key = operator.itemgetter(1) )
        cxChosen = 0
        cxFlip = 0
        for ii, score in cxScore:
            if score < self.pcx:
                if cxFlip == 1:
                    self.pop.extend( self.crossChromosomes( self.pop[cxChosen], self.pop[ii] ) )
                    cxFlip = 0
                else:
                    cxChosen = ii
                    cxFlip = 1
            else:
                if cxFlip == 1:
                    if random.random() < 0.5:
                        self.pop.extend( self.crossChromosomes( self.pop[cxChosen], self.pop[ii] ) )
                break
        
    def crossChromosomes(self, c0, c1):
        pos = int( 1 + random.random() * (len(c0) - 2) )
        c01 = c0[:pos] + c1[pos:]
        c10 = c1[:pos] + c0[pos:]
        return(c01, c10)

    def mutation(self):
        for c in self.pop:
            self.mutateChromsome(c)
    
    def mutateChromsome(self, c):
        for ii, _ in enumerate(c):
            if random.random() < self.pm:
                c[ii] = 1 - c[ii]
            
    def generatePop(self):
        pop = []
        for _ in range(self.popSize):
            pop.append( self.generateCandidate() )
        return(pop)

class AlgorithmGaBihc(AlgorithmGa):
    def getName(self):
        return('Genetic Algorithm boostrapped with post-BIHC (Binary), popSize = ' + str(self.popSize) + ' pm = ' + str(self.pm) + ' pcx = ' + str(self.pcx) + ' selPressureExponent = ' + str(self.selPressure) )
                
    def solveStep(self):
        if self.genCurr >= self.repeats:
            if self.br > self.genCurr - self.genGrace:
                self.repeats += self.genGrace
            else:
                if self.bootstrapBihc():
                    return()#additional solutions are evaluated inside the bootstrap
                if self.doForever == 1:
                    self.restart()
                else:
                    return()
        self.genCurr += 1
        self.repCurr = self.genCurr
        if self.pop == None or len(self.pop) == 0:
            self.pop = self.generatePop()
        self.mutation()
        self.crossOver()
        self.evalPop()
        self.pop = self.selection()

    def bootstrapBihc(self): #TODO: divide into steps
        if hasattr(self, 'bootstrapIdx') == False:
            self.bootstrapIdx = 0
            self.repeats += len(self.pop)
        if self.bootstrapIdx >= len(self.pop):
            return(False)
        ii = self.bootstrapIdx
        improved = True
        #we're in the post-generational phase
        self.genCurr += 1
        while improved:
            improved = False
            te, tp, tv = self.getBestMut(self.pop[ii])
            if self.cmp(te, self.popE[ii]):
                improved = True
                self.pop[ii][tp] = 1 - self.pop[ii][tp]
                self.popE[ii] = te
                self.popV[ii] = tv
        if self.cmp(self.popE[ii], self.be):
            self.be = self.popE[ii]
            self.bb = self.pop[ii][:]
            self.bv = self.popV[ii]
            self.br = self.genCurr
        self.bootstrapIdx += 1
        return(True)

def solve_with_HC(params):
    return {'f_value': None}