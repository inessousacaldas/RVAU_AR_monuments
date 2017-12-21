# MonumentAR

----------------------

# Autores

Inês Caldas

Joel Carneiro


----------------------

# Instalação

Antes de executar a aplicação é necessário instalar as dependências da mesma. As versões em que a aplicação foi desenvolvida encontram-se em baixo.

```
python --> 3.6.3
pillow --> 4.3.0
tk --> 8.6.7
matplotlib --> 2.1.1
numpy  --> 1.13.3
opencv --> opencv_python - 3.3.1
ghostscript --> Ghostscript 9.22 for Windows --> (https://www.ghostscript.com/download/gsdnld.html)

```


Depois de criado o ambiente do python com as restantes dependências da aplicação o utilizador deverá aceder ao ficheiro scriptWin.bat ou scriptUnix.sh, dependendo do seu sistema operativo, que está na pasta Ar_monuments/gui.


----------------------

# Introdução

No âmbito da unidade curricular de Realidade Virtual e Aumentada do Mestrado Integrado em Engenharia Informática e Computação da Faculdade de Engenharia do Porto foi desenvolvida uma aplicação com o objetivo de “aumentar” imagens de fachadas de edifícios, reconhecendo desta forma marcas naturais.

Esta aplicação integra dois subprogramas que são abstraídos pela aplicação, de forma a haver uma melhor interação com o utilizador. Desta forma, o utilizador tem de navegar por janelas para concluir o seu trabalho. O primeiro subprograma é um programa de preparação onde o utilizador escolhe as regiões das imagens que quer usar para calcular os *keypoints*, desenha marcas em cima das imagens usadas como base de dados, para que estas apareçam sobrepostas com a homografia respetiva nas imagens de teste no programa de “aumento” e escolhe que algoritmo usar no programa de “aumento”, assim como a imagem a testar. Este último subprograma tem como função fazer a comparação entre as imagens da base de dados e a imagem escolhida como teste, apresentando no final os resultados obtidos.

A aplicação, MonumentAR, foi desenvolvida usando a linguagem de programação *Python* com recurso à biblioteca *OpenCV* para efeitos de “aumento” e à biblioteca *tkinter* para a interface gráfica.

MonumentAR mostrou-se capaz de resolver os problemas de teste com eficiência, contudo a sua velocidade depende proporcionalmente dos algoritmos escolhidos pelo utilizador.

No restante relatório será apresentada primeiramente uma descrição mais detalhada da aplicação, seguindo-se os resultados obtidos, a análise dos mesmos e as conclusões retiradas.


----------------------

# Descrição da Aplicação

MonumentAR foi desenvolvida usando a linguagem de programação *Python* com recurso à biblioteca *OpenCV* para efeitos de “aumento” e à biblioteca *tkinter* para a interface gráfica. 

Após o utilizador instalar todas as dependências da aplicação e abrir o script de execução da mesma, é apresentada uma janela onde o utilizador pode efetuar todas as tarefas necessárias.
O utilizador deverá escolher as imagens que quer utilizar na base de dados. Após este passo o utilizador pode fazer o carregamento de uma das imagens da base de dados e pintar sobre elas as “marcas” que quer apresentar nas futuras imagens a reconhecer. São fornecidas várias ferramentas de edição de imagem, de forma a que o utilizador tenha liberdade. A aplicação guarda as alterações feitas automaticamente. 
Deverá também carregar na opção Key Points de forma a escolher qual a região da imagem a ser usada para o cálculos dos pontos de interesse da imagem. Poderá efetuar o mesmo processo para as restantes imagens da base de dados.
Agora que a base de dados está completa o utilizador deverá escolher qual o algoritmo a utilizar, *SIFT*[1] ou *SURF*[2], e escolher a imagem a testar.
Após estes passos a aplicação mostra os resultados com a imagem de teste a apresentar as marcas escolhidas pelo utilizador com a homografia aplicada. 

Quanto à utilização da biblioteca *OpenCV*, foram utilizados os seguintes algoritmos, para a computação de *keypoints*, *descriptors* e matches:
```
  SIFT  - Scale-Invariant Feature Transform
  SURF - Speeded-Up Robust Features
  RANSAC [3] - Random sample consensus
  FLANN [4] - Fast Library for Approximate Nearest Neighbors 
```

----------------------

# Resultados

Foram gerados problemas de forma a testar a aplicação desenvolvida, com o objetivo de verificar o tempo de execução, se a homografia é calculada corretamente, e que tipo de influências afeta mais cada algoritmo.

Várias imagens foram utilizadas como base de dados e também como imagem de teste. Para além disso, foi testado o algoritmo *SIFT* com várias imagens (base de dados e de teste) e o mesmo se aplica ao *SURF*. Foram também atribuídos valores diferentes ao valor limite do algoritmo *RANSAC*.
	
No que diz respeito ao algoritmo *SIFT*, este de facto é o mais poderoso. Mostrou sempre uma boa solução mesmo quando comparando imagens com diferentes iluminações e poses pouco frontais.
  
Quanto ao *SURF*, embora seja mais rápido em tempo de execução do que o *SIFT*, o cálculo da homografia, quando se trata de imagens com diferentes iluminações e poses pouco frontais, dá resultados que se podem classificar como maus. De realçar que a homografia mais correta encontrada foi quando a imagem da base de dados e a de teste eram a mesma. Desta forma, conclui-se que com o *SURF* consegue-se calcular homografias corretas, utilizando os seus *keypoints* e *descriptors* para calcular os matches, contudo, os resultados são susceptíveis a grandes variações dependendo das condições das imagens.
  
O *RANSAC* mostrou-se um bom ajudante no cálculo de homografias, eliminando matches incorretos, tendo em conta os restantes. Quanto menor o valor do limite do *RANSAC* mais matches errados são eliminados, resultando um conjunto de *matches* o mais corretos possível para calcular a homografia.


----------------------

# Referências

```
[1] - OpenCV: Introduction to SIFT (Scale-Invariant Feature Transform). (n.d.). Retrieved December 19, 2017, from https://docs.opencv.org/3.1.0/da/df5/tutorial_py_sift_intro.html

[2] - Introduction to SURF (Speeded-Up Robust Features) — OpenCV 3.0.0-dev documentation. (n.d.). Retrieved December 19, 2017, from https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_surf_intro/py_surf_intro.html

[3] - Feature Matching + Homography to find Objects — OpenCV 3.0.0-dev documentation. (n.d.). Retrieved December 19, 2017, from https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_feature_homography/py_feature_homography.html

[4] - Feature Matching — OpenCV 3.0.0-dev documentation. (n.d.). Retrieved December 19, 2017, from https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_matcher/py_matcher.html
```

