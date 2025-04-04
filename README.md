# 🚀 Projet Multi-Agents

Ce projet implémente une solution RAG (Retrieval-Augmented Generation) basée sur des agents spécialisés utilisant LangChain, OpenAI GPT-4, et FAISS, couplée à une interface web. L'objectif principal est de fournir des recommandations de formation personnalisées aux employés à partir d'évaluations initiales avec les 3 agents.

---

## 🎯 Objectifs

- Enrichir les évaluations d'employés grâce à une récupération d'informations pertinentes.
- Générer des recommandations spécifiques via trois agents spécialisés :
  - **Programmes de Formation**
  - **Meilleures Pratiques**
  - **Études de Cas**
- Offrir une expérience utilisateur agréable grâce à une interface front-end.

---

## 📂 Structure du projet

```
DevoTeam-Tek-test-Part-2/
├── agents/
│   └── multi_agent.py
│
├── api/
│   └── main.py
│
├── data/
│   ├── employe.json
│   ├── formation.json
│   ├── programmes.json
│   ├── pratiques.json
│   └── etudes.json
│
├── multi-agent-front/
│   ├── app/page.tsx
│   ├── components/Chat.tsx
│   ├── lib/
│   └── package.json
│
├── tests/
│   └── test_agents.py
│
├── vectors/
│   ├── programmes_faiss/
│   ├── pratiques_faiss/
│   └── etudes_faiss/
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

---

## ⚙️ Installation

### Cloner le projet

```bash
git clone <URL_de_ton_repo>
cd rag-multi-agent-demo
```

### Installer les dépendances

```bash
pip install -r requirements.txt
```

### Configurer l'environnement
Créer un fichier `.env` avec votre clé OpenAI :


```env
OPENAI_API_KEY=votre_cle_openai
```

Créer un fichier `.env.local` dans le dossier multi-agent-front:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🚀 Exécuter le projet

pour la base vectoriel

```bash
python creer_vectorstores.py
```


### Backend (API FastAPI)

```bash
uvicorn api.main:app --reload
```

L'API sera disponible sur [http://localhost:8000](http://localhost:8000).

### Frontend (Next.js)

```bash
cd multi-agent-front
npm install
npm run dev
```

Rendez-vous sur [http://localhost:3000](http://localhost:3000).

---

## ❓ Exemples de questions à poser à l'agent

- Quels programmes de formation recommandes-tu pour améliorer le leadership ?
- Quelles sont les meilleures pratiques pour la gestion du temps ?
- Peux-tu me donner un exemple réel d'une entreprise ayant amélioré sa communication interne ?
- Quelle formation est adaptée pour développer des compétences en management ?
- Donne-moi une étude de cas sur l'intégration d'une nouvelle technologie.

---

## 🧪 Tests

Exécutez les tests unitaires :

```bash
python -m unittest tests/test_agents.py
```

---

## 🛠️ Technologies utilisées

- **LangChain**
- **FAISS**
- **OpenAI GPT-4o**
- **FastAPI**
- **Next.js**
- **Tailwind CSS**

---

## 📚 Auteur

- Leonardo Basbous
