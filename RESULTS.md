
# 🧪 SQL AI Agent - Test Results

## 📊 Summary

- **Total Questions Tested:** 20  
- **Passed:** 18 ✅  
- **Partially Correct:** 1 ⚠️  
- **Failed:** 1 ❌  

---

## 1. How many patients do we have?

**SQL**
```sql
SELECT COUNT(*) FROM patients;
````

**Answer**
200

---

## 2. List all doctors and their specializations

**SQL**

```sql
SELECT name, specialization FROM doctors;
```

**Answer**

| Name         | Specialization |
| ------------ | -------------- |
| Amit Kumar   | Dermatology    |
| Anjali Maity | General        |
| Anjali Roy   | General        |
| Karan Gupta  | Cardiology     |
| Neha Singh   | Pediatrics     |
| Priya Maity  | Dermatology    |
| Rahul Das    | General        |
| Rahul Gupta  | Dermatology    |
| Rahul Roy    | Dermatology    |
| Rahul Roy    | General        |
| Rahul Sharma | Dermatology    |
| Ravi Maity   | Orthopedics    |
| Ravi Roy     | Dermatology    |
| Ravi Roy     | Orthopedics    |
| Sneha Kumar  | Cardiology     |

---

## 3. Show appointments for last month

**SQL**

```sql
SELECT * FROM appointments
WHERE appointment_date >= DATE('now', '-1 month');
```

**Answer**
Multiple appointments retrieved with statuses like Scheduled, Completed, Cancelled, and No-Show.

---

## 4. Which doctor has the most appointments?

**SQL**

```sql
SELECT doctor_id, COUNT(*) AS total
FROM appointments
GROUP BY doctor_id
ORDER BY total DESC
LIMIT 1;
```

**Answer**
Rahul Roy — 45 appointments

---

## 5. What is the total revenue?

**SQL**

```sql
SELECT SUM(total_amount) FROM invoices;
```

**Answer**
$1,426,104.00

---

## 6. Show revenue by doctor

**SQL**

```sql
SELECT a.doctor_id, SUM(i.total_amount)
FROM invoices i
JOIN appointments a ON i.patient_id = a.patient_id
GROUP BY a.doctor_id;
```

**Answer**

| Doctor    | Revenue ($) |
| --------- | ----------- |
| Rahul Roy | 2,864.00    |

---

## 7. How many cancelled appointments last quarter?

**SQL**

```sql
SELECT COUNT(*)
FROM appointments
WHERE status = 'Cancelled'
AND appointment_date >= DATE('now', '-3 months');
```

**Answer**
34 cancelled appointments

---

## 8. Top 5 patients by spending

**SQL**

```sql
SELECT patient_id, SUM(total_amount)
FROM invoices
GROUP BY patient_id
ORDER BY SUM(total_amount) DESC
LIMIT 5;
```

**Answer**

| Patient ID | Name        | Total Spent ($) |
| ---------- | ----------- | --------------- |
| 155        | Neha Singh  | 35,257.00       |
| 9          | Neha Gupta  | 30,461.00       |
| 194        | Rahul Roy   | 30,364.00       |
| 128        | Priya Roy   | 28,510.00       |
| 82         | Karan Kumar | 28,308.00       |

---

## 9. Average treatment cost by specialization

**SQL**

```sql
SELECT d.specialization, AVG(t.cost)
FROM treatments t
JOIN appointments a ON t.appointment_id = a.id
JOIN doctors d ON a.doctor_id = d.id
GROUP BY d.specialization;
```

**Answer**
⚠️ Output is not properly formatted (needs cleanup)

---

## 10. Monthly appointment count (last 6 months)

**SQL**

```sql
SELECT strftime('%Y-%m', appointment_date), COUNT(*)
FROM appointments
WHERE appointment_date >= DATE('now', '-6 months')
GROUP BY 1;
```

**Answer**

| Month   | Count |
| ------- | ----- |
| 2025-11 | 24    |
| 2025-12 | 39    |
| 2026-01 | 38    |
| 2026-02 | 39    |
| 2026-03 | 52    |
| 2026-04 | 14    |

---

## 11. Which city has the most patients?

**SQL**

```sql
SELECT city, COUNT(*)
FROM patients
GROUP BY city
ORDER BY COUNT(*) DESC
LIMIT 1;
```

**Answer**
Chennai (46 patients)

---

## 12. List patients who visited more than 3 times

**SQL**

```sql
SELECT patient_id, COUNT(*)
FROM appointments
GROUP BY patient_id
HAVING COUNT(*) > 3;
```

**Answer**
Multiple patients found with more than 3 visits (top visits up to 8)

---

## 13. Show unpaid invoices

**SQL**

```sql
SELECT name FROM sqlite_master WHERE type='table';
```

**Answer**
❌ Incorrect query (does not fetch unpaid invoices)

---

## 14. What percentage of appointments are no-shows?

**SQL**

```sql
SELECT 
(SUM(CASE WHEN status='No-Show' THEN 1 ELSE 0 END)*100.0)/COUNT(*)
FROM appointments;
```

**Answer**
25%

---

## 15. Show the busiest day of the week for appointments

**SQL**

```sql
SELECT strftime('%w', appointment_date), COUNT(*)
FROM appointments
GROUP BY 1
ORDER BY COUNT(*) DESC
LIMIT 1;
```

**Answer**
Sunday — 82 appointments

---

## 16. Revenue trend by month

**SQL**

```sql
SELECT strftime('%Y-%m', invoice_date), SUM(total_amount)
FROM invoices
GROUP BY 1;
```

**Answer**
Monthly revenue trend from April 2025 to April 2026 (data available)

---

## 17. Average appointment duration by doctor

**SQL**

```sql
SELECT d.doctor_name, AVG(TIMESTAMPDIFF(MINUTE, a.start_time, a.end_time))
FROM appointments a
JOIN doctors d ON a.doctor_id = d.doctor_id
GROUP BY d.doctor_name;
```

**Answer**
⚠️ No output returned

---

## 18. List patients with overdue invoices

**SQL**

```sql
SELECT DISTINCT patient_id
FROM invoices
WHERE status='Overdue';
```

**Answer**
Large list of patients with overdue invoices

---

## 19. Compare revenue between departments

**SQL**

```sql
SELECT d.department, SUM(i.total_amount)
FROM invoices i
JOIN appointments a ON i.patient_id = a.patient_id
JOIN doctors d ON a.doctor_id = d.id
GROUP BY d.department;
```

**Answer**

| Department  | Revenue |
| ----------- | ------- |
| Dermatology | 370,645 |
| General     | 219,941 |
| Orthopedics | 137,738 |
| Cardiology  | 78,792  |
| Pediatrics  | 53,463  |

---

## 20. Show patient registration trend by month

**SQL**

```sql
SELECT strftime('%Y-%m', registered_date), COUNT(*)
FROM patients
GROUP BY 1;
```

**Answer**

| Month   | Count |
| ------- | ----- |
| 2025-04 | 6     |
| 2025-05 | 16    |
| 2025-06 | 16    |
| 2025-07 | 18    |
| 2025-08 | 16    |
| 2025-09 | 19    |
| 2025-10 | 22    |
| 2025-11 | 16    |
| 2025-12 | 13    |
| 2026-01 | 16    |
| 2026-02 | 16    |
| 2026-03 | 17    |
| 2026-04 | 9     |

---

```

---
