# montage-parallele

Entrée « Montage Parallèle » du domaine cd-consulting-rd : les pages qui présentent la squad
« Montage Parallèle », sa méthode et ses leçons. Site statique servi par GitHub Pages, destiné à
`https://montage-parallele.cd-consulting-rd.be/`.

*Ce fichier décrit le dépôt ; il n'en est pas la norme.*

## Contenu

| Page | FR (racine) | EN (`en/`) |
|---|---|---|
| Qui sommes-nous (accueil de l'entrée) | `qui-sommes-nous.html` | `en/qui-sommes-nous.html` |
| Manifeste | `manifeste.html` | `en/manifeste.html` |
| Méthode | `methode.html` | `en/methode.html` |
| Leçons du premier mois | `lecons-du-premier-mois.html` | `en/lecons-du-premier-mois.html` |

- `index.html` : redirection instantanée vers `qui-sommes-nous.html` (aucun contenu propre ; hors sitemap).
- `sitemap.xml` : les 8 URL absolues de l'entrée.
- `assets/` : `fonts.css`, `mobilier.css`, `style.css` et `fonts/` (15 fontes et 3 licences OFL, qui voyagent avec
  les fontes).

## Provenance

Les pages et `assets/` sont portés du dépôt `cdatso/analyses-de-films`, commit
`4300400aebba84b95fae8dfb48027ec5a47bb308`, le 17/09/2026 :

- `qui-sommes-nous`, `manifeste`, `lecons-du-premier-mois` (FR et EN) : pages du même nom ;
- `methode` (FR et EN) : les deux sections « Le cycle » et « Les registres » (« The cycle », « The registers ») de
  `comment-ca-marche.html`, coupées telles quelles ;
- `assets/` : copie à l'identique des fichiers cités par les pages (mêmes objets git).

Le gabarit (chrome et feuilles de style) est **porté le 17/09/2026 et ne suit pas** les évolutions du site des films.

## Règles de tenue (description)

- **Textes d'auteur non réécrits** : seul le chrome a changé au portage — titre de fenêtre (« … — Montage
  Parallèle »), marque, menu, liens de retour, pied, `canonical` et `hreflang`.
- **Chapeau** : chaque page s'ouvre sur un chapeau daté (`p.chapeau-deplacement`), texte de Christo Datso, qui situe
  le texte déplacé.
- **Liens internes relatifs** : entre les pages de l'entrée et entre FR et EN.
- **Liens vers le site des films absolus**, vers `https://www.cdatso.be/analyses-de-films/` :
  `index.html` et `en/index.html` (menu), `comment-ca-marche.html#licences` et `en/…#licences` (pied),
  `comment-ca-marche.html` et `en/comment-ca-marche.html` (corps du manifeste et des leçons),
  `films/dogville.html` et `films/rebecca.html` (corps des leçons).
- **`canonical` et `hreflang`** absolus sur `https://montage-parallele.cd-consulting-rd.be/` ; `x-default` = FR.
- **Aucune ressource externe** n'est chargée.

## Licences

Textes : CC BY-NC-SA 4.0 · code : EUPL 1.2 · logo et identité « Montage Parallèle » : tous droits réservés — détails :
<https://www.cdatso.be/analyses-de-films/comment-ca-marche.html#licences>. Fontes : SIL Open Font License (fichiers
`assets/fonts/LICENSE-*-OFL.txt`).
