

from langchain_core.documents import Document

# =====================================================
# JOB ROLE DOCUMENTS
# =====================================================

docs = [
    # =================================================
    # SOFTWARE DEVELOPMENT
    # =================================================
    Document(page_content="Frontend Developer requires HTML, CSS, JavaScript, TypeScript, React, Next.js, Vue.js, Angular, Tailwind CSS, Bootstrap, Redux, Responsive Design, Web Performance Optimization, REST API Integration, GraphQL, Git, GitHub, Vite, Webpack, Accessibility, SEO"),

    Document(page_content="Backend Developer requires Python, Java, Node.js, Express.js, Django, Flask, FastAPI, Spring Boot, REST API, GraphQL, Authentication, JWT, OAuth, SQL, PostgreSQL, MongoDB, Redis, Microservices, System Design, Docker, Git"),

    Document(page_content="Full Stack Developer requires HTML, CSS, JavaScript, TypeScript, React, Next.js, Node.js, Express.js, Python, Django, SQL, MongoDB, REST APIs, Deployment, Git, Docker, Cloud Basics, System Design"),

    Document(page_content="Software Engineer requires Python, Java, C++, Data Structures, Algorithms, OOP, DBMS, System Design, Git, Software Engineering, Testing, Debugging, CI/CD"),

    Document(page_content="Founding Engineer requires Full Stack Development, Product Thinking, React, Node.js, Python, Cloud Deployment, Startup Agility, System Design, DevOps, APIs, Leadership, Rapid Prototyping"),

    # =================================================
    # MOBILE DEVELOPMENT
    # =================================================
    Document(page_content="Android Developer requires Java, Kotlin, Android Studio, Jetpack Compose, Firebase, REST APIs, Mobile UI Development, Debugging"),

    Document(page_content="iOS Developer requires Swift, SwiftUI, Xcode, Core Data, Firebase, API Integration, Mobile Application Architecture"),

    Document(page_content="Flutter Developer requires Flutter, Dart, Firebase, REST APIs, Cross Platform Development, Mobile UI/UX, Deployment"),

    Document(page_content="React Native Developer requires React Native, JavaScript, TypeScript, Mobile Development, Firebase, API Integration"),

    # =================================================
    # DATA / ANALYTICS
    # =================================================
    Document(page_content="Data Analyst requires Python, SQL, Excel, Advanced Excel, Pandas, NumPy, Power BI, Tableau, Statistics, Data Cleaning, Dashboard Development, Data Visualization, Business Analytics"),

    Document(page_content="Business Intelligence Analyst requires SQL, Power BI, Tableau, Excel, ETL, Dashboard Development, Reporting, Stakeholder Communication"),

    Document(page_content="Product Analyst requires SQL, Python, Excel, Data Visualization, A/B Testing, Statistics, Product Metrics, User Behavior Analysis, Dashboarding"),

    Document(page_content="Data Scientist requires Python, SQL, Statistics, Machine Learning, Deep Learning, Pandas, NumPy, Scikit-learn, TensorFlow, PyTorch, Feature Engineering, Data Visualization, Model Deployment"),

    Document(page_content="Data Engineer requires Python, SQL, Apache Spark, Hadoop, Kafka, Airflow, ETL Pipelines, Snowflake, BigQuery, Data Warehousing, Cloud Platforms"),

    # =================================================
    # AI / ML / GENAI
    # =================================================
    Document(page_content="Machine Learning Engineer requires Python, Machine Learning, Deep Learning, Scikit-learn, TensorFlow, PyTorch, Feature Engineering, MLOps, Docker, Kubernetes, Model Deployment, AWS"),

    Document(page_content="AI Engineer requires Python, NLP, Computer Vision, Transformers, LLMs, LangChain, RAG, Fine-Tuning, Prompt Engineering, Hugging Face, OpenAI API, Vector Databases"),

    Document(page_content="LLM Engineer requires Python, Transformers, Hugging Face, LangChain, LangGraph, Vector Databases, FAISS, Pinecone, RAG, Prompt Engineering, Fine-Tuning, OpenAI API, vLLM, Deployment"),

    Document(page_content="Generative AI Engineer requires Python, Large Language Models, Prompt Engineering, LangChain, Retrieval-Augmented Generation, OpenAI API, Anthropic, Fine-Tuning, Semantic Search, Multi-Agent Systems"),

    Document(page_content="Prompt Engineer requires Prompt Engineering, LLM Optimization, OpenAI API, Claude, LangChain, Prompt Chaining, Guardrails, Testing"),

    Document(page_content="MLOps Engineer requires Python, Docker, Kubernetes, MLflow, CI/CD, AWS, Terraform, Monitoring, Model Deployment, Automation"),

    Document(page_content="Computer Vision Engineer requires Python, OpenCV, CNN, PyTorch, TensorFlow, Object Detection, Image Processing, Deep Learning"),

    Document(page_content="NLP Engineer requires Python, Natural Language Processing, Transformers, BERT, GPT, Hugging Face, Text Classification, Fine-Tuning"),

    # =================================================
    # CLOUD / DEVOPS / INFRASTRUCTURE
    # =================================================
    Document(page_content="DevOps Engineer requires Linux, Docker, Kubernetes, Jenkins, GitHub Actions, Terraform, Ansible, AWS, Azure, CI/CD, Monitoring, Prometheus, Grafana"),

    Document(page_content="Cloud Engineer requires AWS, Azure, Google Cloud Platform, Networking, Cloud Security, Serverless, Storage, Infrastructure as Code, Terraform"),

    Document(page_content="Site Reliability Engineer requires Linux, Kubernetes, Prometheus, Grafana, Automation, Monitoring, System Design, Incident Response"),

    Document(page_content="Platform Engineer requires Kubernetes, Terraform, Cloud Infrastructure, CI/CD, Automation, Scalability Engineering"),

    # =================================================
    # CYBERSECURITY
    # =================================================
    Document(page_content="Security Analyst requires Network Security, SIEM, Threat Detection, Incident Response, Firewalls, Encryption, Vulnerability Assessment"),

    Document(page_content="Penetration Tester requires Kali Linux, Metasploit, Burp Suite, OWASP, Python, Networking, Ethical Hacking, Security Testing"),

    Document(page_content="SOC Analyst requires SIEM, Splunk, Log Analysis, Threat Intelligence, Monitoring, Security Operations"),

    Document(page_content="Cloud Security Engineer requires AWS Security, Azure Security, IAM, Compliance, Encryption, Cloud Security Architecture"),

    # =================================================
    # QA / TESTING
    # =================================================
    Document(page_content="QA Engineer requires Manual Testing, Selenium, Cypress, Test Case Design, Regression Testing, Bug Tracking, API Testing"),

    Document(page_content="Automation Test Engineer requires Selenium, Playwright, JUnit, PyTest, API Testing, CI/CD, Test Automation"),

    Document(page_content="Performance Tester requires JMeter, LoadRunner, Performance Testing, Stress Testing, Monitoring"),

    # =================================================
    # DESIGN / PRODUCT
    # =================================================
    Document(page_content="UI Designer requires Figma, Adobe XD, Wireframing, Design Systems, Responsive Design, Prototyping"),

    Document(page_content="UX Researcher requires User Research, Usability Testing, Journey Mapping, Design Thinking, Analytics"),

    Document(page_content="Product Manager requires Agile, Scrum, Roadmapping, Stakeholder Management, Product Strategy, Analytics, Leadership"),

    Document(page_content="Technical Product Manager requires APIs, System Design, Analytics, Agile, Product Strategy, Technical Documentation"),

    # =================================================
    # BLOCKCHAIN / WEB3
    # =================================================
    Document(page_content="Blockchain Developer requires Solidity, Ethereum, Smart Contracts, Web3, Cryptography, DeFi, Security Audits"),

    Document(page_content="Smart Contract Auditor requires Solidity, Smart Contracts, Security Audits, DeFi Protocols, Blockchain Security"),

    # =================================================
    # EMBEDDED / IOT / ROBOTICS
    # =================================================
    Document(page_content="Embedded Systems Engineer requires C, C++, Microcontrollers, RTOS, Hardware Programming, Firmware Development"),

    Document(page_content="IoT Developer requires Arduino, Raspberry Pi, MQTT, Sensors, Cloud IoT, Embedded Programming"),

    Document(page_content="Robotics Engineer requires ROS, Python, Computer Vision, Control Systems, Sensor Integration"),

    # =================================================
    # GAMING / ARVR
    # =================================================
    Document(page_content="Game Developer requires C++, C#, Unity, Unreal Engine, Game Physics, Animation, 3D Graphics"),

    Document(page_content="AR/VR Developer requires Unity, Unreal Engine, XR SDK, 3D Graphics, Interaction Design"),

    # =================================================
    # ENTERPRISE / BUSINESS TOOLS
    # =================================================
    Document(page_content="CRM Developer requires Salesforce, Dynamics 365, CRM Tools, API Integration, Business Process Automation"),

    Document(page_content="ERP Consultant requires SAP, Oracle ERP, Business Process Management, Enterprise Systems"),

    Document(page_content="SEO Specialist requires SEO, Google Analytics, Search Console, Keyword Research, Content Optimization"),

    Document(page_content="Digital Marketing Technologist requires Marketing Automation, CRM Tools, Analytics, SEO, Campaign Management"),

    # =================================================
    # SCIENTIFIC / ADVANCED
    # =================================================
    Document(page_content="Bioinformatics Engineer requires Python, R, Genomics, Bioinformatics, Machine Learning, Data Analysis"),

    Document(page_content="Quantum Computing Researcher requires Qiskit, Linear Algebra, Quantum Algorithms, Advanced Mathematics, Research"),
]

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def get_all_job_roles():
    roles = []
    for doc in docs:
        role = doc.page_content.split(" requires ")[0].strip().lower()
        roles.append(role)
    return sorted(set(roles))


def get_role_skills(role_name: str):
    role_name = role_name.strip().lower()
    for doc in docs:
        content = doc.page_content.lower()
        if content.startswith(role_name):
            return [skill.strip() for skill in doc.page_content.split(" requires ")[1].split(",")]
    return []


   