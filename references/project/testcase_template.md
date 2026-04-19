# TEMPLATE: TEST CASE STRUCTURE (For AI Agent) - PROJECT A

**[Instruction for AI]:** When a user requests to create Test Cases from an input logic/requirement file, you (AI) MUST understand that logic and extract information to create Test Cases in the exact Markdown format below. Do not add or remove fields unless requested by the user. Analyze both the happy path (Happy Path/Positive) and the error path (Negative/Edge cases).

---

# 🧪 TEST CASE DOCUMENT: [Feature / Module Name]

## 1. GENERAL INFORMATION
* **Feature / Module:** [Feature name extracted from the input file]
* **Logic Source (Reference):** [Input file name or summary of main logic]
* **Testing Objective:** [Briefly describe the purpose of this test case suite]

---

## 2. TEST CASE SUMMARY

| TC ID | Test Case Title (Title) | Classification | Priority Level (Priority) |
| :--- | :--- | :--- | :--- |
| `TC_001` | [Brief description of TC 1] | `Positive` / `Negative` | `Urgent` - `Very Low` |
| `TC_002` | [Brief description of TC 2] | `Positive` / `Negative` | `Urgent` - `Very Low` |
*(AI automatically generates additional rows corresponding to the number of Test Cases created)*

---

## 3. TEST CASE DETAILS

### `TC_001`: [Test Case Title - Example: Successful login with valid account]
* **Objective:** Check how the system handles when [test condition].
* **Type:** `Positive` / `Negative`
* **Severity:** `Blocking` - `Very Low` (Based on Defect matrix)
* **Pre-conditions:**
  * [Condition 1 needed before testing, example: Account has been activated]
  * [Condition 2]
* **Test Data:**
  * Username: `[Sample data from logic]`
  * Password: `[Sample data from logic]`
* **Test Steps:**
  1. [Step 1: User's action]
  2. [Step 2: Next action]
  3. [Step 3: Click on X/Y/Z button]
* **Expected Result:**
  * [What message should the system display?]
  * [How should database/UI states change according to the input logic file?]

---

### `TC_002`: [Test Case 2 Title - Example: Error reported when required field is left blank]
* **Objective:** [Describe objective]
* **Type:** `Negative`
* **Severity:** `Blocking` - `Very Low`
* **Pre-conditions:**
  * [Condition...]
* **Test Data:**
  * Field A: `[Blank]`
* **Test Steps:**
  1. [Step 1]
  2. [Step 2]
* **Expected Result:**
  * [Describe expected error result according to input logic file]

*(AI repeats this structure until it covers all the logic provided in the input file)*
