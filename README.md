# IFT630 TP2

## Équipe

Zachary Déziel, DEZZ2201, 17 022 847
Michael Durand-Chorel, 17 141 086

## Partie 1

Builder main.cpp avec g++ main.cpp -lOpenCL dans un interface linux. Prendre en note que c'est 'L' minuscule.
Ensuite, exécuter le fichier de sortie avec ./a.out.

## Partie 2

La partie 2 peut être exécutée avec:
```
$ mpiexec -n 4 python matrix_mult_mpi.py path_destination path_matrice1 path_matrice2
```

La suite de tests peut être exécutée avec:
```
$ pytest
```
