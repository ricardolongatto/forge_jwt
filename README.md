# forge_jwt

Ferramenta em Python para explorar e forjar tokens JWT, com foco em segurança ofensiva.

---
## Estrutura básica de um JWT

```
<HEADER>.<PAYLOAD>.<SIGNATURE>
```

- O header define o algoritmo (`alg`) e o tipo (`typ`)
- O payload contém as informações do usuário e outras claims
- A assinatura garante a integridade e autenticidade do token

---
## Funcionalidades

✅ **Visualizar conteúdo de um JWT**  
✅ **Realizar brute force para descobrir a chave secreta (HS256)**  
✅ **Forjar tokens válidos com payloads personalizados**  
✅ **Executar ataques clássicos como:**
- `alg: none` (assinatura ausente)
- `null signature` (assinatura inválida ou vazia)

---
## Requisitos

- Python 3.x
- Biblioteca `PyJWT` (instale com: `pip3 install PyJWT`)

---
## Exemplos de uso

### Mostrar conteúdo do token (decode sem validação)
```bash
python3 forge_jwt.py -t <token> -s
```

### Brute Force para descobrir a chave secreta
```bash
python3 forge_jwt.py -t <token> -w /caminho/para/wordlist.txt
```

### Forjar token com alterações (ex: virar admin)
```bash
python3 forge_jwt.py -t <token> -p c4mb10 -alg HS256 -d '{"role": "admin"}'
```

### Ataque `alg: none`
```bash
python3 forge_jwt.py -t <token> -na
```

### Ataque `null signature`
```bash
python3 forge_jwt.py -t <token> -ns
```

---

## Aviso legal

Esta ferramenta foi criada para **uso educativo** e em **testes de segurança ofensiva (Penetration Testing) contratados**.

**Jamais utilize para atacar sistemas de terceiros sem autorização.**
