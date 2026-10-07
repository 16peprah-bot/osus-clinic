from flask import Flask, render_template_string, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Password required to view staff records
ACCESS_PASSWORD = "staff password"

# In-memory storage for medical records and payroll checks
medical_records = []
payroll_records = [
    {"id": 1, "staff_name": "Dr. Sarah Jenkins", "role": "Head Medical Officer", "base_salary": 4500.00, "bonus": 300.00, "total_pay": 4800.00, "pay_date": "2026-09-30"},
    {"id": 2, "staff_name": "Nurse Robert Chen", "role": "Senior Triage Nurse", "base_salary": 3200.00, "bonus": 150.00, "total_pay": 3350.00, "pay_date": "2026-09-30"},
    {"id": 3, "staff_name": "Amanda Vance", "role": "Clinic Administrator", "base_salary": 2800.00, "bonus": 100.00, "total_pay": 2900.00, "pay_date": "2026-09-30"}
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Osus University & Co. // Student Health & Clinical Services</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  
  <style>
    :root {
      --primary-navy: #0f172a;
      --accent-gold: #d97706;
      --gold-light: #fef3c7;
      --border-color: #cbd5e1;
      --bg-slate: #f8fafc;
      --card-white: #ffffff;
      --text-dark: #1e293b;
      --text-muted: #64748b;
      --radius: 12px;
      --shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.08);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    body { 
      font-family: 'Plus Jakarta Sans', sans-serif; 
      background-color: var(--bg-slate); 
      color: var(--text-dark); 
      min-height: 100vh;
    }

    /* Official University Header */
    header { 
      background: var(--primary-navy); 
      color: white;
      padding: 1rem 2rem;
      border-bottom: 4px solid var(--accent-gold);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .university-brand {
      display: flex;
      align-items: center;
      gap: 16px;
    }

    .university-crest {
      width: 48px;
      height: 48px;
      background: var(--accent-gold);
      color: white;
      border-radius: 50%;
      display: grid;
      place-items: center;
      font-family: 'Cinzel', serif;
      font-weight: 700;
      font-size: 1.2rem;
      border: 2px solid white;
    }

    .brand-text h1 { 
      font-family: 'Cinzel', serif;
      font-size: 1.35rem; 
      letter-spacing: 0.03em;
      color: #ffffff;
    }

    .brand-text p {
      color: #94a3b8;
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .campus-badge {
      background: rgba(217, 119, 6, 0.15);
      border: 1px solid var(--accent-gold);
      color: #fef3c7;
      padding: 0.4rem 1rem;
      border-radius: 20px;
      font-size: 0.8rem;
      font-weight: 600;
    }

    .container { max-width: 1200px; margin: 2rem auto; padding: 0 1.5rem; }

    /* University Portal Cards */
    .portal-card { 
      background: var(--card-white); 
      border: 1px solid var(--border-color);
      border-radius: var(--radius); 
      padding: 2.5rem; 
      margin-bottom: 2rem; 
      box-shadow: var(--shadow);
    }

    .hero-banner {
      position: relative;
      border-radius: 10px;
      overflow: hidden;
      margin-bottom: 2rem;
    }

    .hero-banner img {
      width: 100%;
      height: 280px;
      object-fit: cover;
    }

    .hero-overlay {
      position: absolute;
      inset: 0;
      background: linear-gradient(to top, rgba(15, 23, 42, 0.85), transparent 70%);
      display: flex;
      align-items: flex-end;
      padding: 2rem;
      color: white;
    }

    .official-notice {
      background: var(--gold-light);
      border-left: 4px solid var(--accent-gold);
      padding: 1rem 1.25rem;
      border-radius: 6px;
      margin-bottom: 2rem;
      color: #78350f;
      font-size: 0.9rem;
      display: flex;
      align-items: center;
      gap: 15px;
    }

    .notice-thumb {
      width: 70px;
      height: 70px;
      border-radius: 8px;
      object-fit: cover;
      border: 1px solid var(--accent-gold);
    }

    h2 { 
      font-family: 'Cinzel', serif;
      font-size: 1.6rem; 
      color: var(--primary-navy);
      margin-bottom: 1.25rem;
    }

    h3 { 
      font-size: 1.1rem; 
      color: var(--primary-navy);
      margin-bottom: 1rem;
      font-weight: 700;
    }

    /* Form Design & Password Toggle Eye Icon */
    .form-group { margin-bottom: 1.25rem; }

    label { 
      display: block; 
      font-weight: 600; 
      margin-bottom: 0.4rem; 
      color: #334155; 
      font-size: 0.85rem;
      text-transform: uppercase;
    }

    .password-wrapper {
      position: relative;
      display: flex;
      align-items: center;
    }

    input, textarea, select { 
      width: 100%; 
      padding: 0.8rem 1rem; 
      border: 1px solid var(--border-color); 
      border-radius: 8px; 
      font-size: 0.95rem; 
      color: var(--text-dark);
      background-color: #f8fafc;
    }

    .password-wrapper input {
      padding-right: 2.8rem;
    }

    .eye-toggle {
      position: absolute;
      right: 12px;
      cursor: pointer;
      color: var(--text-muted);
      user-select: none;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .eye-toggle:hover {
      color: var(--primary-navy);
    }

    input:focus, textarea:focus { 
      outline: none; 
      border-color: var(--primary-navy); 
      background-color: #ffffff;
    }

    /* Standard Buttons */
    .btn { 
      background: var(--primary-navy); 
      color: white; 
      border: none; 
      padding: 0.8rem 1.6rem; 
      font-size: 0.9rem; 
      font-weight: 600; 
      border-radius: 8px; 
      cursor: pointer; 
      transition: all 0.2s ease;
    }

    .btn:hover { 
      background: #1e293b; 
    }

    .btn-gold {
      background: var(--accent-gold);
    }

    .btn-gold:hover {
      background: #b45309;
    }

    .btn-secondary { 
      background: #e2e8f0; 
      color: var(--text-dark);
      margin-top: 1rem;
    }

    .role-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 1.5rem;
      margin-top: 1.5rem;
    }

    .role-card {
      background: #f8fafc;
      border: 1px solid var(--border-color);
      border-radius: var(--radius);
      overflow: hidden;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .role-card:hover {
      border-color: var(--accent-gold);
      transform: translateY(-3px);
      box-shadow: var(--shadow);
    }

    .role-card-img {
      width: 100%;
      height: 150px;
      object-fit: cover;
    }

    .role-card-body {
      padding: 1.5rem;
    }

    .section-img-banner {
      width: 100%;
      height: 140px;
      object-fit: cover;
      border-radius: 8px;
      margin-bottom: 1.5rem;
      border: 1px solid var(--border-color);
    }

    /* Tables */
    .table-container {
      overflow-x: auto;
      border-radius: 8px;
      border: 1px solid var(--border-color);
      margin-top: 1rem;
    }

    table { 
      width: 100%; 
      border-collapse: collapse;
      text-align: left;
      font-size: 0.9rem;
    }

    th, td { 
      padding: 1rem; 
      border-bottom: 1px solid var(--border-color);
    }

    th { 
      background: #f1f5f9; 
      color: #334155; 
      font-weight: 700; 
      text-transform: uppercase;
      font-size: 0.75rem;
    }

    .rx-badge { 
      background: #dcfce7; 
      color: #15803d; 
      padding: 0.35rem 0.75rem; 
      border-radius: 20px; 
      font-weight: 600; 
      font-size: 0.8rem;
    }

    .hidden { display: none; }
  </style>
</head>
<body>

  <!-- Official Header -->
  <header>
    <div class="university-brand">
      <div class="university-crest">OU</div>
      <div class="brand-text">
        <h1>Osus University & Co.</h1>
        <p>Department of Student Health & Clinical Services</p>
      </div>
    </div>
    <div class="campus-badge">Main Campus Hospital</div>
  </header>

  <div class="container">

    <!-- Face Interface / Main Gateway -->
    <div id="roleSelection" class="portal-card">
      <div class="hero-banner">
        <!-- Main Hospital Face Interface Image -->
        <img src="https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&w=1200&q=80" alt="Osus University Hospital Face Interface Building">
        <div class="hero-overlay">
          <div>
            <h2 style="color: white; margin: 0;">Osus Medical Center Gateway</h2>
            <p style="color: #cbd5e1; margin-top: 0.25rem;">Providing healthcare excellence for students, faculty, and administrative staff.</p>
          </div>
        </div>
      </div>

      <div class="official-notice">
        <img src="https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=200&q=80" class="notice-thumb" alt="Hospital Reception">
        <div>
          <strong>📋 Student & Staff Access:</strong> All registered members of Osus University & Co. have access to log clinical consultations, issue paychecks, and query prescribed treatments.
        </div>
      </div>

      <h3>Select Access Portal:</h3>

      <div class="role-grid">
        <div class="role-card" onclick="showView('student')">
          <img src="https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=600&q=80" alt="Student Medical Care" class="role-card-img">
          <div class="role-card-body">
            <h3>Student Portal</h3>
            <p style="color: var(--text-muted); font-size: 0.85rem;">Submit clinic visit requests and view medical records & prescriptions.</p>
          </div>
        </div>

        <div class="role-card" onclick="showView('staff')">
          <img src="https://images.unsplash.com/photo-1516549655169-df83a0774514?auto=format&fit=crop&w=600&q=80" alt="Staff Management Portal" class="role-card-img">
          <div class="role-card-body">
            <h3>Staff & Administration Portal</h3>
            <p style="color: var(--text-muted); font-size: 0.85rem;">Authorized clinical log management, prescriptions, and payroll processing.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Student Interface -->
    <section id="studentView" class="portal-card hidden">
      <div class="hero-banner" style="height: 200px;">
        <img src="https://images.unsplash.com/photo-1581056771107-24ca5f033842?auto=format&fit=crop&w=1200&q=80" alt="Student Care Ward">
        <div class="hero-overlay">
          <h2 style="color: white; margin: 0;">Student Consultation Portal</h2>
        </div>
      </div>

      <div style="border-bottom: 1px solid var(--border-color); padding-bottom: 2rem; margin-bottom: 2rem;">
        <h3>Submit Clinic Visit Record</h3>
        <form id="studentForm">
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
            <div class="form-group">
              <label for="studentName">Student Full Name</label>
              <input type="text" id="studentName" required placeholder="e.g. Jane Smith">
            </div>
            <div class="form-group">
              <label for="studentId">University Student ID</label>
              <input type="text" id="studentId" required placeholder="e.g. OU-2026-889">
            </div>
            <div class="form-group">
              <label for="grade">Faculty / Program</label>
              <input type="text" id="grade" required placeholder="e.g. Faculty of Law">
            </div>
          </div>
          <div class="form-group">
            <label for="complaint">Symptom Description / Reason for Visit</label>
            <textarea id="complaint" rows="3" required placeholder="Describe how you are feeling..."></textarea>
          </div>
          <button type="submit" class="btn">Submit Visit Request</button>
        </form>
      </div>

      <div>
        <h3>Query My Medical History</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
          <div class="form-group">
            <label for="lookupName">Full Name</label>
            <input type="text" id="lookupName" placeholder="e.g. Jane Smith">
          </div>
          <div class="form-group">
            <label for="lookupId">Student ID</label>
            <input type="text" id="lookupId" placeholder="e.g. OU-2026-889">
          </div>
        </div>
        <button class="btn" onclick="lookupStudentRecords()">Search Records</button>

        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>Date / Time</th>
                <th>Symptom Log</th>
                <th>Prescribed Medication</th>
              </tr>
            </thead>
            <tbody id="studentHistoryBody"></tbody>
          </table>
        </div>
      </div>

      <button class="btn btn-secondary" onclick="showView('role')">← Back to Main Gateway</button>
    </section>

    <!-- Staff & Administration Interface -->
    <section id="staffView" class="portal-card hidden">
      <div class="hero-banner" style="height: 200px;">
        <img src="https://images.unsplash.com/photo-1505751172876-fa1923c5c528?auto=format&fit=crop&w=1200&q=80" alt="Clinical Office">
        <div class="hero-overlay">
          <h2 style="color: white; margin: 0;">Clinical Administration & Payroll Terminal</h2>
        </div>
      </div>

      <!-- Authentication with Password Eye Toggle -->
      <div style="display: flex; gap: 1rem; align-items: flex-end; margin-bottom: 2rem; border-bottom: 1px solid var(--border-color); padding-bottom: 1.5rem;">
        <div class="form-group" style="flex: 1; margin: 0;">
          <label for="viewPassword">Staff Security Clearance Key</label>
          <div class="password-wrapper">
            <input type="password" id="viewPassword" placeholder="Enter staff clearance password...">
            <span class="eye-toggle" onclick="togglePasswordVisibility()">
              <svg id="eyeIcon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                <circle cx="12" cy="12" r="3"></circle>
              </svg>
            </span>
          </div>
        </div>
        <button class="btn" onclick="loadStaffData()">Authenticate Clearance</button>
      </div>

      <!-- Sub-tabs for Medical vs Payroll -->
      <div style="margin-bottom: 1.5rem;">
        <button class="btn btn-gold" onclick="switchStaffTab('medical')">🏥 Patient Log & Prescriptions</button>
        <button class="btn btn-gold" style="background: #475569;" onclick="switchStaffTab('payroll')">💼 Staff Payroll Checks</button>
      </div>

      <!-- Medical Tab -->
      <div id="medicalSection">
        <img src="https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=1200&q=80" class="section-img-banner" alt="Medical Consultation Desk">
        <h3>Patient Consultation Log</h3>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Student Name</th>
                <th>Student ID</th>
                <th>Faculty</th>
                <th>Symptoms</th>
                <th>Prescribe Medication</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody id="staffRecordsBody"></tbody>
          </table>
        </div>
      </div>

      <!-- Payroll Tab -->
      <div id="payrollSection" class="hidden">
        <img src="https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=1200&q=80" class="section-img-banner" alt="Payroll Accounting Desk">
        <h3>Medical Staff Payroll Records</h3>
        
        <!-- Add Paycheck Form -->
        <div style="background: #f8fafc; padding: 1.5rem; border-radius: 8px; border: 1px solid var(--border-color); margin-bottom: 1.5rem;">
          <h4 style="margin-bottom: 1rem; color: var(--primary-navy);">Issue New Paycheck</h4>
          <form id="payrollForm" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem;">
            <div class="form-group">
              <label for="payStaffName">Staff Name</label>
              <input type="text" id="payStaffName" required placeholder="e.g. Dr. Sarah Jenkins">
            </div>
            <div class="form-group">
              <label for="payRole">Role</label>
              <input type="text" id="payRole" required placeholder="e.g. Medical Officer">
            </div>
            <div class="form-group">
              <label for="payBase">Base Pay ($)</label>
              <input type="number" id="payBase" step="0.01" required placeholder="4500.00">
            </div>
            <div class="form-group">
              <label for="payBonus">Bonus ($)</label>
              <input type="number" id="payBonus" step="0.01" value="0.00">
            </div>
            <div class="form-group" style="grid-column: 1 / -1;">
              <button type="submit" class="btn btn-gold">Process Paycheck Issue</button>
            </div>
          </form>
        </div>

        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>Issue Date</th>
                <th>Staff Name</th>
                <th>Role</th>
                <th>Base Pay</th>
                <th>Bonus</th>
                <th>Total Pay Disbursement</th>
              </tr>
            </thead>
            <tbody id="payrollRecordsBody"></tbody>
          </table>
        </div>
      </div>

      <button class="btn btn-secondary" onclick="showView('role')">← Back to Main Gateway</button>
    </section>

  </div>

  <script>
    // Eye Icon Toggle Function
    function togglePasswordVisibility() {
      const pwdInput = document.getElementById("viewPassword");
      const eyeIcon = document.getElementById("eyeIcon");
      
      if (pwdInput.type === "password") {
        pwdInput.type = "text";
        eyeIcon.innerHTML = `
          <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
          <line x1="1" y1="1" x2="23" y2="23"></line>
        `;
      } else {
        pwdInput.type = "password";
        eyeIcon.innerHTML = `
          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
          <circle cx="12" cy="12" r="3"></circle>
        `;
      }
    }

    function showView(view) {
      document.getElementById('roleSelection').classList.add('hidden');
      document.getElementById('studentView').classList.add('hidden');
      document.getElementById('staffView').classList.add('hidden');

      if (view === 'student') {
        document.getElementById('studentView').classList.remove('hidden');
      } else if (view === 'staff') {
        document.getElementById('staffView').classList.remove('hidden');
      } else if (view === 'role') {
        document.getElementById('roleSelection').classList.remove('hidden');
      }
    }

    function switchStaffTab(tab) {
      if (tab === 'medical') {
        document.getElementById('medicalSection').classList.remove('hidden');
        document.getElementById('payrollSection').classList.add('hidden');
      } else {
        document.getElementById('medicalSection').classList.add('hidden');
        document.getElementById('payrollSection').classList.remove('hidden');
      }
    }

    // Submit new student visit
    document.getElementById("studentForm").addEventListener("submit", (e) => {
      e.preventDefault();
      
      const formData = {
        student_name: document.getElementById("studentName").value,
        student_id: document.getElementById("studentId").value,
        grade: document.getElementById("grade").value,
        complaint: document.getElementById("complaint").value
      };

      fetch("/api/records", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
      })
      .then(res => res.json())
      .then(data => {
        if (data.status === "success") {
          document.getElementById("studentForm").reset();
          alert("Visit record successfully submitted to Osus University Health Services!");
        }
      });
    });

    // Student Lookup
    function lookupStudentRecords() {
      const name = document.getElementById("lookupName").value.trim();
      const studentId = document.getElementById("lookupId").value.trim();

      if (!name || !studentId) {
        alert("Please enter both Name and University Student ID.");
        return;
      }

      fetch(`/api/student/records?name=${encodeURIComponent(name)}&student_id=${encodeURIComponent(studentId)}`)
      .then(res => res.json())
      .then(records => {
        const body = document.getElementById("studentHistoryBody");
        body.innerHTML = "";
        if (records.length === 0) {
          body.innerHTML = "<tr><td colspan='3' style='text-align:center; color: var(--text-muted);'>No clinical logs found.</td></tr>";
          return;
        }
        records.forEach(rec => {
          const row = document.createElement("tr");
          row.innerHTML = `
            <td>${rec.date}</td>
            <td>${rec.complaint}</td>
            <td><span class="rx-badge">${rec.prescribed_drug || "Pending Clinical Review"}</span></td>
          `;
          body.appendChild(row);
        });
      });
    }

    // Authenticate and Load Staff Data
    function loadStaffData() {
      const password = document.getElementById("viewPassword").value;

      fetch("/api/staff/records", {
        method: "GET",
        headers: { "X-Clinic-Password": password }
      })
      .then(res => {
        if (res.status === 401) {
          alert("Clearance Denied: Invalid Staff Password");
          return null;
        }
        return res.json();
      })
      .then(data => {
        if (!data) return;

        // Render Patient Records
        const medicalBody = document.getElementById("staffRecordsBody");
        medicalBody.innerHTML = "";
        data.medical_records.forEach(rec => {
          const row = document.createElement("tr");
          row.innerHTML = `
            <td>${rec.id}</td>
            <td><strong>${rec.student_name}</strong></td>
            <td>${rec.student_id}</td>
            <td>${rec.grade}</td>
            <td>${rec.complaint}</td>
            <td>
              <input type="text" id="rx-${rec.id}" value="${rec.prescribed_drug || ''}" placeholder="Prescribe drug...">
            </td>
            <td>
              <button class="btn" style="padding: 0.4rem 0.8rem; font-size: 0.8rem;" onclick="updatePrescription(${rec.id})">Save Rx</button>
            </td>
          `;
          medicalBody.appendChild(row);
        });

        // Render Payroll Records
        renderPayrollTable(data.payroll_records);
      });
    }

    function renderPayrollTable(payrolls) {
      const payrollBody = document.getElementById("payrollRecordsBody");
      payrollBody.innerHTML = "";
      payrolls.forEach(pay => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${pay.pay_date}</td>
          <td><strong>${pay.staff_name}</strong></td>
          <td>${pay.role}</td>
          <td>$${pay.base_salary.toFixed(2)}</td>
          <td>$${pay.bonus.toFixed(2)}</td>
          <td><strong style="color: #15803d;">$${pay.total_pay.toFixed(2)}</strong></td>
        `;
        payrollBody.appendChild(row);
      });
    }

    // Issue New Paycheck
    document.getElementById("payrollForm").addEventListener("submit", (e) => {
      e.preventDefault();
      const password = document.getElementById("viewPassword").value;

      const payrollData = {
        staff_name: document.getElementById("payStaffName").value,
        role: document.getElementById("payRole").value,
        base_salary: parseFloat(document.getElementById("payBase").value),
        bonus: parseFloat(document.getElementById("payBonus").value)
      };

      fetch("/api/staff/payroll", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Clinic-Password": password
        },
        body: JSON.stringify(payrollData)
      })
      .then(res => res.json())
      .then(data => {
        if (data.status === "success") {
          alert("Paycheck issued and disbursed successfully!");
          renderPayrollTable(data.payroll_records);
          document.getElementById("payrollForm").reset();
        } else {
          alert("Error: " + data.message);
        }
      });
    });

    // Update Prescription
    function updatePrescription(recordId) {
      const password = document.getElementById("viewPassword").value;
      const drug = document.getElementById(`rx-${recordId}`).value;

      fetch(`/api/records/${recordId}/prescribe`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "X-Clinic-Password": password
        },
        body: JSON.stringify({ prescribed_drug: drug })
      })
      .then(res => res.json())
      .then(data => {
        if (data.status === "success") {
          alert("Prescription updated!");
        } else {
          alert("Failed to update prescription.");
        }
      });
    }
  </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

# Submit record from student interface
@app.route("/api/records", methods=["POST"])
def add_record():
    data = request.json
    new_record = {
        "id": len(medical_records) + 1,
        "student_name": data["student_name"].strip(),
        "student_id": data["student_id"].strip(),
        "grade": data["grade"].strip(),
        "complaint": data["complaint"].strip(),
        "prescribed_drug": "",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    medical_records.append(new_record)
    return jsonify({"status": "success", "record": new_record})

# Student Lookup Route
@app.route("/api/student/records", methods=["GET"])
def get_student_records():
    name = request.args.get("name", "").strip().lower()
    student_id = request.args.get("student_id", "").strip().lower()
    
    matching = [
        rec for rec in medical_records 
        if rec["student_name"].lower() == name and rec["student_id"].lower() == student_id
    ]
    return jsonify(matching)

# Staff View All Records & Payroll
@app.route("/api/staff/records", methods=["GET"])
def get_staff_records():
    password = request.headers.get("X-Clinic-Password")
    if password != ACCESS_PASSWORD:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    return jsonify({
        "medical_records": medical_records,
        "payroll_records": payroll_records
    })

# Add Paycheck Route
@app.route("/api/staff/payroll", methods=["POST"])
def add_paycheck():
    password = request.headers.get("X-Clinic-Password")
    if password != ACCESS_PASSWORD:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
        
    data = request.json
    base = float(data.get("base_salary", 0))
    bonus = float(data.get("bonus", 0))
    
    new_paycheck = {
        "id": len(payroll_records) + 1,
        "staff_name": data.get("staff_name", "").strip(),
        "role": data.get("role", "").strip(),
        "base_salary": base,
        "bonus": bonus,
        "total_pay": base + bonus,
        "pay_date": datetime.now().strftime("%Y-%m-%d")
    }
    payroll_records.append(new_paycheck)
    return jsonify({"status": "success", "payroll_records": payroll_records})

# Staff Prescribe / Update Drug Route
@app.route("/api/records/<int:record_id>/prescribe", methods=["PUT"])
def update_prescription(record_id):
    password = request.headers.get("X-Clinic-Password")
    if password != ACCESS_PASSWORD:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
        
    data = request.json
    for rec in medical_records:
        if rec["id"] == record_id:
            rec["prescribed_drug"] = data.get("prescribed_drug", "").strip()
            return jsonify({"status": "success", "record": rec})
            
    return jsonify({"status": "error", "message": "Record not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
