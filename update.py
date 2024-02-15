import os
import sys
from dotenv import load_dotenv, find_dotenv

def update_token(new_token):
    try:
        # Mencari file .env
        dotenv_path = find_dotenv()

        # Load environment variable dari file .env
        load_dotenv(dotenv_path)

        # Ubah nilai dari environment variable 'TOKEN' dengan token baru
        os.environ['TOKEN'] = new_token

        # Baca semua baris dari file .env ke dalam list
        with open(dotenv_path, 'r') as f:
            lines = f.readlines()

        # Ubah nilai token di dalam list
        for i in range(len(lines)):
            if lines[i].startswith('TOKEN='):
                lines[i] = f"TOKEN={new_token}\n"
                break

        # Tulis kembali list ke file .env
        with open(dotenv_path, 'w') as f:
            f.writelines(lines)

        print("Token berhasil diperbarui di file .env.")
    except Exception as e:
        print("Gagal memperbarui token:", e)

if __name__ == "__main__":
    # Pastikan argumen yang diberikan sesuai
    if len(sys.argv) != 2:
        print("Penggunaan: python token.py <token_baru>")
        sys.exit(1)

    new_token = sys.argv[1]
    update_token(new_token)
