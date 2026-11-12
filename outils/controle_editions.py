# -*- coding: utf-8 -*-
"""Controle des deux editions produites par build_editions.py (lecture seule : n'ecrit rien).

Usage : python -I -B outils/controle_editions.py
Controles, par edition :
  T1 tronc commun : les segments <!-- commun --> ... <!-- /commun --> de chaque page sont identiques dans les deux editions
  T2 liens internes : toute cible relative (href, src) existe dans la sortie ; les liens absolus sont listes
  T3 ressources distantes : aucune feuille, aucun script, aucune image, aucune fonte chargee depuis http(s)
  T4 canonical / hreflang : toutes les adresses absolues de <head> pointent sur l'hote de l'edition
  T5 soustraction : le texte visible ne contient aucun motif interne (code d'item, chemin, numero d'ecart...)
Code de sortie : 0 si tout est conforme, 1 sinon.
"""
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
DEPOT = os.path.normpath(os.path.join(ICI, '..'))
EDITIONS = {
    'cdc': (DEPOT, 'https://montage-parallele.cd-consulting-rd.be/'),
    'cdatso': (os.path.normpath(os.path.join(DEPOT, '..', 'montage-parallele-cdatso')), 'https://montage-parallele.cdatso.be/'),
}
EXCLUS = {'.git', 'source', 'outils', 'assets'}
MOTIFS = [r'BKL-', r'\bF-\d', r'n°\s?\d', r'[A-Za-z]:\\', r'\bNJ\b', r'\bING\b', r'UNamur', r'Fable (Superviseur|Chercheur) n',
          r'\bR-0\d\d\b', r'claude-config', r'\.md\b', r'\b(CIN|CNF|FOR|LIB|MEM|CDC|COP|DEV|PRG|RUN|SRV)-\d']
CODES = r'\b(CIN|CNF|FOR|LIB|MEM|CDC|COP|DEV|PRG|RUN|SRV)\b'


def pages(racine):
    for r, dossiers, fichiers in os.walk(racine):
        dossiers[:] = [d for d in dossiers if d not in EXCLUS]
        for f in sorted(fichiers):
            if f.endswith('.html'):
                yield os.path.join(r, f)


def lire(p):
    return open(p, encoding='utf-8').read()


def visible(h):
    h = re.sub(r'<(style|script)\b.*?</\1>', ' ', h, flags=re.S)
    h = re.sub(r'<!--.*?-->', ' ', h, flags=re.S)
    h = re.sub(r'<[^>]+>', ' ', h)
    return h


def main():
    defauts = []
    absolus = set()
    for ed, (racine, hote) in EDITIONS.items():
        n = 0
        for p in pages(racine):
            n += 1
            h = lire(p)
            rel = os.path.relpath(p, racine)
            # T2 liens
            for cible in re.findall(r'(?:href|src)="([^"]+)"', h):
                if re.match(r'^(https?:|mailto:)', cible):
                    absolus.add(cible)
                    continue
                if cible.startswith('#'):
                    continue
                chemin = os.path.normpath(os.path.join(os.path.dirname(p), cible.split('#')[0]))
                if not os.path.exists(chemin):
                    defauts.append('T2 %s %s : lien casse -> %s' % (ed, rel, cible))
            for cible in re.findall(r'content="0; url=([^"]+)"', h):
                if not cible.startswith('http') and not os.path.exists(os.path.join(os.path.dirname(p), cible)):
                    defauts.append('T2 %s %s : renvoi casse -> %s' % (ed, rel, cible))
            # T3 ressources distantes
            for balise in re.findall(r'<(?:link|script|img|iframe|source|video|audio)\b[^>]*>', h):
                if re.search(r'rel="(?:canonical|alternate)"', balise):
                    continue  # une adresse declaree, pas une ressource chargee
                m = re.search(r'(?:href|src)="(https?:[^"]+)"', balise)
                if m:
                    defauts.append('T3 %s %s : ressource distante %s' % (ed, rel, m.group(1)))
            if re.search(r'@import|url\(\s*["\']?https?:', h):
                defauts.append('T3 %s %s : import ou url() distant' % (ed, rel))
            # T4 canonical / hreflang
            tete = h.split('</head>')[0]
            for u in re.findall(r'<link rel="(?:canonical|alternate)"[^>]*href="([^"]+)"', tete):
                if not u.startswith(hote):
                    defauts.append('T4 %s %s : adresse hors edition %s' % (ed, rel, u))
            # T5 soustraction (pages generees seulement : les anciennes pages EN gardent leur texte d'aout jusqu'a leur remplacement)
            if '<!-- commun -->' in h or 'http-equiv="refresh"' in h:
                v = visible(h)
                for motif in MOTIFS:
                    for m in re.finditer(motif, v):
                        defauts.append('T5 %s %s : motif %s -> %r' % (ed, rel, motif, v[max(0, m.start() - 30):m.end() + 30]))
                for m in re.finditer(CODES, v):
                    if not re.match(r'\s*\)', v[m.end():m.end() + 2]) or v[m.start() - 1] != '(':
                        defauts.append('T5 %s %s : code hors forme « Intitulé (CODE) » -> %r' % (ed, rel, v[max(0, m.start() - 30):m.end() + 10]))
        print('%s : %d pages lues (%s)' % (ed, n, racine))
    # T1 tronc commun
    (r1, _), (r2, _) = EDITIONS['cdc'], EDITIONS['cdatso']
    compares = 0
    for p in pages(r2):
        rel = os.path.relpath(p, r2)
        a, b = lire(p), os.path.join(r1, rel)
        sa = re.findall(r'<!-- commun -->\n(.*?)<!-- /commun -->', a, re.S)
        if not sa:
            continue
        if not os.path.exists(b):
            defauts.append('T1 %s : absente de l edition cdc' % rel)
            continue
        sb = re.findall(r'<!-- commun -->\n(.*?)<!-- /commun -->', lire(b), re.S)
        compares += 1
        if sa != sb:
            defauts.append('T1 %s : tronc commun DIFFERENT entre les deux editions' % rel)
        else:
            print('T1 %-24s %d segment(s) commun(s) identique(s), %d caracteres' % (rel, len(sa), sum(len(s) for s in sa)))
    print('T1 pages comparees : %d' % compares)
    print('liens absolus (non suivis ici) : %d' % len(absolus))
    for u in sorted(absolus):
        print('  ' + u)
    if defauts:
        print('DEFAUTS : %d' % len(defauts))
        for d in defauts:
            print('  ' + d)
        return 1
    print('CONFORME : T1 a T5, 0 defaut')
    return 0


if __name__ == '__main__':
    if len(sys.argv) > 1:
        raise SystemExit(__doc__)
    sys.exit(main())
