# Document Audit & Improvement

## Objective
Transform a poorly documented project using effective documentation strategies and see how it improves AI collaboration.

## Scenario
You've inherited a working Python project - a customer data analytics tool. The code works, but there's no documentation. Your task is to add strategic documentation that will help you (and Cursor) work more effectively with this codebase.

## **🔍 Step 1: Understand the file**

1. Open Cursor and ask it to explain what the files do.
2. Document your observations in `assessment_notes.md`. Include any areas of confusion or unclear model responses.

## 📖 Step **2: Create documentation**

1. Create a `/documents` folder.
2. Ask Cursor to generate the following files:
    - `product_overview.md`
    - `technical_architecture.md`
    - `package_recommendations.md`

- **Hint**: use/adapt the templates from the lesson
    
    ```markdown
    # [Project Name] - Product Overview
    
    ## Purpose
    What problem does this solve? (2-3 sentences max)
    
    ## Core Features
    1. Feature 1 - Why it matters
    2. Feature 2 - Why it matters
    3. Feature 3 - Why it matters
    
    ## Success Criteria
    - How do we know it's working?
    - What does "done" look like? 
    ```
    
    ```markdown
    # Technical Architecture
    
    ## Major Components
    - Component 1: Responsibility
    - Component 2: Responsibility
    - Component 3: Responsibility
    
    ## Data Flow
    [Simple description of how data moves through the system]
    
    ## Key Dependencies
    - External APIs
    - Required libraries
    - File formats
    
    ## Technical Constraints
    - Performance requirements
    - Platform limitations
    - Integration requirements 
    ```
    
    ```markdown
    # Package Recommendations
    
    ## Recommended Packages
    - Package 1: Why it's recommended
    - Package 2: Why it's recommended
    - Package 3: Why it's recommended
    
    ## Evaluation Criteria
    - How were these packages evaluated?
    - What are the key decision factors?
    
    ## Alternatives Considered
    - Alternative 1: Pros/Cons
    - Alternative 2: Pros/Cons 
    ```
    

## **📌 Step 3: Add inline documentation**

1. Ask Cursor to insert context breadcrumbs into the two main Python files.
2. Include references to your documentation files.
3. Where the logic is complex, add decision explanations.

## **📝 Step 4: Create a decision log**

1. Create `documents/decisions.md`.
2. Ask Cursor to document at least two technical decisions made in the code in this file.

---

## ✅ Success criteria

Make sure you've created the following with the help of Cursor:

- [ ]  `assessment_notes.md`
- [ ]  `/documents` folder
- [ ]  `product_overview.md`
- [ ]  `technical_architecture.md`
- [ ]  `package_recommendations.md`
- [ ]  `documents/decisions.md`
- [ ]  All the files accurately reflect the content of the Python file given

---

Submit your task for automatic review once you’re ready.
