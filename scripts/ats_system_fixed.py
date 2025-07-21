import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import re
import pickle
from datetime import datetime

# Try to import file handling libraries
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("⚠️ PyPDF2 not available. PDF support disabled.")

try:
    import docx
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False
    print("⚠️ python-docx not available. DOCX support disabled.")

class ATSSystem:
    """Complete ATS System - Works in Any Environment"""
    
    def __init__(self):
        print("🎯 ATS Resume Screening System")
        print("="*50)
        self.vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        self.model = None
        self.is_trained = False
        self.model_file = 'ats_model.pkl'
        
        # Try to load existing model
        self.try_load_existing_model()
    
    def try_load_existing_model(self):
        """Try to load existing trained model"""
        try:
            with open(self.model_file, 'rb') as f:
                model_data = pickle.load(f)
            
            self.model = model_data['model']
            self.vectorizer = model_data['vectorizer']
            self.training_date = model_data.get('training_date', 'Unknown')
            self.accuracy = model_data.get('accuracy', 0)
            self.categories = model_data.get('categories', [])
            self.is_trained = True
            
            print(f"✅ Found existing trained model!")
            print(f"🗓️ Training date: {self.training_date}")
            print(f"📈 Model accuracy: {self.accuracy:.2%}")
            
        except FileNotFoundError:
            print("📝 No existing model found. You can train a new one.")
        except Exception as e:
            print(f"⚠️ Error loading model: {e}")
    
    def upload_file_colab(self, file_type="file"):
        """Upload file in Google Colab"""
        try:
            from google.colab import files
            print(f"📁 Please select your {file_type}...")
            uploaded = files.upload()
            
            if uploaded:
                filename = list(uploaded.keys())[0]
                print(f"✅ File uploaded: {filename}")
                return filename
            else:
                print("❌ No file uploaded!")
                return None
        except ImportError:
            print("❌ File upload only works in Google Colab!")
            print("Please use option 2 to enter file path manually.")
            return None
    
    def clean_text(self, text):
        """Clean resume text"""
        if pd.isna(text) or not text:
            return ""
        
        text = str(text).lower()
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def create_labels_from_scores(self, df):
        """Create category labels based on highest scores"""
        print("🏷️ Creating labels from scores...")
        
        # Convert score columns to numeric
        score_columns = ['Software_Engineer_Score', 'Data_Analyst_Score', 'Consultant_Score']
        
        for col in score_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Create category based on highest score
        def get_best_category(row):
            scores = {}
            if 'Software_Engineer_Score' in df.columns:
                scores['software_engineering'] = row.get('Software_Engineer_Score', 0)
            if 'Data_Analyst_Score' in df.columns:
                scores['data_analyst'] = row.get('Data_Analyst_Score', 0)
            if 'Consultant_Score' in df.columns:
                scores['consultant'] = row.get('Consultant_Score', 0)
            
            if scores:
                return max(scores, key=scores.get)
            else:
                return 'unknown'
        
        df['category'] = df.apply(get_best_category, axis=1)
        
        # Show distribution
        print("📊 Category distribution:")
        print(df['category'].value_counts())
        
        return df
    
    def train_model_from_csv(self, csv_filename):
        """Train model from CSV file"""
        print("📚 Loading dataset...")
        
        try:
            # Load dataset
            df = pd.read_csv(csv_filename)
            print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
            print(f"Columns: {list(df.columns)}")
            
            # Check for resume text column
            text_column = None
            possible_text_columns = ['Resume_Text', 'resume_text', 'text', 'resume', 'Resume']
            
            for col in possible_text_columns:
                if col in df.columns:
                    text_column = col
                    break
            
            if not text_column:
                print("❌ Could not find resume text column!")
                print("Looking for columns like: Resume_Text, resume_text, text, resume")
                return False
            
            print(f"✅ Using '{text_column}' as resume text column")
            
            # Check for score columns
            score_columns = ['Software_Engineer_Score', 'Data_Analyst_Score', 'Consultant_Score']
            available_score_columns = [col for col in score_columns if col in df.columns]
            
            if len(available_score_columns) < 2:
                print("❌ Need at least 2 score columns for training!")
                print(f"Available: {available_score_columns}")
                print(f"Expected: {score_columns}")
                return False
            
            print(f"✅ Using score columns: {available_score_columns}")
            
            # Create category labels from scores
            df = self.create_labels_from_scores(df)
            
            print("🧹 Cleaning text data...")
            # Clean the resume text
            df['cleaned_text'] = df[text_column].apply(self.clean_text)
            
            # Remove empty texts
            df = df[df['cleaned_text'].str.len() > 10]  # At least 10 characters
            print(f"After cleaning: {df.shape[0]} resumes")
            
            if df.shape[0] < 10:
                print("❌ Not enough data for training! Need at least 10 resumes.")
                return False
            
            print("🔤 Converting text to features...")
            # Convert text to TF-IDF features
            X = self.vectorizer.fit_transform(df['cleaned_text'])
            y = df['category']
            
            # Check if we have enough samples for each category
            category_counts = y.value_counts()
            print(f"Category counts: {dict(category_counts)}")
            
            if len(category_counts) < 2:
                print("❌ Need at least 2 different categories for training!")
                return False
            
            print("📊 Splitting data for training...")
            # Split data (adjust test_size if dataset is small)
            test_size = min(0.3, max(0.1, len(df) * 0.2 / len(df)))
            
            try:
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=test_size, random_state=42, stratify=y
                )
            except ValueError:
                # If stratify fails, do without stratification
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=test_size, random_state=42
                )
            
            print("🤖 Training model...")
            # Train Random Forest model
            self.model = RandomForestClassifier(n_estimators=50, random_state=42)
            self.model.fit(X_train, y_train)
            
            # Test accuracy
            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            print(f"✅ Model trained successfully!")
            print(f"📈 Accuracy: {accuracy:.2%}")
            
            # Save the model
            model_data = {
                'model': self.model,
                'vectorizer': self.vectorizer,
                'training_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'accuracy': accuracy,
                'categories': list(self.model.classes_)
            }
            
            with open(self.model_file, 'wb') as f:
                pickle.dump(model_data, f)
            
            print(f"💾 Model saved as: {self.model_file}")
            
            # Update instance variables
            self.training_date = model_data['training_date']
            self.accuracy = accuracy
            self.categories = list(self.model.classes_)
            self.is_trained = True
            
            print("🎉 Training completed! Model is ready for use.")
            return True
            
        except Exception as e:
            print(f"❌ Error during training: {str(e)}")
            return False
    
    def extract_text_from_pdf(self, pdf_file_path):
        """Extract text from PDF file"""
        if not PDF_AVAILABLE:
            print("❌ PDF support not available. Please install PyPDF2.")
            return None
        
        try:
            with open(pdf_file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            print(f"❌ Error reading PDF: {str(e)}")
            return None
    
    def extract_text_from_docx(self, docx_file_path):
        """Extract text from Word document"""
        if not DOCX_AVAILABLE:
            print("❌ DOCX support not available. Please install python-docx.")
            return None
        
        try:
            doc = docx.Document(docx_file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            print(f"❌ Error reading DOCX: {str(e)}")
            return None
    
    def extract_text_from_file(self, file_path):
        """Extract text from any supported file format"""
        file_extension = file_path.lower().split('.')[-1]
        
        print(f"📄 Reading {file_extension.upper()} file...")
        
        if file_extension == 'pdf':
            return self.extract_text_from_pdf(file_path)
        elif file_extension in ['docx', 'doc']:
            return self.extract_text_from_docx(file_path)
        elif file_extension == 'txt':
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                print(f"❌ Error reading TXT: {str(e)}")
                return None
        else:
            print(f"❌ Unsupported file format: {file_extension}")
            print("Supported formats: PDF, DOCX, TXT")
            return None
    
    def calculate_ats_score(self, resume_text):
        """Calculate ATS score for the resume"""
        if not self.is_trained:
            print("❌ Model not trained! Please train the model first.")
            return None
        
        print("🔍 Analyzing resume...")
        
        # Clean the resume text
        cleaned_text = self.clean_text(resume_text)
        
        if not cleaned_text.strip():
            print("❌ No valid text found in resume!")
            return None
        
        # Convert to features
        resume_features = self.vectorizer.transform([cleaned_text])
        
        # Get prediction and probabilities
        prediction = self.model.predict(resume_features)[0]
        probabilities = self.model.predict_proba(resume_features)[0]
        
        # Create results
        results = {
            'predicted_category': prediction,
            'confidence': max(probabilities) * 100,
            'all_scores': {}
        }
        
        # Add scores for all categories
        for i, category in enumerate(self.categories):
            results['all_scores'][category] = round(probabilities[i] * 100, 1)
        
        return results
    
    def display_ats_results(self, results):
        """Display ATS scoring results"""
        print("\n" + "="*60)
        print("🎯 ATS RESUME SCORING RESULTS")
        print("="*60)
        
        print(f"\n🏆 BEST MATCH: {results['predicted_category'].upper()}")
        print(f"🎯 CONFIDENCE: {results['confidence']:.1f}%")
        
        print(f"\n📊 ATS SCORES FOR ALL CATEGORIES:")
        for category, score in results['all_scores'].items():
            category_name = category.replace('_', ' ').title()
            print(f"  • {category_name}: {score}%")
        
        # ATS Score interpretation
        confidence = results['confidence']
        if confidence >= 85:
            grade = "A+"
            interpretation = "Excellent! Resume perfectly matches the role."
        elif confidence >= 75:
            grade = "A"
            interpretation = "Very Good! Strong candidate for this position."
        elif confidence >= 65:
            grade = "B"
            interpretation = "Good match! Consider for interview."
        elif confidence >= 55:
            grade = "C"
            interpretation = "Average fit. Review carefully."
        elif confidence >= 45:
            grade = "D"
            interpretation = "Below average. May need resume improvements."
        else:
            grade = "F"
            interpretation = "Poor match. Resume needs significant improvements."
        
        print(f"\n📈 ATS GRADE: {grade}")
        print(f"💡 INTERPRETATION: {interpretation}")
        print("="*60)

def main():
    """Main application"""
    
    print("🎯 Welcome to ATS Resume Screening System!")
    print("="*50)
    
    # Initialize system
    system = ATSSystem()
    
    while True:
        print("\n" + "="*50)
        print("🎯 ATS SYSTEM - MAIN MENU")
        print("="*50)
        
        if system.is_trained:
            print("✅ Model Status: TRAINED & READY")
        else:
            print("⚠️  Model Status: NOT TRAINED")
        
        print("\nChoose an option:")
        print("1. 🎓 Train Model (Upload CSV dataset)")
        print("2. 📝 Score Resume (Get ATS score)")
        print("3. 🧪 Test with Sample Resume")
        print("4. ℹ️  System Info")
        print("5. 🚪 Exit")
        
        choice = input("\nEnter your choice (1/2/3/4/5): ")
        
        if choice == "1":
            print("\n🎓 MODEL TRAINING")
            print("="*30)
            
            print("Your CSV file should have columns like:")
            print("• Resume_Text (or similar)")
            print("• Software_Engineer_Score")
            print("• Data_Analyst_Score") 
            print("• Consultant_Score")
            
            print("\nChoose upload method:")
            print("1. Upload CSV in Google Colab")
            print("2. Enter CSV file path")
            
            train_choice = input("Enter choice (1/2): ")
            
            if train_choice == "1":
                csv_file = system.upload_file_colab("CSV file")
                if csv_file:
                    system.train_model_from_csv(csv_file)
            
            elif train_choice == "2":
                csv_path = input("Enter CSV file path: ")
                system.train_model_from_csv(csv_path)
        
        elif choice == "2":
            if not system.is_trained:
                print("❌ No trained model found! Please train first.")
                continue
            
            print("\n📝 ATS RESUME SCORER")
            print("="*30)
            
            print("Choose input method:")
            print("1. Upload resume file in Google Colab")
            print("2. Enter resume file path")
            print("3. Paste resume text")
            
            score_choice = input("Enter choice (1/2/3): ")
            
            if score_choice == "1":
                resume_file = system.upload_file_colab("resume file")
                if resume_file:
                    resume_text = system.extract_text_from_file(resume_file)
                    if resume_text:
                        results = system.calculate_ats_score(resume_text)
                        if results:
                            system.display_ats_results(results)
            
            elif score_choice == "2":
                file_path = input("Enter resume file path: ")
                resume_text = system.extract_text_from_file(file_path)
                if resume_text:
                    results = system.calculate_ats_score(resume_text)
                    if results:
                        system.display_ats_results(results)
            
            elif score_choice == "3":
                print("\nPaste your resume text (press Enter twice when done):")
                resume_lines = []
                empty_lines = 0
                
                while empty_lines < 2:
                    line = input()
                    if line == "":
                        empty_lines += 1
                    else:
                        empty_lines = 0
                    resume_lines.append(line)
                
                resume_text = "\n".join(resume_lines)
                
                if resume_text.strip():
                    results = system.calculate_ats_score(resume_text)
                    if results:
                        system.display_ats_results(results)
        
        elif choice == "3":
            # Test with sample resume
            sample_resume = """
            John Doe - Software Engineer
            
            Experience: 5 years in software development
            Skills: Python, Java, JavaScript, React, SQL, AWS, Docker
            Education: Bachelor's in Computer Science
            
            - Developed web applications using React and Node.js
            - Implemented REST APIs and microservices
            - Worked with agile development methodologies
            - Led a team of 3 developers
            """
            
            print("🧪 Testing with sample resume...")
            if system.is_trained:
                results = system.calculate_ats_score(sample_resume)
                if results:
                    system.display_ats_results(results)
            else:
                print("❌ Please train the model first!")
        
        elif choice == "4":
            print("\n" + "="*50)
            print("ℹ️  SYSTEM INFORMATION")
            print("="*50)
            if system.is_trained:
                print(f"✅ Model Status: TRAINED")
                print(f"🗓️  Training Date: {system.training_date}")
                print(f"📈 Accuracy: {system.accuracy:.2%}")
                print(f"📋 Categories: {', '.join(system.categories)}")
            else:
                print("⚠️  Model Status: NOT TRAINED")
            
            print(f"💾 Model File: {system.model_file}")
            print(f"📄 PDF Support: {'✅' if PDF_AVAILABLE else '❌'}")
            print(f"📄 DOCX Support: {'✅' if DOCX_AVAILABLE else '❌'}")
        
        elif choice == "5":
            print("\n👋 Thank you for using ATS System!")
            break
        
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
