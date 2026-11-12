# -*- coding: utf-8 -*-
"""Assemble les deux editions du site « Montage Parallele » depuis UNE source Markdown a blocs.

Source : source/<page>.md (francais) et source/en/<page>.md (anglais, s'il existe), blocs balises
<!-- commun --> / <!-- cdatso --> / <!-- cdc --> (convention : source/README.md).
Sorties :
  edition cdc    -> la racine de ce depot           (https://montage-parallele.cd-consulting-rd.be/)
  edition cdatso -> ../../montage-parallele-cdatso  (https://montage-parallele.cdatso.be/)
Usage : python -I -B outils/build_editions.py      (aucun argument ; deterministe : deux executions = memes octets)
Le script n'ecrit un fichier que si son contenu change ; il ne supprime rien.
"""
import html
import io
import os
import re
import shutil
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
DEPOT = os.path.normpath(os.path.join(ICI, '..'))
SRC = os.path.join(DEPOT, 'source')

EDITIONS = {
    'cdc': {'sortie': DEPOT, 'hote': 'https://montage-parallele.cd-consulting-rd.be/'},
    'cdatso': {'sortie': os.path.normpath(os.path.join(DEPOT, '..', 'montage-parallele-cdatso')),
               'hote': 'https://montage-parallele.cdatso.be/'},
}
PAGES = [  # (fichier, libelle FR du menu, libelle EN du menu)
    ('qui-sommes-nous', 'Qui sommes-nous', 'Who we are'),
    ('manifeste', 'Manifeste', 'Manifesto'),
    ('methode', 'Méthode', 'Method'),
    ('lecons', 'Leçons', 'Lessons'),
]
BUDGET = {'qui-sommes-nous': 400, 'manifeste': 300, 'methode': 350, 'lecons': 700}
ANCIENNES = {'lecons': 'lecons-du-premier-mois'}  # ancienne adresse -> page-renvoi (edition cdc seulement)
FILMS = 'https://www.cdatso.be/analyses-de-films/'
MENU_EXT = {
    'cdc': [('Analyses de films', FILMS + 'index.html', FILMS + 'en/index.html', ''),
            ('CD Consulting R&amp;D ↗', 'https://www.cd-consulting-rd.be/', 'https://www.cd-consulting-rd.be/', ' rel="noopener"')],
    'cdatso': [('Analyses de films', FILMS + 'index.html', FILMS + 'en/index.html', ''),
               ('Christo Datso ↗', 'https://www.cdatso.be/', 'https://www.cdatso.be/', ' rel="noopener"')],
}
TXT = {
    'fr': {'nav': 'Navigation principale', 'theme': 'Basculer entre clair et sombre', 'retour': "Retour à l'accueil",
           'autre': ('English', 'en'),
           'ia': "Textes rédigés avec une IA (Claude, d'Anthropic) et relus par un humain — mention de transparence, AI Act, article 50.",
           'ext': "Aucune ressource externe n'est chargée par ce site ; aucune donnée de lecture n'est transmise à un tiers.",
           'lic': 'Licences : textes CC BY-NC-SA 4.0 · code EUPL 1.2 —', 'det': 'détails', 'lic_url': FILMS + 'comment-ca-marche.html#licences',
           'deplace': "Cette page a changé d'adresse.",
           'deplace2': 'Le texte est désormais publié à la page {lien}. Votre navigateur devrait vous y conduire ; sinon, suivez ce lien.'},
    'en': {'nav': 'Main navigation', 'theme': 'Switch between light and dark', 'retour': 'Back to the home page',
           'autre': ('Français', 'fr'),
           'ia': 'Texts written with an AI (Claude, by Anthropic) and reviewed by a human — transparency notice, AI Act, Article 50.',
           'ext': 'This site loads no external resource; no reading data is passed to any third party.',
           'lic': 'Licences: texts CC BY-NC-SA 4.0 · code EUPL 1.2 —', 'det': 'details', 'lic_url': FILMS + 'en/comment-ca-marche.html#licences',
           'deplace': 'This page has moved.',
           'deplace2': 'The text is now published at {lien}. Your browser should take you there; if not, follow this link.'},
}
SOMBRE = [('--ink', '#ece8df'), ('--ink-soft', '#cfc9bd'), ('--ink-muted', '#a29c92'), ('--paper', '#161519'),
          ('--paper-alt', '#1e1d22'), ('--line', '#38352f'), ('--accent', '#d9a08c'),
          ('--mobilier-filet', '#38352f'), ('--mobilier-attenue', '#a29c92')]
BALISE = re.compile(r'^<!-- (commun|cdatso|cdc) -->\s*$')

LOGO = '''  <div class="logo-squad">
    <svg xmlns="http://www.w3.org/2000/svg" width="680" height="300" viewBox="0 0 680 300" role="img">
      <title>{titre}</title>
      <desc>{desc}</desc>
      <circle cx="262" cy="120" r="70" fill="none" class="strip" stroke-width="20"/>
      <circle cx="418" cy="120" r="70" fill="none" class="strip" stroke-width="20"/>
{perfs}
      <rect x="330" y="110" width="20" height="4" rx="1" class="flow"/>
      <rect x="330" y="126" width="20" height="4" rx="1" class="flow"/>
      <path d="M186 105 L174 120 L186 135 Z" class="flow"/>
      <path d="M494 135 L506 120 L494 105 Z" class="flow"/>
      <text x="340" y="243" text-anchor="middle" class="word" style="font-family:ui-sans-serif,system-ui,sans-serif;font-size:25px;font-weight:500;letter-spacing:0.12em;">Squad Montage Parallèle</text>
      <text x="340" y="270" text-anchor="middle" class="tag" style="font-family:ui-sans-serif,system-ui,sans-serif;font-size:12px;letter-spacing:0.08em;">{devise}</text>
    </svg>
  </div>
  <p class="logo-squad-legende">{legende}</p>
'''
LOGO_TXT = {
    'fr': {'titre': 'Logo Squad Montage Parallèle',
           'desc': 'Deux bobines de film côte à côte reliées par des amorces de coupe dorées — des actions parallèles, un seul récit.',
           'devise': 'des actions parallèles · un seul récit — conception · dev · test · prod',
           'legende': 'Deux bobines de film reliées par des amorces de coupe : des actions parallèles, un seul récit.'},
    'en': {'titre': 'Montage Parallèle squad logo',
           'desc': 'Two film reels side by side, joined by golden splice leaders — parallel actions, a single story.',
           'devise': 'parallel actions · a single story — design · dev · test · prod',
           'legende': 'Two film reels joined by splice leaders: parallel actions, a single story.'},
}


def perforations():
    out = []
    for cx, angles in ((262, (0, 30, 60, 90, 150, 180, 210, 240, 270, 330)), (418, (0, 30, 90, 120, 150, 180, 210, 270, 300, 330))):
        for a in angles:
            out.append('      <g transform="rotate(%d %d 120)"><rect x="%d" y="47" width="6" height="6" rx="1" class="perf"/></g>' % (a, cx, cx - 3))
    return '\n'.join(out)


def style_page(avec_logo):
    var = ' '.join('%s: %s;' % kv for kv in SOMBRE)
    s = ['<style>',
         '/* Gabarit des deux éditions : clair par défaut, sombre selon le système, bouton Light / Dark (clé kb-theme). */',
         ':root[data-theme="light"] { color-scheme: light; }',
         ':root[data-theme="dark"] { color-scheme: dark; %s }' % var,
         '@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { color-scheme: dark; %s } }' % var,
         '.theme { margin-left: 0.4rem; font-family: var(--sans); font-size: 0.7rem; letter-spacing: 0.06em; text-transform: uppercase;',
         '  background: transparent; color: var(--mobilier-attenue); border: 1px solid var(--line); border-radius: 3px;',
         '  padding: 0.2rem 0.5rem; cursor: pointer; }',
         '.theme:hover { color: var(--accent); border-color: var(--accent); }',
         '@media print { .theme { display: none; } }',
         'main.wrap { padding-top: 3.4rem; padding-bottom: 5rem; max-width: 44rem; }',
         'main.wrap h1 { font-family: var(--serif); font-weight: 600; font-size: 2.2rem; color: var(--ink); margin: 0 0 1.6rem; line-height: 1.2; }']
    if avec_logo:
        s += ['.logo-squad { text-align: center; margin: 0 0 0.7rem; }',
              '.logo-squad svg { width: 200px; max-width: 100%; height: auto; }',
              '.logo-squad .strip { stroke: var(--ink); } .logo-squad .word { fill: var(--ink); } .logo-squad .tag { fill: var(--ink-muted); }',
              '.logo-squad .perf, .logo-squad .flow { fill: #b28d3f; }',
              '.logo-squad-legende { font-family: var(--sans); font-size: 0.78rem; color: var(--ink-muted); text-align: center; margin: 0 0 2.2rem; }']
    s.append('</style>')
    return '\n'.join(s)


INIT_THEME = '<script>(function(){try{var t=localStorage.getItem("kb-theme");if(t==="light"||t==="dark"){document.documentElement.setAttribute("data-theme",t);}}catch(e){}})();</script>'
BOUTON_THEME = '<script>(function(){var b=document.getElementById("theme");b.addEventListener("click",function(){var r=document.documentElement;var cur=r.getAttribute("data-theme");var sys=window.matchMedia&&window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light";var now=(cur||sys)==="dark"?"light":"dark";r.setAttribute("data-theme",now);try{localStorage.setItem("kb-theme",now);}catch(e){}});})();</script>'


# --- Markdown : le sous-ensemble employe par les textes -------------------------------------------
def inline(s):
    liens = []

    def _lien(m):
        texte, cible = m.group(1), m.group(2)
        liens.append('<a href="%s">%s</a>' % (html.escape(cible, quote=True), inline_simple(texte)))
        return '\x00%d\x00' % (len(liens) - 1)
    s = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', _lien, s)
    s = inline_simple(s)
    return re.sub(r'\x00(\d+)\x00', lambda m: liens[int(m.group(1))], s)


def inline_simple(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<em>\1</em>', s)
    return s


def rendre(lignes):
    """Rend une suite de lignes Markdown (un bloc) en HTML indente de deux espaces."""
    out, i, n = [], 0, len(lignes)
    while i < n:
        l = lignes[i]
        if not l.strip():
            i += 1
            continue
        if l.startswith('# '):
            out.append('  <h1>%s</h1>' % inline(l[2:].strip()))
            i += 1
            continue
        if l.startswith('## '):
            out.append('  <h2>%s</h2>' % inline(l[3:].strip()))
            i += 1
            continue
        m = re.match(r'^(- |\d+\. )', l)
        if m:
            ordonnee = m.group(1) != '- '
            items = []
            while i < n and re.match(r'^(- |\d+\. )', lignes[i]):
                courant = [re.sub(r'^(- |\d+\. )', '', lignes[i]).strip()]
                i += 1
                while i < n and lignes[i].startswith(' ') and lignes[i].strip():
                    courant.append(lignes[i].strip())
                    i += 1
                items.append(' '.join(courant))
            balise = 'ol' if ordonnee else 'ul'
            out.append('  <%s>' % balise)
            out.extend('    <li>%s</li>' % inline(it) for it in items)
            out.append('  </%s>' % balise)
            continue
        para = []
        while i < n and lignes[i].strip() and not re.match(r'^(#{1,2} |- |\d+\. )', lignes[i]):
            para.append(lignes[i].strip())
            i += 1
        out.append('  <p>%s</p>' % inline(' '.join(para)))
    return out


def blocs(chemin):
    cour, res = None, []
    for ligne in io.open(chemin, encoding='utf-8').read().splitlines():
        m = BALISE.match(ligne)
        if m:
            cour = m.group(1)
            res.append((cour, []))
            continue
        if cour is None:
            raise SystemExit('%s : texte hors bloc : %r' % (chemin, ligne))
        res[-1][1].append(ligne)
    return res


def mots(lignes):
    s = '\n'.join(lignes)
    s = re.sub(r'\]\([^)]*\)', ']', s)
    s = re.sub(r'[#*`\[\]>|_]', ' ', s)
    return len([t for t in s.split() if re.search(r'\w', t)])


# --- Gabarit -------------------------------------------------------------------------------------
def chrome(ed, lang, courante, pre):
    lignes = ['<header class="chrome">', '  <div class="chrome-in">',
              '    <a class="marque" href="qui-sommes-nous.html">Montage Parallèle</a>',
              '    <nav class="menu" aria-label="%s">' % TXT[lang]['nav']]
    for f, lfr, len_ in PAGES:
        cur = ' aria-current="page"' if f == courante else ''
        lignes.append('      <a href="%s.html"%s>%s</a>' % (f, cur, lfr if lang == 'fr' else len_))
    for lib, ufr, uen, rel in MENU_EXT[ed]:
        lignes.append('      <a href="%s"%s>%s</a>' % (ufr if lang == 'fr' else uen, rel, lib))
    lignes += ['    </nav>',
               '    <button class="theme" id="theme" type="button" aria-label="%s">Light / Dark</button>' % TXT[lang]['theme'],
               '  </div>', '</header>']
    return '\n'.join(lignes)


def pied(lang, lien_langue):
    t = TXT[lang]
    l = ['<footer><div class="f-in">']
    if lien_langue:
        l += ['  <a href="%s" hreflang="%s" lang="%s">%s</a>' % (lien_langue, t['autre'][1], t['autre'][1], t['autre'][0]), '  <br>']
    l += ['  ' + t['ia'], '  <br>', '  ' + t['ext'], '  <br>',
          '  %s <a href="%s">%s</a>.' % (t['lic'], t['lic_url'], t['det']), '</div></footer>']
    return '\n'.join(l)


def tete(lang, titre, canonical, alternates, pre, logo, refresh=None):
    l = ['<!DOCTYPE html>', '<html lang="%s">' % lang, '<head>', '<meta charset="UTF-8">',
         '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
         '<title>%s — Montage Parallèle</title>' % html.escape(titre, quote=False),
         '<link rel="canonical" href="%s">' % canonical]
    if refresh:
        l.append('<meta http-equiv="refresh" content="0; url=%s">' % refresh)
    for hl, u in alternates:
        l.append('<link rel="alternate" hreflang="%s" href="%s">' % (hl, u))
    l += ['<link rel="stylesheet" href="%sassets/fonts.css">' % pre, '<link rel="stylesheet" href="%sassets/mobilier.css">' % pre,
          '<link rel="stylesheet" href="%sassets/style.css">' % pre, style_page(logo), INIT_THEME, '</head>', '<body>', '']
    return '\n'.join(l)


def ecrire(chemin, texte, journal):
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    donnees = texte.encode('utf-8')
    if os.path.exists(chemin) and open(chemin, 'rb').read() == donnees:
        return
    tmp = chemin + '.tmp'
    with open(tmp, 'wb') as f:
        f.write(donnees)
    os.replace(tmp, chemin)
    journal.append(chemin)


def construire():
    ecrits, comptes = [], []
    langues = ['fr'] + (['en'] if os.path.isdir(os.path.join(SRC, 'en')) else [])
    sources = {}
    for lang in langues:
        for f, _, _ in PAGES:
            p = os.path.join(SRC, f + '.md') if lang == 'fr' else os.path.join(SRC, 'en', f + '.md')
            if os.path.exists(p):
                sources[(lang, f)] = blocs(p)
    for ed, conf in EDITIONS.items():
        sortie, hote = conf['sortie'], conf['hote']
        os.makedirs(sortie, exist_ok=True)
        urls = []
        for lang in langues:
            pre = '' if lang == 'fr' else '../'
            dossier = sortie if lang == 'fr' else os.path.join(sortie, 'en')
            total = 0
            for f, _, _ in PAGES:
                if (lang, f) not in sources:
                    continue
                bl = [(k, v) for k, v in sources[(lang, f)] if k in ('commun', ed)]
                titre = next(v[2:].strip() for k, vs in bl for v in vs if v.startswith('# '))
                n = sum(mots(v) for k, v in bl)
                total += n
                comptes.append((ed, lang, f, n))
                url_fr, url_en = hote + f + '.html', hote + 'en/' + f + '.html'
                a_en = ('en', f) in sources
                canon = url_fr if lang == 'fr' else url_en
                alts = [('fr', url_fr), ('en', url_en), ('x-default', url_fr)] if a_en else []
                if lang == 'en':
                    lien_langue = '../%s.html' % f
                elif a_en:
                    lien_langue = 'en/%s.html' % f
                elif ed == 'cdc' and os.path.exists(os.path.join(sortie, 'en', ANCIENNES.get(f, f) + '.html')):
                    lien_langue = 'en/%s.html' % ANCIENNES.get(f, f)   # ancien texte anglais, jusqu'a la version neuve
                else:
                    lien_langue = None
                corps = []
                for k, v in bl:
                    corps.append('<!-- %s -->' % k)
                    rendu = rendre(v)
                    if f == 'qui-sommes-nous' and k == 'commun' and rendu and rendu[0].startswith('  <h1>'):
                        rendu = [rendu[0], LOGO.format(perfs=perforations(), **LOGO_TXT[lang]).rstrip('\n')] + rendu[1:]
                    corps.extend(rendu)
                    corps.append('<!-- /%s -->' % k)
                page = (tete(lang, titre, canon, alts, pre, f == 'qui-sommes-nous') + chrome(ed, lang, f, pre) + '\n\n'
                        + '<main class="wrap">\n\n' + '\n'.join(corps) + '\n\n'
                        + '  <p><a class="lien-retour" href="qui-sommes-nous.html">%s</a></p>\n\n</main>\n\n' % TXT[lang]['retour']
                        + pied(lang, lien_langue) + '\n\n' + BOUTON_THEME + '\n</body>\n</html>\n')
                ecrire(os.path.join(dossier, f + '.html'), page, ecrits)
                urls.append(canon)
                # page-renvoi de l'ancienne adresse (edition cdc : la seule ou elle a existe)
                if ed == 'cdc' and f in ANCIENNES:
                    ecrire(os.path.join(dossier, ANCIENNES[f] + '.html'), renvoi(lang, titre, canon, f, pre, ed), ecrits)
            comptes.append((ed, lang, 'TOTAL', total))
        ecrire(os.path.join(sortie, 'index.html'), index(hote), ecrits)
        ecrire(os.path.join(sortie, 'sitemap.xml'), sitemap(urls), ecrits)
        if ed == 'cdatso':
            # sans saut de ligne final : c'est la forme que GitHub Pages ecrit lui-meme quand on (re)saisit le domaine
            ecrire(os.path.join(sortie, 'CNAME'), 'montage-parallele.cdatso.be', ecrits)
            ecrire(os.path.join(sortie, 'README.md'), README_CDATSO, ecrits)
            copier_assets(os.path.join(DEPOT, 'assets'), os.path.join(sortie, 'assets'), ecrits)
    return ecrits, comptes


def renvoi(lang, titre, canon, f, pre, ed):
    t = TXT[lang]
    lien = '<a href="%s.html">%s</a>' % (f, canon.split('//', 1)[1])
    return (tete(lang, titre, canon, [], pre, False, refresh='%s.html' % f) + chrome(ed, lang, None, pre) + '\n\n'
            + '<main class="wrap">\n\n  <p><strong>%s</strong></p>\n  <h1>%s</h1>\n  <p>%s</p>\n\n' % (t['deplace'], html.escape(titre, quote=False), t['deplace2'].format(lien=lien))
            + '  <p><a class="lien-retour" href="qui-sommes-nous.html">%s</a></p>\n\n</main>\n\n' % t['retour']
            + pied(lang, None) + '\n\n' + BOUTON_THEME + '\n</body>\n</html>\n')


def index(hote):
    return ('<!DOCTYPE html>\n<html lang="fr">\n<head>\n<meta charset="UTF-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            '<title>Qui sommes-nous — Montage Parallèle</title>\n'
            '<link rel="canonical" href="%squi-sommes-nous.html">\n'
            '<meta http-equiv="refresh" content="0; url=qui-sommes-nous.html">\n</head>\n<body>\n'
            '<p><a href="qui-sommes-nous.html">qui-sommes-nous.html</a></p>\n</body>\n</html>\n') % hote


def sitemap(urls):
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + ''.join('  <url><loc>%s</loc></url>\n' % u for u in urls) + '</urlset>\n')


def copier_assets(src, dst, ecrits):
    for racine, _, fichiers in os.walk(src):
        for nom in sorted(fichiers):
            a = os.path.join(racine, nom)
            b = os.path.join(dst, os.path.relpath(a, src))
            if os.path.exists(b) and open(a, 'rb').read() == open(b, 'rb').read():
                continue
            os.makedirs(os.path.dirname(b), exist_ok=True)
            shutil.copyfile(a, b)
            ecrits.append(b)


README_CDATSO = '''# montage-parallele (édition cdatso.be)

Édition cdatso.be du site « Montage Parallèle », servie par GitHub Pages à `https://montage-parallele.cdatso.be/`.

**Sortie générée** par `CD-Consulting-R-D/montage-parallele/outils/build_editions.py` à partir des textes de
`CD-Consulting-R-D/montage-parallele/source/` : ne pas éditer à la main. Toute correction se fait dans la source, puis
le script reconstruit les deux éditions.

Licences : textes CC BY-NC-SA 4.0 · code EUPL 1.2. Fontes : SIL Open Font License (`assets/fonts/LICENSE-*-OFL.txt`).
'''


if __name__ == '__main__':
    if len(sys.argv) > 1:
        raise SystemExit(__doc__)
    ecrits, comptes = construire()
    print('fichiers ecrits ou changes : %d' % len(ecrits))
    for c in ecrits:
        print('  ' + os.path.relpath(c, os.path.join(DEPOT, '..')))
    print('mots (edition, langue, page, compte / budget) :')
    for ed, lang, f, n in comptes:
        b = 1750 if f == 'TOTAL' else BUDGET[f]
        print('  %-7s %-3s %-16s %5d / %d%s' % (ed, lang, f, n, b, '' if n <= b * 1.1 else '  HORS BUDGET'))
