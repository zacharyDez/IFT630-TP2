#
# Modèle de base pour «mpi4py».
# Par : Daniel-Junior Dubé
#
# Exemple d'exécution du programme :
#   - `mpiexec -n 4 python main.py` : (Recommendé) Défini par le standard MPI.
#   - `mpirun -n 4 python comm.py` : Commande alternative fournie par plusieurs implémentation d'MPI.
# Documentation : https://mpi4py.readthedocs.io/en/stable/tutorial.html
# Autre ressource sur mpi4py : https://rabernat.github.io/research_computing/parallel-programming-with-mpi-for-python.html

from mpi4py import MPI

# Objet représentatnt l'espace de calcul.
comm = MPI.COMM_WORLD

# Taille de l'espace de travail. Représente le nombre de entités de travail (gestionnaires/travailleurs).
size = comm.Get_size()

# Rang du processus actuel. Permet d'identifier le processus de façon unique.
rank = comm.Get_rank()

if rank == 0:

    # ...
    # Gestionnaire
    # ...

    data = {
        'x': 1,
        'y': 2,
    }

    # Envoi de données par appel bloquant.
    comm.send(data, dest=1)
elif rank == 1:

    # ...
    # Travailleur
    # ...

    # Réception de données par appel bloquant.
    data = comm.recv(source=0)
