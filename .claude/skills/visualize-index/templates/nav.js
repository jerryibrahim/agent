(function () {
  var NAV_HEIGHT = 36;

  // Detect current project and page from URL
  var parts = window.location.pathname.split('/').filter(Boolean);
  var filename = parts[parts.length - 1] || 'index.html';
  var project = parts[parts.length - 2] || '';

  // Derive a display name from the folder name
  var displayName = project.replace(/-/g, ' ').replace(/\b\w/g, function (c) {
    return c.toUpperCase();
  });

  // Build nav links
  var pages = [
    { label: 'Overview', file: 'index.html' },
    { label: 'Interactive', file: 'interactive.html' },
    { label: 'Deep Dive', file: 'deep-dive.html' }
  ];

  var linksHtml = pages.map(function (p) {
    var active = filename === p.file;
    return '<a href="' + p.file + '" style="' +
      'color:' + (active ? '#e2e8f0' : '#3b82f6') + ';' +
      'text-decoration:none;' +
      'font-weight:' + (active ? '600' : '400') + ';' +
      'padding:4px 10px;' +
      'border-radius:4px;' +
      'background:' + (active ? '#1e293b' : 'transparent') + ';' +
      'font-size:13px;' +
      '">' + p.label + '</a>';
  }).join('');

  // Create nav element
  var nav = document.createElement('div');
  nav.id = 'site-nav';
  nav.style.cssText =
    'position:fixed;top:0;left:0;right:0;z-index:9999;' +
    'height:' + NAV_HEIGHT + 'px;' +
    'background:#060a14;' +
    'border-bottom:1px solid #1e293b;' +
    'display:flex;align-items:center;' +
    'padding:0 16px;' +
    'font-family:system-ui,-apple-system,sans-serif;' +
    'gap:8px;';

  nav.innerHTML =
    '<a href="../index.html" style="color:#3b82f6;text-decoration:none;font-size:13px;font-weight:500;padding:4px 10px;border-radius:4px;white-space:nowrap;">' +
    '&#8592; All Projects</a>' +
    '<span style="color:#334155;font-size:13px;">/</span>' +
    '<span style="color:#94a3b8;font-size:13px;font-weight:600;white-space:nowrap;">' + displayName + '</span>' +
    '<span style="color:#334155;font-size:13px;">/</span>' +
    '<div style="display:flex;gap:2px;">' + linksHtml + '</div>';

  // Insert nav and push content down
  document.body.insertBefore(nav, document.body.firstChild);
  document.body.style.paddingTop = NAV_HEIGHT + 'px';

  // Pages using height:100vh need to shrink to fit the nav bar
  var cs = window.getComputedStyle(document.body);
  if (cs.height === window.innerHeight + 'px' || cs.overflow === 'hidden') {
    document.body.style.height = 'calc(100vh - ' + NAV_HEIGHT + 'px)';
  }
})();
