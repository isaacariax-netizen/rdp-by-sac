import os
import re
import time

def clean_filename(name):
    return name.replace("https://", "").replace("http://", "").replace("/", "").replace(":", "").replace(".", "_")

def human_readable_size(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"

def extract_both_combos_from_lines(lines):
    email_pattern = re.compile(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+):([^\s:]+)')
    user_pattern = re.compile(r'\b([a-zA-Z0-9_.+-]{3,}):([^\s:]+)\b')
    seen_email = set()
    seen_user = set()
    email_combos = []
    user_combos = []

    for line in lines:
        email_matches = email_pattern.findall(line)
        if email_matches:
            email, pwd = email_matches[-1]
            key = f"{email.lower()}:{pwd}"
            if key not in seen_email:
                seen_email.add(key)
                email_combos.append(key)
        else:
            user_matches = user_pattern.findall(line)
            if user_matches:
                user, pwd = user_matches[-1]
                if "@" not in user:  # avoid email-looking usernames
                    key = f"{user}:{pwd}"
                    if key.lower() not in seen_user:
                        seen_user.add(key.lower())
                        user_combos.append(key)
    return email_combos, user_combos

def process_file(input_file, keywords, keyword_lines, keyword_seen, keyword_dupes, file_counter, total_files):
    file_size = os.path.getsize(input_file)
    print(f"📦 Processing file {file_counter}/{total_files}: {input_file} ({human_readable_size(file_size)})")
    file_lines = {k: 0 for k in keywords}
    file_dupes = {k: 0 for k in keywords}

    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line_clean = line.strip()
            if not line_clean:
                continue
            for keyword in keywords:
                if keyword in line_clean.lower():
                    if line_clean not in keyword_seen[keyword]:
                        keyword_lines[keyword].append(line_clean)
                        keyword_seen[keyword].add(line_clean)
                        file_lines[keyword] += 1
                    else:
                        keyword_dupes[keyword] += 1
                        file_dupes[keyword] += 1
                    break
    for keyword in keywords:
        if file_lines[keyword] > 0 or file_dupes[keyword] > 0:
            print(f"   ➤ Keyword: {keyword} - Found {file_lines[keyword]} lines ({file_dupes[keyword]} duplicates)")

def main():
    folder_path = "ulp"
    if not os.path.exists(folder_path):
        print(f"❌ Folder '{folder_path}' not found!")
        return
    input_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    if not input_files:
        print(f"❌ No files found in folder '{folder_path}'!")
        return

    total_files = len(input_files)
    print(f"📂 Found {total_files} files in '{folder_path}'")

    # Step 1: Get email-based keywords
    email_input = input("🔍 Enter EMAIL domain keywords (comma-separated): ").strip()
    email_keywords = [k.strip().lower() for k in email_input.split(",")] if email_input else []

    # Step 2: Get username-based keywords
    user_input = input("🔍 Enter USERNAME keywords (comma-separated): ").strip()
    user_keywords = [k.strip().lower() for k in user_input.split(",")] if user_input else []

    all_keywords = email_keywords + user_keywords
    if not all_keywords:
        print("❌ No keywords provided.")
        return

    keyword_lines = {k: [] for k in all_keywords}
    keyword_seen = {k: set() for k in all_keywords}
    keyword_dupes = {k: 0 for k in all_keywords}

    print(f"🔄 Processing {total_files} files in '{folder_path}'...")
    start_time = time.time()

    file_counter = 0
    for input_file in input_files:
        if os.path.isfile(input_file):
            file_counter += 1
            process_file(input_file, all_keywords, keyword_lines, keyword_seen, keyword_dupes, file_counter, total_files)

    print("💾 Extracting combos...\n")

    for keyword in all_keywords:
        lines = keyword_lines[keyword]
        dupes = keyword_dupes[keyword]
        if not lines:
            print(f"⚠️ Keyword: {keyword} - No matching lines found.")
            continue

        emailpass_list, userpass_list = extract_both_combos_from_lines(lines)

        if keyword in email_keywords and emailpass_list:
            combo_file = f"emailpass_{clean_filename(keyword)}.txt"
            with open(combo_file, 'a', encoding='utf-8') as f1:
                for combo in sorted(emailpass_list):
                    f1.write(combo + "\n")
            print(f"✅ Keyword: {keyword} (email)")
            print(f"   ➤ Unique matched lines: {len(lines)}")
            print(f"   ➤ Duplicate lines skipped: {dupes}")
            print(f"   ➤ Extracted email:pass: {len(emailpass_list)}")
            print(f"   🔐 Saved to: {combo_file}\n")

        if keyword in user_keywords and userpass_list:
            combo_file = f"userpass_{clean_filename(keyword)}.txt"
            with open(combo_file, 'a', encoding='utf-8') as f2:
                for combo in sorted(userpass_list):
                    f2.write(combo + "\n")
            print(f"✅ Keyword: {keyword} (user)")
            print(f"   ➤ Unique matched lines: {len(lines)}")
            print(f"   ➤ Duplicate lines skipped: {dupes}")
            print(f"   ➤ Extracted user:pass: {len(userpass_list)}")
            print(f"   🔐 Saved to: {combo_file}\n")

    end_time = time.time()
    total_sec = end_time - start_time
    if total_sec < 60:
        print(f"⏱ Processing time: {total_sec:.2f} seconds")
    else:
        minutes = total_sec // 60
        seconds = total_sec % 60
        print(f"⏱ Processing time: {int(minutes)} min {int(seconds)} sec")

    print(f"🎉 Done! Processed {file_counter}/{total_files} files.")

if __name__ == "__main__":
    main()