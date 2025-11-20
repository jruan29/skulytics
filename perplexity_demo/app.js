// State Management
const state = {
  activeModule: 'dashboard',
  isFiltered: false,
  filterSKU: null,
  filterChannel: null,
  contentDeployed: false,
  showImpactTracking: false
};

// Chart instances
let salesTrendChart = null;
let topProductsChart = null;
let skuComparisonChart = null;
let cvrTrendChart = null;

// Data
const chartColors = ['#1FB8CD', '#FFC185', '#B4413C', '#ECEBD5', '#5D878F', '#DB4545', '#D2BA4C', '#964325', '#944454', '#13343B'];

// Initialize application
document.addEventListener('DOMContentLoaded', () => {
  initializeNavigation();
  initializeFilters();
  initializeAlerts();
  initializeCharts();
  initializeModals();
  initializeChat();
  initializeContentCrafter();
});

// Navigation
function initializeNavigation() {
  const navTabs = document.querySelectorAll('.nav-tab:not(.disabled)');
  navTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const module = tab.dataset.module;
      switchModule(module);
    });
  });
}

function switchModule(moduleId) {
  // Update nav tabs
  document.querySelectorAll('.nav-tab').forEach(tab => tab.classList.remove('active'));
  document.querySelector(`[data-module="${moduleId}"]`).classList.add('active');
  
  // Update modules
  document.querySelectorAll('.module').forEach(module => module.classList.remove('active'));
  document.getElementById(moduleId).classList.add('active');
  
  state.activeModule = moduleId;
}

// Filters
function initializeFilters() {
  const filterToggle = document.getElementById('filterToggle');
  const filterBar = document.getElementById('filterBar');
  const filtersGroup = document.querySelector('.filters-group');
  
  filterToggle.addEventListener('click', () => {
    if (filtersGroup.style.display === 'none') {
      filtersGroup.style.display = 'flex';
      filterToggle.textContent = 'Hide Filters';
      filterBar.classList.remove('collapsed');
    } else {
      filtersGroup.style.display = 'none';
      filterToggle.textContent = 'Show Filters';
      filterBar.classList.add('collapsed');
    }
  });
  
  // Clear filter button
  const clearFilter = document.getElementById('clearFilter');
  if (clearFilter) {
    clearFilter.addEventListener('click', () => {
      clearDashboardFilter();
    });
  }
}

// Alerts
function initializeAlerts() {
  const investigateButtons = document.querySelectorAll('.btn-investigate');
  investigateButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const sku = btn.dataset.sku;
      const channel = btn.dataset.channel;
      if (sku && channel) {
        applyDashboardFilter(sku, channel);
      }
    });
  });
  
  // View Full Analysis button
  const viewFullAnalysis = document.getElementById('viewFullAnalysis');
  if (viewFullAnalysis) {
    viewFullAnalysis.addEventListener('click', () => {
      switchModule('product');
    });
  }
  
  // Chat buttons
  const chatButtons = document.querySelectorAll('.btn-chat');
  chatButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      openChat();
    });
  });
}

function applyDashboardFilter(sku, channel) {
  state.isFiltered = true;
  state.filterSKU = sku;
  state.filterChannel = channel;
  
  // Update filter badge
  const filterBadge = document.getElementById('activeFilterBadge');
  const filterBadgeText = document.getElementById('filterBadgeText');
  filterBadge.style.display = 'block';
  filterBadgeText.textContent = `${sku} | ${channel}`;
  
  // Update filter dropdowns
  document.getElementById('skuFilter').value = sku;
  document.getElementById('channelFilter').value = channel;
  
  // Update KPIs
  updateKPIsFiltered();
  
  // Update charts
  updateChartsFiltered();
  
  // Update funnel
  updateFunnelFiltered();
}

function clearDashboardFilter() {
  state.isFiltered = false;
  state.filterSKU = null;
  state.filterChannel = null;
  
  // Hide filter badge
  document.getElementById('activeFilterBadge').style.display = 'none';
  
  // Reset filter dropdowns
  document.getElementById('skuFilter').value = 'all';
  document.getElementById('channelFilter').value = 'all';
  
  // Reset KPIs
  resetKPIs();
  
  // Reset charts
  resetCharts();
  
  // Reset funnel
  resetFunnel();
}

function updateKPIsFiltered() {
  // Gross Sales
  document.getElementById('kpiGrossSales').textContent = '$12,400';
  document.getElementById('kpiGrossSalesChange').textContent = '↓ 18% vs LW';
  document.getElementById('kpiGrossSalesChange').className = 'kpi-change negative';
  
  // Units Sold
  document.getElementById('kpiUnitsSold').textContent = '890';
  document.getElementById('kpiUnitsSoldChange').textContent = '↓ 3.3% vs LW';
  document.getElementById('kpiUnitsSoldChange').className = 'kpi-change negative';
  
  // CVR
  document.getElementById('kpiCVR').textContent = '2.8%';
  document.getElementById('kpiCVRChange').textContent = '↓ 22% vs LW';
  document.getElementById('kpiCVRChange').className = 'kpi-change negative';
  document.getElementById('kpiCVRChange').style.fontWeight = 'bold';
  
  // Rank
  document.getElementById('kpiRank').textContent = '#3';
  document.getElementById('kpiRankChange').textContent = 'Stable';
  document.getElementById('kpiRankChange').className = 'kpi-change positive';
  
  // OOS
  document.getElementById('kpiOOS').textContent = '⚠️ 8.5%';
  document.getElementById('kpiOOSChange').textContent = '↑ 8.5pts vs LW';
  document.getElementById('kpiOOSChange').className = 'kpi-change negative';
  
  // Content
  document.getElementById('kpiContent').textContent = '58/100';
  document.getElementById('kpiContentChange').textContent = '↓ 33% vs LM';
  document.getElementById('kpiContentChange').className = 'kpi-change negative';
}

function resetKPIs() {
  // Gross Sales
  document.getElementById('kpiGrossSales').textContent = '$1,247,890';
  document.getElementById('kpiGrossSalesChange').textContent = '↑ 12.4% vs LM';
  document.getElementById('kpiGrossSalesChange').className = 'kpi-change positive';
  
  // Units Sold
  document.getElementById('kpiUnitsSold').textContent = '18,432';
  document.getElementById('kpiUnitsSoldChange').textContent = '↑ 8.2% vs LM';
  document.getElementById('kpiUnitsSoldChange').className = 'kpi-change positive';
  
  // CVR
  document.getElementById('kpiCVR').textContent = '3.4%';
  document.getElementById('kpiCVRChange').textContent = '↓ 2.1% vs LM';
  document.getElementById('kpiCVRChange').className = 'kpi-change negative';
  document.getElementById('kpiCVRChange').style.fontWeight = 'normal';
  
  // Rank
  document.getElementById('kpiRank').textContent = '#6.2';
  document.getElementById('kpiRankChange').textContent = 'Stable';
  document.getElementById('kpiRankChange').className = 'kpi-change neutral';
  
  // OOS
  document.getElementById('kpiOOS').textContent = '4.2%';
  document.getElementById('kpiOOSChange').textContent = '↑ 1.8% vs LM';
  document.getElementById('kpiOOSChange').className = 'kpi-change negative';
  
  // Content
  document.getElementById('kpiContent').textContent = '72/100';
  document.getElementById('kpiContentChange').textContent = '↓ 8pts vs LM';
  document.getElementById('kpiContentChange').className = 'kpi-change warning';
}

function updateFunnelFiltered() {
  // Discovery
  document.getElementById('funnelViews').textContent = '48K Views';
  document.getElementById('funnelRank').textContent = 'Avg Rank #3';
  
  // Engagement
  document.getElementById('funnelTraffic').textContent = '16.8K P-Page Traffic';
  document.getElementById('funnelContentScore').textContent = 'Content Score 58/100';
  
  // Conversion
  document.getElementById('funnelCVR').textContent = 'CVR 2.8%';
  document.getElementById('funnelATC').textContent = '5.2K Add-to-Cart';
  const conversionStage = document.getElementById('funnelConversionStage');
  conversionStage.className = 'funnel-stage critical';
  document.getElementById('funnelConversionStatus').textContent = 'Critical';
  document.getElementById('funnelConversionStatus').className = 'status-badge critical-badge';
  
  // Sales
  document.getElementById('funnelSales').textContent = '$12.4K Sales';
  document.getElementById('funnelUnits').textContent = '890 Units';
  const salesStage = document.getElementById('funnelSalesStage');
  salesStage.className = 'funnel-stage warning';
  document.getElementById('funnelSalesStatus').textContent = 'Below Target';
  document.getElementById('funnelSalesStatus').className = 'status-badge warning-badge';
}

function resetFunnel() {
  // Discovery
  document.getElementById('funnelViews').textContent = '245K Views';
  document.getElementById('funnelRank').textContent = 'Avg Rank #6.2';
  
  // Engagement
  document.getElementById('funnelTraffic').textContent = '89K P-Page Traffic';
  document.getElementById('funnelContentScore').textContent = 'Content Score 72/100';
  
  // Conversion
  document.getElementById('funnelCVR').textContent = 'CVR 3.4%';
  document.getElementById('funnelATC').textContent = '28.5K Add-to-Cart';
  const conversionStage = document.getElementById('funnelConversionStage');
  conversionStage.className = 'funnel-stage warning';
  document.getElementById('funnelConversionStatus').textContent = 'Needs Work';
  document.getElementById('funnelConversionStatus').className = 'status-badge warning-badge';
  
  // Sales
  document.getElementById('funnelSales').textContent = '$1.24M Sales';
  document.getElementById('funnelUnits').textContent = '18.4K Units';
  const salesStage = document.getElementById('funnelSalesStage');
  salesStage.className = 'funnel-stage healthy';
  document.getElementById('funnelSalesStatus').textContent = 'Healthy';
  document.getElementById('funnelSalesStatus').className = 'status-badge healthy-badge';
}

// Charts
function initializeCharts() {
  createSalesTrendChart();
  createTopProductsChart();
  createSKUComparisonChart();
  createCVRTrendChart();
}

function createSalesTrendChart() {
  const ctx = document.getElementById('salesTrendChart').getContext('2d');
  salesTrendChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['Jul 2025', 'Aug 2025', 'Sep 2025', 'Oct 2025', 'Nov 2025', 'Dec 2025'],
      datasets: [{
        label: 'Sales',
        data: [980000, 1050000, 1120000, 1180000, 1247890, 1320000],
        borderColor: '#FF8300',
        backgroundColor: 'rgba(255, 131, 0, 0.1)',
        borderWidth: 3,
        pointRadius: 5,
        pointBackgroundColor: '#FF8300',
        tension: 0.4
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
          callbacks: {
            label: function(context) {
              return '$' + context.parsed.y.toLocaleString();
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: false,
          ticks: {
            callback: function(value) {
              return '$' + (value / 1000000).toFixed(2) + 'M';
            }
          }
        }
      }
    }
  });
}

function createTopProductsChart() {
  const ctx = document.getElementById('topProductsChart').getContext('2d');
  topProductsChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['SKU001', 'SKU006', 'SKU008', 'SKU002', 'SKU007', 'SKU004', 'SKU005', 'SKU003'],
      datasets: [{
        label: 'Sales',
        data: [45000, 38000, 32000, 28000, 22000, 18000, 15000, 12400],
        backgroundColor: '#1CB192',
        borderRadius: 6
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              return '$' + context.parsed.x.toLocaleString();
            }
          }
        }
      },
      scales: {
        x: {
          beginAtZero: true,
          ticks: {
            callback: function(value) {
              return '$' + (value / 1000).toFixed(0) + 'K';
            }
          }
        }
      }
    }
  });
}

function createSKUComparisonChart() {
  const ctx = document.getElementById('skuComparisonChart').getContext('2d');
  const data = [22000, 19000, 17000, 16000, 15000, 12400, 11000, 10000];
  const backgroundColors = data.map((val, idx) => idx === 5 ? '#DC3545' : '#1CB192');
  
  skuComparisonChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['SKU006', 'SKU015', 'SKU018', 'SKU012', 'SKU009', 'SKU003', 'SKU021', 'SKU024'],
      datasets: [{
        label: 'Sales',
        data: data,
        backgroundColor: backgroundColors,
        borderRadius: 6
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              return '$' + context.parsed.x.toLocaleString();
            }
          }
        }
      },
      scales: {
        x: {
          beginAtZero: true,
          ticks: {
            callback: function(value) {
              return '$' + (value / 1000).toFixed(0) + 'K';
            }
          }
        }
      }
    }
  });
}

function createCVRTrendChart() {
  const ctx = document.getElementById('cvrTrendChart').getContext('2d');
  
  // Generate 30 days of data
  const days = Array.from({length: 30}, (_, i) => i + 1);
  const cvrData = [];
  
  // Days 1-20: steady around 3.5-3.6%
  for (let i = 0; i < 20; i++) {
    cvrData.push(3.5 + Math.random() * 0.1);
  }
  
  // Days 21-24: sharp drop (OOS period)
  cvrData.push(3.4);
  cvrData.push(2.2);
  cvrData.push(1.8);
  cvrData.push(2.0);
  
  // Days 25-30: partial recovery to 2.8%
  for (let i = 24; i < 30; i++) {
    cvrData.push(2.7 + Math.random() * 0.2);
  }
  
  cvrTrendChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: days,
      datasets: [{
        label: 'CVR %',
        data: cvrData,
        borderColor: '#0075FF',
        backgroundColor: 'rgba(0, 117, 255, 0.1)',
        borderWidth: 2,
        pointRadius: 2,
        pointBackgroundColor: '#0075FF',
        tension: 0.3
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        },
        annotation: {
          annotations: {
            box1: {
              type: 'box',
              xMin: 21,
              xMax: 24,
              backgroundColor: 'rgba(220, 53, 69, 0.1)',
              borderColor: 'rgba(220, 53, 69, 0.3)',
              borderWidth: 1,
              label: {
                content: 'OOS Period',
                enabled: true,
                position: 'center'
              }
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: false,
          min: 0,
          max: 4,
          ticks: {
            callback: function(value) {
              return value.toFixed(1) + '%';
            }
          }
        },
        x: {
          ticks: {
            maxTicksLimit: 10
          }
        }
      }
    }
  });
}

function updateChartsFiltered() {
  // Update sales trend chart
  if (salesTrendChart) {
    salesTrendChart.data.datasets[0].data = [15000, 16000, 17000, 18000, 12400, 14000];
    salesTrendChart.options.scales.y.ticks.callback = function(value) {
      return '$' + (value / 1000).toFixed(0) + 'K';
    };
    salesTrendChart.update();
  }
  
  // Update top products chart - highlight SKU003
  if (topProductsChart) {
    const colors = topProductsChart.data.datasets[0].backgroundColor;
    topProductsChart.data.datasets[0].backgroundColor = colors.map((c, i) => 
      i === 7 ? '#FF8300' : c
    );
    topProductsChart.update();
  }
}

function resetCharts() {
  // Reset sales trend chart
  if (salesTrendChart) {
    salesTrendChart.data.datasets[0].data = [980000, 1050000, 1120000, 1180000, 1247890, 1320000];
    salesTrendChart.options.scales.y.ticks.callback = function(value) {
      return '$' + (value / 1000000).toFixed(2) + 'M';
    };
    salesTrendChart.update();
  }
  
  // Reset top products chart
  if (topProductsChart) {
    topProductsChart.data.datasets[0].backgroundColor = '#1CB192';
    topProductsChart.update();
  }
}

// Modals
function initializeModals() {
  const openSimulator = document.getElementById('openSimulator');
  const closeSimulator = document.getElementById('closeSimulator');
  const cancelSimulator = document.getElementById('cancelSimulator');
  const applyChanges = document.getElementById('applyChanges');
  const simulatorModal = document.getElementById('simulatorModal');
  
  if (openSimulator) {
    openSimulator.addEventListener('click', () => {
      simulatorModal.style.display = 'flex';
    });
  }
  
  if (closeSimulator) {
    closeSimulator.addEventListener('click', () => {
      simulatorModal.style.display = 'none';
    });
  }
  
  if (cancelSimulator) {
    cancelSimulator.addEventListener('click', () => {
      simulatorModal.style.display = 'none';
    });
  }
  
  if (applyChanges) {
    applyChanges.addEventListener('click', () => {
      simulatorModal.style.display = 'none';
      switchModule('content');
    });
  }
  
  // Close modal on overlay click
  simulatorModal?.addEventListener('click', (e) => {
    if (e.target === simulatorModal) {
      simulatorModal.style.display = 'none';
    }
  });
}

// Chat
function initializeChat() {
  const closeChat = document.getElementById('closeChat');
  const chatPanel = document.getElementById('chatPanel');
  const quickReplies = document.querySelectorAll('.quick-reply');
  
  if (closeChat) {
    closeChat.addEventListener('click', () => {
      chatPanel.style.display = 'none';
    });
  }
  
  quickReplies.forEach(btn => {
    btn.addEventListener('click', () => {
      const reply = btn.dataset.reply;
      handleQuickReply(reply);
    });
  });
}

function openChat() {
  const chatPanel = document.getElementById('chatPanel');
  chatPanel.style.display = 'flex';
}

function handleQuickReply(reply) {
  const chatBody = document.getElementById('chatBody');
  const quickRepliesDiv = document.getElementById('quickReplies');
  
  if (reply === 'combined') {
    // Add user message
    const userMsg = document.createElement('div');
    userMsg.className = 'chat-message user';
    userMsg.innerHTML = '<div class="message-bubble">What if we fix stock and images?</div>';
    chatBody.insertBefore(userMsg, quickRepliesDiv);
    
    // Add AI response
    const aiMsg = document.createElement('div');
    aiMsg.className = 'chat-message ai';
    aiMsg.innerHTML = `
      <div class="message-icon"><i class="fas fa-robot"></i></div>
      <div class="message-bubble">
        <p><strong>Scenario: Combined Fixes (Restock + Content)</strong></p>
        <p><strong>Actions:</strong></p>
        <ul>
          <li>Eliminate OOS (maintain 100% stock availability)</li>
          <li>Add 2 lifestyle images (3 → 5 total)</li>
          <li>Expand description (+150 chars with keywords)</li>
        </ul>
        <p><strong>Forecasted Impact:</strong></p>
        <ul>
          <li>Content Score: 58 → 85 (+27pts)</li>
          <li>Organic Rank: #3 → #1 (+2 spots)</li>
          <li>CVR: 2.8% → 4.1% (+1.3pts, +46%)</li>
          <li>Sales Lift: +$3,200 over next 2 weeks</li>
          <li>Confidence: 89%</li>
        </ul>
        <p><strong>Why This Works:</strong> The combination addresses both availability and appeal, maximizing conversion recovery while defending against competitor pricing.</p>
        <p>Would you like to apply these changes?</p>
      </div>
    `;
    chatBody.insertBefore(aiMsg, quickRepliesDiv);
    
    // Update quick replies
    quickRepliesDiv.innerHTML = `
      <button class="quick-reply" onclick="applyChangesFromChat()"><i class="fas fa-check"></i> Apply Changes</button>
      <button class="quick-reply"><i class="fas fa-sync"></i> Compare Other Scenarios</button>
    `;
    
    // Scroll to bottom
    chatBody.scrollTop = chatBody.scrollHeight;
  }
}

function applyChangesFromChat() {
  document.getElementById('chatPanel').style.display = 'none';
  switchModule('content');
}

// Content Crafter
function initializeContentCrafter() {
  const deployChanges = document.getElementById('deployChanges');
  const trackImpactBtn = document.getElementById('trackImpactBtn');
  
  if (deployChanges) {
    deployChanges.addEventListener('click', () => {
      state.contentDeployed = true;
      document.getElementById('contentActions').style.display = 'none';
      document.getElementById('successMessage').style.display = 'block';
      
      // Scroll to success message
      document.getElementById('successMessage').scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
  }
  
  if (trackImpactBtn) {
    trackImpactBtn.addEventListener('click', () => {
      state.showImpactTracking = true;
      document.getElementById('impactTracking').style.display = 'block';
      
      // Scroll to impact tracking
      document.getElementById('impactTracking').scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  }
}