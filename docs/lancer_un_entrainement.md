# Lancer un entraînement

## Soumettre un job d'entraînement
Un entraînement se lance en soumettant un job au cluster avec la commande `sbatch train.sh`. Le script précise le nombre de GPU demandés, la durée maximale et l'environnement à utiliser.

## Suivre un job
La commande `squeue -u $USER` affiche l'état de vos jobs (en attente, en cours). Les journaux sont écrits dans le fichier `slurm-<id>.out`.

## Annuler un job
Pour arrêter un job, utilisez `scancel <id_du_job>`.
