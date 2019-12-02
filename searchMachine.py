import cv2
import numpy as np
from matplotlib import pyplot as plt
import os


def isImageOrVideo(file):
    formatosVideo = set(['.mp4', '.avi', '.mpeg'])
    formatosImagem = set(['.jpg', '.png'])
    if file.endswith(tuple(formatosImagem)):
        return True
    elif file.endswith(tuple(formatosVideo)):
        return False


def pesquisaDiretorio(template, minSimilaridade, qtdRetornos):
    diretorio = 'imgs'

    methods = ['cv2.TM_CCOEFF_NORMED']
    matches = []
    w, h = template.shape[::-1]

    for meth in methods:
        method = eval(meth)

        for file in os.listdir(diretorio):
            if isImageOrVideo(file):
                img = cv2.imread('{}/{}'.format(diretorio, file), 0)
                img2 = img.copy()
                similaridade = calculaSimilaridade(minSimilaridade, img, template, method, meth)

                if similaridade >= minSimilaridade:
                    aux = "A imagem {} possui {}% de similaridade".format(file, similaridade)
                    matches.append((aux, similaridade))

            else:
                cap = cv2.VideoCapture('{}/{}'.format(diretorio, file), 0)
                i = 0
                while (cap.isOpened()):
                    ret, frame = cap.read()

                    if ret == True:
                        i += 1
                        nomeFrame = "{} - no Frame: {}".format(file, i)
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        img = gray.copy()
                        similaridade = calculaSimilaridade(
                            minSimilaridade, img, template, method, meth)

                        if similaridade >= minSimilaridade:
                            aux = "No Video: {} a Similaridade é de {}%".format(nomeFrame, similaridade)
                            matches.append((aux, similaridade))

                    else:
                        break

    
    matches.sort(key=lambda x: x[1], reverse=True)

   
    print(*matches[:qtdRetornos], quebraLinha ='\n')


def calculaSimilaridade(minSimilaridade, img, template, method, meth):
    res = cv2.matchTemplate(img, template, method)

    # Recupera a similaridade entre o template e o conteúdo da Imagem de busca
    min_val, similaridade, min_loc, max_loc = cv2.minMaxLoc(res)
    texto = 'Similaridade com {0} entre Imagens é {1}%'.format(meth, round(similaridade*100, 2))
    return similaridade


def realizaBusca(arquivoTemplate, minSimilaridade, qtdeRetornos):

    if isImageOrVideo(arquivoTemplate):
        template = cv2.imread(arquivoTemplate, 0)
        pesquisaDiretorio(template, minSimilaridade, qtdeRetornos)

    else:
        cap = cv2.VideoCapture(arquivoTemplate, 0)
        while (cap.isOpened()):
            ret, template = cap.read()
            if ret == True:
                gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
                img = gray.copy()
                pesquisaDiretorio(img, minSimilaridade, qtdeRetornos)


#minSimilaridade = float(input('Informe a taxa de similaridade minima a ser aplicada: '))
#qtdeRetornos = int(input('Informe a quantidade de registros a serem retornados: '))
minSimilaridade = 0.85
Retornos = 8
arq = 'images.jpg'

realizaBusca(arq, minSimilaridade, Retornos)