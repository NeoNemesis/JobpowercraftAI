# 🔒 SÄKERHETSGUIDE - JobCraftAI

## ✅ Säkerhetsfixar Implementerade

Följande kritiska säkerhetsproblem har åtgärdats:

### 1. 🚨 API Key Logging - FIXAD
- **Problem**: API-nycklar loggades i `open_ai_calls.json`
- **Åtgärd**: Implementerat `SecurityValidator.sanitize_for_logging()` som tar bort API-nycklar, lösenord och tokens innan loggning
- **Fil**: `src/libs/llm_manager.py` (rad 220-325)

### 2. 🚨 Email Validering - FIXAD
- **Problem**: Ingen validering av email-adresser (risk för injection)
- **Åtgärd**: RFC 5322-kompatibel regex-validering + kontroll för farliga tecken
- **Fil**: `src/security_utils.py` + `src/email_sender.py`

### 3. 🚨 URL Validering - FIXAD
- **Problem**: Användare kunde ange `javascript:` eller `file://` URLs
- **Åtgärd**: Whitelist för HTTP/HTTPS, blockerar localhost och interna IP-adresser (SSRF-skydd)
- **Fil**: `src/security_utils.py` + `main.py`

### 4. 🚨 Lösenordshantering - FIXAD
- **Problem**: SMTP-lösenord i klartext i YAML-filer
- **Åtgärd**: Environment variables via `SecurePasswordManager`
- **Fil**: `src/security_utils.py` + `src/email_sender.py`

---

## 🚀 SETUP-INSTRUKTIONER

### Steg 1: Installera Dependencies

```powershell
pip install -r requirements.txt
```

### Steg 2: Konfigurera Environment Variables (VIKTIGT!)

#### Windows PowerShell:

**Tillfälligt (bara för nuvarande session):**
```powershell
$env:JOBCRAFT_SMTP_PASSWORD = "ditt-gmail-app-password"
$env:JOBCRAFT_API_KEY = "sk-din-openai-api-key"
```

**Permanent (rekommenderat):**
```powershell
# Öppna System Environment Variables
[System.Environment]::SetEnvironmentVariable('JOBCRAFT_SMTP_PASSWORD', 'ditt-password', 'User')
[System.Environment]::SetEnvironmentVariable('JOBCRAFT_API_KEY', 'din-api-key', 'User')

# Starta om PowerShell efter detta!
```

#### Linux/Mac (Bash/Zsh):

**Tillfälligt:**
```bash
export JOBCRAFT_SMTP_PASSWORD="ditt-gmail-app-password"
export JOBCRAFT_API_KEY="din-openai-api-key"
```

**Permanent (lägg till i ~/.bashrc eller ~/.zshrc):**
```bash
echo 'export JOBCRAFT_SMTP_PASSWORD="ditt-password"' >> ~/.bashrc
echo 'export JOBCRAFT_API_KEY="din-api-key"' >> ~/.bashrc
source ~/.bashrc
```

### Steg 3: Uppdatera Email-konfiguration

Redigera `data_folder/email_config.yaml` och **ta bort** password-raden:

```yaml
smtp_server: 'smtp.gmail.com'
smtp_port: 587
email: 'din.email@gmail.com'
# password: 'TA BORT DENNA RAD!'  # Hämtas nu från environment variable
sender_name: 'Ditt Namn'
```

### Steg 4: (Valfritt) Använd .env-fil

För lokal utveckling kan du skapa en `.env`-fil i projektroten:

```bash
# .env
JOBCRAFT_SMTP_PASSWORD=ditt-gmail-app-password
JOBCRAFT_API_KEY=sk-din-openai-api-key
```

**VIKTIGT**: Lägg till `.env` i `.gitignore`!

```bash
echo ".env" >> .gitignore
```

---

## ✅ Verifiera Installation

Kör detta test för att kontrollera att allt fungerar:

```powershell
python -c "from src.security_utils import SecurityValidator, SecurePasswordManager; print('✅ Security utils loaded'); print('Password:', 'SET' if SecurePasswordManager.get_smtp_password() else 'NOT SET')"
```

Du bör se:
```
✅ Security utils loaded
Password: SET
```

---

## 📋 Säkerhetschecklist Innan Produktion

- [ ] **Environment variables satta** - Kör `echo $env:JOBCRAFT_SMTP_PASSWORD` (ska inte vara tom)
- [ ] **Lösenord borttaget från YAML** - Kontrollera `data_folder/email_config.yaml`
- [ ] **API-nyckel borttagen från YAML** - Kontrollera `data_folder/secrets.yaml`
- [ ] **.env i .gitignore** - Kör `git check-ignore .env` (ska returnera `.env`)
- [ ] **Gamla logs rensade** - Ta bort gamla `open_ai_calls.json` som kan innehålla API-nycklar
- [ ] **Dependencies uppdaterade** - Kör `pip list --outdated` och uppdatera kritiska paket

---

## 🛡️ Vad Händer Nu?

### Vid Email-sändning:
1. ✅ Email-adress valideras med regex
2. ✅ Farliga tecken blockeras (|, ;, &, $, `)
3. ✅ Lösenord hämtas från environment variable (inte YAML)

### Vid Jobb-URL Inmatning:
1. ✅ URL parsas och valideras
2. ✅ Endast HTTP/HTTPS tillåts (blockerar `javascript:`, `file://`)
3. ✅ Localhost och interna IPs blockeras (SSRF-skydd)

### Vid LLM API-anrop:
1. ✅ Prompts saniteras innan loggning
2. ✅ API-nycklar tas bort med regex
3. ✅ Lösenord tas bort från loggade data

---

## 🚨 Kända Begränsningar

### Fortfarande Ej Fixat (Medium Priority):
1. **Rate Limiting** - Ingen begränsning på antal emails/dag
2. **SQLite istället för YAML** - Jobbloggar sparas fortfarande i YAML
3. **Dependency vulnerabilities** - `selenium==4.9.1` är 1.5 år gammal

### För Framtida Förbättringar:
- Implementera `pip-audit` i CI/CD
- Lägg till rate limiting för email-sändning
- Migrera från YAML till SQLite för strukturerad data
- Lägg till unit tests för säkerhetsfunktioner

---

## 📞 Support

Om du stöter på problem:
1. Kontrollera att environment variables är satta: `echo $env:JOBCRAFT_SMTP_PASSWORD`
2. Kör `python main.py` och leta efter `⚠️ WARNING` meddelanden
3. Kontrollera logs i `log/app.log`

---

## 🎯 Sammanfattning

**INNAN säkerhetsfixar:**
- ❌ API-nycklar loggades i klartext
- ❌ Lösenord i YAML-filer
- ❌ Ingen email/URL validering
- ⚠️ Risk för injection-attacker

**EFTER säkerhetsfixar:**
- ✅ API-nycklar saniteras före loggning
- ✅ Lösenord i environment variables
- ✅ RFC-kompatibel email-validering
- ✅ URL whitelist och SSRF-skydd

**Nu kan du köra programmet säkert! 🚀**

```powershell
python main.py
```

