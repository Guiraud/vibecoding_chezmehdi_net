# Déploiement Cloudflare Pages

Le dépôt GitHub public est https://github.com/Guiraud/vibecoding_chezmehdi_net.

La création du projet Pages avec source GitHub a été tentée le 2 octobre 2026. Cloudflare a refusé avec le code `8000011` : problème dans l’installation Git du compte. Aucun projet Pages n’a été créé par cette tentative et le domaine n’a pas été configuré.

## Action nécessaire dans Cloudflare

Depuis Workers & Pages, créer une application Pages en important un dépôt Git. Autoriser ou réinstaller l’application Cloudflare Pages sur GitHub avec accès au dépôt `Guiraud/vibecoding_chezmehdi_net`.

Réglages : nom `vibecoding-chezmehdi-net`, branche `main`, framework aucun, commande `npm run build`, sortie `dist`, racine du dépôt, variable `NODE_VERSION=22`.

Après le premier déploiement réussi, ajouter `vibecoding.chezmehdi.net` dans les domaines personnalisés du projet et suivre la validation DNS proposée. Vérifier le certificat, la page d’accueil et les fiches.

Documentation : https://developers.cloudflare.com/pages/configuration/git-integration/

## Vérification de la première version

Construction et tests Node réussis. Vérification navigateur Chrome : neuf fiches, filtre données, dialogue et Escape, titre traité comme texte, choix de thème, progression et remise à zéro. Aucun débordement à 390 px ni erreur JavaScript constatée. Captures locales dans `.test-results/` (non versionnées).
