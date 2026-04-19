# Bug Evaluation Standards - PROJECT A

This document defines the criteria to systematize the process of classifying, evaluating the impact, and prioritizing the resolution of bugs (Defect) in the project.

---

## 1. Distinguishing the Nature: Severity vs. Priority

| Characteristic | **Severity** (Severity Level) | **Priority** (Priority Level) |
| :--- | :--- | :--- |
| **Focus** | Technical & system operational aspects. | Business, time & resource aspects. |
| **Main question** | "How much does this bug break the system?" | "How quickly does this bug need to be fixed?" |
| **Subject** | **QA / Tester** (Based on spec & system) | **PO / PM / Lead** (Based on Roadmap & customers) |

---

## 2. DEFECT BY SEVERITY (Severity Level)
*Evaluated based on the bug's impact on the features and operability of the software.*

| Level | Detailed description |
| :--- | :--- |
| **Blocking** | The bug completely paralyzes the system or main function. No temporary workaround. Prevents testing of related parts. |
| **Important** | The bug heavily affects core features. Users cannot complete the main business flow (Critical Path). |
| **Moderate** | The bug causes loss of functionality but has a temporary workaround. Affects the experience but does not completely disrupt the process. |
| **Low** | Minor interface (UI) bug or secondary features, does not affect business logic. |
| **Very Low** | Extremely minor bugs, typos, or subjective cosmetic improvement suggestions. |

---

## 3. DEFECT BY PRIORITY (Priority Level)
*Evaluated based on the urgency of the repair needed.*

| Level | Expected resolution time |
| :--- | :--- |
| **Urgent** | **Fix immediately.** Usually resolved within a few hours or within the day. The bug halts the team's progress or causes direct damage. |
| **High** | **High priority.** Needs to be resolved in the current Sprint or before the next release cycle (Release). |
| **Normal** | **Normal processing.** Scheduled for fixing after critical bugs are completed. Can wait until periodic updates. |
| **Low** | **Low priority.** Fix when there is free time, does not affect the main Release plan. |
| **Very Low** | **Consider fixing.** Usually cosmetic bugs or improvement requests (Suggestion) to be handled when resources are abundant. |

---

## 4. Triage Matrix (Defect Triage Matrix)

Combining Severity and Priority helps the development team optimize resources:

* **High Severity / High Priority:** System severely broken + Needs urgent fixing (Example: Cannot checkout on Production).
* **High Severity / Low Priority:** Severe technical bug but rarely encountered (Example: App crashes on an old phone model that is no longer supported).
* **Low Severity / High Priority:** Minor bug but major brand impact (Example: Incorrect company logo, wrong promotional message on the homepage).
* **Low Severity / Low Priority:** Minor bug, rarely seen by people (Example: Typo on the terms of use page).

---

## 5. Bug Type (Defect Type)

When reporting a bug, it needs to be labeled under the following groups:
* **Functional:** Business logic deviation bug, feature does not run according to spec.
* **UI/UX:** Interface bug, design deviation, user experience is not smooth.
* **Performance:** Bug regarding response speed, slow loading, memory leak.
* **Security:** Security vulnerabilities, data leaks.
* **Suggestion/Improvement:** Proposed changes to make the product better (not a bug).

---

> [!IMPORTANT]
> **Notes for Workflow:**
> 1. **QA** sets the Severity. **PM/PO** has the final decision on Priority.
> 2. **Severity** is usually fixed throughout the bug's lifecycle, but **Priority** can change depending on time pressure (for example: a Low bug can jump to High when nearing the handover date).
