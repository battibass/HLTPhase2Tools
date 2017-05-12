import FWCore.ParameterSet.Config as cms

RED    = "\033[1;31m"  
BLUE   = "\033[1;34m"
CYAN   = "\033[1;36m"
GREEN  = "\033[0;32m"
YELLOW = "\033[0;33m"
RESET  = "\033[0;0m"
BOLD   = "\033[;1m"

import sys

def printParams(process,label,params,nTab = 0) :
    
    if nTab == 0 :
        sys.stdout.write(GREEN)
    else :
        sys.stdout.write(YELLOW)
    print ("  "*nTab) + "   [" + label + "]"
    sys.stdout.write(BLUE)
    for parName, par in sorted(params.iteritems()) :
        if par.configTypeName() == "VPSet" :
            for parInVPset in par :
                printParams(process,parName,parInVPset.parameters_(),nTab+1)
        elif par.configTypeName() == "PSet" :
            printParams(process,parName,par.parameters_(),nTab+1)
        elif parName == "refToPSet_" :
            pSet = getattr(process,par.value())
            printParams(process,pSet.label(),pSet.parameters_(),nTab+1)        
        else :
            print ("  "*(nTab+1))," ",parName, "=", par
    if nTab == 0 :
        sys.stdout.write(GREEN)
    else :
        sys.stdout.write(YELLOW)
    print ("  "*nTab) + "   [" + label + "]"
    sys.stdout.write(BLUE)

def getParams(process, params, parType = "string") :

    getParameters = []

    for parName, par in sorted(params.iteritems()) :
        if par.configTypeName() == "VPSet" :
            for parInVPset in par :
                getParameters += getParams(process,parInVPset.parameters_(),parType)
        elif par.configTypeName() == "PSet" :
                getParameters += getParams(process,par.parameters_(),parType)
        elif parName == "refToPSet_" :
            pSet = getattr(process,par.value())
            getParameters += getParams(process,pSet.parameters_(),parType)
        elif par.configTypeName() == parType : 
            getParameters.append(par)

    return getParameters

def getParamNames(process, params, parType = "string") :

    getParameterNames = []

    for parName, par in sorted(params.iteritems()) :
        if par.configTypeName() == "VPSet" :
            for parInVPset in par :
                getParameterNames += getParamNames(process,parInVPset.parameters_(),parType)
        elif par.configTypeName() == "PSet" :
                getParameterNames += getParamNames(process,par.parameters_(),parType)
        elif parName == "refToPSet_" :
            pSet = getattr(process,par.value())
            getParameterNames += getParamNames(process,pSet.parameters_(),parType)
        elif par.configTypeName() == parType :
            getParameterNames.append(parName)

    return getParameterNames

def printObject(process,obj) :

    print
    printParams(process,obj.label_() + " == " + obj.type_(),obj.parameters_())
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

def guessEventSetup(process,params) :

    eventSetup = []

    for parName, par in sorted(params.iteritems()) :
        if par.configTypeName() == "VPSet" :
            for parInVPset in par :
                eventSetup.extend(guessEventSetup(process,parInVPset.parameters_()))
        elif par.configTypeName() == "PSet" :
                eventSetup.extend(guessEventSetup(process,par.parameters_()))
        elif par.configTypeName() == "string" and \
             par.value().find("ES") >= 0 :
            eventSetup.append(par.value())
        elif par.configTypeName() == "string" and len(par.value()) > 0 :
            for esProducer in process.es_producers_() :
                for esPar in getParams(process,process.es_producers_()[esProducer].parameters_()) :
                    if esPar == par.value() :
                        eventSetup.append(process.es_producers_()[esProducer].label_())
            for esSource in process.es_sources_() :
                for esPar in getParams(process,process.es_sources_()[esSource].parameters_()) :
                    if esPar == par.value() :
                        eventSetup.append(process.es_sources_()[esSource].label_())

    return eventSetup
            

def printSequence(process,seq,printObj=False) :

    inputTags = []
    eventSetups = []

    sys.stdout.write(RED)
    print "[" + seq.label_() + "]"
    sys.stdout.write(BLUE)
    
    for moduleName in str(seq).replace("+","*").split("*") :

        if process.producerNames().find(moduleName) >= 0 :

            inputTags.extend(guessInputTags(process.producers_()[moduleName].parameters_()))
            eventSetups.extend(guessEventSetup(process,process.producers_()[moduleName].parameters_()))
            print "  [EDProducer] :", moduleName, GREEN, \
                  "\ttype :", process.producers_()[moduleName].type_(), BLUE            
            continue



            inputTags.extend(guessInputTags(process.filters_()[moduleName].parameters_()))
            eventSetups.extend(guessEventSetup(process,process.filters_()[moduleName].parameters_()))
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

        for moduleName in str(seq).replace("+","*").split("*") :
            printObject(process,getattr(process,moduleName))

    sys.stdout.write(RED)
    print "\n[Printing guessed InputTags]"
    sys.stdout.write(GREEN)
    print set(inputTags)

    sys.stdout.write(RED)
    print "\n[Printing guessed ES dependencies]"
    sys.stdout.write(YELLOW)
    print set(eventSetups)

def findByType(process,typeName) :
    
    sys.stdout.write(RED)
    print "\n[Checking EDProducers]"
    sys.stdout.write(GREEN)

    for name, prod in process.producers_().iteritems() :
        if prod.type_() == typeName :
            print "  ", prod.label_()

    sys.stdout.write(RED)
    print "\n[Checking EDFilters]"
    sys.stdout.write(GREEN)

    for name, prod in process.filters_().iteritems() :
        if prod.type_() == typeName :
            print "  ", prod.label_()

    sys.stdout.write(RED)
    print "\n[Checking ESProducers]"
    sys.stdout.write(GREEN)

    for name, prod in process.es_producers_().iteritems() :
        if prod.type_() == typeName :
            print "  ", prod.label_()

    sys.stdout.write(RED)
    print "\n[Checking ESSources]"
    sys.stdout.write(GREEN)

    for name, prod in process.es_sources_().iteritems() :
        if prod.type_() == typeName :
            print "  ", prod.label_()


def findByParamValueObjs(process, objects, paramValue, parType = "string") :
    
    for name, prod in objects.iteritems() :
        params = getParams(process, prod.parameters_(), parType)
        
        for param in params :
            if param.value() == paramValue :    
                print "  ", prod.label_()


def findByParamValue(process, paramValue, parType = "string") :
               
    sys.stdout.write(RED)
    print "\n[Checking EDProducers]"
    sys.stdout.write(GREEN)

    findByParamValueObjs(process, process.producers_(), paramValue, parType)
    
    sys.stdout.write(RED)
    print "\n[Checking EDFilters]"
    sys.stdout.write(GREEN)

    findByParamValueObjs(process, process.filters_(), paramValue, parType)
    
    sys.stdout.write(RED)
    print "\n[Checking ESProducers]"
    sys.stdout.write(GREEN)

    findByParamValueObjs(process, process.es_producers_(), paramValue, parType)

    sys.stdout.write(RED)
    print "\n[Checking ESSources]"
    sys.stdout.write(GREEN)

    findByParamValueObjs(process, process.es_sources_(), paramValue, parType)

    
def findByParamNameObjs(process, objects, parName, parType = "string") :
    
    sys.stdout.write(GREEN)

    for name, prod in objects.iteritems() :
        paramNames = getParamNames(process, prod.parameters_(), parType)
        
        for paramName in paramNames :
            if paramName == parName :    
                print prod.label_()

def findByParamName(process,parName, parType = "string") :
               
    sys.stdout.write(RED)
    print "\n[Checking EDProducers]"
    sys.stdout.write(GREEN)

    findByParamNameObjs(process, process.producers_(), parName, parType)

    sys.stdout.write(RED)
    print "\n[Checking EDFilters]"
    sys.stdout.write(GREEN)

    findByParamNameObjs(process, process.filters_(), parName, parType)

    sys.stdout.write(RED)
    print "\n[Checking ESProducers]"
    sys.stdout.write(GREEN)
    
    findByParamNameObjs(process, process.es_producers_(), parName, parType)

    sys.stdout.write(RED)
    print "\n[Checking ESSources]"
    sys.stdout.write(GREEN)
    
    findByParamNameObjs(process, process.es_sources_(), parName, parType)

    
    
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
        


        
        

