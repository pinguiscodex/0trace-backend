"""Seeded in-game website documents for trusted predefined domains."""

PREDEFINED_SITE_INDEX = [
    {"domain": "searchable.com", "title": "Searchable", "desc": "Search the public 0trace network, shops, manuals, markets, and services."},
    {"domain": "microhard.com", "title": "Microhard", "desc": "DoorsOS downloads, manuals, terminal help, and preinstalled drives."},
    {"domain": "pear.com", "title": "Pear", "desc": "FruitOS, polished system guides, and P-series integrated chips."},
    {"domain": "arctic.org", "title": "Arctic", "desc": "ArcticOS downloads, open manuals, window managers, and public funding."},
    {"domain": "techhub.com", "title": "TechHub", "desc": "CPUs, GPUs, motherboards, RAM, storage, cases, USB media, and OS bundles."},
    {"domain": "secondlife.com", "title": "SecondLife", "desc": "Player-to-player marketplace for hardware parts and software files."},
    {"domain": "cryptfront.trade", "title": "CryptFront", "desc": "Fictional in-game coin trading, wallets, transfers, and price charts."},
    {"domain": "domania.com", "title": "Domania", "desc": "Domains and HTTPS certificates for player-hosted 0trace websites."},
    {"domain": "deliveries.com", "title": "Deliveries", "desc": "Package tracking, delivery claims, and 20-minute express subscription."},
]

BASE_CSS = """
:root {
  color-scheme: light;
  --brand: #2563eb;
  --brand-2: #0f766e;
  --ink: #111827;
  --muted: #64748b;
  --line: rgba(15, 23, 42, .12);
  --panel: #ffffff;
  --panel-soft: #f8fafc;
  --shadow: 0 18px 60px rgba(15, 23, 42, .14);
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
* { box-sizing: border-box; }
html { min-height: 100%; scroll-behavior: smooth; }
body {
  margin: 0;
  min-height: 100%;
  background: #f5f7fb;
  color: var(--ink);
  font-size: 15px;
}
a, button, input, select { font: inherit; }
a { color: inherit; text-decoration: none; }
button, input, select { max-width: 100%; }
button {
  border: 0;
  cursor: pointer;
}
.site-shell { min-height: 100vh; background: linear-gradient(180deg, #fff 0%, #f6f8fc 44%, #eef3f8 100%); }
.site-nav {
  position: sticky;
  top: 0;
  z-index: 20;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 14px clamp(18px, 4vw, 54px);
  border-bottom: 1px solid rgba(15, 23, 42, .08);
  background: rgba(255, 255, 255, .86);
  backdrop-filter: blur(18px);
}
.brand { display: flex; align-items: center; gap: 10px; font-weight: 850; letter-spacing: 0; }
.brand-mark {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background:
    linear-gradient(135deg, var(--brand), var(--brand-2));
  box-shadow: 0 12px 32px rgba(37, 99, 235, .22);
}
.nav-links { display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 8px; }
.nav-link {
  padding: 8px 11px;
  border-radius: 8px;
  color: #475569;
  font-weight: 680;
}
.nav-link:hover, .nav-link.active { background: rgba(15, 23, 42, .06); color: var(--ink); }
.hero {
  display: grid;
  grid-template-columns: minmax(0, 1.08fr) minmax(280px, .92fr);
  gap: clamp(22px, 5vw, 58px);
  align-items: center;
  padding: clamp(44px, 8vw, 96px) clamp(18px, 5vw, 68px) clamp(28px, 6vw, 70px);
}
.hero-full { grid-template-columns: minmax(0, 1fr); max-width: 1180px; }
.eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  width: fit-content;
  margin: 0 0 16px;
  padding: 7px 10px;
  border: 1px solid rgba(15, 23, 42, .1);
  border-radius: 8px;
  background: rgba(255, 255, 255, .74);
  color: var(--brand);
  font-weight: 800;
  font-size: .78rem;
  text-transform: uppercase;
}
h1 {
  margin: 0;
  max-width: 920px;
  font-size: clamp(2.45rem, 7vw, 6.25rem);
  line-height: .94;
  letter-spacing: 0;
}
h2 { margin: 0; font-size: clamp(1.32rem, 2.2vw, 2rem); letter-spacing: 0; }
h3 { margin: 0; font-size: 1.04rem; letter-spacing: 0; }
p { line-height: 1.62; }
.lede { max-width: 780px; color: #475569; font-size: clamp(1rem, 1.45vw, 1.18rem); }
.hero-panel, .panel, .product-card, .result-card, .listing-card, .wallet-card, .delivery-card {
  border: 1px solid var(--line);
  border-radius: 8px;
  background: rgba(255, 255, 255, .92);
  box-shadow: var(--shadow);
}
.hero-panel { padding: clamp(20px, 4vw, 34px); }
.hero-panel.dark {
  background: #111827;
  color: white;
  border-color: rgba(255, 255, 255, .16);
}
.section { padding: 24px clamp(18px, 5vw, 68px) 56px; }
.section.compact { padding-top: 0; }
.section-head {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 18px;
  margin: 0 0 18px;
}
.section-head p { margin: 7px 0 0; color: var(--muted); }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 16px; }
.grid.wide { grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); }
.panel, .product-card, .result-card, .listing-card, .wallet-card, .delivery-card { padding: 18px; }
.metric { display: block; color: var(--brand); font-size: 2rem; line-height: 1; font-weight: 900; }
.muted { color: var(--muted); }
.fine { color: var(--muted); font-size: .86rem; }
.toolbar { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin: 0 0 18px; }
.field {
  min-height: 42px;
  border: 1px solid rgba(15, 23, 42, .16);
  border-radius: 8px;
  background: white;
  color: var(--ink);
  padding: 10px 12px;
  outline: none;
}
.field:focus { border-color: var(--brand); box-shadow: 0 0 0 4px rgba(37, 99, 235, .12); }
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 42px;
  padding: 10px 14px;
  border-radius: 8px;
  background: var(--brand);
  color: white;
  font-weight: 820;
  box-shadow: 0 14px 32px rgba(37, 99, 235, .24);
  transition: transform .16s ease, box-shadow .16s ease, opacity .16s ease;
}
.btn:hover { transform: translateY(-1px); box-shadow: 0 18px 38px rgba(37, 99, 235, .28); }
.btn.secondary { background: #111827; box-shadow: 0 14px 32px rgba(17, 24, 39, .18); }
.btn.subtle { background: white; color: var(--ink); border: 1px solid rgba(15, 23, 42, .14); box-shadow: none; }
.btn.danger { background: #dc2626; box-shadow: 0 14px 32px rgba(220, 38, 38, .2); }
.btn:disabled { opacity: .55; cursor: wait; transform: none; }
.tabs { display: flex; flex-wrap: wrap; gap: 8px; margin: 0 0 20px; }
.tab { padding: 9px 12px; border-radius: 8px; background: rgba(15, 23, 42, .06); color: #475569; font-weight: 750; }
.tab.active { background: var(--ink); color: white; }
.tab-panel { display: none; }
.tab-panel.active { display: block; }
.list { display: grid; gap: 10px; margin: 14px 0 0; padding: 0; list-style: none; }
.list li { display: flex; justify-content: space-between; gap: 14px; padding: 11px 0; border-bottom: 1px solid rgba(15, 23, 42, .08); }
.search-box {
  width: min(760px, 100%);
  min-height: 58px;
  border-radius: 8px;
  padding: 0 18px;
  font-size: 1.08rem;
}
.result-card { cursor: pointer; transition: transform .16s ease, border-color .16s ease; }
.result-card:hover { transform: translateY(-2px); border-color: rgba(37, 99, 235, .42); }
.url { color: #047857; font-weight: 760; font-size: .88rem; }
.status {
  min-height: 20px;
  color: var(--muted);
  font-size: .9rem;
}
.toast {
  position: fixed;
  right: 18px;
  bottom: 18px;
  z-index: 80;
  display: none;
  max-width: min(420px, calc(100vw - 36px));
  padding: 12px 14px;
  border-radius: 8px;
  background: #111827;
  color: white;
  box-shadow: 0 20px 60px rgba(15, 23, 42, .34);
}
.toast.show { display: block; }
.toast.error { background: #991b1b; }
.chart { display: grid; gap: 10px; margin: 12px 0 0; }
.bar { display: grid; grid-template-columns: 92px minmax(80px, 1fr) 80px; gap: 10px; align-items: center; }
.bar-track { height: 12px; border-radius: 8px; background: rgba(15, 23, 42, .09); overflow: hidden; }
.bar-fill { height: 100%; width: 40%; border-radius: 8px; background: linear-gradient(90deg, var(--brand), var(--brand-2)); }
.code { font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace; font-size: .9rem; }
footer { padding: 24px clamp(18px, 5vw, 68px); border-top: 1px solid rgba(15, 23, 42, .08); color: var(--muted); }
@media (max-width: 760px) {
  .site-nav { align-items: flex-start; flex-direction: column; }
  .nav-links { justify-content: flex-start; }
  .hero { grid-template-columns: 1fr; padding-top: 34px; }
  .section-head { align-items: flex-start; flex-direction: column; }
  .bar { grid-template-columns: 1fr; }
}
"""

BASE_JS = r"""
(function() {
  var requestSequence = 0;
  var pending = {};
  function $(selector, root) { return (root || document).querySelector(selector); }
  function $all(selector, root) { return Array.prototype.slice.call((root || document).querySelectorAll(selector)); }
  function escapeHtml(value) {
    return String(value == null ? '' : value).replace(/[&<>"']/g, function(ch) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[ch];
    });
  }
  function toast(message, kind) {
    var node = $('#trace-toast');
    if (!node) {
      node = document.createElement('div');
      node.id = 'trace-toast';
      node.className = 'toast';
      document.body.appendChild(node);
    }
    node.textContent = message;
    node.className = 'toast show' + (kind === 'error' ? ' error' : '');
    window.clearTimeout(node._timer);
    node._timer = window.setTimeout(function() { node.className = 'toast'; }, 3600);
  }
  function request(action, payload) {
    var requestId = 'site-' + Date.now().toString(36) + '-' + (++requestSequence);
    parent.postMessage({ type: '0trace:trusted-action', requestId: requestId, action: action, payload: payload || {} }, '*');
    return new Promise(function(resolve, reject) {
      pending[requestId] = { resolve: resolve, reject: reject, action: action };
      window.setTimeout(function() {
        if (pending[requestId]) {
          delete pending[requestId];
          reject(new Error('The action timed out.'));
        }
      }, 15000);
    });
  }
  function navigate(domain) {
    var target = domain.indexOf('://') > -1 ? domain : 'https://www.' + domain + '/';
    parent.postMessage({ type: '0trace:navigate', url: target }, '*');
  }
  function bindTabs() {
    $all('[data-tab-target]').forEach(function(tab) {
      tab.addEventListener('click', function(event) {
        event.preventDefault();
        var target = tab.getAttribute('data-tab-target');
        $all('[data-tab-target]').forEach(function(item) { item.classList.toggle('active', item === tab); });
        $all('.tab-panel').forEach(function(panel) { panel.classList.toggle('active', panel.id === target); });
      });
    });
  }
  function setBusy(button, busy) {
    if (!button) return;
    button.disabled = busy;
    if (busy) button.setAttribute('data-label', button.textContent);
    button.textContent = busy ? 'Working...' : (button.getAttribute('data-label') || button.textContent);
  }
  window.addEventListener('message', function(event) {
    var data = event.data || {};
    if (data.type !== '0trace:trusted-result' || !pending[data.requestId]) return;
    var task = pending[data.requestId];
    delete pending[data.requestId];
    if (data.ok) task.resolve(data.payload);
    else task.reject(new Error(data.error || 'The action failed.'));
  });
  document.addEventListener('click', function(event) {
    var link = event.target.closest('a[href^="https://"]');
    if (link) {
      event.preventDefault();
      navigate(link.href);
    }
  });
  window.TraceSite = {
    $: $,
    $all: $all,
    escape: escapeHtml,
    toast: toast,
    request: request,
    navigate: navigate,
    bindTabs: bindTabs,
    setBusy: setBusy,
    formatCredits: function(value) {
      var number = Number(value || 0);
      return Number.isFinite(number) ? number.toLocaleString(undefined, { maximumFractionDigits: 2 }) + ' CR' : escapeHtml(value) + ' CR';
    }
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', bindTabs);
  else bindTabs();
})();
"""


def _site(html: str, *, brand: str, brand_2: str, js: str = "", extra_css: str = ""):
    return {
        "html": html,
        "css": f"{BASE_CSS}\n:root{{--brand:{brand};--brand-2:{brand_2};}}\n{extra_css}",
        "js": f"{BASE_JS}\n{js}",
    }


SEARCHABLE_JS = """
(function() {
  var sites = %r;
  var input = TraceSite.$('#site-search');
  var results = TraceSite.$('#search-results');
  function render() {
    var q = (input.value || '').toLowerCase().trim();
    var filtered = sites.filter(function(site) {
      return !q || (site.domain + ' ' + site.title + ' ' + site.desc).toLowerCase().indexOf(q) >= 0;
    });
    results.innerHTML = filtered.map(function(site) {
      return '<article class="result-card" data-domain="' + TraceSite.escape(site.domain) + '">' +
        '<h3>' + TraceSite.escape(site.title) + '</h3>' +
        '<p class="url">https://www.' + TraceSite.escape(site.domain) + '</p>' +
        '<p class="muted">' + TraceSite.escape(site.desc) + '</p>' +
      '</article>';
    }).join('');
  }
  input.addEventListener('input', render);
  results.addEventListener('click', function(event) {
    var card = event.target.closest('[data-domain]');
    if (card) TraceSite.navigate(card.getAttribute('data-domain'));
  });
  render();
})();
""" % PREDEFINED_SITE_INDEX

MICROHARD_JS = """
(function() {
  function bind(selector, handler) {
    TraceSite.$all(selector).forEach(function(button) {
      button.addEventListener('click', function() { handler(button); });
    });
  }
  bind('[data-install-os]', function(button) {
    TraceSite.setBusy(button, true);
    TraceSite.request('install-os', { osSlug: button.getAttribute('data-install-os') })
      .then(function() { TraceSite.toast('DoorsOS is installed on this machine.'); })
      .catch(function(error) { TraceSite.toast(error.message, 'error'); })
      .finally(function() { TraceSite.setBusy(button, false); });
  });
  bind('[data-buy-sku]', function(button) {
    TraceSite.setBusy(button, true);
    TraceSite.request('buy-hardware', { sku: button.getAttribute('data-buy-sku') })
      .then(function() { TraceSite.toast('Order placed. Deliveries will track the package.'); })
      .catch(function(error) { TraceSite.toast(error.message, 'error'); })
      .finally(function() { TraceSite.setBusy(button, false); });
  });
})();
"""

PEAR_JS = """
(function() {
  TraceSite.$all('[data-install-os]').forEach(function(button) {
    button.addEventListener('click', function() {
      TraceSite.setBusy(button, true);
      TraceSite.request('install-os', { osSlug: 'fruitos' })
        .then(function() { TraceSite.toast('FruitOS installation complete.'); })
        .catch(function(error) { TraceSite.toast(error.message, 'error'); })
        .finally(function() { TraceSite.setBusy(button, false); });
    });
  });
  TraceSite.$all('[data-buy-sku]').forEach(function(button) {
    button.addEventListener('click', function() {
      TraceSite.setBusy(button, true);
      TraceSite.request('buy-hardware', { sku: button.getAttribute('data-buy-sku') })
        .then(function() { TraceSite.toast('Pear chip ordered. Check Deliveries.'); })
        .catch(function(error) { TraceSite.toast(error.message, 'error'); })
        .finally(function() { TraceSite.setBusy(button, false); });
    });
  });
})();
"""

ARCTIC_JS = """
(function() {
  var wm = TraceSite.$('#arctic-wm');
  TraceSite.$('#install-arctic').addEventListener('click', function() {
    var button = this;
    TraceSite.setBusy(button, true);
    TraceSite.request('install-os', { osSlug: 'arcticos', windowManager: wm.value })
      .then(function() { TraceSite.toast('ArcticOS installed with ' + wm.value + '.'); })
      .catch(function(error) { TraceSite.toast(error.message, 'error'); })
      .finally(function() { TraceSite.setBusy(button, false); });
  });
})();
"""

TECHHUB_JS = """
(function() {
  var products = [];
  var grid = TraceSite.$('#catalog-grid');
  var filter = TraceSite.$('#catalog-filter');
  var search = TraceSite.$('#catalog-search');
  function render() {
    var kind = filter.value;
    var q = (search.value || '').toLowerCase();
    var visible = products.filter(function(item) {
      var haystack = (item.name + ' ' + item.sku + ' ' + item.category).toLowerCase();
      return (!kind || item.category === kind) && (!q || haystack.indexOf(q) >= 0);
    });
    grid.innerHTML = visible.map(function(item) {
      var stats = Object.keys(item.stats || {}).map(function(key) {
        return '<span class="fine">' + TraceSite.escape(key) + ': ' + TraceSite.escape(item.stats[key]) + '</span>';
      }).join('<br>');
      return '<article class="product-card">' +
        '<h3>' + TraceSite.escape(item.name) + '</h3>' +
        '<p class="muted">' + TraceSite.escape(item.category) + ' · SKU ' + TraceSite.escape(item.sku) + '</p>' +
        '<p>' + (stats || '<span class="fine">Standard compatibility profile</span>') + '</p>' +
        '<div class="toolbar"><strong>' + TraceSite.formatCredits(item.price) + '</strong>' +
        '<button class="btn" data-buy-sku="' + TraceSite.escape(item.sku) + '">Buy</button></div>' +
      '</article>';
    }).join('');
  }
  function load() {
    TraceSite.request('list-hardware', {}).then(function(data) {
      products = data.items || data || [];
      render();
    }).catch(function(error) {
      TraceSite.toast(error.message, 'error');
      grid.innerHTML = '';
    });
  }
  grid.addEventListener('click', function(event) {
    var button = event.target.closest('[data-buy-sku]');
    if (!button) return;
    TraceSite.setBusy(button, true);
    TraceSite.request('buy-hardware', { sku: button.getAttribute('data-buy-sku') })
      .then(function() { TraceSite.toast('Hardware purchased. Delivery created.'); })
      .catch(function(error) { TraceSite.toast(error.message, 'error'); })
      .finally(function() { TraceSite.setBusy(button, false); });
  });
  filter.addEventListener('change', render);
  search.addEventListener('input', render);
  load();
})();
"""

SECONDLIFE_JS = """
(function() {
  var listings = [];
  var grid = TraceSite.$('#listing-grid');
  var filter = TraceSite.$('#listing-filter');
  function render() {
    var type = filter.value;
    var visible = listings.filter(function(item) { return !type || item.item_type === type; });
    grid.innerHTML = visible.map(function(item) {
      return '<article class="listing-card">' +
        '<h3>' + TraceSite.escape(item.title) + '</h3>' +
        '<p class="muted">' + TraceSite.escape(item.item_type || 'listing') + '</p>' +
        '<p>' + TraceSite.escape(item.description || 'Player-owned listing') + '</p>' +
        '<div class="toolbar"><strong>' + TraceSite.formatCredits(item.price) + '</strong>' +
        '<button class="btn" data-listing-id="' + TraceSite.escape(item.id) + '">Buy</button></div>' +
      '</article>';
    }).join('');
  }
  function load() {
    TraceSite.request('list-marketplace', {}).then(function(data) {
      listings = data.items || data || [];
      render();
    }).catch(function(error) {
      TraceSite.toast(error.message, 'error');
      render();
    });
  }
  grid.addEventListener('click', function(event) {
    var button = event.target.closest('[data-listing-id]');
    if (!button) return;
    TraceSite.setBusy(button, true);
    TraceSite.request('buy-marketplace-listing', { listingId: button.getAttribute('data-listing-id') })
      .then(function() { TraceSite.toast('Listing purchased. Inventory will update.'); load(); })
      .catch(function(error) { TraceSite.toast(error.message, 'error'); })
      .finally(function() { TraceSite.setBusy(button, false); });
  });
  filter.addEventListener('change', render);
  load();
})();
"""

CRYPTFRONT_JS = """
(function() {
  var wallets = [];
  var coins = [];
  function coinName(slug) {
    var coin = coins.find(function(item) { return item.slug === slug; });
    return coin ? coin.symbol + ' · ' + coin.name : slug;
  }
  function renderWallets() {
    var grid = TraceSite.$('#wallet-grid');
    grid.innerHTML = wallets.map(function(wallet) {
      var balances = (wallet.balances || []).map(function(balance) {
        return '<li><span>' + TraceSite.escape(balance.coin.slug) + '</span><strong>' + TraceSite.escape(balance.amount) + '</strong></li>';
      }).join('');
      return '<article class="wallet-card">' +
        '<h3>' + TraceSite.escape(wallet.label || 'Wallet') + '</h3>' +
        '<p class="code fine">' + TraceSite.escape(wallet.address || wallet.id) + '</p>' +
        '<ul class="list">' + balances + '</ul>' +
        '<button class="btn danger" data-delete-wallet="' + TraceSite.escape(wallet.id) + '">Delete</button>' +
      '</article>';
    }).join('');
    var selects = TraceSite.$all('[data-wallet-select]');
    selects.forEach(function(select) {
      select.innerHTML = wallets.map(function(wallet) {
        return '<option value="' + TraceSite.escape(wallet.id) + '">' + TraceSite.escape(wallet.label || wallet.address || wallet.id) + '</option>';
      }).join('');
    });
  }
  function renderCoins() {
    var chart = TraceSite.$('#coin-chart');
    chart.innerHTML = coins.map(function(coin, index) {
      var width = Math.max(12, Math.min(100, 24 + index * 24));
      return '<div class="bar"><strong>' + TraceSite.escape(coin.symbol) + '</strong><span class="bar-track"><span class="bar-fill" style="width:' + width + '%"></span></span><span class="fine">' + TraceSite.escape(coin.name) + '</span></div>';
    }).join('');
    TraceSite.$all('[data-coin-select]').forEach(function(select) {
      select.innerHTML = coins.filter(function(coin) { return coin.slug !== 'credits'; }).map(function(coin) {
        return '<option value="' + TraceSite.escape(coin.slug) + '">' + TraceSite.escape(coinName(coin.slug)) + '</option>';
      }).join('');
    });
  }
  function load() {
    Promise.all([TraceSite.request('list-coins', {}), TraceSite.request('list-wallets', {})]).then(function(results) {
      coins = results[0].items || results[0] || [];
      wallets = results[1].items || results[1] || [];
      renderCoins();
      renderWallets();
    }).catch(function(error) { TraceSite.toast(error.message, 'error'); });
  }
  TraceSite.$('#create-wallet').addEventListener('click', function() {
    var label = TraceSite.$('#wallet-label').value || 'Trading wallet';
    var button = this;
    TraceSite.setBusy(button, true);
    TraceSite.request('create-wallet', { label: label })
      .then(function() { TraceSite.toast('Wallet created.'); load(); })
      .catch(function(error) { TraceSite.toast(error.message, 'error'); })
      .finally(function() { TraceSite.setBusy(button, false); });
  });
  TraceSite.$('#wallet-grid').addEventListener('click', function(event) {
    var button = event.target.closest('[data-delete-wallet]');
    if (!button) return;
    TraceSite.setBusy(button, true);
    TraceSite.request('delete-wallet', { walletId: button.getAttribute('data-delete-wallet') })
      .then(function() { TraceSite.toast('Wallet deleted.'); load(); })
      .catch(function(error) { TraceSite.toast(error.message, 'error'); })
      .finally(function() { TraceSite.setBusy(button, false); });
  });
  TraceSite.$('#coin-trade').addEventListener('submit', function(event) {
    event.preventDefault();
    var form = event.currentTarget;
    var action = form.trade.value;
    TraceSite.request(action === 'sell' ? 'sell-coin' : 'buy-coin', {
      walletId: form.wallet.value,
      coinSlug: form.coin.value,
      creditAmount: form.amount.value,
      coinAmount: form.amount.value
    }).then(function() { TraceSite.toast('Trade completed.'); load(); })
      .catch(function(error) { TraceSite.toast(error.message, 'error'); });
  });
  TraceSite.$('#coin-transfer').addEventListener('submit', function(event) {
    event.preventDefault();
    var form = event.currentTarget;
    TraceSite.request('send-coin', {
      walletId: form.wallet.value,
      toAddress: form.to.value,
      coinSlug: form.coin.value,
      amount: form.amount.value
    }).then(function() { TraceSite.toast('Transfer sent.'); load(); })
      .catch(function(error) { TraceSite.toast(error.message, 'error'); });
  });
  load();
})();
"""

DOMANIA_JS = """
(function() {
  var domains = [];
  function render() {
    var list = TraceSite.$('#domain-list');
    list.innerHTML = domains.map(function(domain) {
      return '<article class="panel"><h3>' + TraceSite.escape(domain.name) + '</h3><p class="muted">Status: ' + TraceSite.escape(domain.status || 'active') + '</p><button class="btn" data-cert-domain="' + TraceSite.escape(domain.id) + '">Buy HTTPS certificate</button></article>';
    }).join('');
  }
  function load() {
    TraceSite.request('list-domains', {}).then(function(data) {
      domains = data.items || data || [];
      render();
    }).catch(function(error) { TraceSite.toast(error.message, 'error'); });
  }
  TraceSite.$('#domain-form').addEventListener('submit', function(event) {
    event.preventDefault();
    var input = TraceSite.$('#domain-name');
    TraceSite.request('buy-domain', { name: input.value })
      .then(function() { TraceSite.toast('Domain registered.'); input.value = ''; load(); })
      .catch(function(error) { TraceSite.toast(error.message, 'error'); });
  });
  TraceSite.$('#domain-list').addEventListener('click', function(event) {
    var button = event.target.closest('[data-cert-domain]');
    if (!button) return;
    TraceSite.setBusy(button, true);
    TraceSite.request('buy-certificate', { domainId: button.getAttribute('data-cert-domain') })
      .then(function() { TraceSite.toast('HTTPS certificate issued.'); })
      .catch(function(error) { TraceSite.toast(error.message, 'error'); })
      .finally(function() { TraceSite.setBusy(button, false); });
  });
  load();
})();
"""

DELIVERIES_JS = """
(function() {
  function renderDeliveries(items) {
    var grid = TraceSite.$('#delivery-grid');
    grid.innerHTML = items.map(function(item) {
      return '<article class="delivery-card"><h3>' + TraceSite.escape(item.label || item.catalog_item_name || 'Package') + '</h3>' +
        '<p class="muted">Status: ' + TraceSite.escape(item.status) + '</p>' +
        '<p><span class="metric">' + TraceSite.escape(item.etaMinutes != null ? item.etaMinutes : '0') + '</span><span class="fine"> minutes ETA</span></p>' +
        '<button class="btn" data-claim-delivery="' + TraceSite.escape(item.id) + '">Claim package</button></article>';
    }).join('');
  }
  function renderSubscription(sub) {
    var status = TraceSite.$('#express-status');
    status.innerHTML = sub && sub.active ? '<strong>Express active</strong><p class="muted">20-minute delivery is enabled.</p>' : '<strong>Standard delivery</strong><p class="muted">Packages arrive in about 2 hours.</p>';
  }
  function load() {
    Promise.all([TraceSite.request('list-deliveries', {}), TraceSite.request('get-delivery-subscription', {})]).then(function(results) {
      renderDeliveries(results[0].items || results[0] || []);
      renderSubscription(results[1]);
    }).catch(function(error) { TraceSite.toast(error.message, 'error'); });
  }
  TraceSite.$('#delivery-grid').addEventListener('click', function(event) {
    var button = event.target.closest('[data-claim-delivery]');
    if (!button) return;
    TraceSite.setBusy(button, true);
    TraceSite.request('claim-delivery', { deliveryId: button.getAttribute('data-claim-delivery') })
      .then(function() { TraceSite.toast('Package claimed into inventory.'); load(); })
      .catch(function(error) { TraceSite.toast(error.message, 'error'); })
      .finally(function() { TraceSite.setBusy(button, false); });
  });
  TraceSite.$('#subscribe-express').addEventListener('click', function() {
    var button = this;
    TraceSite.setBusy(button, true);
    TraceSite.request('subscribe-express', {})
      .then(function() { TraceSite.toast('Express delivery enabled.'); load(); })
      .catch(function(error) { TraceSite.toast(error.message, 'error'); })
      .finally(function() { TraceSite.setBusy(button, false); });
  });
  TraceSite.$('#cancel-express').addEventListener('click', function() {
    var button = this;
    TraceSite.setBusy(button, true);
    TraceSite.request('cancel-express', {})
      .then(function() { TraceSite.toast('Express subscription cancelled.'); load(); })
      .catch(function(error) { TraceSite.toast(error.message, 'error'); })
      .finally(function() { TraceSite.setBusy(button, false); });
  });
  load();
})();
"""


PREDEFINED_WEBSITE_CONTENT = {
    "searchable.com": _site(
        """
<div class="site-shell">
  <nav class="site-nav"><a class="brand" href="https://www.searchable.com/"><span class="brand-mark"></span><span>Searchable</span></a><div class="nav-links"><a class="nav-link" href="https://www.techhub.com/">Shopping</a><a class="nav-link" href="https://www.cryptfront.trade/">Finance</a><a class="nav-link" href="https://www.domania.com/">Hosting</a></div></nav>
  <section class="hero hero-full">
    <div><p class="eyebrow">0trace network index</p><h1>Find every trusted service in the game.</h1><p class="lede">Search shops, OS vendors, delivery tracking, wallet tools, domain services, and player-market destinations without leaving the simulated network.</p><div class="toolbar"><input id="site-search" class="field search-box" aria-label="Search websites" autofocus></div></div>
  </section>
  <section class="section compact"><div id="search-results" class="grid wide"></div></section>
  <footer>Searchable indexes only fictional in-game domains.</footer>
</div>
""",
        brand="#2563eb",
        brand_2="#14b8a6",
        js=SEARCHABLE_JS,
    ),
    "microhard.com": _site(
        """
<div class="site-shell">
  <nav class="site-nav"><a class="brand" href="https://www.microhard.com/"><span class="brand-mark"></span><span>Microhard</span></a><div class="nav-links"><a class="nav-link active" href="#doorsos">DoorsOS</a><a class="nav-link" href="#manuals">Manuals</a><a class="nav-link" href="https://www.deliveries.com/">Deliveries</a></div></nav>
  <section class="hero">
    <div><p class="eyebrow">Default starter OS</p><h1>DoorsOS for everyday operators.</h1><p class="lede">Familiar, compatible, heavily used, and bundled free for new accounts. DoorsOS is not the fastest OS, but it runs the standard 0trace desktop without surprises.</p><div class="toolbar"><button class="btn" data-install-os="doorsos">Install DoorsOS</button><button class="btn secondary" data-buy-sku="doorsos-hdd">Buy 1TB DoorsOS Drive</button></div></div>
    <aside class="hero-panel dark"><span class="metric">10.0</span><h2>DoorsOS Current</h2><ul class="list"><li><span>Terminal style</span><strong>Windows-like</strong></li><li><span>Processing modifier</span><strong>-20%</strong></li><li><span>Starter license</span><strong>Free</strong></li></ul></aside>
  </section>
  <section id="manuals" class="section"><div class="section-head"><div><h2>Operator manuals</h2><p>Core shortcuts, app commands, and terminal references.</p></div></div><div class="grid"><article class="panel"><h3>Desktop basics</h3><p>Use the taskbar, launch apps from Start, drag windows by their title bar, and resize from edges.</p></article><article class="panel"><h3>Terminal commands</h3><p class="code">dir · type · notepad · runas · ipconfig · tasklist · sysinfo · crack · mine</p></article><article class="panel"><h3>Recovery drive</h3><p>The DoorsOS drive ships as physical hardware and appears in Resources after delivery.</p></article></div></section>
  <footer>Microhard products are fictional 0trace game assets.</footer>
</div>
""",
        brand="#0078d4",
        brand_2="#22c55e",
        js=MICROHARD_JS,
    ),
    "pear.com": _site(
        """
<div class="site-shell pear">
  <nav class="site-nav"><a class="brand" href="https://www.pear.com/"><span class="brand-mark"></span><span>Pear</span></a><div class="nav-links"><a class="nav-link active" href="#fruitos">FruitOS</a><a class="nav-link" href="#chips">P chips</a><a class="nav-link" href="#guide">Guide</a></div></nav>
  <section class="hero">
    <div><p class="eyebrow">Polished premium OS</p><h1>FruitOS feels expensive because it is.</h1><p class="lede">Elegant motion, friendlier workflows, and stronger resistance against incoming fictional cracking attempts. FruitOS is built for players who value polish over raw openness.</p><div class="toolbar"><button class="btn" data-install-os="fruitos">Buy and install FruitOS</button><a class="btn subtle" href="#guide">Read the guide</a></div></div>
    <aside class="hero-panel"><span class="metric">-20%</span><h2>Incoming crack speed</h2><p class="muted">FruitOS slows attackers targeting your machine.</p></aside>
  </section>
  <section id="chips" class="section"><div class="section-head"><div><h2>P-series integrated chips</h2><p>CPU and RAM in one sealed part. Fast, quiet, and incompatible with GPUs.</p></div></div><div class="grid"><article class="product-card"><h3>Pear P1</h3><p>16GB integrated memory, efficient compute.</p><button class="btn" data-buy-sku="pear-p1">Buy P1</button></article><article class="product-card"><h3>Pear P1 Pro</h3><p>32GB memory and stronger CPU throughput.</p><button class="btn" data-buy-sku="pear-p1-pro">Buy P1 Pro</button></article><article class="product-card"><h3>Pear P2</h3><p>64GB memory for high-end operator builds.</p><button class="btn" data-buy-sku="pear-p2">Buy P2</button></article></div></section>
  <section id="guide" class="section compact"><div class="grid"><article class="panel"><h3>FruitOS terminal</h3><p class="code">ls · cat · nano · sudo · ifconfig · ps · sysinfo</p></article><article class="panel"><h3>Shortcuts</h3><p>Use the dock for apps, menu controls for system actions, and smooth workspace switching for multitasking.</p></article></div></section>
  <footer>Pear hardware and software are fictional 0trace game assets.</footer>
</div>
""",
        brand="#111827",
        brand_2="#ef4444",
        js=PEAR_JS,
        extra_css=".pear .site-shell,.pear.site-shell{background:linear-gradient(180deg,#fbfbfd,#eef2ff)}",
    ),
    "arctic.org": _site(
        """
<div class="site-shell">
  <nav class="site-nav"><a class="brand" href="https://www.arctic.org/"><span class="brand-mark"></span><span>Arctic</span></a><div class="nav-links"><a class="nav-link active" href="#download">Download</a><a class="nav-link" href="#wm">Window managers</a><a class="nav-link" href="#funding">Funding</a></div></nav>
  <section class="hero">
    <div><p class="eyebrow">Free and open source</p><h1>ArcticOS is transparent, fast, and yours.</h1><p class="lede">A community OS with a +20% processing modifier, terminal-first tooling, and install-time window manager choice.</p><div class="toolbar"><select id="arctic-wm" class="field"><option value="fruitly">Fruitly window manager</option><option value="carpened">Carpened window manager</option></select><button id="install-arctic" class="btn">Download ArcticOS</button></div></div>
    <aside class="hero-panel"><span class="metric">+20%</span><h2>Processing speed</h2><p class="muted">Boosts cracking and mining job throughput.</p></aside>
  </section>
  <section id="wm" class="section"><div class="grid"><article class="panel"><h3>Fruitly</h3><p>Soft dock-led layout inspired by premium consumer desktops.</p></article><article class="panel"><h3>Carpened</h3><p>Sharp panel and window workflow for productive, familiar multitasking.</p></article><article class="panel"><h3>Terminal guide</h3><p class="code">ls · cat · nano · sudo · pacman · ip · ps · sysinfo</p></article></div></section>
  <section id="funding" class="section compact"><div class="section-head"><div><h2>Public donations</h2><p>Community funding is public by design.</p></div></div><div class="grid" id="funding-grid"></div></section>
  <footer>ArcticOS is fictional open-source software inside 0trace.</footer>
</div>
""",
        brand="#0f766e",
        brand_2="#38bdf8",
        js=ARCTIC_JS,
    ),
    "techhub.com": _site(
        """
<div class="site-shell">
  <nav class="site-nav"><a class="brand" href="https://www.techhub.com/"><span class="brand-mark"></span><span>TechHub</span></a><div class="nav-links"><a class="nav-link active" href="#catalog">Catalog</a><a class="nav-link" href="https://www.deliveries.com/">Track orders</a></div></nav>
  <section class="hero hero-full"><div><p class="eyebrow">Hardware retail</p><h1>Build the machine your jobs require.</h1><p class="lede">Buy CPUs, GPUs, RAM, storage, motherboards, USB sticks, cases, and OS bundle drives. Hardware is delivered before it appears in Resources.</p></div></section>
  <section id="catalog" class="section compact"><div class="toolbar"><select id="catalog-filter" class="field"><option value="">All categories</option><option value="cpu">CPU</option><option value="gpu">GPU</option><option value="motherboard">Motherboard</option><option value="ram">RAM</option><option value="hdd">HDD</option><option value="ssd">SSD</option><option value="usb">USB</option><option value="case">Case</option><option value="pear_chip">Pear chip</option></select><input id="catalog-search" class="field" aria-label="Search catalog"></div><div id="catalog-grid" class="grid wide"></div></section>
  <footer>TechHub ships only fictional game hardware.</footer>
</div>
""",
        brand="#ea580c",
        brand_2="#2563eb",
        js=TECHHUB_JS,
    ),
    "secondlife.com": _site(
        """
<div class="site-shell">
  <nav class="site-nav"><a class="brand" href="https://www.secondlife.com/"><span class="brand-mark"></span><span>SecondLife</span></a><div class="nav-links"><a class="nav-link active" href="#market">Market</a><a class="nav-link" href="#selling">Selling</a></div></nav>
  <section class="hero"><div><p class="eyebrow">Player market</p><h1>Used parts. Leveled files. Real inventory.</h1><p class="lede">SecondLife lists hardware and software files that players put up for sale. Purchases are final and settle through in-game wallets.</p></div><aside class="hero-panel"><h2>How selling works</h2><p class="muted">List hardware and software files from the Resources app, then manage them here.</p></aside></section>
  <section id="market" class="section compact"><div class="toolbar"><select id="listing-filter" class="field"><option value="">All listings</option><option value="hardware">Hardware</option><option value="software">Software</option></select></div><div id="listing-grid" class="grid wide"><article class="panel">Loading marketplace...</article></div></section>
  <footer>SecondLife is an in-game player marketplace.</footer>
</div>
""",
        brand="#7c3aed",
        brand_2="#f97316",
        js=SECONDLIFE_JS,
    ),
    "cryptfront.trade": _site(
        """
<div class="site-shell">
  <nav class="site-nav"><a class="brand" href="https://www.cryptfront.trade/"><span class="brand-mark"></span><span>CryptFront</span></a><div class="nav-links"><a class="nav-link active" href="#markets">Markets</a><a class="nav-link" href="#wallets">Wallets</a><a class="nav-link" href="#transfer">Transfer</a></div></nav>
  <section class="hero"><div><p class="eyebrow">Fictional exchange</p><h1>Trade coins mined inside 0trace.</h1><p class="lede">Buy, sell, hold, and transfer fictional coins. No external finance, real crypto, or real wallet exists here.</p></div><aside class="hero-panel dark"><h2>Market pulse</h2><div id="coin-chart" class="chart"></div></aside></section>
  <section id="wallets" class="section compact"><div class="section-head"><div><h2>Wallets</h2><p>Create and manage active in-game wallets.</p></div><div class="toolbar"><input id="wallet-label" class="field" aria-label="Wallet label"><button id="create-wallet" class="btn">Create wallet</button></div></div><div id="wallet-grid" class="grid wide"></div></section>
  <section id="markets" class="section compact"><div class="grid"><form id="coin-trade" class="panel"><h3>Trade</h3><div class="toolbar"><select class="field" name="trade"><option value="buy">Buy with credits</option><option value="sell">Sell for credits</option></select><select class="field" name="wallet" data-wallet-select></select><select class="field" name="coin" data-coin-select></select><input class="field" name="amount" aria-label="Trade amount"><button class="btn">Execute trade</button></div></form><form id="coin-transfer" class="panel"><h3>Send coins</h3><div class="toolbar"><select class="field" name="wallet" data-wallet-select></select><select class="field" name="coin" data-coin-select></select><input class="field" name="to" aria-label="Recipient wallet address"><input class="field" name="amount" aria-label="Transfer amount"><button class="btn">Send</button></div></form></div></section>
  <footer>CryptFront handles fictional in-game balances only.</footer>
</div>
""",
        brand="#172554",
        brand_2="#22c55e",
        js=CRYPTFRONT_JS,
    ),
    "domania.com": _site(
        """
<div class="site-shell">
  <nav class="site-nav"><a class="brand" href="https://www.domania.com/"><span class="brand-mark"></span><span>Domania</span></a><div class="nav-links"><a class="nav-link active" href="#register">Register</a><a class="nav-link" href="#owned">My domains</a></div></nav>
  <section class="hero"><div><p class="eyebrow">Domains and certificates</p><h1>Publish your own corner of the 0trace web.</h1><p class="lede">Register a domain, attach it to your active machine, issue HTTPS certificates, and publish HTML/CSS/JS through the Webserver app.</p></div><aside class="hero-panel"><span class="metric">.com</span><h2>In-game DNS</h2><p class="muted">Domains only resolve inside the 0trace browser.</p></aside></section>
  <section id="register" class="section compact"><form id="domain-form" class="panel"><h2>Register a domain</h2><div class="toolbar"><input id="domain-name" class="field" aria-label="Domain name"><button class="btn">Register</button></div><p class="fine">Do not include real external hosting. Player sites are sandboxed.</p></form></section>
  <section id="owned" class="section compact"><div class="section-head"><div><h2>Owned domains</h2><p>Issue certificates for active domains.</p></div></div><div id="domain-list" class="grid wide"></div></section>
  <footer>Domania manages fictional in-game domains and certificates.</footer>
</div>
""",
        brand="#0891b2",
        brand_2="#6366f1",
        js=DOMANIA_JS,
    ),
    "deliveries.com": _site(
        """
<div class="site-shell">
  <nav class="site-nav"><a class="brand" href="https://www.deliveries.com/"><span class="brand-mark"></span><span>Deliveries</span></a><div class="nav-links"><a class="nav-link active" href="#track">Tracking</a><a class="nav-link" href="#express">Express</a></div></nav>
  <section class="hero"><div><p class="eyebrow">Package logistics</p><h1>Track every hardware shipment.</h1><p class="lede">Standard hardware delivery takes about two hours. Express subscribers receive eligible packages in 20 minutes.</p></div><aside id="express-status" class="hero-panel">Loading subscription...</aside></section>
  <section id="express" class="section compact"><div class="toolbar"><button id="subscribe-express" class="btn">Subscribe to Express</button><button id="cancel-express" class="btn subtle">Cancel Express</button></div></section>
  <section id="track" class="section compact"><div class="section-head"><div><h2>Active deliveries</h2><p>Claim packages after ETA reaches zero.</p></div></div><div id="delivery-grid" class="grid wide"><article class="panel">Loading deliveries...</article></div></section>
  <footer>Deliveries moves fictional hardware inside 0trace.</footer>
</div>
""",
        brand="#16a34a",
        brand_2="#0ea5e9",
        js=DELIVERIES_JS,
    ),
}
