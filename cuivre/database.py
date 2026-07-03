import sqlite3


def creer_base():

    conn = sqlite3.connect("usine.db")
    cur = conn.cursor()

    # ================= PRODUCTION =================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS production(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        quantite REAL
    )
    """)

    # ================= STOCK =================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS stock(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        minerai REAL,
        cathodes REAL
    )
    """)

    # ================= FINANCE =================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS finance(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        revenus REAL,
        depenses REAL
    )
    """)

    # ================= EXTRACTION =================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS extraction(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        tonnage REAL,
        teneur REAL
    )
    """)

    # ================= BROYAGE =================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS broyage(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        entree REAL,
        sortie REAL
    )
    """)

    # ================= LIXIVIATION =================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS lixiviation(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        minerai_traite REAL,
        acide_utilise REAL
    )
    """)

    # ================= SX =================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS sx(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        solution_entree REAL,
        cuivre_extrait REAL
    )
    """)

    # ================= EW =================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS ew(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        cathodes_produites REAL
    )
    """)

    # ================= HISTORIQUE =================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS historique(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date_action TEXT,
        module TEXT,
        operation TEXT,
        valeur TEXT
    )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    creer_base()
    print("✅ Base de données usine créée avec succès")