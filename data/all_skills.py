




# =========================================================
# PrepNexus Production-Grade Master Skills Database
# Startup-Level Scalable Skill Intelligence System
# =========================================================

# ---------------------------------------------------------
# CORE MASTER SKILLS
# ---------------------------------------------------------

all_skills = [

    # =====================================================
    # Programming Languages
    # =====================================================
    "python", "java", "c", "c++", "c#", "javascript",
    "typescript", "php", "ruby", "go", "rust",
    "kotlin", "swift", "dart", "r", "sql",
    "html", "css", "bash", "powershell",

    # =====================================================
    # Computer Science Fundamentals
    # =====================================================
    "data structures", "algorithms",
    "object-oriented programming",
    "dbms", "operating systems",
    "computer networks", "system design",
    "software engineering",

    # =====================================================
    # Frontend Development
    # =====================================================
    "react", "next.js", "angular", "vue.js",
    "tailwind css", "bootstrap",
    "responsive design", "graphql",
    "rest api", "webpack", "vite",

    # =====================================================
    # Backend Development
    # =====================================================
    "node.js", "express.js",
    "django", "flask", "fastapi",
    "spring boot", "laravel",
    "authentication", "jwt", "oauth",
    "microservices", "deployment",

    # =====================================================
    # Databases / Data Infrastructure
    # =====================================================
    "mysql", "postgresql", "mongodb",
    "redis", "sqlite", "oracle",
    "snowflake", "bigquery",
    "etl", "data warehousing",

    # =====================================================
    # Mobile Development
    # =====================================================
    "android studio", "kotlin",
    "jetpack compose",
    "swiftui", "xcode",
    "flutter", "firebase",

    # =====================================================
    # Desktop / Game Development
    # =====================================================
    "electron.js", "pyqt",
    "unity", "unreal engine",

    # =====================================================
    # Data Analysis / Business Intelligence
    # =====================================================
    "excel", "power bi", "tableau",
    "pandas", "numpy",
    "statistics", "data visualization",

    # =====================================================
    # Data Science / Machine Learning
    # =====================================================
    "machine learning",
    "deep learning",
    "scikit learn",
    "tensorflow",
    "pytorch",
    "mlops",

    # =====================================================
    # AI / LLM Engineering
    # =====================================================
    "natural language processing",
    "computer vision",
    "transformers",
    "large language models",
    "langchain",
    "llamaindex",
    "retrieval-augmented generation",
    "vector databases",
    "faiss",
    "chromadb",
    "pinecone",
    "fine-tuning",
    "prompt engineering",
    "agentic ai",
    "openai api",
    "hugging face",
    "streamlit",
    "gradio",
    "langgraph",
    "crew ai",
    "autogen",

    # =====================================================
    # Data Engineering / Big Data
    # =====================================================
    "apache spark",
    "hadoop",
    "kafka",
    "airflow",

    # =====================================================
    # Cloud / DevOps / SRE
    # =====================================================
    "linux",
    "docker",
    "kubernetes",
    "jenkins",
    "github actions",
    "terraform",
    "ansible",
    "aws",
    "azure",
    "google cloud platform",
    "cloud architecture",
    "ci/cd",
    "prometheus",
    "grafana",

    # =====================================================
    # Cybersecurity
    # =====================================================
    "network security",
    "siem",
    "threat detection",
    "incident response",
    "firewalls",
    "owasp",
    "penetration testing",
    "splunk",
    "encryption",

    # =====================================================
    # Networking / Infrastructure
    # =====================================================
    "networking",
    "tcp/ip",
    "routing",
    "switching",
    "cisco",
    "vpn",
    "windows server",
    "active directory",

    # =====================================================
    # QA / Testing
    # =====================================================
    "manual testing",
    "selenium",
    "cypress",
    "playwright",
    "api testing",
    "test automation",
    "jmeter",

    # =====================================================
    # UI / UX Design
    # =====================================================
    "figma",
    "adobe xd",
    "wireframing",
    "design systems",
    "user research",

    # =====================================================
    # Product / Business / Collaboration
    # =====================================================
    "agile",
    "scrum",
    "roadmapping",
    "stakeholder management",
    "product strategy",
    "jira",
    "confluence",
    "notion",
    "slack",

    # =====================================================
    # Blockchain / Web3
    # =====================================================
    "solidity",
    "ethereum",
    "smart contracts",
    "web3.js",

    # =====================================================
    # Embedded / IoT / Robotics
    # =====================================================
    "microcontrollers",
    "rtos",
    "arduino",
    "raspberry pi",
    "mqtt",
    "ros",
    "control systems",

    # =====================================================
    # AR / VR
    # =====================================================
    "xr sdk",
    "3d graphics",

    # =====================================================
    # Enterprise Platforms
    # =====================================================
    "sap",
    "oracle erp",
    "salesforce",
    "crm tools",

    # =====================================================
    # Marketing / Analytics
    # =====================================================
    "google analytics",
    "seo",
    "marketing automation",

    # =====================================================
    # Scientific / Specialized
    # =====================================================
    "bioinformatics",
    "genomics",
    "qiskit",
    "quantum computing",

    # =====================================================
    # Professional Skills
    # =====================================================
    "git",
    "github",
    "problem solving",
    "debugging",
    "technical documentation",
    "leadership",
    "troubleshooting",
    "customer support"
]

# ---------------------------------------------------------
# SKILL ALIASES
# ---------------------------------------------------------

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
    "rag": "retrieval-augmented generation",
    "postgres": "postgresql",
    "mongo": "mongodb",
    "gcp": "google cloud platform",
    "k8s": "kubernetes",
    "tf": "tensorflow",
    "hf": "hugging face",
    "pbi": "power bi",
    "sklearn": "scikit-learn",
    "gen ai": "generative ai",
    "llmops": "large language models"
}

# ---------------------------------------------------------
# MASTER SKILL BUILDER
# ---------------------------------------------------------

def build_master_skills():
    combined_skills = list(all_skills)
    combined_skills.extend(skill_aliases.keys())

    return sorted(
        set(skill.lower() for skill in combined_skills)
    )

ALL_SKILLS = build_master_skills()

# ---------------------------------------------------------
# NORMALIZATION FUNCTION
# ---------------------------------------------------------

def normalize_skill(skill: str) -> str:
    skill = skill.strip().lower()
    return skill_aliases.get(skill, skill)

# ---------------------------------------------------------
# IMPLICIT SKILL INFERENCE MAP
# ---------------------------------------------------------

skill_inference_map = {

    # Data / BI
    "pandas": [
        "data analysis",
        "data manipulation",
        "data cleaning"
    ],
    "numpy": [
        "data analysis"
    ],
    "power bi": [
        "dashboard development",
        "business intelligence"
    ],
    "tableau": [
        "dashboard development",
        "data visualization"
    ],

    # ML / AI
    "scikit-learn": [
        "machine learning"
    ],
    "tensorflow": [
        "deep learning"
    ],
    "pytorch": [
        "deep learning"
    ],
    "langchain": [
        "retrieval-augmented generation",
        "llm applications"
    ],
    "faiss": [
        "vector search",
        "semantic retrieval"
    ],

    # Frontend
    "react": [
        "frontend development"
    ],
    "next.js": [
        "frontend development"
    ],

    # Backend
    "node.js": [
        "backend development"
    ],
    "django": [
        "backend development"
    ],
    "fastapi": [
        "backend development"
    ],

    # DevOps
    "docker": [
        "containerization"
    ],
    "kubernetes": [
        "container orchestration"
    ],
    "aws": [
        "cloud computing"
    ]
}

# ---------------------------------------------------------
# SKILL EXPANSION FUNCTION
# ---------------------------------------------------------

def expand_inferred_skills(extracted_skills):
    expanded_skills = set(extracted_skills)

    for skill in extracted_skills:
        normalized = normalize_skill(skill)

        if normalized in skill_inference_map:
            expanded_skills.update(
                skill_inference_map[normalized]
            )

    return sorted(expanded_skills)