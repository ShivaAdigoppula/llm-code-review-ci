pipeline {
    agent any

    stages {
        stage('Setup Python') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Prepare Test Code') {
            steps {
                sh '''
                mkdir -p reports
                echo "def divide(a, b): return a / b" > reports/changed_code.txt
                echo "print(divide(10, 0))" >> reports/changed_code.txt
                '''
            }
        }

        stage('LLM Code Review') {
            steps {
                sh '''
                . venv/bin/activate
                python scripts/llm_review_cloud.py
                '''
            }
        }

        stage('Show Results') {
            steps {
                sh '''
                echo "===== REVIEW ====="
                cat reports/local_review.md

                echo "===== METRICS ====="
                cat reports/local_metrics.txt
                '''
            }
        }
    }
}
