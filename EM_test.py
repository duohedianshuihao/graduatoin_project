import math  
import copy  
import numpy as np  
import matplotlib.animation as animationuibl

def ini_data(Sigma,Mu1,Mu2,k,N):  
    global X  
    global Mu  
    global Expectations  
    X = np.zeros((1,N))                     # Add 1*N zeros                          
    Mu = np.random.random(2)                # Add two random number between [0,1)
    Expectations = np.zeros((N,k))          # Add N*k zeros
    for i in xrange(0,N):                   # Generate a random array in Gaussian distribution. expand 6 and add 20 or 40
        if np.random.random()>0.5 :
            X[0,i] = np.random.normal()*Sigma + Mu1   # random.normal() - Generate a (0,1)Gaussian distribution
        else:  
            X[0,i] = np.random.normal()*Sigma + Mu2   # Mu1 = 40, Mu2 = 20
    print X

def e_step(Sigma,k,N):  
    global Expectations  
    global Mu  
    global X  
    for i in xrange(0,N):           # Calculate the Expectations, when X[i] occur, which X[i ; k] belong to Z[k] distribution   
        Denom = 0  
        for j in xrange(0,k):       
            Denom += math.exp((-1/(2*(float(Sigma**2))))*(float(X[0,i]-Mu[j]))**2) # thought Z belong to Gaussian
        for j in xrange(0,k):                                                      # actually Z belong to two different Gaussian
            Numer = math.exp((-1/(2*(float(Sigma**2))))*(float(X[0,i]-Mu[j]))**2)  
            Expectations[i,j] = Numer / Denom  

def m_step(k,N):  
    global Expectations  
    global X  
    for j in xrange(0,k):  
        Numer = 0  
        Denom = 0  
        for i in xrange(0,N):  
            Numer += Expectations[i,j]*X[0,i]  
            Denom += Expectations[i,j]          
        Mu[j] = Numer / Denom   

def main(Sigma,Mu1,Mu2,k,N,iter_num,Epsilon):  
    ini_data(Sigma,Mu1,Mu2,k,N)  
    for i in range(iter_num):  
        Old_Mu = copy.deepcopy(Mu)   # Mu is a two arguments array, so it has to use deepcopy, rather than copy  
        e_step(Sigma,k,N)  
        m_step(k,N)  
        print i
        if sum(abs(Mu-Old_Mu))< Epsilon: 
            print Expectations  
            print Mu
            break  

if __name__ == '__main__':
    main(6,40,20,2,10,1000,0.000001)    
