# Architecture Decision Records

- [0005](0005-composed-emoji-faces.md): random emoji is a composed ASCII face, as big as a big animal, with one-line kaomoji kept behind `big=False`
- [0004](0004-detect-stale-installed-copies.md): a stale installed copy is detected and reported (`--version`, stderr warning, editable installs), never auto-reinstalled
- [0003](0003-composed-random-art-and-animals.md): random art and random animals are composed (coin / frame / themed scene via the smart generator), not fixed drawings or character noise
- [0002](0002-figlet-fonts-via-pyfiglet.md): text-to-ASCII renders through optional pyfiglet (FIGlet fonts), with built-in fonts as fallback
- [0001](0001-taught-mood-synonyms.md): mood vocabulary grows via a user-taught `teach` command, persisted per-user, not automatic prompting or NLP
