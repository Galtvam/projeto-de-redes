#coding: utf-8

def beautifulPrintCandidates(listOfCandidates):
    n = 0
    print('Escolha o número do seu candidato: \n')
    for candidate in listOfCandidates:
        print('['+str(n)+'] - '+candidate + '\n')
        n += 1
