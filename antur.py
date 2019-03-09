#!/usr/bin/env python
# ----------------------------------------------------------------
# ANTUR: PAWs to DAAD Transcompiler
# Copyright (C) 2019 Stefan Vogt, Pond Soft.
# http://8bitgames.itch.io
#
# This source code is licensed under the BSD 2-Clause License.
# ----------------------------------------------------------------

__author__ = "Stefan Vogt"
__version__ = "0.1.0"

import sys
import os.path
import re

# general 
def versionInfo():
    print("ANTUR | version:", __version__, "| Python 3")
    print("Copyright (C) 2019 Stefan Vogt, Pond Soft.")
    print("http://8bitgames.itch.io\n")

def synopsis():
    print("ANTUR - PAWs to DAAD Transcompiler")
    print("--> usage: antur.py input output -flag")
    print("--> release information: antur.py --version\n")
    print("input: Gilsoft PAWs (CP/M) .SCE file")
    print("output: DAAD v2 (DOS) .SCE file")
    print("flags: -e for English or -s for Spanish language\n")

# sections
voc = "/VOC" # vocabulary
stx = "/STX" # system messages
mtx = "/MTX" # message texts
otx = "/OTX" # object texts
ltx = "/LTX" # location texts
con = "/CON" # connections
obj = "/OBJ" # object definitions
pro = "/PRO" # process table
ant = "/ANT" # antur temp marker

header = "; DAAD syntax automatically generated with ANTUR\n\
; http://8bitgames.itch.io\n\
;\n"

divider = ";------------------------------------------------\
------------------------------\n"

gilsoftDiv = "\n; - - - - - - - - - - - - - - - - - - - - - -"

controlSection = "#include symbols.sce\n\
/CTL    ;Control Section (null char is an underline)\n\
_\n"

tokensEnglish = "/TOK    ;Tokens as supplied with PAW under CP/M\n_the_\n\
_you_\n_are_\ning_\n_to_\n_and\n_is_\nYou_\nand_\nThe_\nn't_\n_of_\n_you\n\
ing\ned_\n_a_\n_op\nith\nout\nent\n_to\n_in\nall\n_th\n_it\nter\nave\n_be\n\
ver\nher\nand\near\nYou\n_on\nen_\nose\nno\nic\nap\n_b\ngh\n__\nad\nis\n_c\n\
ir\nay\nur\nun\noo\n_d\nlo\nro\nac\nse\nri\nli\nti\nom\nbl\nck\nI_\ned\nee\n\
_f\nha\npe\ne_\nt_\nin\ns_\nth\n,_\ner\nd_\non\nto\nan\nar\nen\nou\nor\nst\n\
._\now\nle\nat\nal\nre\ny_\nch\nam\nel\n_w\nas\nes\nit\n_s\nll\ndo\nop\nsh\n\
me\nhe\nbo\nhi\nca\npl\nil\ncl\n_a\nof\n_h\ntt\nmo\nke\nve\nso\ne.\nd.\nt.\n\
vi\nly\nid\nsc\n_p\nem\nr_\n"

tokensSpanish = "/TOK\n_____\n_que_\na_de_\no_de_\n_una_\n_del_\ns_de_\n\
_de_l\n_con_\nente_\n_por_\n_está\ntiene\ns_un_\nante_\n_para\n_las_\nentra\n\
n_el_\ne_de_\na_la_\nerior\nción_\nando_\niente\n_el_\n_la_\n_de_\n_con\n\
_en_\nlos_\nado_\n_se_\nesta\n_un_\nlas_\nenta\n_des\n_al_\nada_\nas_\nes_\n\
os_\n_y_\nado\n11te_\nada\nla_\nen1t\nres\nque\nan_\no_p\nrec\nido\ns,_\nant\n\
ina\nida\nlar\nero\nmpl\na_\no_\ner\nes\nor\nar\nal\nen\nas\nos\ne_\nan\nel\n\
on\nin\nci\nun\n._\nco\nre\ndi\n,_\nur\ntr\nde\nsu\nab\nol\nam\nst\ncu\ns_\n\
ac\nil\ngr\nad\nte\ny_\nim\nto\nue\npi\ngu\nch\nca\nla\nn_\nro\nri\nlo\nmi\n\
l_\nti\nob\nme\nsi\npe\n_n\ntu\nat\nfi\ndo\nem\nay\n\".\nll\n"

stxDiffEnglish = "/54 ;Letter for Tape\nT\n/55 ;Disc\nD\n\
/56\nDrive not ready - press any key to retry.\n\n/57\nI/O Error.\n\n\
/58\nDisc or Directory may be full.\n\n/59\nInvalid filename.\n\n\
/60\nType in name of file:\n/61\nStart tape.\n\n/62\nTape or Disc?\n"

stxDiffSpanish = "/54 ;Inicial de Cinta\nC\n/55 ;Disco\nD\n\
/56\nUnidad no preparada. Pulsa una tecla para volver a intentarlo.\n\n\
/57\nError de entrada/salida.\n\n/58\n\
El disco o el directorio puede estar lleno.\n\n/59\n\
Nombre de fichero no válido.\n\n/60\nNombre del fichero:\n/61\n\
Pon en marcha la cinta.\n\n/62\n¿Cinta o disco?\n"

stxWornEnglish = "/10\nYou are wearing:\n\n/11"

stxWornSpanish = "/10\nLlevas puesto:\n\n/11"

daadObjHeader = "\n;obj  starts  weight    c w  5 4 3 2 1 0 9 8 7 6 5 4 3 2 1 \
0    noun   adjective\n;num    at\n"

daadObjAttrib = "  _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _"

pro0to2English = "/PRO 0       ;Main Location Loop\n\n\
_       _       AT      0               ; Starting game\n\
                PROCESS 6               ; then we need init sequence\n\n\
_       _       WINDOW  0               ; Select graphics window\n\
                CLEAR   DarkF           ; Assume light\n\
                NOTZERO 0\n\
                ABSENT  0\n\
                SET     DarkF           ; Dark\n\n\
; This needs to be commented for text-only adventures\n\
; _       _       PICTURE [Player]        ; If there is a picture, Load it\n\
;                 DISPLAY [DarkF]         ; & Display it if not dark, else CLS\n\n\
_       _       WINDOW  1\n\
                NOTZERO DarkF           ; Dark\n\
                SYSMESS 0\n\n\
_       _       ZERO    DarkF\n\
                DESC    [Player]        ; Doesn't exit loop now\n\n\
_       _       PROCESS 3\n\n\
; Now we use Process 1 as the main code loop, a return from it is the end\n\
; of the game\n\n\
_       _       PROCESS 1\n\n\
;------------------------------------------------------------------------------\n\
/PRO 1\n\
_       _       PROCESS 4               ; Do process 2 stuff here\n\n\
_       _       PARSE   0               ; Get next LS from current buffer\n\
                PROCESS 2               ; Failed cos of invalid or timeout\n\
                REDO\n\n\
_       _       EQ      Turns   255     ; Max for one byte\n\
                PLUS    Turns+1 1\n\
                CLEAR   Turns\n\
                SKIP    1\n\n\
_       _       PLUS    Turns   1\n\n\
_       _       PROCESS 5               ; Do any commands\n\
                ISDONE                  ; Done something\n\
                REDO\n\n\
_       _       MOVE    Player          ; No so try to move player\n\
                RESTART                 ; Absolute jump to start process 0\n\n\
_       _       NEWTEXT\n\
                LT      Verb    14\n\
                SYSMESS 7\n\
                REDO\n\n\
_       _       SYSMESS 8\n\
                REDO\n\n\
;------------------------------------------------------------------------------\n\
/PRO 2\n\
_       _       HASAT TIMEOUT\n\
                SYSMESS 35\n\
                DONE\n\n\
_       _       SYSMESS 6               ; I didn't understand\n\n\
;------------------------------------------------------------------------------\n"

pro3HeaderEnglish = "\
/PRO 3 ; Old process 1. Note that both the response table and the old PAW\n\
; process tables 1 and 2 can now be anywhere or completely absent. Everything\n\
; is implemented in the DAAD language itself.\n\n\
;This is better carried out than the old system without access to DarkF\n\
_       _       NEWLINE\n\
                ZERO    DarkF            ; Isn't dark\n\
                LISTOBJ\n"

pro6English = "/PRO 6 ; Initialise the DAAD system\n\n\
_       _       WINDOW  1               ; Windows are random\n\
_       _       WINAT   0       0       ; set 14 0 for split screen with GFX\n\
                WINSIZE 25      127     ; Maximum window\n\
                CLS\n\
                DESC    0               ; Introduction\n\
                ANYKEY\n\
                CLS\n\
                CLEAR   255             ; Clear all flags\n\n\
_       _       NOTEQ   255     GFlags\n\
                CLEAR   [255]\n\n\
_       _       PLUS    255     1\n\
                LT      255     255     ; Will be set at end to indicate init\n\
                SKIP    -2              ; BUGFIX: SKIP -1 was the original value\n\n\
_       _       RESET                   ; Set objects to start location & Flag 1\n\
                LET     Strength 10\n\
                LET     MaxCarr  4\n\
                SET     CPNoun\n\
                SET     CPAdject\n\
                GOTO    1               ; Main game\n\n"

daadInventory = "SYSMESS 9\n\
                LISTAT CARRIED\n\
                SYSMESS 10\n\
                LISTAT WORN\n"

# the format police is here!   
def spaceWarrior(dirtyString):
    # delete double empty newlines
    cleanString = re.sub(r"\n\s*\n", "\n\n", dirtyString)
    # nuke the awful trailing whitespace from John Wilson's files :D
    while " \n" in cleanString:
        cleanString = cleanString.replace(" \n", "\n")
    return cleanString

# changes PROCESS CondActs from old value to relocated table 
def condActCop(pawsProcesses, conDict):
    for k, v in conDict.items():
            pawsProcesses = pawsProcesses.replace(k, v)
    return pawsProcesses

# parsing and conversion
def transcompile(defaultLang):
    # read PAWs input file
    pawsFile = open(sys.argv[1], "r", encoding = "CP437")
    pawsData = pawsFile.read()
    # clean CP/M paws dividers from source file
    pawsData = pawsData.replace(gilsoftDiv, "")
    # write DAAD output file
    daadFile = open(sys.argv[2], "w", encoding = "CP437")
    daadFile.write(header) # header
    daadFile.write(controlSection) # controlSection
    # default language is English, check if Spanish flag provided
    if defaultLang is False:
        daadFile.write(tokensSpanish) # tokens
    else:
        daadFile.write(tokensEnglish) # tokens
    # vocabulary 
    vocStart, vocEnd = pawsData.find("/VOC"), pawsData.find("/STX")
    vocabulary = voc + (pawsData[vocStart+4:vocEnd])
    vocabulary = re.sub(r"^$\n", "", vocabulary, flags=re.MULTILINE)
    daadFile.write(vocabulary)
    # system messages: import whole section from PAWs file
    stxStart, stxEnd = pawsData.find("/STX"), pawsData.find("/MTX")
    stxTemp = stx + (pawsData[stxStart+4:stxEnd]) + ant
    # replace PAW's standard (worn) message with DAAD"s equivalent
    if defaultLang is False:
        stxContent = re.sub("/10.*?/11", stxWornSpanish, stxTemp, flags=re.DOTALL)
    else:
        stxContent = re.sub("/10.*?/11", stxWornEnglish, stxTemp, flags=re.DOTALL)
    # replace 54-62 with DAAD"s mandatory messages
    if defaultLang is False:
        sysmes1 = re.sub("/54.*?/ANT", stxDiffSpanish, stxContent, flags=re.DOTALL)
    else:
        sysmes1 = re.sub("/54.*?/ANT", stxDiffEnglish, stxContent, flags=re.DOTALL)
    # get messages above 62 if there are any
    if "/63" in stxContent:
        stxStart, stxEnd = stxContent.find("/63"), stxContent.find("/ANT")
        sysmes2 = "/63\n" + (stxContent[stxStart+4:stxEnd])
    # write first segment of system messages
    daadFile.write(sysmes1)
    # write second segment if there are messages above 62
    if "/63" in stxContent:
        daadFile.write(sysmes2)
    # message texts, object texts, location texts and connections are
    # identical to PAWs syntax, so we copy them in one block from source
    blockStart, blockEnd = pawsData.find("/MTX"), pawsData.find("/OBJ")
    block = mtx + (pawsData[blockStart+4:blockEnd])
    # write block to file
    daadFile.write(block)
    # object definitions: import whole block
    objStart, objEnd = pawsData.find("/OBJ"), pawsData.find("/PRO 0")
    objectDef = (pawsData[objStart+4:objEnd]) + ant
    # create object definition chunck
    objStart, objEnd = objectDef.find("/0"), objectDef.find("/ANT")
    objects = "/0 " + (objectDef[objStart+2:objEnd])
    # move any comments into a new line
    objects = objects.replace(";", "\n;")
    # replace tabs in object definitions with spaces (if existing)
    objects = objects.replace("\t", " ")
    # delete empty newlines and unnecessary whitespace
    objects = re.sub(r"^$\n", "", objects, flags=re.MULTILINE)
    objects = re.sub(" +", " ", objects)
    objects = objects.replace(" \n", "\n")
    # split objects (by line) into list, (True) keeps trailing newline
    objList = objects.splitlines(True)
    # remove any comments
    objList = [x for x in objList if not ";" in x]
    # join list into new string, only to split it again at whitespace
    objects = "".join(objList)
    objList = objects.split()
    # add newline control char after every 7th item in list
    objList[6::7] = [item + "\n" for item in objList[6::7]]
    # insert tab after every object number definition
    objList[0::7] = [item + "\t" for item in objList[0::7]]
    # append tab after each start location
    objList[1::7] = [item + "\t" for item in objList[1::7]]
    # iterate tab insertion after each object weight
    objList[2::7] = [item + "\t" for item in objList[2::7]]
    # place whitespace after container flags
    objList[3::7] = [item + " " for item in objList[3::7]]
    # insert DAAD's per-object attributes after wearable flags
    objList[4::7] = [item + daadObjAttrib +"\t" for item in objList[4::7]]
    # append tab after object nouns
    objList[5::7] = [item +"\t" for item in objList[5::7]]
    # create objects from properly reformatted list
    objects = "".join(objList)
    # write object definitions in DAAD syntax to file
    daadFile.write(obj)
    daadFile.write(daadObjHeader)
    daadFile.write(objects)
    # process tables: create intial DAAD process structure
    daadPROs = divider + pro0to2English + pro3HeaderEnglish
    # this goes first: get tables above PRO 2 (if existing) and relocate them
    if "/PRO 3" in pawsData:
        proStart, proEnd = pawsData.find("/PRO 3"), pawsData.find("/ANT")
        relocData = "/PRO 3" + (pawsData[proStart+6:proEnd])
        # count existing process tables higher than PRO 2
        occurence = sum(1 for _ in re.finditer
        (r'\b%s\b' % re.escape("PRO"), relocData))
        # create dicitionaries for contents to relocate
        mapping = {}
        condActs = {}
        # count down loop from last table in source file
        for count in range(occurence, 0, -1):
            pawsInt = count + 2 # actual PAWs process table number
            relocInt = count + 6 # relocate to DAAD process table number
            # merge to strings for table definitions
            pawsTable = "/PRO " + str(pawsInt) + "\n"
            daadTable = divider + "/PRO " + str(relocInt) + "\n"
            # create strings for PROCESS ConAct relocation
            pawsCondAct = "PROCESS " + str(pawsInt) +"\n"
            daadCondAct = "PROCESS " + str(relocInt) +"\n"
            # add created key pairs to dictionaries
            mapping[pawsTable] = daadTable
            condActs[pawsCondAct] = daadCondAct
        # loop until all process table definitions are relocated
        for k, v in mapping.items():
            relocData = relocData.replace(k, v)
        # call condActCop to update PROCESS values to relocated tables
        relocData = spaceWarrior(relocData)
        relocData = condActCop(relocData, condActs)
    # get PRO 1 content and place it in DAAD's PRO 3 
    proStart, proEnd = pawsData.find("/PRO 1"), pawsData.find("/PRO 2")
    proContent = (pawsData[proStart+6:proEnd])
    if "/PRO 3" in pawsData: # let condActCop update the PROCESS entries
        proContent = spaceWarrior(proContent)
        proContent = condActCop(proContent, condActs)
    # add newly generated content to process structure
    daadPROs = daadPROs + proContent + divider
    # get PRO 2 content and adapt it in DAAD's PRO 4
    if "/PRO 3" in pawsData:
        # in case there is more than the standard amount of tables defined 
        proStart, proEnd = pawsData.find("/PRO 2"), pawsData.find("/PRO 3")
        proContent = (pawsData[proStart+6:proEnd])
        # make sure process CondActs are properly updated, too
        proContent = spaceWarrior(proContent)
        proContent = condActCop(proContent, condActs)
    else:
        # if it's just the standard tables...
        proStart, proEnd = pawsData.find("/PRO 2"), pawsData.find("/ANT")
        proContent = (pawsData[proStart+6:proEnd])
    # adapt PRO 2 content to DAAD's PRO 4 table
    daadPROs = daadPROs + "/PRO 4 ; Old process 2" + proContent + divider
    # import response table aka PRO 0 in PRO 5 command decoder
    proStart, proEnd = pawsData.find("/PRO 0"), pawsData.find("/PRO 1")
    proContent = (pawsData[proStart+6:proEnd])
    if "/PRO 3" in pawsData: # once again, let condActCop do it's thing
        proContent = spaceWarrior(proContent)
        proContent = condActCop(proContent, condActs)
    # add process table data in memory
    daadPROs = daadPROs + "/PRO 5 ; Command decoder" + proContent
    # add DAAD's PRO 6 to the data in memory
    daadPROs = daadPROs + divider + pro6English
    # finally(!) add any relocated process tables to data in memory
    if "/PRO 3" in pawsData:
        daadPROs = daadPROs + relocData
    # send string over to the format police 
    daadPROs = spaceWarrior(daadPROs)
    # split string in memory into single lines
    daadPROList = daadPROs.splitlines(True)
    # refactor TIMEOUT CondAct to DAAD's "HASAT TIMEOUT" symbol
    daadPROList = [w.replace('TIMEOUT', 'HASAT TIMEOUT') for w in daadPROList]
    daadPROList = [w.replace('HASAT HASAT', 'HASAT') for w in daadPROList]
    # change PROMPT CondAct to DAAD's "LET Prompt" symbol
    daadPROList = [w.replace('PROMPT', 'LET Prompt') for w in daadPROList]
    # DESC now needs locno. argument, DAAD's RESTART CondAct is what we need
    daadPROList = [w.replace('DESC\n', 'RESTART\n') for w in daadPROList]
    # PARSE needs a parameter in DAAD, so duplicate PAW's behavior
    daadPROList = [w.replace('PARSE\n', 'PARSE 1\n') for w in daadPROList]
    # SAVE and LOAD in DAAD need an argument so we will provide it
    daadPROList = [w.replace('SAVE\n', 'SAVE 0\n\t\tRESTART\n') for w in daadPROList]
    daadPROList = [w.replace('LOAD\n', 'LOAD 0\n\t\tRESTART\n') for w in daadPROList]
    # the RAMSAVE CondAct, unlike in PAWs, doesn't take any arguments
    daadPROList = [w.replace('RAMSAVE 0', 'RAMSAVE') for w in daadPROList]
    # since INVEN CondAct is gone, recreate the functionality
    daadPROList = [w.replace('INVEN\n', daadInventory) for w in daadPROList]
    # TURNS CondAct is wiped in DAAD but we can recreate a basic output like this
    daadPROList = [w.replace('TURNS\n', "PRINT Turns\n") for w in daadPROList]
    # even SCORE is gone but there is a symbol now leading to flag 30
    daadPROList = [w.replace('SCORE\n', "PRINT Score\n") for w in daadPROList]
    # join process table data lines to new string
    daadPROs = "".join(daadPROList)
    # write DAAD process table data to output file
    daadFile.write(daadPROs)
    # end file operations
    pawsFile.close()
    daadFile.close()
    if defaultLang is False:
        print("\nFile:", sys.argv[2], "successfully compiled using Spanish language.")
    else:
        print("\nFile:", sys.argv[2], "successfully compiled using English language.")

# main process
if __name__ == "__main__":

    # show version information
    if len(sys.argv) == 2:
        if sys.argv[1] == "--version" or sys.argv[1] == "-v":
            versionInfo()
        else: 
            synopsis()

    # English flag provided
    elif len(sys.argv) == 4 and sys.argv[3] == "-e":
        if os.path.isfile(sys.argv[1]):
            # initiate conversion process using default language (true)
            transcompile(True)
        else:
            # no vaild file is detected, print error & exit
            print("No valid file at given path.\n")
            exit()

    # Spanish flag provided
    elif len(sys.argv) == 4 and sys.argv[3] == "-s":
        if os.path.isfile(sys.argv[1]):
            # initiate conversion process using alternative language (false)
            transcompile(False)
        else:
            # no vaild file is detected, print error & exit
            print("No valid file at given path.\n")
            exit()
    
    # in all other cases
    else:
        synopsis()
    
    # end program
    exit()