

# Production-Grade `job_roles.py` for PrepNus

from langchain_core.documents import Document

docs = [

    # =====================================================
    # SOFTWARE DEVELOPMENT
    # =====================================================

    Document(page_content="Frontend Developer requires HTML, CSS, JavaScript, TypeScript, React, Next.js, Angular, Vue.js, Tailwind CSS, Bootstrap, Responsive Design, REST API, GraphQL, Git, Webpack, Vite"),

    Document(page_content="Backend Developer requires Python, Java, Node.js, Express.js, Django, Flask, FastAPI, Spring Boot, SQL, MongoDB, Redis, Authentication, JWT, OAuth, REST API, GraphQL, Microservices, Deployment"),

    Document(page_content="Full Stack Developer requires HTML, CSS, JavaScript, TypeScript, React, Node.js, Express.js, SQL, MongoDB, REST API, Git, Deployment, Cloud Basics, System Design"),

    Document(page_content="Software Engineer requires Python, Java, C++, Data Structures, Algorithms, System Design, SQL, Git, Software Engineering"),

    Document(page_content="Desktop Application Developer requires C#, .NET, Java, Electron.js, PyQt, Tkinter, GUI Development"),

    Document(page_content="Game Developer requires C++, C#, Unity, Unreal Engine, 3D Modeling, Game Physics, Animation"),

    # =====================================================
    # MOBILE DEVELOPMENT
    # =====================================================

    Document(page_content="Android Developer requires Java, Kotlin, Android Studio, Jetpack Compose, Firebase, REST API"),

    Document(page_content="iOS Developer requires Swift, SwiftUI, Xcode, Core Data, Firebase, API Integration"),

    Document(page_content="Flutter Developer requires Flutter, Dart, Firebase, REST API, Cross Platform Development"),

    Document(page_content="React Native Developer requires React Native, JavaScript, TypeScript, Firebase, Mobile UI Development, API Integration"),

    # =====================================================
    # DATA / ANALYTICS / BI
    # =====================================================

    Document(page_content="Data Analyst requires Python, SQL, Excel, Pandas, NumPy, Power BI, Tableau, Statistics, Data Visualization"),

    Document(page_content="Business Intelligence Analyst requires SQL, Excel, Power BI, Tableau, ETL, Dashboard Development, Data Visualization"),

    Document(page_content="Data Engineer requires Python, SQL, Apache Spark, Hadoop, Kafka, Airflow, ETL Pipelines, Snowflake, BigQuery, Data Warehousing"),

    Document(page_content="Database Administrator requires SQL, PostgreSQL, MySQL, Oracle, Backup, Replication, Performance Tuning, Database Security"),

    # =====================================================
    # DATA SCIENCE / AI / MACHINE LEARNING
    # =====================================================

    Document(page_content="Data Scientist requires Python, Machine Learning, Deep Learning, Statistics, Pandas, NumPy, Scikit-learn, Data Visualization"),

    Document(page_content="Machine Learning Engineer requires Python, Machine Learning, Deep Learning, TensorFlow, PyTorch, Scikit-learn, MLOps, Docker, Kubernetes"),

    Document(page_content="AI Engineer requires Python, Natural Language Processing, Computer Vision, Transformers, Large Language Models, LangChain, Retrieval-Augmented Generation, Fine-Tuning, Prompt Engineering"),

    Document(page_content="LLM Engineer requires Python, Large Language Models, Transformers, LangChain, LangGraph, Vector Databases, Retrieval-Augmented Generation, Prompt Engineering, Fine-Tuning, Hugging Face"),

    Document(page_content="MLOps Engineer requires Python, Machine Learning, Docker, Kubernetes, CI/CD, Model Deployment, AWS, Terraform, Monitoring"),

    Document(page_content="Research Scientist AI requires Deep Learning, Advanced Mathematics, PyTorch, TensorFlow, Research Methodology, Model Optimization"),

    Document(page_content="Computer Vision Engineer requires Python, OpenCV, Deep Learning, CNN, Object Detection, PyTorch, TensorFlow"),

    Document(page_content="NLP Engineer requires Python, Natural Language Processing, Transformers, BERT, Hugging Face, Deep Learning, Large Language Models"),

    # =====================================================
    # DEVOPS / CLOUD / INFRASTRUCTURE
    # =====================================================

    Document(page_content="DevOps Engineer requires Linux, Docker, Kubernetes, Jenkins, GitHub Actions, Terraform, Ansible, AWS, Azure, Monitoring, CI/CD"),

    Document(page_content="Cloud Engineer requires AWS, Azure, Google Cloud Platform, Networking, Storage, Serverless, Cloud Architecture, Terraform"),

    Document(page_content="Site Reliability Engineer requires Linux, Kubernetes, Docker, Monitoring, Prometheus, Grafana, CI/CD, Incident Response, Cloud Infrastructure"),

    Document(page_content="Solutions Architect requires Cloud Architecture, AWS, Azure, System Design, Networking, Security, Infrastructure Design"),

    # =====================================================
    # CYBERSECURITY
    # =====================================================

    Document(page_content="Cybersecurity Analyst requires Network Security, SIEM, Threat Detection, Incident Response, Firewalls, Splunk, Security Monitoring"),

    Document(page_content="Security Engineer requires Network Security, Penetration Testing, Encryption, IAM, Cloud Security, Incident Response, Firewalls"),

    Document(page_content="SOC Analyst requires SIEM, Threat Detection, Incident Monitoring, Splunk, Log Analysis, Incident Response"),

    Document(page_content="Penetration Tester requires Ethical Hacking, Penetration Testing, OWASP, Burp Suite, Metasploit, Network Security"),

    # =====================================================
    # UI / UX / PRODUCT
    # =====================================================

    Document(page_content="UI/UX Designer requires Figma, Adobe XD, Wireframing, Design Systems, User Research, Prototyping, Usability Testing"),

    Document(page_content="Product Manager requires Agile, Scrum, Roadmapping, Stakeholder Management, Analytics, Product Strategy, Jira"),

    Document(page_content="Technical Product Manager requires Product Strategy, API Knowledge, Agile, Analytics, Roadmapping, Stakeholder Management"),

    # =====================================================
    # QA / TESTING
    # =====================================================

    Document(page_content="QA Engineer requires Manual Testing, Selenium, Cypress, API Testing, CI/CD, Test Automation, JMeter"),

    Document(page_content="Automation Test Engineer requires Selenium, Cypress, Playwright, API Testing, Test Automation Frameworks, CI/CD"),

    # =====================================================
    # BLOCKCHAIN / WEB3
    # =====================================================

    Document(page_content="Blockchain Developer requires Solidity, Ethereum, Smart Contracts, Web3.js, Cryptography, Security Audits"),

    # =====================================================
    # EMBEDDED / ROBOTICS / IOT
    # =====================================================

    Document(page_content="Embedded Systems Engineer requires C, C++, Microcontrollers, RTOS, Hardware Programming, IoT Systems"),

    Document(page_content="Robotics Engineer requires ROS, Python, Computer Vision, Control Systems, Sensors, Automation"),

    Document(page_content="IoT Engineer requires Embedded Systems, Microcontrollers, MQTT, Sensors, Cloud IoT, Networking"),
]

