SUPPORTED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}

REQUIRED_FIELDS = ("nom_destinataire", "total_ht")

EXPORT_COLUMNS = [
    "nom_destinataire",
    "nom_fournisseur",
    "numero_facture",
    "date_facture",
    "designation",
    "qte",
    "prix",
    "prix_unitaire_ht",
    "total_ligne",
    "total_ht_ligne",
    "total_ht_facture",
    "tva",
    "ttc",
    "currency",
]

VALID_CURRENCIES = {"DH", "MAD", "dirham", "dirhams"}

TARGET_FIELDS = [
    "nom_destinataire",
    "nom_fournisseur",
    "numero_facture",
    "date_facture",
    "total_ht",
    "tva",
    "ttc",
    "currency",
    "line_items",
]