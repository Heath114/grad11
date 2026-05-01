async function initDashboard() {
    const isAuthed = await isAuthenticated();
    
    const logoutBtn = document.getElementById('logoutBtn');
    if (!isAuthed) {
        // Just browsing mode - change "Sign Out" to "Go Back"
        logoutBtn.textContent = 'Go Back to Login';
        logoutBtn.addEventListener('click', () => {
            window.location.href = 'index.html';
        });
        return;
    }
    
    logoutBtn.addEventListener('click', () => {
        logout();
    });

    fetchOrders();
    setInterval(fetchOrders, 2000); // 2 seconds polling
}

let lastOrdersMarkup = '';
let lastOrdersVisible = false;

async function fetchOrders() {
    const { ok, data } = await apiCall('/orders/user');
    const container = document.getElementById('activeOrdersContainer');
    const list = document.getElementById('orderList');

    if (!ok || !data || data.length === 0) {
        if (lastOrdersVisible) {
            container.style.display = 'none';
            lastOrdersVisible = false;
            lastOrdersMarkup = '';
        }
        return;
    }

    // Only show orders that are not completed
    const recentOrders = data.filter(o => o.status !== 'completed').slice(0, 3);
    
    if (recentOrders.length > 0) {
        const nextMarkup = recentOrders.map(OrderCard).join('');
        if (!lastOrdersVisible) {
            container.style.display = 'block';
            lastOrdersVisible = true;
        }
        if (nextMarkup !== lastOrdersMarkup) {
            list.innerHTML = nextMarkup;
            lastOrdersMarkup = nextMarkup;
        }
    } else {
        if (lastOrdersVisible) {
            container.style.display = 'none';
            lastOrdersVisible = false;
            lastOrdersMarkup = '';
        }
    }
}

function getSteps(orderType, currentStatus) {
    const steps = orderType === 'Delivery' 
        ? ['pending', 'preparing', 'ready', 'out_for_delivery']
        : ['pending', 'preparing', 'ready'];
        
    const labels = orderType === 'Delivery' 
        ? ['Pending', 'Preparing', 'Ready', 'Out for Delivery']
        : ['Pending', 'Preparing', 'Ready for Pickup'];

    const currentIndex = steps.indexOf(currentStatus) !== -1 ? steps.indexOf(currentStatus) : steps.length - 1;

    return steps.map((step, idx) => {
        let className = 'tracker-step';
        if (idx < currentIndex) className += ' completed';
        if (idx === currentIndex) className += ' active';
        
        return `<div class="${className}">${labels[idx]}</div>`;
    }).join('');
}

function formatStatus(status) {
    if (status === 'out_for_delivery') return 'Out for Delivery';
    if (status === 'ready') return 'Ready for Pickup';
    if (status === 'preparing') return 'Preparing';
    return 'Pending';
}

function OrderCard(order) {
    const isDelivery = order.orderType === 'Delivery';
    const items = order.items.map(i => `${i.name} (x1)`).join(', ');
    const time = new Date(order.createdAt).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});

    return `
        <div class="order-tracker">
            <div class="tracker-header">
                <div>
                    <div class="tracker-title">Order #${order.id} - ${order.orderType}</div>
                    <div class="tracker-meta">${time} • ${items.length > 40 ? items.substring(0,40)+'...' : items}</div>
                </div>
                <div style="display: flex; gap: 8px;">
                    ${order.status === 'ready' || order.status === 'out_for_delivery' ? 
                        `<button onclick="collectOrder(${order.id})" class="collect-btn">Mark as ${isDelivery ? 'Received' : 'Collected'}</button>` 
                    : ''}
                    <div class="tracker-badge ${order.status}">${formatStatus(order.status)}</div>
                </div>
            </div>
            <div class="tracker-steps">
                ${getSteps(order.orderType, order.status)}
            </div>
        </div>
    `;
}

document.addEventListener('DOMContentLoaded', initDashboard);

async function collectOrder(orderId) {
    await apiCall(`/orders/${orderId}/complete`, 'POST');
    fetchOrders();
}

// --- Complaints System ---
document.getElementById('complaintForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const type = document.getElementById('complaintType').value;
    const email = document.getElementById('complaintEmail').value.trim();
    const subject = document.getElementById('complaintSubject').value.trim();
    const message = document.getElementById('complaintMessage').value.trim();
    const feedback = document.getElementById('complaintFeedback');
    const btn = document.getElementById('submitComplaintBtn');

    if (!email || !subject || !message) {
        feedback.textContent = 'All fields are required.';
        feedback.className = 'complaint-feedback error';
        return;
    }

    btn.disabled = true;
    btn.textContent = 'Sending...';
    feedback.className = 'complaint-feedback';
    feedback.textContent = '';

    const { ok, data } = await apiCall('/complaints/', 'POST', {
        type,
        email,
        subject,
        message
    });

    btn.disabled = false;
    btn.textContent = 'Send Message';

    if (ok && data?.success) {
        feedback.textContent = data.message || 'Submitted successfully!';
        feedback.className = 'complaint-feedback success';
        document.getElementById('complaintForm').reset();
    } else {
        feedback.textContent = data?.message || 'Failed to submit. Please try again.';
        feedback.className = 'complaint-feedback error';
    }
});
