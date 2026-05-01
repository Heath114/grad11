        async function fetchAdminOrders() {
            const { ok, data } = await apiCall(`/orders/cafeteria/${activeCafeteriaId}`);
            if (!ok) return;

            const orders = data || [];
            
            if (orders.length === 0) {
                ordersContainer.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-state-icon">📋</div>
                        <h3>No orders yet</h3>
                        <p>Orders will appear here in real-time</p>
                    </div>
                `;
                return;
            }

            ordersContainer.innerHTML = `
                <div class="orders-list">
                    ${orders.map(order => {
                        return `
                            <div class="order-card">
                                <div class="order-header">
                                    <div class="order-cafeteria">${resolvedCafeteriaName}</div>
                                    <div class="order-meta">
                                        <span class="order-type order-type--${(order.orderType || 'Pickup').toLowerCase()}">${(order.orderType || 'Pickup').toUpperCase()}</span>
                                        <span class="order-type" style="background:#edf2f7;color:#333;margin-left:4px;">${order.status.toUpperCase()}</span>
                                        <span class="order-type">${order.paymentMethod || 'CASH'}</span>
                                        <span class="order-time">${formatDateTime(new Date(order.createdAt))}</span>
                                    </div>
                                </div>
                                ${order.deliveryLocation ? `
                                    <div class="delivery-location">
                                        <span class="location-icon">📍</span>
                                        <span class="location-text">${order.deliveryLocation}</span>
                                    </div>
                                ` : ''}
                                ${order.items.map(item => `
                                    <div class="order-item">
                                        <div class="order-details">
                                            <span class="order-item-name">${item.name}</span>
                                            ${item.addOns && item.addOns.length ? `
                                                <ul class="order-addons">
                                                    ${item.addOns.map(addOn => `
                                                        <li>${addOn.name}<span class="addon-price">${addOn.price} JOD</span></li>
                                                    `).join('')}
                                                </ul>
                                            ` : ''}
                                        </div>
                                        <span class="order-price">${item.price} JOD</span>
                                    </div>
                                `).join('')}
                                <div class="order-total">
                                    <strong>Total:</strong> ${order.total.toFixed(2)} JOD
                                </div>
                                <div class="order-user">
                                    <span class="order-user-name">${order.userName}</span>
                                    ${order.userPhone ? `<span class="order-user-phone">${order.userPhone}</span>` : ''}
                                </div>
                            </div>
                        `;
                    }).join('')}
                </div>
            `;
        }

        async function fetchAdminReviews() {
            const reviewsContainer = document.getElementById('reviewsContainer');
            const adminReviewStats = document.getElementById('adminReviewStats');
            
            const { ok, data } = await apiCall(`/ratings/${activeCafeteriaId}`);
            if (!ok || !data) return;

            adminReviewStats.innerHTML = `<strong>${data.average.toFixed(1)}</strong> ⭐ (${data.total} reviews)`;

            if (data.reviews.length === 0) {
                reviewsContainer.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-state-icon">⭐</div>
                        <h3>No reviews yet</h3>
                        <p>Customer feedback will appear here</p>
                    </div>
                `;
                return;
            }

            reviewsContainer.innerHTML = `
                <div class="orders-list">
                    ${data.reviews.map(r => `
                        <div class="order-card" style="border-left: 4px solid #f4a261;">
                            <div class="order-header" style="border-bottom: none; margin-bottom: 8px; padding-bottom: 0;">
                                <div class="order-meta">
                                    <div style="color: #f4a261; font-size: 14px; margin-bottom: 4px;">
                                        ${'★'.repeat(r.score)}${'☆'.repeat(5 - r.score)}
                                    </div>
                                </div>
                                <span class="order-time">${formatDateTime(new Date(r.createdAt))}</span>
                            </div>
                            ${r.comment ? `<p style="margin: 0 0 12px 0; font-size: 14px; color: #1f1f1f; line-height: 1.5;">"${r.comment}"</p>` : ''}
                            <div class="order-user" style="border-top: 1px solid #f1f1f1; padding-top: 12px;">
                                <span class="order-user-name" style="font-weight: 500; font-size: 13px; color: #666;">By: ${r.userName}</span>
                            </div>
                        </div>
                    `).join('')}
                </div>
            `;
        }

        function updateAdminDashboard() {
            fetchAdminOrders();
            fetchAdminReviews();
        }

        updateAdminDashboard();

        document.getElementById('clearOrdersBtn').addEventListener('click', async function() {
            if (confirm('Are you sure you want to clear all orders for this cafeteria? This action cannot be undone.')) {
                const { ok } = await apiCall(`/orders/cafeteria/${activeCafeteriaId}/clear`, 'DELETE');
                if (ok) {
                    fetchAdminOrders();
                } else {
                    alert('Failed to clear orders. Please try again.');
                }
            }
        });

        setInterval(updateAdminDashboard, 2000);
