import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# --- 1. The Expanded Dataset ---
# A larger and more diverse dataset to improve model accuracy.
data = [
    # --- NDAs (Non-Disclosure Agreements) ---
    ("This NON-DISCLOSURE AGREEMENT (the 'Agreement') is made between Party A and Party B to prevent the unauthorized disclosure of Confidential Information as defined below.", "NDA"),
    ("This Confidentiality Agreement is effective as of the last date signed below. The Disclosing Party may provide the Receiving Party with certain confidential and proprietary information.", "NDA"),
    ("The parties have entered into discussions in which it may be necessary to disclose confidential, proprietary, or private information. This agreement establishes the terms of that disclosure.", "NDA"),
    ("Receiving Party shall hold and maintain the Confidential Information in strictest confidence for the sole and exclusive benefit of the Disclosing Party.", "NDA"),
    ("This is a mutual non-disclosure agreement. Both parties agree not to disclose trade secrets or any confidential information provided by the other party.", "NDA"),

    # --- Employment Agreements ---
    ("This EMPLOYMENT AGREEMENT is entered into by and between Example Corp ('the Company') and John Doe ('the Employee'). The Company desires to employ the Employee on the terms and conditions set forth.", "Employment Agreement"),
    ("The Employee shall be employed in the position of Senior Software Engineer, responsible for duties as assigned by their supervisor. This is a full-time, salaried position.", "Employment Agreement"),
    ("This agreement outlines the terms of employment, including an annual salary of $90,000, eligibility for company benefits, and a probationary period of 90 days.", "Employment Agreement"),
    ("The Employee's employment with the Company is 'at-will,' meaning either the Employee or the Company may terminate the employment relationship at any time, with or without cause.", "Employment Agreement"),
    ("This contract of employment is made on January 1st, 2024. The employer agrees to employ the employee, who agrees to serve in the capacity of a graphic designer.", "Employment Agreement"),

    # --- Lease Agreements ---
    ("This LEASE AGREEMENT is made on this day by and between Landlord Name ('Landlord') and Tenant Name ('Tenant'). The Landlord agrees to lease the premises located at 123 Main St.", "Lease Agreement"),
    ("The tenant shall pay rent to the landlord in the amount of $1500 per month, due on the first day of each month. A late fee of $50 will be applied after a 5-day grace period.", "Lease Agreement"),
    ("This Residential Lease describes the terms and conditions of the tenancy. The term of this lease is for 12 months, beginning on the start date.", "Lease Agreement"),
    ("The Tenant agrees to use the leased property for residential purposes only and shall not conduct any commercial activities on the premises without prior written consent from the Landlord.", "Lease Agreement"),
    ("A security deposit of $1500 shall be paid by the Tenant to the Landlord upon execution of this lease. This deposit will be returned within 30 days of lease termination, less any deductions for damages.", "Lease Agreement"),

    # --- Consulting Agreements (New Category) ---
    ("This CONSULTING AGREEMENT is made between Client Inc. ('Client') and Consultant LLC ('Consultant'). The Consultant is an independent contractor, not an employee of the Client.", "Consulting Agreement"),
    ("The Consultant agrees to provide services in the field of marketing strategy. The scope of work is detailed in Exhibit A attached hereto.", "Consulting Agreement"),
    ("In consideration for the services, the Client shall pay the Consultant a fee of $100 per hour. Invoices shall be submitted monthly.", "Consulting Agreement"),
    ("This Agreement for consulting services will begin on the effective date and continue until the project is completed, unless terminated earlier by either party with 30 days written notice.", "Consulting Agreement"),
    ("The Consultant shall perform the services listed in the statement of work. As an independent contractor, the Consultant will provide their own tools and equipment.", "Consulting Agreement")
]


# Separate the texts and the labels
texts, labels = zip(*data)

# --- 2. Split Data ---
X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.25, random_state=42, stratify=labels)

# --- 3. Create the ML Pipeline ---
model_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english', ngram_range=(1, 2))),
    ('clf', LogisticRegression(solver='liblinear')),
])

# --- 4. Train the Model ---
print("Training the model with the expanded dataset...")
model_pipeline.fit(X_train, y_train)
print("Training complete.")

# --- 5. Evaluate the Model ---
print("\nEvaluating model performance on the test set:")
y_pred = model_pipeline.predict(X_test)
print(classification_report(y_test, y_pred))

# --- 6. Save the Trained Model ---
# Ensure you have a 'models' directory in your 'backend' folder
model_filename = "models/contract_classifier_model.joblib"
joblib.dump(model_pipeline, model_filename)
print(f"\nModel saved to {model_filename}")
