document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const form = document.getElementById('fuzzy-form');
    const businessFieldSelect = document.getElementById('business-field');
    const scaleSelect = document.getElementById('scale');
    const usageTypeSelect = document.getElementById('usage-type');
    const submitBtn = document.querySelector('.submit-btn');
    const resultSection = document.getElementById('result-section');
    const newEvaluationBtn = document.getElementById('new-evaluation');
    
    // Stats elements
    const totalCreditEl = document.getElementById('total-credit');
    const totalFieldsEl = document.getElementById('total-fields');
    
    // Result elements
    const approvalScoreEl = document.getElementById('approval-score');
    const approvalCategoryEl = document.getElementById('approval-category');
    const recommendationsListEl = document.getElementById('recommendations-list');
    
    // Analysis elements
    const inputFieldEl = document.getElementById('input-field');
    const inputScaleEl = document.getElementById('input-scale');
    const inputUsageEl = document.getElementById('input-usage');
    const fuzzyScaleEl = document.getElementById('fuzzy-scale');
    const fuzzyRiskEl = document.getElementById('fuzzy-risk');
    const fuzzyPriorityEl = document.getElementById('fuzzy-priority');
    const creditRangeEl = document.getElementById('credit-range');
    const fieldCreditEl = document.getElementById('field-credit');
    const usageCreditEl = document.getElementById('usage-credit');
    
    // Visualization elements
    const fuzzyVisualizationEl = document.getElementById('fuzzy-visualization');
    const visualizationPlaceholder = document.querySelector('.visualization-placeholder');
    
    // Tab elements
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    // Chart instances
    let businessFieldsChart = null;
    let scalesChart = null;
    let usageChart = null;

    // Initialize the application
    init();

    async function init() {
        await loadStatistics();
        await loadOptions();
        await loadCharts();
        setupEventListeners();
        initializeAnimations();
    }

    // Load statistics from API
    async function loadStatistics() {
        try {
            const response = await fetch('/api/statistics');
            const stats = await response.json();
            
            // Animate statistics
            animateValue(totalCreditEl, 0, parseInt(stats.total_credit.replace(/,/g, '')), 2000, true);
            animateValue(totalFieldsEl, 0, stats.total_business_fields, 1500);
            
        } catch (error) {
            console.error('Error loading statistics:', error);
            totalCreditEl.textContent = 'N/A';
            totalFieldsEl.textContent = 'N/A';
        }
    }

    // Load form options from API
    async function loadOptions() {
        try {
            const response = await fetch('/api/get_options');
            const options = await response.json();
            
            // Clear existing options except the first one
            while (businessFieldSelect.children.length > 1) {
                businessFieldSelect.removeChild(businessFieldSelect.lastChild);
            }
            while (scaleSelect.children.length > 1) {
                scaleSelect.removeChild(scaleSelect.lastChild);
            }
            while (usageTypeSelect.children.length > 1) {
                usageTypeSelect.removeChild(usageTypeSelect.lastChild);
            }
            
            // Populate business fields
            options.business_fields.forEach(field => {
                const option = document.createElement('option');
                option.value = field;
                option.textContent = field;
                businessFieldSelect.appendChild(option);
            });
            
            // Populate scales
            options.scales.forEach(scale => {
                const option = document.createElement('option');
                option.value = scale;
                option.textContent = scale;
                scaleSelect.appendChild(option);
            });
            
            // Populate usage types
            options.usage_types.forEach(usage => {
                const option = document.createElement('option');
                option.value = usage;
                option.textContent = usage;
                usageTypeSelect.appendChild(option);
            });
            
            // Add change event listeners for immediate selection
            businessFieldSelect.addEventListener('change', handleSelectionChange);
            scaleSelect.addEventListener('change', handleSelectionChange);
            usageTypeSelect.addEventListener('change', handleSelectionChange);
            
        } catch (error) {
            console.error('Error loading options:', error);
            showError('Gagal memuat opsi. Silakan refresh halaman.');
        }
    }

    // Handle selection changes
    function handleSelectionChange(event) {
        const select = event.target;
        if (select.value) {
            select.style.borderColor = 'var(--success-color)';
            select.style.boxShadow = '0 0 0 3px rgba(16, 185, 129, 0.2)';
            
            // Remove validation styling after 2 seconds
            setTimeout(() => {
                select.style.borderColor = '';
                select.style.boxShadow = '';
            }, 2000);
        }
    }

    // Load charts data
    async function loadCharts() {
        try {
            const response = await fetch('/api/chart_data');
            const chartData = await response.json();
            
            // Initialize charts
            initializeBusinessFieldsChart(chartData.business_fields);
            initializeScalesChart(chartData.scales);
            initializeUsageChart(chartData.usage_types);
            
        } catch (error) {
            console.error('Error loading chart data:', error);
        }
    }

    // Initialize business fields chart
    function initializeBusinessFieldsChart(data) {
        const ctx = document.getElementById('business-fields-chart').getContext('2d');
        
        // Get top 10 business fields
        const sortedData = data.labels
            .map((label, index) => ({ label, value: data.values[index] }))
            .sort((a, b) => b.value - a.value)
            .slice(0, 10);
        
        businessFieldsChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: sortedData.map(item => item.label.length > 20 ?
                    item.label.substring(0, 20) + '...' : item.label),
                datasets: [{
                    label: 'Jumlah Kredit (Miliar)',
                    data: sortedData.map(item => item.value),
                    backgroundColor: 'rgba(59, 130, 246, 0.6)',
                    borderColor: 'rgba(59, 130, 246, 1)',
                    borderWidth: 2,
                    borderRadius: 8,
                    hoverBackgroundColor: 'rgba(59, 130, 246, 0.8)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        borderRadius: 8,
                        callbacks: {
                            label: function(context) {
                                return `Kredit: ${context.parsed.y.toLocaleString('id-ID')} Miliar`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        },
                        ticks: {
                            callback: function(value) {
                                return value.toLocaleString('id-ID');
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            maxRotation: 45,
                            minRotation: 45
                        }
                    }
                },
                animation: {
                    duration: 1500,
                    easing: 'easeOutQuart'
                }
            }
        });
    }

    // Initialize scales chart
    function initializeScalesChart(data) {
        const ctx = document.getElementById('scales-chart').getContext('2d');
        
        scalesChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.values,
                    backgroundColor: [
                        'rgba(59, 130, 246, 0.8)',
                        'rgba(16, 185, 129, 0.8)',
                        'rgba(245, 158, 11, 0.8)'
                    ],
                    borderColor: [
                        'rgba(59, 130, 246, 1)',
                        'rgba(16, 185, 129, 1)',
                        'rgba(245, 158, 11, 1)'
                    ],
                    borderWidth: 2,
                    hoverOffset: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 15,
                            font: {
                                size: 12
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        borderRadius: 8,
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((context.parsed / total) * 100).toFixed(1);
                                return `${context.label}: ${context.parsed.toLocaleString('id-ID')} Miliar (${percentage}%)`;
                            }
                        }
                    }
                },
                animation: {
                    animateRotate: true,
                    animateScale: true,
                    duration: 1500,
                    easing: 'easeOutQuart'
                }
            }
        });
    }

    // Initialize usage chart
    function initializeUsageChart(data) {
        const ctx = document.getElementById('usage-chart').getContext('2d');
        
        usageChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.values,
                    backgroundColor: [
                        'rgba(147, 51, 234, 0.8)',
                        'rgba(236, 72, 153, 0.8)'
                    ],
                    borderColor: [
                        'rgba(147, 51, 234, 1)',
                        'rgba(236, 72, 153, 1)'
                    ],
                    borderWidth: 2,
                    hoverOffset: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 15,
                            font: {
                                size: 12
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        borderRadius: 8,
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((context.parsed / total) * 100).toFixed(1);
                                return `${context.label}: ${context.parsed.toLocaleString('id-ID')} Miliar (${percentage}%)`;
                            }
                        }
                    }
                },
                animation: {
                    animateRotate: true,
                    animateScale: true,
                    duration: 1500,
                    easing: 'easeOutQuart'
                }
            }
        });
    }

    // Setup event listeners
    function setupEventListeners() {
        form.addEventListener('submit', handleFormSubmit);
        newEvaluationBtn.addEventListener('click', resetForm);
        
        // Tab switching
        tabBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const targetTab = btn.dataset.tab;
                switchTab(targetTab);
            });
        });
    }

    // Switch tab functionality
    function switchTab(targetTab) {
        // Remove active class from all tabs and panes
        tabBtns.forEach(btn => btn.classList.remove('active'));
        tabPanes.forEach(pane => pane.classList.remove('active'));
        
        // Add active class to target tab and pane
        const targetBtn = document.querySelector(`[data-tab="${targetTab}"]`);
        const targetPane = document.getElementById(`${targetTab}-tab`);
        
        if (targetBtn && targetPane) {
            targetBtn.classList.add('active');
            targetPane.classList.add('active');
        }
    }

    // Initialize animations
    function initializeAnimations() {
        // Add entrance animations to stat cards
        const statCards = document.querySelectorAll('.stat-card');
        statCards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            setTimeout(() => {
                card.style.transition = 'all 0.6s ease-out';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 200);
        });
        
        // Add entrance animations to chart cards
        const chartCards = document.querySelectorAll('.chart-card');
        chartCards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            setTimeout(() => {
                card.style.transition = 'all 0.6s ease-out';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 600 + (index * 200));
        });
    }

    // Handle form submission
    async function handleFormSubmit(e) {
        e.preventDefault();
        
        if (!validateForm()) {
            return;
        }
        
        const formData = {
            business_field: businessFieldSelect.value,
            scale: scaleSelect.value,
            usage_type: usageTypeSelect.value
        };
        
        showLoading(true);
        
        try {
            const response = await fetch('/api/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            
            if (!response.ok) {
                throw new Error(result.error || 'Terjadi kesalahan');
            }
            
            displayResults(result);
            
        } catch (error) {
            console.error('Error calculating:', error);
            showError(error.message);
        } finally {
            showLoading(false);
        }
    }

    // Validate form
    function validateForm() {
        const businessField = businessFieldSelect.value;
        const scale = scaleSelect.value;
        const usageType = usageTypeSelect.value;
        
        if (!businessField || !scale || !usageType) {
            showError('Silakan lengkapi semua field');
            return false;
        }
        
        return true;
    }

    // Show loading state
    function showLoading(isLoading) {
        if (isLoading) {
            submitBtn.classList.add('loading');
            submitBtn.disabled = true;
        } else {
            submitBtn.classList.remove('loading');
            submitBtn.disabled = false;
        }
    }

    // Display results
    function displayResults(result) {
        // Update score with animation
        animateScore(approvalScoreEl, result.approval_score);
        
        // Update approval category
        approvalCategoryEl.textContent = result.approval_category;
        approvalCategoryEl.style.backgroundColor = result.approval_color + '20';
        approvalCategoryEl.style.color = result.approval_color;
        approvalCategoryEl.style.borderColor = result.approval_color;
        approvalCategoryEl.style.borderWidth = '2px';
        approvalCategoryEl.style.borderStyle = 'solid';
        
        // Update input analysis
        inputFieldEl.textContent = result.input_values.business_field;
        inputScaleEl.textContent = result.input_values.scale;
        inputUsageEl.textContent = result.input_values.usage_type;
        
        // Update fuzzy values
        fuzzyScaleEl.textContent = result.analysis.scale_value;
        fuzzyRiskEl.textContent = result.analysis.risk_value;
        fuzzyPriorityEl.textContent = result.analysis.priority_value;
        
        // Update credit information
        creditRangeEl.textContent = result.analysis.credit_range_million;
        fieldCreditEl.textContent = result.analysis.field_credit_billion;
        usageCreditEl.textContent = result.analysis.usage_credit_billion;
        
        // Update recommendations
        recommendationsListEl.innerHTML = '';
        result.recommendations.forEach((recommendation, index) => {
            const li = document.createElement('li');
            li.textContent = recommendation;
            li.style.animationDelay = `${index * 0.1}s`;
            recommendationsListEl.appendChild(li);
        });
        
        // Display fuzzy visualization
        if (result.visualization) {
            fuzzyVisualizationEl.src = `data:image/png;base64,${result.visualization}`;
            fuzzyVisualizationEl.classList.remove('hidden');
            visualizationPlaceholder.classList.add('hidden');
        }
        
        // Display detailed analysis
        displayDetailedAnalysis(result.analysis.detailed_analysis);
        
        // Show result section with animation
        resultSection.classList.remove('hidden');
        setTimeout(() => {
            resultSection.classList.add('visible');
            resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 100);
    }

    // Display detailed analysis
    function displayDetailedAnalysis(analysis) {
        const inputMembershipEl = document.getElementById('input-membership-details');
        const outputMembershipEl = document.getElementById('output-membership-details');
        
        // Display input membership analysis
        inputMembershipEl.innerHTML = '';
        
        // Scale analysis
        const scaleAnalysis = createMembershipAnalysis('Skala Usaha', analysis.input_analysis.scale);
        inputMembershipEl.appendChild(scaleAnalysis);
        
        // Risk analysis
        const riskAnalysis = createMembershipAnalysis('Tingkat Risiko', analysis.input_analysis.risk);
        inputMembershipEl.appendChild(riskAnalysis);
        
        // Priority analysis
        const priorityAnalysis = createMembershipAnalysis('Prioritas Penggunaan', analysis.input_analysis.priority);
        inputMembershipEl.appendChild(priorityAnalysis);
        
        // Display output membership analysis
        outputMembershipEl.innerHTML = '';
        const outputAnalysis = createMembershipAnalysis('Skor Persetujuan', analysis.output_analysis);
        outputMembershipEl.appendChild(outputAnalysis);
    }

    // Create membership analysis element
    function createMembershipAnalysis(title, memberships) {
        const container = document.createElement('div');
        container.className = 'membership-group';
        
        const titleEl = document.createElement('h5');
        titleEl.textContent = title;
        titleEl.style.marginBottom = '1rem';
        titleEl.style.fontWeight = '600';
        titleEl.style.color = 'var(--text-primary)';
        container.appendChild(titleEl);
        
        Object.entries(memberships).forEach(([term, value]) => {
            const item = document.createElement('div');
            item.className = 'membership-item';
            
            const label = document.createElement('span');
            label.className = 'membership-label';
            label.textContent = term.charAt(0).toUpperCase() + term.slice(1);
            
            const valueEl = document.createElement('span');
            valueEl.className = 'membership-value';
            valueEl.textContent = value.toFixed(3);
            
            const bar = document.createElement('div');
            bar.className = 'membership-bar';
            
            const fill = document.createElement('div');
            fill.className = 'membership-fill';
            fill.style.width = '0%';
            
            bar.appendChild(fill);
            
            item.appendChild(label);
            item.appendChild(valueEl);
            item.appendChild(bar);
            container.appendChild(item);
            
            // Animate the bar
            setTimeout(() => {
                fill.style.width = `${value * 100}%`;
            }, 100);
        });
        
        return container;
    }

    // Animate score
    function animateScore(element, targetValue) {
        const duration = 2000;
        const startTime = performance.now();
        const startValue = 0;
        
        function updateScore(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function for smooth animation
            const easeOutQuart = 1 - Math.pow(1 - progress, 4);
            const currentValue = startValue + (targetValue - startValue) * easeOutQuart;
            
            element.textContent = Math.round(currentValue);
            
            if (progress < 1) {
                requestAnimationFrame(updateScore);
            }
        }
        
        requestAnimationFrame(updateScore);
    }

    // Animate numeric values
    function animateValue(element, start, end, duration, isFormatted = false) {
        const startTime = performance.now();
        
        function updateValue(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const easeOutQuart = 1 - Math.pow(1 - progress, 4);
            const currentValue = start + (end - start) * easeOutQuart;
            
            if (isFormatted) {
                element.textContent = currentValue.toLocaleString('id-ID') + ' Miliar';
            } else {
                element.textContent = Math.round(currentValue);
            }
            
            if (progress < 1) {
                requestAnimationFrame(updateValue);
            }
        }
        
        requestAnimationFrame(updateValue);
    }

    // Show error message
    function showError(message) {
        // Create error element
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        errorDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #ef4444;
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            z-index: 1000;
            animation: slideInRight 0.3s ease-out;
            max-width: 300px;
        `;
        
        // Add animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideInRight {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
        `;
        document.head.appendChild(style);
        
        document.body.appendChild(errorDiv);
        
        // Remove after 5 seconds
        setTimeout(() => {
            errorDiv.style.animation = 'slideInRight 0.3s ease-out reverse';
            setTimeout(() => {
                document.body.removeChild(errorDiv);
            }, 300);
        }, 5000);
    }

    // Reset form
    function resetForm() {
        form.reset();
        resultSection.classList.remove('visible');
        setTimeout(() => {
            resultSection.classList.add('hidden');
        }, 300);
        
        // Scroll to form
        form.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        // Reset score display
        approvalScoreEl.textContent = '0';
        approvalCategoryEl.textContent = 'Menunggu Evaluasi';
        approvalCategoryEl.style.backgroundColor = '';
        approvalCategoryEl.style.color = '';
        approvalCategoryEl.style.borderColor = '';
        approvalCategoryEl.style.borderWidth = '';
        approvalCategoryEl.style.borderStyle = '';
        
        // Reset recommendations
        recommendationsListEl.innerHTML = '<li>Menunggu hasil evaluasi...</li>';
        
        // Reset visualization
        fuzzyVisualizationEl.classList.add('hidden');
        visualizationPlaceholder.classList.remove('hidden');
        
        // Reset detailed analysis
        document.getElementById('input-membership-details').innerHTML = '';
        document.getElementById('output-membership-details').innerHTML = '';
        
        // Reset to first tab
        switchTab('input');
    }

    // Add smooth hover effects for form elements
    function addHoverEffects() {
        const formGroups = document.querySelectorAll('.form-group');
        formGroups.forEach(group => {
            const select = group.querySelector('select');
            
            select.addEventListener('focus', () => {
                group.style.transform = 'scale(1.02)';
            });
            
            select.addEventListener('blur', () => {
                group.style.transform = 'scale(1)';
            });
        });
    }

    // Initialize hover effects
    addHoverEffects();

    // Add keyboard navigation
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + Enter to submit form
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            if (document.activeElement.form === form) {
                form.dispatchEvent(new Event('submit'));
            }
        }
        
        // Escape to reset form
        if (e.key === 'Escape' && !resultSection.classList.contains('hidden')) {
            resetForm();
        }
    });

    // Add intersection observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.6s ease-out forwards';
            }
        });
    }, observerOptions);

    // Observe elements for animation
    document.querySelectorAll('.stat-card, .form-container, .analysis-card').forEach(el => {
        observer.observe(el);
    });

    // Add fadeInUp animation
    const animationStyle = document.createElement('style');
    animationStyle.textContent = `
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    `;
    document.head.appendChild(animationStyle);
});

// Utility function to debounce rapid events
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Add touch support for mobile devices
if ('ontouchstart' in window) {
    document.body.classList.add('touch-device');
}

// Flickering Grid Background Effect
function initFlickeringGrid() {
    const grid = document.getElementById('flickering-grid');
    if (!grid) return;
    
    const createFlickeringSquare = () => {
        const square = document.createElement('div');
        square.className = 'flickering-square';
        
        // Random properties
        const size = Math.random() * 6 + 2; // 2-8px
        const duration = Math.random() * 3 + 1; // 1-4s
        const delay = Math.random() * 2; // 0-2s delay
        const opacity = Math.random() * 0.3 + 0.1; // 0.1-0.4 opacity
        
        square.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            background: rgba(59, 130, 246, ${opacity});
            border-radius: 2px;
            animation: flickerSquare ${duration}s ${delay}s infinite;
            pointer-events: none;
        `;
        
        return square;
    };
    
    // Add CSS animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes flickerSquare {
            0%, 100% { 
                opacity: 0.1; 
                transform: scale(1);
            }
            50% { 
                opacity: 0.4; 
                transform: scale(1.1);
            }
        }
        
        .flickering-square {
            transition: all 0.3s ease;
        }
    `;
    document.head.appendChild(style);
    
    // Create grid of squares
    const gridSize = 50;
    for (let i = 0; i < gridSize; i++) {
        const square = createFlickeringSquare();
        square.style.left = `${Math.random() * 100}%`;
        square.style.top = `${Math.random() * 100}%`;
        grid.appendChild(square);
        
        // Regenerate square periodically
        setInterval(() => {
            if (Math.random() < 0.1) { // 10% chance to regenerate
                const newSquare = createFlickeringSquare();
                newSquare.style.left = square.style.left;
                newSquare.style.top = square.style.top;
                grid.replaceChild(newSquare, square);
            }
        }, 5000);
    }
}

// Enhanced animations for cards
function enhanceCardAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'slideInUp 0.6s ease-out forwards';
                
                // Add glow effect on hover
                entry.target.addEventListener('mouseenter', () => {
                    entry.target.style.transform = 'translateY(-5px) scale(1.02)';
                    entry.target.style.boxShadow = '0 20px 40px rgba(59, 130, 246, 0.3)';
                });
                
                entry.target.addEventListener('mouseleave', () => {
                    entry.target.style.transform = 'translateY(0) scale(1)';
                    entry.target.style.boxShadow = '';
                });
            }
        });
    }, { threshold: 0.1 });
    
    document.querySelectorAll('.stat-card, .chart-card, .form-container').forEach(card => {
        observer.observe(card);
    });
}

// Parallax effect for mouse movement
function initParallaxEffect() {
    document.addEventListener('mousemove', (e) => {
        const x = e.clientX / window.innerWidth;
        const y = e.clientY / window.innerHeight;
        
        const grid = document.getElementById('flickering-grid');
        if (grid) {
            grid.style.transform = `translate(${x * 20 - 10}px, ${y * 20 - 10}px)`;
        }
    });
}

// Smooth scroll enhancement
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Loading animation enhancement
function enhanceLoadingAnimation() {
    const submitBtn = document.querySelector('.submit-btn');
    if (submitBtn) {
        submitBtn.addEventListener('click', () => {
            submitBtn.classList.add('loading');
            submitBtn.innerHTML = `
                <span class="btn-text">Memproses...</span>
                <div class="btn-loader"></div>
            `;
        });
    }
}

// Initialize all enhancements
document.addEventListener('DOMContentLoaded', () => {
    initFlickeringGrid();
    enhanceCardAnimations();
    initParallaxEffect();
    initSmoothScroll();
    enhanceLoadingAnimation();
});

// Performance optimization - throttle scroll events
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Apply throttling to scroll events
window.addEventListener('scroll', throttle(() => {
    // Parallax and other scroll-based animations
}, 16)); // ~60fps
