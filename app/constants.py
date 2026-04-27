
CHAMPS_A_EXTRAIRE = [
    "nom_fournisseur",
    "prix_unitaire",
    "quantite",
    "total",
    "total_ht",
    "tva",
    "ttc",
]

CHAMPS_OBLIGATOIRES = [
    "nom_fournisseur",
    "ttc",
]

COLONNES_EXPORT = [
    "nom_fournisseur",
    "prix_unitaire",
    "quantite",
    "total",
    "total_ht",
    "tva",
    "ttc",
]

DATA_SUBDIRECTORIES = [
    "uploads",
    "rendered_pages",
    "processed",
    "extracted_json",
    "exports",
    "temp",
    "logs",
]

MOTS_CLES_MONTANTS = {
    "prix_unitaire": [
        "prix unitaire",
        "p.u",
        "pu",
        "prix u",
        "prix unit",
        "prix/unit",
        "prix / unité",
    ],

    "quantite": [
        "quantite",
        "quantité",
        "qte",
        "qté",
        "qty",
        "nombre",
    ],

    "total": [
        "total",
        "montant",
        "montant ligne",
        "total ligne",
    ],

    "total_ht": [
        "total ht",
        "montant ht",
        "ht",
        "hors taxe",
        "hors taxes",
        "total hors taxe",
        "total hors taxes",
    ],

    "tva": [
        "tva",
        "taxe",
        "taxe sur la valeur ajoutée",
        "taxe sur la valeur ajoutee",
        "montant tva",
    ],

    "ttc": [
        "ttc",
        "total ttc",
        "montant ttc",
        "net à payer",
        "net a payer",
        "total à payer",
        "total a payer",
        "montant total",
        "total général",
        "total general",
    ],
}

MOTS_CLES_FOURNISSEUR = [
    "fournisseur",
    "vendeur",
    "société",
    "societe",
    "entreprise",
    "raison sociale",
]

DEVISE_DIRHAM = [
    "mad",
    "dh",
    "dhs",
    "dh.",
    "dhs.",
    "dirham",
    "dirhams",
    "د.م",
    "درهم",
    "دراهم",
]

MOTS_IGNORES_FOURNISSEUR = {
    "facture",
    "client",
    "date",
    "total",
    "total ht",
    "total ttc",
    "ttc",
    "tva",
    "quantite",
    "quantité",
    "prix",
    "prix unitaire",
    "montant",
    "page",
    "adresse",
    "telephone",
    "téléphone",
    "email",
    "ice",
    "if",
    "rc",
}

COLONNES_AUDIT = [
    "nom_fichier",
    "numero_page",
    "confiance_ocr",
    "statut",
    "notes",
]