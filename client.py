import requests
import sys
import time

BASE_URL = "http://127.0.0.1:8000"

USERS = {
    "user1": "key-user-1",
    "user2": "key-user-2"
}


# =========================
# REQUEST FUNCTIONS
# =========================
def encrypt(text, user):
    res = requests.post(
        f"{BASE_URL}/crypt",
        headers={"x-api-key": USERS[user]},
        json={"text": text}
    )
    return res.json()


def decrypt(text, user):
    res = requests.post(
        f"{BASE_URL}/decrypt",
        headers={"x-api-key": USERS[user]},
        json={"text": text}
    )
    return res.json()


# =========================
# STRESS TEST
# =========================
def stress_test(user, count=1000):
    print(f"🚀 Stress test başlıyor ({count} request)...")

    start = time.time()

    for i in range(count):
        encrypt(f"test-{i}", user)

    end = time.time()

    print(f"Bitti!")
    print(f"Süre: {end - start:.2f} saniye")
    print(f"RPS: {count / (end - start):.2f} request/s")


# =========================
# CLI
# =========================
def main():
    if len(sys.argv) < 2:
        print("""
KULLANIM:

Encrypt:
python client.py encrypt user1 "Merhaba Dünya"

Decrypt:
python client.py decrypt user1 "encrypted_text"

Stress test:
python client.py stress user1 1000
        """)
        return

    command = sys.argv[1]

    # =========================
    # ENCRYPT
    # =========================
    if command == "encrypt":
        user = sys.argv[2]
        text = sys.argv[3]

        result = encrypt(text, user)
        print("RESULT:", result)

    # =========================
    # DECRYPT
    # =========================
    elif command == "decrypt":
        user = sys.argv[2]
        text = sys.argv[3]

        result = decrypt(text, user)
        print("RESULT:", result)

    # =========================
    # STRESS TEST
    # =========================
    elif command == "stress":
        user = sys.argv[2]
        count = int(sys.argv[3]) if len(sys.argv) > 3 else 1000

        stress_test(user, count)

    else:
        print("❌ Unknown command")


if __name__ == "__main__":
    main()
