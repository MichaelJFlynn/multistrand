# FD, Oct 20th, 2017. 
# This demonstrates the co-transcriptional folding.
import sys

from multistrand.objects import Complex, Domain, Strand, StopCondition
from multistrand.options import Options
from multistrand.system import SimSystem
from multistrand.utils import pairType
from multistrand.experiment import standardOptions, hybridization

from rawdata.readensemble import setArrParams

import time


def printTrajectory(o):
    
    seqstring = ""
    
    for i in range(len(o.full_trajectory)):
    
        time = 1e3 * o.full_trajectory_times[i]
        states = o.full_trajectory[i]
        
        ids = []
        newseqs = []
        structs = []
        dG = 0.0;
        
        pairTypes = []
        
        for state in states: 
            
            ids += [ str(state[2]) ]
            newseqs += [ state[3] ]  # extract the strand sequences in each complex (joined by "+" for multistranded complexes)
            structs += [ state[4] ]  # similarly extract the secondary structures for each complex
            dG += dG + state[5]
            
        newseqstring = ' '.join(newseqs)  # make a space-separated string of complexes, to represent the whole tube system sequence
        tubestruct = ' '.join(structs)  # give the dot-paren secondary structure for the whole test tube
                 
        
        if not newseqstring == seqstring : 
            print newseqstring
            seqstring = newseqstring  # because strand order can change upon association of dissociation, print it when it changes        

        print tubestruct + ('   t=%.6f ms,  dG=%3.2f kcal/mol  ' % (time, dG)) 

        

def doSims(strandSeq, numTraj=2):    



    curr = time.time()

    o1 = standardOptions(tempIn = 36.95)
    
    o1.num_simulations = numTraj
    o1.output_time = 0.0004# 0.2 ms output
    o1.simulation_time = 0.20 # 10 ms
    o1.gt_enable = 1;
    o1.substrate_type = Options.substrateRNA
    o1.simulation_mode = Options.trajectory
       
#     onedomain = Domain(name="itall", sequence="GGAACCGUCUCCCUCUGCCAAAAGGUAGAGGGAGAUGGAGCAUCUCUCUCUACGAAGCAGAGAGAGACGAAGG")    
#     onedomain = Domain(name="itall", sequence="GGAACCGTCTCCCTCTGCCAAAAGGTAGAGGGAGATGGAGCATCTCTCTCTACGAAGCAGAGAGAGACGAAGG")    
    onedomain = Domain(name="itall", sequence="GGAACCGTCTCCCTCTGCCAAAAGGTAGAGGGAGATGGAGCATCTCTCTCTACGAAGCAGAGAGAGACGAAGGGGAACCGTCTCCCTCTGCCAAAAGGTAGAGGGAGATGGAGCATCTCTCTCTACGAAGCAGAGAGAGACGAAGG")    
    top = Strand(name="top", domains=[onedomain])
    startTop = Complex(strands=[top], structure=".")
    o1.start_state = [startTop]

    setArrParams(o1,92)   

#     o1.initial_seed = 1777+6

    s = SimSystem(o1)
    s.start()
    printTrajectory(o1)     
    
    print "Exe time is " + str(time.time() - curr)   
        

    
# # The actual main method
if __name__ == '__main__':
    
    print sys.argv
    doSims( "GCGTTTCAC",1)
         
        
        

















