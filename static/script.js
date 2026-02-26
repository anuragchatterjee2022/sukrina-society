// --- 8 Member Data ---
const societyMembers = [
    { id: 1, name: "Kingshuk Dasgupta", role: "Chairman", flat: "A-101", phone: "9876543210", address: "Tower A, Sukrina Co-op", nominee: "Anushka", photo: "static/1.jpeg" },
    { id: 2, name: "Debajyoti Ghosal", role: "Vice Chairman", flat: "A-102", phone: "9830011223", address: "Tower A, Sukrina Co-op", nominee: "Sunita", photo: "static/rahul.jpg" },
    { id: 3, name: "Koushik Ghosh", role: "Secretary", flat: "B-201", phone: "9831155443", address: "Tower B, Sukrina Co-op", nominee: "Amit", photo: "static/priya.jpg" },
    { id: 4, name: "Amitabha Ganguly", role: "Treasurer", flat: "B-205", phone: "7001223344", address: "Tower B, Sukrina Co-op", nominee: "Rina", photo: "static/sayan.jpg" },
    { id: 5, name: "Arindam Saha", role: "Member", flat: "C-104", phone: "+91 96470 18272", address: "Tower C, Sukrina Co-op", nominee: "Mallika Saha", photo: "static/112.jpeg" },
    { id: 6, name: "Chandan Bandopadhyay", role: "Member", flat: "C-302", phone: "8100223344", address: "Tower C, Sukrina Co-op", nominee: "Raj", photo: "static/sneha.jpg" },
    { id: 7, name: "Abhijit Biswas", role: "Member", flat: "D-101", phone: "9433066778", address: "Tower D, Sukrina Co-op", nominee: "Pooja", photo: "static/arjun.jpg" },
    { id: 8, name: "Manisha Dutta", role: "Member", flat: "D-404", phone: "9123445566", address: "Tower D, Sukrina Co-op", nominee: "Sujit", photo: "static/ishani.jpg" }
];

// --- SPA View Swapper ---
function showSection(id) {
    // Hide all views
    document.querySelectorAll('.view').forEach(v => v.style.display = 'none');
    // Show requested view
    const target = document.getElementById(id);
    if(target) {
        target.style.display = 'block';
    }
    // Always scroll to top
    window.scrollTo(0, 0);
}

// --- Directory Table Generator ---
function loadDirectory() {
    const tableBody = document.getElementById('member-list-body');
    if(!tableBody) return;

    // This loop connects your 8 members to the table
    tableBody.innerHTML = societyMembers.map(m => `
        <tr onclick="showProfile(${m.id}); showSection('profile-view')" style="cursor: pointer;">
            <td>${m.flat}</td>
            <td class="resident-link">${m.name}</td>
            <td><span class="status-dot"></span> Active</td>
        </tr>
    `).join('');
}

// Make sure the list loads when the page opens
window.onload = loadDirectory;

// --- Profile Page Logic ---
function showProfile(id) {
    const m = societyMembers.find(member => member.id === id);
    if (!m) return;

    // These IDs must match your <span> tags in index.html
    document.getElementById('p-name').innerText = m.name;
    document.getElementById('p-role').innerText = m.role;
    document.getElementById('p-phone').innerText = m.phone;
    document.getElementById('p-address').innerText = m.address;
    document.getElementById('p-nominee').innerText = m.nominee;
    document.getElementById('p-flat').innerText = m.flat;
    document.getElementById('p-display-name').innerText = m.name;
    document.getElementById('p-photo').src = m.photo;

}
    // Updates profile photo with fallback
    const photoEl = document.getElementById('p-photo');
    photoEl.src = m.photo;
    photoEl.onerror = function() {
        this.src = `https://ui-avatars.com/api/?name=${m.name}&background=1a1a1a&color=fff&size=200`;
    };

    // Switch to the profile view
    showSection('profile-view');


// --- FIXED RECEIPT GENERATOR ---
function generateReceipt(e) {
    e.preventDefault();
    const name = document.getElementById('pay-name').value;
    const flat = document.getElementById('pay-flat').value;
    const amount = document.getElementById('pay-amount').value;
    const month = document.getElementById('pay-month').value;

    const receiptWin = window.open('', '_blank');
    receiptWin.document.write(`
        <div style="font-family: sans-serif; padding: 50px; border: 10px solid #1a1a6c; max-width: 500px; margin: auto; border-radius: 20px;">
            <h1 style="color: #1a1a6c; text-align: center;">SUKRINA CO-OP</h1>
            <h3 style="text-align: center; border-bottom: 2px solid #f1c40f; padding-bottom: 10px;">Payment Receipt</h3>
            <p><strong>Resident:</strong> ${name}</p>
            <p><strong>Flat:</strong> ${flat}</p>
            <p><strong>Month:</strong> ${month}</p>
            <p style="font-size: 1.5rem; color: #27ae60;"><strong>Amount Paid: ₹${amount}</strong></p>
            <p style="margin-top: 40px; font-style: italic; font-size: 0.8rem;">Computer generated receipt. Valid as proof of payment.</p>
            <button onclick="window.print()" style="padding: 10px 20px; background: #1a1a6c; color: white; border: none; cursor: pointer; border-radius: 5px;">Print Receipt</button>
        </div>
    `);
}

// --- Helpdesk Logic ---
function handleComplaint(e) {
    e.preventDefault();
    const id = "SUK-" + Math.floor(1000 + Math.random() * 9000);
    document.getElementById('ticket-status').innerHTML = 
        `<p style="color:#27ae60; margin-top:15px;">Success! Formal Ticket ID: <strong>${id}</strong></p>`;
}

// --- Poll Logic ---
function castVote(choice) {
    document.getElementById('poll-options').style.display = 'none';
    document.getElementById('poll-results').style.display = 'block';
    document.getElementById('poll-bar').style.width = choice === 'Yes' ? "90%" : "10%";
    document.getElementById('poll-text').innerText = choice === 'Yes' ? "90% agreed" : "10% disagreed";
}

// Ensure the directory loads on startup
window.onload = function() {
    loadDirectory();
    // Default starting notices
    const noticeArea = document.getElementById('notice-list');
    if (noticeArea && !noticeArea.innerHTML.trim()) {
        noticeArea.innerHTML = `
            <p>● Maintenance Payment deadline: March 5th.</p>
            <p>● Lift Service in Block B scheduled for Saturday.</p>
        `;
    }
};