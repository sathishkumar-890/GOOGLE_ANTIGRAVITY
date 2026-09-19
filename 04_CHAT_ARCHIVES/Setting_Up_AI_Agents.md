# Chat Archive: Setting Up AI Agents

- **Conversation ID**: `ee68b143-78fb-4822-a649-4fea485846b5`
- **Last Modified**: 2026-09-19 13:54:17.1761818+00:00
- **Total Messages**: 4

---

### 👤 User:
நான் எப்படி ஏ ஏஜென்ட் நான் இங்க வைக்கிறது? என்னோட டாஸ்க்க அந்த ஏ ஏஜென்ட் வந்து பண்ண சொல்லணும். ஃபார் எக்ஸாம்பிள் நான் அந்த சாட்ஸ்ல வந்துட்டு நான் வி எக்ஸ்ட்ராக்ஷன் ஸ்பேர் எக்ஸ்ட்ராக்ஷன் போட்டோ எடிட் பண்றதுக்கு இந்த மாதிரி தனித்தனி எக்ஸ்ட்ராக்ஷன் சாட்ல தான் நான் ப்ராம்ட் போட்டு வச்சிருக்கேன். இனிமே நான் வந்து ஒரு ஏஜென்ட் அந்த மாதிரி வச்சிரணும். ஒவ்வொன்னுக்கு ஒரு ஏஜென்ட் வச்சிரணும். விஎல் எக்ஸ்ட்ராக்ஷனுக்கு ஒரு ஏஜென்ட், ஸ்பேர் ஏஜென்ட் என்னோட வெப் ஆப் வந்துட்டு எடிட் பண்றதுக்கு ஒரு ஏஜென்ட் வச்சுக்கணும். அதுக்கு நான் என்ன பண்ணனும்? சில ஸ்டெப்ஸ் பண்ணு எனக்கு.

### 🤖 Antigravity Agent:
சரி! இப்போது உங்களுக்கு தெளிவான விளக்கம் தருகிறேன். Antigravity-ல் **Skills** என்ற feature உள்ளது — இதுதான் உங்களுக்கு வேண்டியது.

---

## Antigravity-ல் Agent (Skill) எப்படி உருவாக்குவது?

### Skill என்றால் என்ன?

ஒவ்வொரு Skill-உம் ஒரு "specialized agent" போல் செயல்படும். நீங்கள் ஒரு Skill உருவாக்கி வைத்தால், அந்த குறிப்பிட்ட task-க்கு chat-ல் prompts type பண்ண வேண்டாம் — agent தானாக அந்த Skill-ஐ பயன்படுத்தும்.

---

### Step-by-Step: மூன்று Skills உருவாக்குவதற்கு

உங்கள் project folder-ல் இந்த structure உருவாக்கவும்:

```
your-project/
└── .agents/
    └── skills/
        ├── vl-extraction/
        │   └── SKILL.md
        ├── spare-extraction/
        │   └── SKILL.md
        └── webapp-editor/
            └── SKILL.md
```

---

### Step 1: `.agents/skills/` folder உருவாக்கு

---

### 🤖 Antigravity Agent:
### Step 2: மூன்று SKILL.md files உருவாக்கு

இவை template files மட்டும் — உங்கள் actual prompts இவற்றில் நீங்கள் சேர்க்க வேண்டும்:

---

### 🤖 Antigravity Agent:
---

## ✅ உருவாக்கப்பட்டது! இப்போது இந்த structure உள்ளது:

```
test/
└── .agents/
    └── skills/
        ├── vl-extraction/
        │   └── SKILL.md  ← VL Extraction Agent
        ├── spare-extraction/
        │   └── SKILL.md  ← Spare Extraction Agent
        └── webapp-editor/
        │   └── SKILL.md  ← Web App Editor Agent
```

---

## 🔑 Key Steps — இனி என்ன பண்ண வேண்டும்:

### 1️⃣ உங்கள் Prompts சேர்க்கவும்

ஒவ்வொரு SKILL.md-லும் உங்களிடம் இப்போது இருக்கும் prompts-ஐ `## Steps` section-ல் paste பண்ணுங்கள்:

- [`vl-extraction/SKILL.md`](file:///C:/Users/User/Documents/antigravity/test/.agents/skills/vl-extraction/SKILL.md) — உங்கள் VL extraction prompt
- [`spare-extraction/SKILL.md`](file:///C:/Users/User/Documents/antigravity/test/.agents/skills/spare-extraction/SKILL.md) — உங்கள் Spare extraction prompt  
- [`webapp-editor/SKILL.md`](file:///C:/Users/User/Documents/antigravity/test/.agents/skills/webapp-editor/SKILL.md) — உங்கள் Web app edit prompt

### 2️⃣ Chat-ல் எப்படி Use பண்றது?

Skills automatic ஆக detect ஆகும். நீங்கள் சொன்னால் போதும்:
- *"VL extraction பண்ணு"* → `vl-extraction` skill activate ஆகும்
- *"Spare extraction பண்ணு"* → `spare-extraction` skill activate ஆகும்
- *"Web app-ல் இதை மாத்து"* → `webapp-editor` skill activate ஆகும்

### 3️⃣ Important — `description` field

SKILL.md-ல் `description:` என்பது மிகவும் முக்கியம். Agent இதை படித்து, user என்ன கேட்கிறார் என்று match பண்ணி skill-ஐ activate பண்ணும். **உங்கள் Tamil keywords-ஐயும் description-ல் சேர்க்கலாம்** — நான் ஏற்கனவே சேர்த்துள்ளேன்.

---

## 💡 SKILL.md-ல் என்ன போட வேண்டும்?

உங்கள் current prompt இப்படி இருந்தால்:
> *"You are a VL extraction expert. Extract the following fields from the document: part number, description..."*

அதை அப்படியே SKILL.md-ல் `## Instructions` section-ல் வையுங்கள். Agent அதை follow பண்ணும்.

---

**அடுத்த கேள்வி**: உங்கள் existing VL / Spare extraction prompts share பண்ண முடியுமா? அதை directly SKILL.md-ல் paste பண்ணி தருகிறேன்! 🚀

---

