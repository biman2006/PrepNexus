




"""
Enhanced Master Skills Database
Production-grade for:
- Resume parsing
- ATS systems
- Job-role matching
- RAG pipelines
- Semantic search
- Startup hiring intelligence
"""

# =====================================================
# MASTER SKILL LIST
# =====================================================

all_skills = [
    # Programming Languages
    "python", "c", "c++", "java", "javascript", "typescript", "sql",
    "html", "css", "bash", "powershell", "go", "rust", "kotlin",
    "swift", "php", "ruby", "r", "matlab", "scala", "perl",

    # Core CS
    "data structures", "algorithms", "oop", "object oriented programming",
    "dbms", "operating systems", "computer networks", "system design",

    # Frontend
    "react", "next.js", "vue.js", "angular", "tailwind css",
    "bootstrap", "redux", "html5", "css3", "responsive design",

    # Backend
    "node.js", "express.js", "django", "flask", "fastapi",
    "spring boot", "rest api", "graphql", "jwt", "oauth",

    # Databases
    "mysql", "postgresql", "mongodb", "redis", "sqlite",
    "snowflake", "bigquery", "etl", "data warehousing",

    # Mobile
    "flutter", "dart", "react native", "android", "kotlin", "swift",

    # Data Analysis
    "excel", "power bi", "tableau", "pandas", "numpy",
    "matplotlib", "seaborn", "statistics", "probability",
    "data cleaning", "exploratory data analysis", "feature engineering",
    "dashboard development", "data visualization",

    # Big Data
    "apache spark", "hadoop", "kafka", "airflow",

    # Machine Learning
    "machine learning", "linear regression", "logistic regression",
    "decision trees", "random forest", "gradient descent",
    "xgboost", "lightgbm", "scikit-learn", "mlops",

    # Deep Learning
    "tensorflow", "pytorch", "keras", "cnn", "rnn", "lstm",
    "transformers", "bert", "gpt", "large language models",
    "fine-tuning", "lora", "qlora",

    # AI / LLMOps
    "natural language processing", "computer vision",
    "langchain", "llamaindex", "retrieval-augmented generation",
    "rag", "faiss", "chromadb", "pinecone",
    "prompt engineering", "openai api", "hugging face",
    "langgraph", "streamlit", "gradio",
    "semantic search", "multi-agent systems",

    # Cloud / DevOps
    "aws", "azure", "google cloud platform",
    "docker", "kubernetes", "terraform",
    "ci/cd", "jenkins", "github actions",
    "linux", "prometheus", "grafana",

    # Cybersecurity
    "network security", "siem", "penetration testing",
    "ethical hacking", "incident response",

    # Testing
    "selenium", "playwright", "pytest", "junit",
    "manual testing", "api testing",

    # UI/UX
    "figma", "adobe xd", "wireframing", "prototyping",

    # Product
    "agile", "scrum", "jira", "product strategy",

    # Blockchain
    "solidity", "ethereum", "web3", "smart contracts",

    # IoT / Robotics
    "arduino", "raspberry pi", "mqtt", "robotics", "ros",

    # Soft Skills
    "problem solving", "debugging", "leadership",
    "technical documentation", "product thinking"
]

# =====================================================
# SKILL ALIASES / NORMALIZATION
# =====================================================

skill_aliases = {
    "py": "python",
    "python3": "python",
    "js": "javascript",
    "ts": "typescript",
    "react.js": "react",
    "reactjs": "react",
    "nextjs": "next.js",
    "vue": "vue.js",
    "vuejs": "vue.js",
    "node": "node.js",
    "express": "express.js",
    "ml": "machine learning",
    "dl": "deep learning",
    "nlp": "natural language processing",
    "cv": "computer vision",
    "llm": "large language models",
    "llms": "large language models",
    "genai": "generative ai",
    "rag": "retrieval-augmented generation",
    "postgres": "postgresql",
    "mongo": "mongodb",
    "gcp": "google cloud platform",
    "k8s": "kubernetes",
    "tf": "tensorflow",
    "hf": "hugging face",
    "pbi": "power bi"
}

# =====================================================
# MASTER SKILLS BUILD
# =====================================================

def build_master_skills():
    combined_skills = list(all_skills)
    combined_skills.extend(skill_aliases.keys())
    return sorted(set(skill.lower() for skill in combined_skills))


ALL_SKILLS = build_master_skills()

# =====================================================
# NORMALIZE SKILL
# =====================================================

def normalize_skill(skill: str) -> str:
    skill = skill.strip().lower()
    return skill_aliases.get(skill, skill)

# =====================================================
# IMPLICIT SKILL INFERENCE MAP
# =====================================================

skill_inference_map = {
    # Data
    "pandas": [
        "data cleaning",
        "data analysis",
        "data manipulation",
        "exploratory data analysis"
    ],
    "numpy": [
        "numerical computing",
        "data analysis"
    ],
    "matplotlib": [
        "data visualization"
    ],
    "seaborn": [
        "data visualization"
    ],
    "power bi": [
        "dashboard development",
        "business intelligence"
    ],
    "tableau": [
        "dashboard development",
        "data visualization"
    ],
    "excel": [
        "data cleaning",
        "reporting",
        "business analysis"
    ],

    # ML / AI
    "scikit-learn": [
        "machine learning",
        "model building"
    ],
    "tensorflow": [
        "deep learning",
        "neural networks"
    ],
    "pytorch": [
        "deep learning",
        "model training"
    ],
    "langchain": [
        "llm applications",
        "retrieval-augmented generation"
    ],
    "faiss": [
        "vector search",
        "semantic retrieval"
    ],
    "hugging face": [
        "transformers",
        "model fine-tuning"
    ],

    # Frontend
    "react": [
        "frontend development",
        "component architecture"
    ],
    "next.js": [
        "frontend development",
        "server-side rendering"
    ],
    "vue.js": [
        "frontend development"
    ],

    # Backend
    "node.js": [
        "backend development",
        "api development"
    ],
    "django": [
        "backend development",
        "web development"
    ],
    "fastapi": [
        "api development",
        "backend development"
    ],

    # DevOps / Cloud
    "docker": [
        "containerization"
    ],
    "kubernetes": [
        "container orchestration"
    ],
    "aws": [
        "cloud computing",
        "deployment"
    ],
    "terraform": [
        "infrastructure as code"
    ],

    # Security
    "siem": [
        "threat monitoring",
        "incident response"
    ],
    "penetration testing": [
        "ethical hacking",
        "security auditing"
    ]
}

# =====================================================
# EXPAND IMPLIED SKILLS
# =====================================================

def expand_inferred_skills(extracted_skills):
    expanded_skills = set(extracted_skills)

    for skill in extracted_skills:
        normalized = normalize_skill(skill)

        if normalized in skill_inference_map:
            expanded_skills.update(
                skill_inference_map[normalized]
            )

    return sorted(expanded_skills)