# GPU et quotas

## Demander des GPU
Indiquez le nombre de GPU dans votre script avec l'option `--gres=gpu:2`. Demandez uniquement les GPU nécessaires pour ne pas bloquer les autres utilisateurs.

## Quotas par projet
Chaque projet dispose d'un quota d'heures GPU par mois. Le quota restant est consultable sur le portail du cluster.

## Mémoire GPU insuffisante
En cas d'erreur « CUDA out of memory », réduisez la taille du batch ou utilisez la précision mixte.
