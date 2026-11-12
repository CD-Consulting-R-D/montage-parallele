# source — les textes du site « Montage Parallèle », une source pour deux éditions

Ce dossier tient les textes des quatre pages (qui sommes-nous, manifeste, méthode, leçons), en Markdown, en français à la racine
du dossier et en anglais sous `en/`. Le script `outils/build_editions.py` les assemble en deux éditions :

| Édition | Adresse | Sortie |
|---|---|---|
| `cdc` | `https://montage-parallele.cd-consulting-rd.be/` | la racine de ce dépôt |
| `cdatso` | `https://montage-parallele.cdatso.be/` | le dépôt `montage-parallele` du compte `cdatso` |

On corrige un texte ICI, jamais dans une page générée.

## La convention des blocs

Chaque texte est découpé en blocs. Un bloc s'ouvre par une ligne de balise seule, et court jusqu'à la balise suivante ou jusqu'à la fin
du fichier :

| Balise | Le bloc va dans |
|---|---|
| `<!-- commun -->` | les deux éditions, au mot près (le tronc commun) |
| `<!-- cdatso -->` | l'édition cdatso.be seulement |
| `<!-- cdc -->` | l'édition cd-consulting-rd.be seulement |

- Une édition = les blocs `commun` et ses blocs propres, dans l'ordre du fichier.
- Le premier titre `#` du fichier donne le titre de la page ; il vit dans un bloc `commun`.
- Les liens entre pages visent le fichier HTML de la page (`methode.html`), en relatif ; les liens vers un autre site sont absolus.
- Rien d'autre que du texte publiable : aucun chemin du poste, aucun identifiant interne, aucun nom de tiers. Les lignes de
  production se nomment « Intitulé (CODE) ».
- Le budget est de 1 750 mots par édition et par langue (400 / 300 / 350 / 700 par page), compté par le script.
