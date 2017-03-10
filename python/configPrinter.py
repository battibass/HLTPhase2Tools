import FWCore.ParameterSet.Config as cms

RED    = "\033[1;31m"  
BLUE   = "\033[1;34m"
CYAN   = "\033[1;36m"
GREEN  = "\033[0;32m"
YELLOW = "\033[0;33m"
RESET  = "\033[0;0m"
BOLD   = "\033[;1m"

import sys

def printParams(label,params,nTab = 0) :
    
    if nTab == 0 :
        sys.stdout.write(GREEN)
    else :
        sys.stdout.write(YELLOW)
    print ("  "*nTab) + "   [" + label + "]"
    sys.stdout.write(BLUE)
    for parName, par in sorted(params.iteritems()) :
        if par.configTypeName() == "VPSet" :
            for parInVPset in par :
                printParams(parName,parInVPset.parameters_(),nTab+1)
        elif par.configTypeName() == "PSet" :
                printParams(parName,par.parameters_(),nTab+1)
        else :
            print ("  "*(nTab+1))," ",parName, "=", par
    if nTab == 0 :
        sys.stdout.write(GREEN)
    else :
        sys.stdout.write(YELLOW)
    print ("  "*nTab) + "   [" + label + "]"
    sys.stdout.write(BLUE)


def printObject(obj) :

    print
    printParams(obj.label_(),obj.parameters_())
    print

def guessInputTags(params) :

    inputTags = []

    for parName, par in sorted(params.iteritems()) :
        if par.configTypeName() == "VPSet" :
            for parInVPset in par :
                inputTags.extend(guessInputTags(parInVPset.parameters_()))
        elif par.configTypeName() == "PSet" :
                inputTags.extend(guessInputTags(par.parameters_()))
        elif par.configTypeName() == "InputTag" :
            inputTags.append(par.value())

    return inputTags

def guessEventSetup(params) :

    eventSetup = []

    for parName, par in sorted(params.iteritems()) :
        if par.configTypeName() == "VPSet" :
            for parInVPset in par :
                eventSetup.extend(guessEventSetup(parInVPset.parameters_()))
        elif par.configTypeName() == "PSet" :
                eventSetup.extend(guessEventSetup(par.parameters_()))
        elif par.configTypeName() == "string" and \
             par.value().find("ES") >= 0 :
            eventSetup.append(par.value())

    return eventSetup

    
            

def printSequence(process,seq,printObj=False) :

    inputTags = []
    eventSetups = []

    sys.stdout.write(RED)
    print "[" + seq.label_() + "]"
    sys.stdout.write(BLUE)
    
    for moduleName in seq.moduleNames() :

        if process.producerNames().find(moduleName) >= 0 :

            inputTags.extend(guessInputTags(process.producers_()[moduleName].parameters_()))
            eventSetups.extend(guessEventSetup(process.producers_()[moduleName].parameters_()))
            print "  [EDProducer] :", moduleName, GREEN, \
                  "\ttype :", process.producers_()[moduleName].type_(), BLUE            
            continue


        if process.filterNames().find(moduleName) >= 0 :

            inputTags.extend(guessInputTags(process.filters_()[moduleName].parameters_()))
            eventSetups.extend(guessEventSetup(process.filters_()[moduleName].parameters_()))
            print "  [EDFilter] :", moduleName, GREEN, \
                  "\ttype :", process.filters_()[moduleName].type_(), BLUE
            continue

        for mySeq in process.sequences_() :

            if mySeq == moduleName :
                print "  [EDSequence] :", mySeq
                continue

        print "  [OTHER] :", moduleName

    sys.stdout.write(RED)
    print "[" + seq.label_() + "]"
    sys.stdout.write(BLUE)

    
    if printObj :

        sys.stdout.write(RED)
        print "\n[Printing sequence objects]"
        sys.stdout.write(BLUE)

        for moduleName in seq.moduleNames() :
            printObject(getattr(process,moduleName))

    sys.stdout.write(RED)
    print "\n[Printing guessed InputTags]"
    sys.stdout.write(GREEN)
    print inputTags

    sys.stdout.write(RED)
    print "\n[Printing guessed ES dependencies]"
    sys.stdout.write(YELLOW)
    print eventSetups


def compareParams(obj1,obj2,nTab = 0) :

    comparison = []
    
    paramNames = set(obj1.keys() + obj2.keys())

    for parName in paramNames :
        
        if obj1.has_key(parName) and \
           obj2.has_key(parName) :

            par1 = obj1[parName]
            par2 = obj2[parName]

            if par1.configTypeName() == "VPSet" :
                comparison.append((RESET + ("  "*nTab) + "   [" + parName + "] NO VPSET SUPPORT"))                                 
            #    for parInVPset in par :
            #        compareParams(parName,parInVPset.parameters_(),nTab+1)
            #el
            if par1.configTypeName() == "PSet" :
                comparison.extend(compareParams(par1.parameters_(),par2.parameters_(),nTab+1))
                comparison.append((CYAN + ("  "*nTab) + "   [" + parName + "]")) 
            else :
                if par1 == par2 :                                     
                    comparison.append((CYAN + ("  "*(nTab+1)) + " " + parName + "=" + str(par1)))
                else :
                    comparison.append((YELLOW + ("  "*(nTab+1)) + " " + parName + "has differences : "))
                    comparison.append((YELLOW + ("  "*(nTab+2)) + " " + str(par1)))
                    comparison.append((YELLOW + ("  "*(nTab+2)) + " " + str(par2)))

        elif obj1.has_key(parName) :

            par1 = obj1[parName]
            par2 = {}

            if par1.configTypeName() == "VPSet" :
                comparison.append((GREEN + ("  "*nTab) + "   [" + parName + "] NO VPSET SUPPORT")) 

            #if par1.configTypeName() == "VPSet" :
            #    for parInVPset in par :
            #        compareParams(parName,parInVPset.parameters_(),nTab+1)
            #el
            if par1.configTypeName() == "PSet" :
                comparison.append((GREEN + ("  "*nTab) + "   [" + parName + "]")) 
                comparison.extend(compareParams(par1.parameters_(),par2,nTab+1))
                comparison.append((GREEN + ("  "*nTab) + "   [" + parName + "]")) 
            else :
                comparison.append((GREEN+ ("  "*(nTab+1)) + " " + parName +  "=" + str(par1)))

        else :

            par1 = {}
            par2 = obj2[parName]
            
            if par2.configTypeName() == "VPSet" :
                comparison.append((RED + ("  "*nTab) + "   [" + parName + "] NO VPSET SUPPORT")) 
                
                
#if par1.configTypeName() == "VPSet" :
            #    for parInVPset in par :
            #        compareParams(parName,parInVPset.parameters_(),nTab+1)
            #el
            if par2.configTypeName() == "PSet" :
                comparison.append((RED + ("  "*nTab) + "   [" + parName + "]")) 
                comparison.extend(compareParams(par1,par2parameters_(),nTab+1))
                comparison.append((RED + ("  "*nTab) + "   [" + parName + "]")) 
            else :
                comparison.append((RED+ ("  "*(nTab+1)) + " " + parName + "=" + str(par2)))

    return comparison


def compareObjects(obj1,obj2) :

    print
    sys.stdout.write(BLUE)
    print "   [" + obj1.label_()+ " vs " + obj2.label_() +"]"
    for line in compareParams(obj1.parameters_(),obj2.parameters_()) :
        print line
    sys.stdout.write(BLUE)
    print "   [" + obj1.label_()+ " vs " + obj2.label_() +"]"
    print
        


        
        

