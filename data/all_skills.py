

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
    "haskell", "elixir", "clojure", "erlang", "fortran", "cobol",
    "assembly", "cuda", "webassembly",

    # CS Fundamentals
    "data structures", "algorithms", "object-oriented programming",
    "functional programming", "operating systems", "dbms",
    "computer networks", "system design", "software engineering",
    "design patterns", "distributed systems", "compiler design",
    "parallel computing", "quantum computing", "formal verification",

    # Frontend Development
    "html5", "css3", "responsive design", "dom manipulation",
    "accessibility", "seo", "react", "next.js",
    "vue.js", "nuxt.js", "angular", "svelte", "redux",
    "zustand", "tailwind css", "bootstrap", "webpack", "vite",
    "web performance optimization", "ssr", "ssg",
    "progressive web apps", "micro frontends",

    # Backend Development
    "node.js", "express.js", "django", "flask",
    "fastapi", "spring boot", "asp.net", "laravel",
    "graphql", "grpc", "websockets", "microservices",
    "event-driven architecture", "cqrs", "domain driven design",
    "rest api", "jwt", "oauth", "authentication",

    # Databases
    "mysql", "postgresql", "mongodb", "redis", "sqlite",
    "mariadb", "oracle", "cassandra", "dynamodb",
    "neo4j", "database normalization", "indexing",
    "query optimization", "etl", "data warehousing",
    "data lakes", "lakehouse", "snowflake", "bigquery",

    # Mobile Development
    "android development", "android studio", "jetpack compose",
    "ios development", "swiftui", "xcode",
    "core data", "flutter", "dart", "react native",
    "xamarin", "ionic", "cross platform development",

    # Desktop Development
    "electron.js", "pyqt", "tkinter", ".net", "wpf",

    # Data Analysis / BI
    "excel", "microsoft excel", "power bi", "tableau",
    "pandas", "numpy", "matplotlib", "seaborn",
    "statistics", "probability", "data cleaning",
    "exploratory data analysis", "feature engineering",
    "a/b testing", "time series analysis",
    "data visualization", "dashboard development",

    # Big Data / Data Engineering
    "apache spark", "hadoop", "big data analytics",
    "kafka", "airflow", "etl pipelines",

    # Machine Learning
    "machine learning", "linear regression",
    "logistic regression", "decision trees",
    "random forest", "gradient descent",
    "support vector machines", "svm",
    "knn", "clustering",
    "dimensionality reduction", "xgboost",
    "lightgbm", "catboost",
    "ensemble learning", "hyperparameter tuning",
    "model deployment", "mlops", "scikit-learn",

    # Deep Learning
    "tensorflow", "pytorch", "keras",
    "neural networks", "cnn", "rnn",
    "lstm", "transformers", "bert",
    "gpt", "large language models",
    "gans", "diffusion models",
    "reinforcement learning", "transfer learning",
    "fine-tuning", "lora", "qlora",

    # AI Engineering / LLMOps
    "natural language processing", "computer vision", "langchain",
    "llamaindex", "retrieval-augmented generation",
    "rag", "vector databases", "faiss",
    "chromadb", "pinecone", "prompt engineering",
    "agentic ai", "tool calling",
    "model quantization", "rlhf",
    "knowledge graphs", "ai safety",
    "openai api", "anthropic", "claude",
    "llama", "mistral", "hugging face",
    "vllm", "langgraph", "crew ai",
    "autogen", "streamlit", "gradio",
    "semantic search", "multi-agent systems",
    "guardrails", "prompt chaining",

    # Cloud Computing
    "aws", "azure", "google cloud platform",
    "ec2", "s3", "lambda",
    "rds", "iam", "serverless",
    "docker", "kubernetes", "terraform",
    "infrastructure as code", "cloud security",
    "cloud architecture", "multi-cloud",

    # DevOps / SRE
    "git", "github", "gitlab",
    "ci/cd", "jenkins", "ansible",
    "prometheus", "grafana",
    "observability", "site reliability engineering",
    "chaos engineering", "linux",
    "automation", "monitoring",
    "github actions",

    # Cybersecurity
    "network security", "encryption",
    "owasp", "firewalls", "siem",
    "ethical hacking", "penetration testing",
    "reverse engineering", "malware analysis",
    "zero trust security",
    "threat detection", "incident response",

    # Networking
    "tcp/ip", "dns", "http", "https",
    "routing", "switching", "bgp",
    "sdn", "load balancing", "vpn",
    "network automation", "cisco",

    # Testing / QA
    "manual testing", "regression testing",
    "selenium", "cypress", "playwright",
    "junit", "pytest",
    "performance testing", "security testing",
    "api testing", "test case design",
    "bug tracking", "jmeter", "loadrunner",

    # UI/UX
    "figma", "adobe xd", "photoshop",
    "illustrator", "wireframing",
    "prototyping", "user research",
    "interaction design", "design systems",
    "usability testing", "journey mapping",

    # Product / Business
    "agile", "scrum", "roadmapping",
    "stakeholder management", "product strategy",
    "analytics", "business process management",
    "jira", "confluence", "notion",
    "slack", "trello", "asana",

    # Blockchain
    "bitcoin", "ethereum", "solidity",
    "smart contracts", "web3",
    "nfts", "defi",
    "consensus mechanisms", "cryptography",

    # Embedded / IoT / Robotics
    "microcontrollers", "rtos",
    "hardware programming", "arduino",
    "raspberry pi", "mqtt",
    "sensors", "cloud iot",
    "robotics", "ros",
    "control systems",

    # AR/VR / Gaming
    "unity", "unreal engine",
    "3d modeling", "game physics",
    "animation", "3d graphics",
    "xr sdk", "ar/vr",

    # Enterprise Tools
    "sap", "oracle erp",
    "salesforce", "dynamics 365",
    "crm tools", "marketing automation",

    # Scientific / Specialized
    "genomics", "bioinformatics",
    "qiskit", "linear algebra",
    "quantum algorithms",

    # Soft Skills
    "problem solving", "debugging",
    "code review", "technical documentation",
    "leadership", "product thinking",
    "customer support", "troubleshooting"
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
# OPTIONAL CATEGORY LOOKUP
# =====================================================

def get_skill_category(skill: str):
    skill = normalize_skill(skill)

    category_map = {
        "programming": ["python", "java", "c", "c++", "javascript", "typescript"],
        "frontend": ["react", "next.js", "vue.js", "angular", "tailwind css"],
        "backend": ["node.js", "django", "flask", "fastapi", "spring boot"],
        "database": ["mysql", "postgresql", "mongodb", "redis"],
        "data_science": ["pandas", "numpy", "power bi", "tableau"],
        "machine_learning": ["machine learning", "tensorflow", "pytorch", "scikit-learn"],
        "ai_engineering": ["langchain", "faiss", "retrieval-augmented generation", "prompt engineering"],
        "cloud_devops": ["aws", "docker", "kubernetes", "terraform"],
        "cybersecurity": ["penetration testing", "siem", "network security"],
        "product": ["agile", "scrum", "jira"]
    }

    for category, skills in category_map.items():
        if skill in skills:
            return category

    return "unknown"

