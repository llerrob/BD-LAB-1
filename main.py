import re


def check_password_strength(pwd: str, user_name: str, birth_date: str):
    issues = []

    uname = user_name.lower()
    pwd_lower = pwd.lower()

    translit_name = (
        uname.replace("і", "i")
             .replace("ї", "i")
             .replace("й", "i")
             .replace("в", "v")
             .replace("а", "a")
             .replace("н", "n")
    )

    if uname in pwd_lower or translit_name in pwd_lower:
        issues.append(f"У паролі використано ім’я або його транслітерацію ({user_name})")

    date_numbers = re.sub(r"[^\d]", "", birth_date)
    date_fragments = [
        date_numbers,
        date_numbers[-2:],
        date_numbers[:2],
        date_numbers[2:4]
    ]

    for fragment in date_fragments:
        if fragment and fragment in pwd:
            issues.append("У паролі присутні фрагменти дати народження")
            break

    length_points = min(len(pwd) / 2, 5)
    complexity_points = 0
    patterns = [r"[a-z]", r"[A-Z]", r"\d", r"[^a-zA-Z\d]"]

    for pattern in patterns:
        if re.search(pattern, pwd):
            complexity_points += 1

    raw_score = length_points + complexity_points
    final_score = max(1, min(10, int(raw_score - len(issues))))

    tips = []

    if uname in pwd_lower or translit_name in pwd_lower:
        tips.append("Уникайте використання власного імені в паролі.")
    if any(part in pwd for part in date_fragments):
        tips.append("Не варто включати дату народження до пароля.")
    if not re.search(r"[A-Z]", pwd):
        tips.append("Рекомендується додати великі літери.")
    if not re.search(r"\d", pwd):
        tips.append("Рекомендується використати цифри.")
    if not re.search(r"[^a-zA-Z\d]", pwd):
        tips.append("Додайте спеціальні символи (наприклад: !, @, #).")
    if len(pwd) < 12:
        tips.append("Збільште довжину пароля щонайменше до 12 символів.")

    print("\n=== ПІДСУМОК ПЕРЕВІРКИ ===")
    print(f"Рівень надійності: {final_score}/10")

    print("Знайдені зауваження:")
    if issues:
        for issue in issues:
            print(" -", issue)
    else:
        print(" - Персональні дані у паролі не виявлені")

    print("\nРекомендації щодо покращення:")
    for tip in tips:
        print(" -", tip)


if __name__ == "__main__":
    user_name = input("Вкажіть ваше ім’я: ")
    birth_date = input("Вкажіть дату народження (ДД.ММ.РРРР): ")
    pwd = input("Введіть пароль для аналізу: ")

    check_password_strength(pwd, user_name, birth_date)
