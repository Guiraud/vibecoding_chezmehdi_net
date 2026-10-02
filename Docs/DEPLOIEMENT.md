# Déploiement Cloudflare Pages

Le dépôt GitHub public est https://github.com/Guiraud/vibecoding_chezmehdi_net.

## Source de déploiement

L’intégration GitHub a échoué avec l’erreur Cloudflare `8000011`. Le 2 octobre 2026, une copie du dépôt a été créée sur GitLab : https://gitlab.com/Guiraud/vibecoding_chezmehdi_net.

La création du projet Pages par API avec cette source GitLab a réussi. Projet : `vibecoding-chezmehdi-net`, adresse : https://vibecoding-chezmehdi-net.pages.dev.

Réglages : branche `main`, commande `npm run build`, sortie `dist`, variable `NODE_VERSION=22`. Le remote local `gitlab` alimente le déploiement ; `origin` conserve la copie GitHub. Pousser les modifications sur les deux dépôts.

Après le premier déploiement réussi, ajouter `vibecoding.chezmehdi.net` dans les domaines personnalisés du projet et suivre la validation DNS proposée. Vérifier le certificat, la page d’accueil et les fiches.

Documentation : https://developers.cloudflare.com/pages/configuration/git-integration/

## Vérification de la première version

Construction et tests Node réussis. Vérification navigateur Chrome : neuf fiches, filtre données, dialogue et Escape, titre traité comme texte, choix de thème, progression et remise à zéro. Aucun débordement à 390 px ni erreur JavaScript constatée. Captures locales dans `.test-results/` (non versionnées).
