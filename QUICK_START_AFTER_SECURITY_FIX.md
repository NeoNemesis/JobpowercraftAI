# 🚀 SNABBSTART - JobCraftAI (Efter Säkerhetsfixar)

## ✅ Vad har fixats?

1. ✅ **API-nycklar saniteras** - Loggas inte längre i klartext
2. ✅ **Email-validering** - RFC 5322-kompatibel regex + injection-skydd
3. ✅ **URL-validering** - Blockerar farliga URLs (`javascript:`, `file://`, localhost)
4. ✅ **Säkra lösenord** - Environment variables istället för YAML

---

## 🎯 STEG 1: Installera Dependencies

```powershell
pip install -r requirements.txt
```

**Vänta tills alla paket är installerade (~30 sekunder)**

---

## 🔑 STEG 2: Sätt Environment Variables (VIKTIGT!)

### Windows PowerShell (Kopiera och kör):

```powershell
# Sätt din OpenAI API-nyckel (från secrets.yaml)
$env:JOBCRAFT_API_KEY = "your-openai-api-key-here"

# Sätt ditt Gmail App Password (endast om du ska skicka email)
# $env:JOBCRAFT_SMTP_PASSWORD = "ditt-app-password-här"
```

**Verifiera att det fungerar:**
```powershell
echo $env:JOBCRAFT_API_KEY
# Ska visa: sk-proj-... (din API-nyckel)
```

---

## ▶️ STEG 3: Kör Programmet!

```powershell
python main.py
```

### Vad händer nu?

1. **Välj åtgärd** från menyn:
   ```
   ● Generate Resume
   ● Generate Resume Tailored for Job Description
   ● Generate Tailored Cover Letter for Job Description
   ● Generate and Send Job Application via Email
   ```

2. **Välj CV-modell**:
   - `URSPRUNGLIGA` - Klassiska mallar
   - `MODERN_DESIGN_1` - Moderna professionella mallar
   - `MODERN_DESIGN_2` - Kreativa sidopanel-mallar

3. **Välj mall/template**

4. **Ange jobb-URL** (om du valde "Tailored")
   - ✅ URL valideras automatiskt för säkerhet
   - ❌ Farliga URLs blockeras

5. **Vänta medan AI genererar dokumentet** (~10-30 sekunder)

6. **Hitta ditt PDF** i: `data_folder/output/[hash]/`

---

## 📧 STEG 4: Email-funktion (Valfritt)

Om du vill använda "Generate and Send Job Application via Email":

### 4a. Skaffa Gmail App Password:

1. Gå till: https://myaccount.google.com/security
2. Aktivera **2-stegsverifiering**
3. Gå till **Applösenord** (App Passwords)
4. Generera lösenord för "Mail"
5. Kopiera lösenordet (16 tecken, t.ex. `abcd efgh ijkl mnop`)

### 4b. Uppdatera email_config.yaml:

Redigera `data_folder/email_config.yaml`:

```yaml
smtp_server: 'smtp.gmail.com'
smtp_port: 587
email: 'din.email@gmail.com'  # Ändra till din email
sender_name: 'Ditt Namn'       # Ändra till ditt namn
```

**TA BORT** `password:`-raden om den finns!

### 4c. Sätt environment variable:

```powershell
$env:JOBCRAFT_SMTP_PASSWORD = "ditt-app-password-från-steg-4a"
```

### 4d. Testa email-funktion:

```powershell
python main.py
# Välj: "Generate and Send Job Application via Email"
```

---

## ⚠️ Troubleshooting

### Problem: "Module not found: src.security_utils"

**Lösning:**
```powershell
# Kontrollera att filen finns
ls src/security_utils.py

# Om den saknas, kör:
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Problem: "API key not found"

**Lösning:**
```powershell
# Kontrollera environment variable
echo $env:JOBCRAFT_API_KEY

# Om tom, sätt den igen
$env:JOBCRAFT_API_KEY = "sk-din-api-key"
```

### Problem: "Invalid email format"

**Lösning:**
- Email-validering är NU aktiverad (säkerhetsfix!)
- Kontrollera att email-adressen är korrekt formaterad: `user@domain.com`
- Inga specialtecken som `|`, `;`, `&` tillåts (säkerhet)

### Problem: "Invalid URL scheme"

**Lösning:**
- URL-validering är NU aktiverad (säkerhetsfix!)
- Använd endast `http://` eller `https://` URLs
- `file://` och `javascript:` blockeras av säkerhetsskäl

---

## 🎯 Vanliga Use Cases

### 1. Snabbt Generera CV för Specifikt Jobb

```powershell
python main.py
# 1. Välj: "Generate Resume Tailored for Job Description"
# 2. Välj modell: MODERN_DESIGN_1
# 3. Välj mall (valfri)
# 4. Klistra in jobb-URL från LinkedIn/TheHub
# 5. Vänta 20 sekunder
# 6. PDF sparas i: data_folder/output/
```

### 2. Generera Personligt Brev

```powershell
python main.py
# 1. Välj: "Generate Tailored Cover Letter for Job Description"
# 2. Välj modell och mall
# 3. Ange jobb-URL
# 4. Personligt brev genereras automatiskt
```

### 3. Komplett Ansökan via Email

```powershell
python main.py
# 1. Välj: "Generate and Send Job Application via Email"
# 2. Välj modell och mall
# 3. Ange jobb-URL
# 4. Ange mottagarens email
# 5. Ange företag och position
# 6. Email skickas automatiskt med CV + brev!
```

---

## 📊 Vad Händer I Bakgrunden?

1. **URL valideras** 🔒
   - Kontrollerar att URL är säker
   - Blockerar localhost/interna IPs (SSRF-skydd)

2. **Jobb skrapas** 🌐
   - Chrome öppnas automatiskt (headless)
   - Jobbbeskrivning extraheras med AI

3. **CV anpassas** 🤖
   - OpenAI API analyserar jobbkrav
   - Ditt CV optimeras för specifik position
   - HTML genereras från vald mall

4. **PDF skapas** 📄
   - Chrome konverterar HTML → PDF
   - Sparas med unikt filnamn

5. **Email skickas** 📧 (om valt)
   - Email valideras 🔒
   - Lösenord från environment variable (säkert!)
   - CV och brev bifogas
   - Gmail SMTP skickar email

---

## 🎉 Klart!

Du kan nu köra programmet säkert med:
- ✅ Saniterade API-logs
- ✅ Validerade emails
- ✅ Säkra URLs
- ✅ Environment variable-lösenord

**Lycka till med jobbansökningarna! 🚀**

---

## 📞 Behöver Hjälp?

1. Läs fullständig guide: `SECURITY_SETUP_GUIDE.md`
2. Kontrollera logs: `log/app.log`
3. Kontakta Victor Vilches: victorvilches@protonmail.com

