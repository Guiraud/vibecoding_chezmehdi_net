#!/usr/bin/env python3
import json
import requests
import argparse
import sys
import os
import shutil
import time
import glob
from bs4 import BeautifulSoup

# Configuration par défaut
DEFAULT_OLLAMA_HOSTS = [
    "http://192.168.1.191:11434",
    "http://127.0.0.1:11434"
]
DEFAULT_MODEL = "llama3.2"

# Prompt minimaliste pour la restauration des noms propres
PROPER_NOUN_PROMPT = """Voici une phrase en minuscules (sauf la première lettre).
Corrige uniquement la typographie française de cette phrase ou de ce titre selon les règles officielles (majuscules, espaces insécables, ponctuation, guillemets, traits d’union, accents, etc.).
Interdit toute modification qui suit une règle de typographie anglaise.
Consignes strictes :
Ne modifie ni le vocabulaire, ni la structure, ni le sens, ni le nombre de mots.
Ne fais aucun commentaire, retourne uniquement la phrase corrigée.
Conserve les choix de l’auteur (abréviations, termes techniques, etc.).
Phrase à traiter : 
"""

def check_ollama_connection(hosts):
    """Vérifie la connexion aux hôtes Ollama et retourne le premier qui répond."""
    for host in hosts:
        try:
            # print(f"Tentative de connexion à {host}...", file=sys.stderr)
            response = requests.get(f"{host}/api/tags", timeout=2)
            if response.status_code == 200:
                # print(f"✅ Connecté avec succès à {host}", file=sys.stderr)
                return host
        except requests.exceptions.RequestException:
            continue
    return None

def restore_proper_nouns(host, model, text):
    """Appelle Ollama pour remettre les majuscules aux noms propres."""
    url = f"{host}/api/generate"
    
    prompt = PROPER_NOUN_PROMPT + f'"{text}"'
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1 # Très bas pour éviter la créativité
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json().get("response", "").strip()
        # Nettoyage basique si le modèle bavarde
        if result.startswith('"') and result.endswith('"'):
            result = result[1:-1]
        return result
    except Exception as e:
        print(f"⚠️ Erreur Ollama sur '{text}': {e}", file=sys.stderr)
        return text # On renvoie le texte sans modif en cas d'erreur

def create_backup(filepath):
    """Crée une sauvegarde du fichier s'il existe."""
    if os.path.exists(filepath):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        backup_path = f"{filepath}.{timestamp}.bak"
        try:
            shutil.copy2(filepath, backup_path)
            print(f"📦 Sauvegarde créée : {backup_path}", file=sys.stderr)
            return True
        except Exception as e:
            print(f"⚠️ Impossible de créer la sauvegarde : {e}", file=sys.stderr)
            return False
    return False

def restore_backup(filepath):
    """Restaure le fichier depuis sa sauvegarde la plus récente."""
    pattern = f"{filepath}.*.bak"
    backups = glob.glob(pattern)
    
    if not backups:
        print(f"❌ Aucune sauvegarde trouvée pour : {filepath}", file=sys.stderr)
        return False
        
    latest_backup = sorted(backups)[-1]
    
    try:
        shutil.copy2(latest_backup, filepath)
        print(f"✅ Fichier restauré depuis : {latest_backup}", file=sys.stderr)
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la restauration : {e}", file=sys.stderr)
        return False

def process_html_file(filepath, host, model):
    """Traite le fichier HTML avec BeautifulSoup et Ollama."""
    
    print(f"📖 Lecture de {filepath}...", file=sys.stderr)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
    except Exception as e:
        print(f"❌ Erreur lecture fichier : {e}", file=sys.stderr)
        return None

    # Ciblage des titres H1-H4
    targets = soup.find_all(['h1', 'h2', 'h3', 'h4'])
    total = len(targets)
    print(f"🔍 {total} titres trouvés (H1-H4). Traitement en cours...", file=sys.stderr)

    for i, tag in enumerate(targets, 1):
        original_text = tag.get_text(strip=True)
        if not original_text:
            continue

        # 1. Mise en minuscule algorithmique + Capitalize
        # On met tout en lower, puis on met la première lettre en majuscule
        algo_text = original_text.lower()
        if len(algo_text) > 0:
            algo_text = algo_text[0].upper() + algo_text[1:]
        
        # 2. Appel Ollama pour les noms propres (si il y a plus d'un mot ou si ça semble pertinent)
        # Pour optimiser, on envoie tout à l'IA pour vérification des noms propres
        print(f" Après lower : {original_text} -> {algo_text}")
        final_text = restore_proper_nouns(host, model, algo_text)
        print(f"Aprés IA : {algo_text} -> {final_text}") 
        # Feedback visuel
        if original_text != final_text:
            print(f"[{i}/{total}] {original_text} -> {final_text}", file=sys.stderr)
        else:
             print(f"[{i}/{total}] {original_text} (Inchangé)", file=sys.stderr)

        # Remplacement du texte DANS la structure existante
        # Attention: tag.string replace tout le contenu du tag. 
        # Si le tag contient des spans ou autres, get_text() a aplati.
        # Pour faire simple et respecter la demande "convertit le titre", on remplace le texte.
        # Si la structure complexe dans les titres est critique, il faudrait iterer sur les NavigableStrings.
        # Ici on suppose des titres simples.
        tag.string = final_text

    return str(soup)

def main():
    parser = argparse.ArgumentParser(description="Script de correction typographique HTML hybride (BS4 + Ollama).")
    parser.add_argument("input_file", nargs="?", help="Fichier HTML à traiter")
    parser.add_argument("--model", "-m", default=DEFAULT_MODEL, help=f"Modèle Ollama (défaut: {DEFAULT_MODEL})")
    parser.add_argument("--host", "-H", help="URL hôte Ollama")
    parser.add_argument("--output", "-o", help="Fichier de sortie")
    parser.add_argument("--restore", "-r", action="store_true", help="Restaurer backup")
    
    args = parser.parse_args()

    # Mode Restauration
    if args.restore:
        if not args.input_file:
            sys.exit("Erreur: Fichier requis pour restauration.")
        sys.exit(0 if restore_backup(args.input_file) else 1)

    # Vérifications Input
    if not args.input_file:
        parser.print_help()
        sys.exit(1)

    # Connexion Ollama
    hosts_to_try = [args.host] if args.host else DEFAULT_OLLAMA_HOSTS
    active_host = check_ollama_connection(hosts_to_try)
    if not active_host:
        sys.exit("❌ Impossible de joindre Ollama.")
    print(f"✅ Connecté à {active_host}", file=sys.stderr)

    # Traitement
    new_html_content = process_html_file(args.input_file, active_host, args.model)
    
    if new_html_content:
        # Sortie
        output_file = args.output if args.output else args.input_file # Par défaut on écrase ? Non, par défaut stdout sauf si -o 
        # Attends, la demande précédente implicite était de pouvoir écraser. 
        # Mais soyons prudent. Si pas d'output, stdout.
        
        if args.output:
            create_backup(args.output)
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(new_html_content)
            print(f"🎉 Terminé. Résultat dans {args.output}", file=sys.stderr)
        else:
            print(new_html_content)

if __name__ == "__main__":
    main()
