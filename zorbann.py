import math
import random

class ZorbaNN(object):
    

    #constructor int nl, std::vector<int> sz, double learn,double mom
    def __init__(self, nl = 0, sz = [], learn = 0.3, mom = 0.1):
        
        # le variabili vanno spostate dentro la init  https:#docs.python.org/2/tutorial/classes.html#class-and-instance-variables
        #private:
        
            #	output of neurons
        self.out = [[0.0 for x in range(2)] for y in range(2)]
    
        #	self.delta value
        self.delta = [[0.0 for x in range(2)] for y in range(2)]
    
        #	total self.layers number
        self.layers = 0
    
        #	vector of each layer's elements
        self.lsize =[0 for x in range(2)]
        
        #	vector of self.weights for each neuron
        self.weights = [[[0.0 for x in range(2)] for y in range(2)] for z in range(2)]
    
        #	self.weights of the previous iteration
        self.oldWeights = [[[0.0 for x in range(2)] for y in range(2)] for z in range(2)]
    
        #the self.population of chromosomes
        self.population = [[0.0 for x in range(2)] for y in range(2)]
    
        
        
        #public:
        self.actualMinError = 1000.0
        self.actualMaxError = 1001.0
    
        #would you like to view self.weights (this will slow all the training)
        self.viewweights =  False;
        self.fileviewweights = ''
    
        #	learning rate
        self.learningRate = 0.3
        
        #	self.momentum parameter
        self.momentum = 0.1
    
        #the error should not be too much little (at least in comparison with the result we want)
        self.minAcceptableError = math.pow(10,-2);
    
    
        #probability of a mutation
        self.mutationRate = 0.6

        #probability of a crossover
        self.crossoverRate = 0.7
    
        #number of self.population members (equal to chromosomes number)
        self.MAXpopulation = 15
    
    
        #da qui comicnia la procedura di costruzione della classe
        self.learningRate = learn
        self.momentum = mom
        #self.layers = nl
        self.layers = len(sz)

        #resizing vectors
        #self.lsize.resize(self.layers);

        #for(int i=0;i<self.layers;i++){
        #    self.lsize[i] = sz[i]
        #}
        self.lsize = sz

        self.resizeVectors()

        #generate new self.weights
        self.generateWeights()


    
    def resizeVectors(self):
        #global self.layers
        #global self.lsize
        #global MAXself.population
        
        #std::vector<std::vector<double> > self.out;
        self.out = [0.0 for x in range(self.layers)]
        for i in range(self.layers):
            self.out[i] = [0.0 for x in range(self.lsize[i])]

        #std::vector<std::vector<double> > self.delta;
        self.delta = [0.0 for x in range(self.layers)]
        for i in range(self.layers):
            self.delta[i] = [0.0 for x in range(self.lsize[i])]

        #std::vector<std::vector<std::vector<double> > > self.weights;
        self.weights = [0.0 for x in range(self.layers)]
        for i in range(len(self.weights)):
            self.weights[i] = [0.0 for y in range(self.lsize[i])]
            for j in range(self.lsize[i]):
                if (self.lsize[i-1]+1 > 0): self.weights[i][j] = [0.0 for y in range(self.lsize[i-1]+1)]
                if (self.lsize[i-1]+1 <= 0): self.weights[i][j] = [0.0 for y in range(1)]
    
        #std::vector<std::vector<std::vector<double> > > self.oldWeights;
        self.oldWeights = [0.0 for x in range(self.layers)]
        for i in range(len(self.oldWeights)):
            self.oldWeights[i] = [0.0 for y in range(self.lsize[i])]
            for j in range(self.lsize[i]):
                if (self.lsize[i-1]+1 > 0): self.oldWeights[i][j] = [0.0 for y in range(self.lsize[i-1]+1)]
                if (self.lsize[i-1]+1 <= 0): self.oldWeights[i][j] = [0.0 for y in range(1)]
    
        length = 0  #total self.weights number
        for i in range(len(self.weights)):
            for j in range(self.lsize[i]):
                for k in range(self.lsize[i-1]+1):
                    length = length + 1
    
        self.population = [[0.0 for x in range(self.MAXpopulation)] for y in range(length+1)]
        #self.population = [[0.0 for x in range(self.MAXpopulation+1)] for y in range(length+1)]



    #generate initial self.weights
    def generateWeights(self):
        #global self.layers
        #global self.lsize
        #global self.weights

        #	calculate random self.weights
        for i in range(self.layers):
            for j in range(self.lsize[i]):
                for k in range(self.lsize[i-1]+1):
                    self.weights[i][j][k] = random.uniform(0.0, 1.0)
                    
        #	initialize old self.weights to 0
        for i in range(self.layers):
            for j in range(self.lsize[i]):
                for k in range(self.lsize[i-1]+1):
                    self.oldWeights[i][j][k] = 0.0



    
    #	sigmoid function
    
    def sigmoid(self, d = 1.0):
        return (1/(1+math.exp(-d)))

    def getWeight(self, i = 0, j = 0, k = 0):
        #global self.weights
        return self.weights[i][j][k]

    #	calculate root mean square error of the actual self.weights
    def rmsError(self, wanted = 0.0):
        #global self.out
        #global self.layers
        #global self.lsize
        
        #root mean square
        Error = 0.0
        for i in range(self.lsize[self.layers-1]):
            Error += math.pow((wanted-self.out[self.layers-1][i]), 2)

        return math.pow((Error/self.lsize[self.layers-1]),0.5);


    #	return content of self.out vector
    def output(self, i = 0):
        ##global self.out
        ##global self.layers
        return self.out[self.layers-1][i]


    # feed forward
    def runNet(self, inputarr = []):
        sum = 0.0
        i = 0
        #self.weights = [[[-5.846174],[-5.738041],[6.805966]],[[-5.940364],[-6.734592],[0.513172]],[[-6.500991],[-5.154499],[4.425203]],[[-0.365688],[-6.146828],[4.540907]],[[13.589394],[6.756695],[-7.841028]]]
        
        for i in range(self.lsize[0]):
            self.out[0][i]=inputarr[i]
    
        # i = current layer, j= current neuron, k = current input = number of neurons in the preceeding layer
        # k'th input of j'th neuron in i'th layer
        for i in range(1,self.layers):
            for j in range(self.lsize[i]):
                sum = 0.0
                for k in range(self.lsize[i-1]):
                    sum += self.out[i-1][k]*self.weights[i][j][k]
                sum += self.weights[i][j][self.lsize[i-1]]
                self.out[i][j] = self.sigmoid(sum)
    
    

    def trainBackProp(self, inputarr = [], wanted = 0.0):
        sum = 0.0
        i = 0

        self.runNet(inputarr)

        #	calculate self.delta
        for i in range(self.lsize[self.layers-1]):
            self.delta[self.layers-1][i] = self.out[self.layers-1][i]*(1-self.out[self.layers-1][i])*(wanted-self.out[self.layers-1][i])
        
#        print list(reversed(range(1,self.layers-2)))
        for i in list(reversed(range(1,self.layers-1))):
            for j in range(self.lsize[i]):
                sum = 0.0
                for k in range(self.lsize[i+1]):
                    sum+=self.delta[i+1][k]*self.weights[i+1][k][j]
                self.delta[i][j] = self.out[i][j]*(1-self.out[i][j])*sum

        # considering self.momentum        
        for i in range(1,self.layers):
            for j in range(self.lsize[i]):
                for k in range(self.lsize[i-1]):
                    self.weights[i][j][k]+=self.momentum*self.oldWeights[i][j][k]
                    #if (viewweights) saveWeights(fileviewweights);
                self.weights[i][j][self.lsize[i-1]]+=self.momentum*self.oldWeights[i][j][self.lsize[i-1]]
        
        # considering learning rate
        for i in range(1,self.layers):
            for j in range(self.lsize[i]):
                for k in range(self.lsize[i-1]):
                    self.oldWeights[i][j][k]=self.learningRate*self.delta[i][j]*self.out[i-1][k]
                    self.weights[i][j][k]+=self.oldWeights[i][j][k]
                self.oldWeights[i][j][self.lsize[i-1]]=self.learningRate*self.delta[i][j]
                self.weights[i][j][self.lsize[i-1]]+=self.oldWeights[i][j][self.lsize[i-1]]


    def recursiveTrainBackProp(self, data = [], maxIters = 2000):
        i = 0
        j = len(data)
        t = len(data[0]) -1
        
        for i in range(maxIters):
            #print data[i%j][:2]
            #print "$"
            #print data[i%j][t]
            #print "\n"
            #self.trainBackProp(data[i%j][:2], data[i%j][t])
            self.trainBackProp(data[i%j], data[i%j][t])
#            print self.rmsError(data[(i-1)%j][t])
            #TODO is it possible to show somewhere the actual self.weights?
            #if (viewweights) saveWeights(fileviewweights);
        #std::cself.out << std::endl << i << " iterations completed with back propagation "   << "Mean Error: " << rmsError(data[(i-1)%j][t]) << std::endl;

    #this function will take a standard zorbaneural weights file to fill the weights vector
    def setWeights(self, filec = ""):
        texto = ""
        text_file = open(filec, "r")
        texto = text_file.read()
        text_file.close()
        
        #tmpchr = ""
        tempval = ""
        inn = 1
        jn = 0
        tn = 0
        if texto != "" :
            for tmpchr in texto:
                if tmpchr!='|' and tmpchr!='&' and tmpchr!='$' :
                    tempval = tempval + str(tmpchr)
                if tmpchr=='|' :
                    tempnum =  float(tempval)
                    self.weights[inn][jn][tn] = tempnum
                    tn+=1
                    tempval = ""
                if tmpchr=='&' :
                    tn=0
                    jn+=1
                if tmpchr=='$' :
                    jn=0
                    tn=0
                    inn+=1
    

    #this function will create a standard zorbaneural weights file
    def saveWeights(self, filec = ""):
        endval = ""
        for i in range(1,self.layers):
            for j in range(self.lsize[i]):
                for k in range(self.lsize[i-1]):
                    endval+=str(self.weights[i][j][k])
                    endval+="|"
                endval += "&\n"
            endval += "$\n"
        if filec != "":
            text_file = open(filec, "w")
            text_file.write(endval)
            text_file.close()
        else:
            return endval

#this function will take a standard zorbaneural weights file to fill the oldWeights vector
    def setOldWeights(self, filec = ""):
        texto = ""
        text_file = open(filec, "r")
        texto = text_file.read()
        text_file.close()
        
        #tmpchr = ""
        tempval = ""
        inn = 1
        jn = 0
        tn = 0
        if texto != "" :
            for tmpchr in texto:
                if tmpchr!='|' and tmpchr!='&' and tmpchr!='$' :
                    tempval = tempval + str(tmpchr)
                if tmpchr=='|' :
                    tempnum =  float(tempval)
                    self.oldWeights[inn][jn][tn] = tempnum
                    tn+=1
                    tempval = ""
                if tmpchr=='&' :
                    tn=0
                    jn+=1
                if tmpchr=='$' :
                    jn=0
                    tn=0
                    inn+=1


#this function will create a standard zorbaneural oldWeights file
    def saveOldWeights(self, filec = ""):
        endval = ""
        for i in range(1,self.layers):
            for j in range(self.lsize[i]):
                for k in range(self.lsize[i-1]):
                    endval+=str(self.oldWeights[i][j][k])
                    endval+="|"
                endval += "&\n"
            endval += "$\n"
        if filec != "":
            text_file = open(filec, "w")
            text_file.write(endval)
            text_file.close()
        else:
            return endval


 
#this function will fill the population vector
    def setPopulation(self, filec = ""):
        texto = ""
        text_file = open(filec, "r")
        texto = text_file.read()
        text_file.close()
        
        #tmpchr = ""
        tempval = ""
        inn = 1
        jn = 0
        tn = 0
        if texto != "" :
            for tmpchr in texto:
                if tmpchr!='|' and tmpchr!='&' :
                    tempval = tempval + str(tmpchr)
                if tmpchr=='|' :
                    tempnum =  float(tempval)
                    if inn < len(self.population) and jn <len(self.population[0]):
                        self.population[inn][jn] = tempnum
                    jn+=1
                    tempval = ""
                if tmpchr=='&' :
                    jn=0
                    inn+=1
        #print self.population



#this function will create a standard zorbaneural population file
    def savePopulation(self, filec = ""):
        length = 0  #total self.weights number
        for i in range(len(self.weights)):
            for j in range(self.lsize[i]):
                for k in range(self.lsize[i-1]+1):
                    length = length + 1
        
        endval = ""
        for t in range(self.MAXpopulation):
            for n in range(length+1):
                if t < len(self.population) and n <len(self.population[0]):
                    endval+=str(self.population[t][n])
                    endval+="|"
            endval += "&\n"
        if filec != "":
            text_file = open(filec, "w")
            text_file.write(endval)
            text_file.close()
        else:
            return endval


#this function will load the entire network
    def setNetwork(self, filec = ""):
        
        tmpweights = filec[:-4] + "-weights.zwf"
        tmpold = filec[:-4] + "-oldweights.zwf"
        tmppop = filec[:-4] + "-population.zpf"
        
        texto = ""
        text_file = open(filec, "r")
        texto = text_file.read()
        text_file.close()
        
        #tmpchr = ""
        tempval = ""
        inn = 0
        #jn = 0
        cont = 0
        if texto != "" :
            for tmpchr in texto:
                if tmpchr!='|' and tmpchr!='&' :
                    tempval = tempval + str(tmpchr)
                if tmpchr=='|' :
                    tempnum =  float(tempval)
                    if cont == 0:
                        self.layers = int(tempnum)
                        self.lsize =[0 for x in range(int(tempnum))]
                    if cont == 1: self.MAXpopulation = int(tempnum)
                    if cont == 2: self.learningRate = tempnum
                    if cont == 3: self.momentum = tempnum
                    if cont == 4: self.actualMinError = tempnum
                    if cont == 5: self.actualMaxError = tempnum
                    if cont == 6: self.minAcceptableError = tempnum
                    if cont == 7: self.mutationRate = tempnum
                    if cont == 8: self.crossoverRate = tempnum
                    if cont == 9:
                        self.lsize[inn] = int(tempnum)
                        inn+=1
                    tempval = ""
                if tmpchr=='&' :
                    cont+=1
        self.resizeVectors()
        self.setPopulation(tmppop)
        self.setWeights(tmpweights)
        self.setOldWeights(tmpold)
        #print self.population
        

#this function will save the entire network
    def saveNetwork(self, filec = ""):
        tmpweights = filec[:-4] + "-weights.zwf"
        tmpold = filec[:-4] + "-oldweights.zwf"
        tmppop = filec[:-4] + "-population.zpf"
        
        self.savePopulation(tmppop)
        self.saveWeights(tmpweights)
        self.saveOldWeights(tmpold)
        
        endval = ""
        
        endval = endval + str(self.layers) + "|"
        endval = endval + "&\n"

        endval = endval + str(self.MAXpopulation) + "|"
        endval = endval + "&\n"

        endval = endval + str(self.learningRate) + "|"
        endval = endval + "&\n"
    
        endval = endval + str(self.momentum) + "|"
        endval = endval + "&\n"
    
        endval = endval + str(self.actualMinError) + "|"
        endval = endval + "&\n"
    
        endval = endval + str(self.actualMaxError) + "|"
        endval = endval + "&\n"
    
        endval = endval + str(self.minAcceptableError) + "|"
        endval = endval + "&\n"
    
        endval = endval + str(self.mutationRate) + "|"
        endval = endval + "&\n"
    
        endval = endval + str(self.crossoverRate) + "|"
        endval = endval + "&\n"
        
        for t in range(len(self.lsize)):
            endval+=str(self.lsize[t])
            endval+="|"
        endval += "&\n"
        
        if filec != "":
            text_file = open(filec, "w")
            text_file.write(endval)
            text_file.close()
        else:
            return endval
