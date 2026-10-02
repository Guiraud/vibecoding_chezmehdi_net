# Vibecoding Chez Mehdi

Site pédagogique pour explorer les applications possibles du développement avec l’IA. Domaine prévu : https://vibecoding.chezmehdi.net.

## Première version

Dix fiches de réalisations, filtres par usage, présentation de la méthode et simulation interactive locale. Les fiches distinguent le code existant des démonstrations et preuves restant à préparer. Aucun appel à une IA, cookie applicatif ou service d’analyse d’audience.

## Développement

Node.js 22+ et Python 3 pour le serveur local.

```bash
npm ci
npm run dev
npm test
npm run build
```

Ouvrir http://localhost:4173. Sources dans `web/`, sortie statique dans `dist/`. La CI GitHub vérifie les ressources locales et construit le site.

## Cloudflare Pages avec GitHub

- Dépôt : `Guiraud/vibecoding_chezmehdi_net`
- Branche de production : `main`
- Framework : aucun
- Commande : `npm run build`
- Répertoire de sortie : `dist`
- Variable de build : `NODE_VERSION=22`
- Domaine personnalisé : `vibecoding.chezmehdi.net`

Connecter ce dépôt depuis Workers & Pages → créer une application Pages → importer un dépôt Git. Ajouter ensuite le domaine personnalisé depuis le projet Pages. Ne pas créer un projet Direct Upload si l’objectif est l’intégration Git native.

Documentation officielle : https://developers.cloudflare.com/pages/configuration/git-integration/

## Prochaines étapes

Vérifier les applications externes, préparer des jeux de données fictifs, rassembler les traces de fabrication et produire de vraies démonstrations. La galerie inclut des captures des sites ATT, Récits, Fred2Baro et Roundnet prises le 2 octobre 2026. Les autres visuels sont des illustrations. Liens directs disponibles pour ces quatre sites et la présentation de l’extension Woodat sur charte-de-munich.org.
