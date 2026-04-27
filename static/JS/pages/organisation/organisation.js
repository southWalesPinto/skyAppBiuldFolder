(function () {
  function setupOrganisationFilters() {
    var page = document.querySelector('[data-organisation-page]');
    if (!page) {
      return;
    }

    var gridPanel = page.querySelector('[data-org-grid-panel]');
    var grid = page.querySelector('[data-org-grid]');
    var networkPanel = page.querySelector('[data-org-network-panel]');
    var cards = Array.prototype.slice.call(page.querySelectorAll('[data-org-team-card]'));
    var departmentInput = page.querySelector('[data-org-filter="department"]');
    var teamTypeInput = page.querySelector('[data-org-filter="team_type"]');
    var dependenciesInput = page.querySelector('[data-org-filter="dependencies"]');
    var globalSearch = page.querySelector('[data-org-global-search]');
    var totalTeams = page.querySelector('[data-org-total-teams]');
    var totalMembers = page.querySelector('[data-org-total-members]');
    var emptyState = page.querySelector('[data-org-empty-state]');
    var viewButtons = Array.prototype.slice.call(page.querySelectorAll('[data-org-view]'));
    var exportLink = page.querySelector('.org-export-btn');
    var networkSvg = null;
    var selectedNodeId = null;
    var inspectorShell = page.querySelector('[data-org-inspector]');
    var inspectorBody = page.querySelector('[data-org-inspector-body]');
    var zoomOutButton = page.querySelector('[data-org-zoom-out]');
    var zoomResetButton = page.querySelector('[data-org-zoom-reset]');
    var zoomInButton = page.querySelector('[data-org-zoom-in]');
    var zoomLevel = 1;
    var zoomStep = 0.2;
    var zoomMin = 0.7;
    var zoomMax = 1.6;
    var currentNetworkWidth = 0;
    var currentNetworkHeight = 0;
    var inspectorTitle = page.querySelector('[data-org-inspector-title]');
    var inspectorSubtitle = page.querySelector('[data-org-inspector-subtitle]');
    var inspectorMembers = page.querySelector('[data-org-inspector-members]');
    var inspectorDepartment = page.querySelector('[data-org-inspector-department]');
    var inspectorUpstreamCount = page.querySelector('[data-org-inspector-upstream-count]');
    var inspectorDownstreamCount = page.querySelector('[data-org-inspector-downstream-count]');
    var inspectorUpstream = page.querySelector('[data-org-inspector-upstream]');
    var inspectorDownstream = page.querySelector('[data-org-inspector-downstream]');

    function rawValue(input) {
      return input ? input.value.trim() : '';
    }

    function value(input) {
      return rawValue(input).toLowerCase();
    }

    function getActiveView() {
      var activeButton = viewButtons.find(function (button) {
        return button.classList.contains('is-active');
      });
      return activeButton ? activeButton.getAttribute('data-org-view') : 'grid';
    }

    function updateExportLink() {
      if (!exportLink) {
        return;
      }

      var baseHref = exportLink.getAttribute('href') || '';
      var url = new URL(baseHref, window.location.origin);
      var params = new URLSearchParams(url.search);
      var department = rawValue(departmentInput);
      var teamType = rawValue(teamTypeInput);
      var dependencies = rawValue(dependenciesInput);
      var search = rawValue(globalSearch);
      var view = getActiveView();

      if (department) {
        params.set('department', department);
      } else {
        params.delete('department');
      }

      if (teamType) {
        params.set('team_type', teamType);
      } else {
        params.delete('team_type');
      }

      if (dependencies) {
        params.set('dependencies', dependencies);
      } else {
        params.delete('dependencies');
      }

      if (search) {
        params.set('search', search);
      } else {
        params.delete('search');
      }

      params.set('view', view);
      url.search = params.toString();
      exportLink.setAttribute('href', url.pathname + (url.search ? '?' + url.search : ''));
    }

    function visibleCards() {
      return cards.filter(function (card) {
        return !card.classList.contains('is-hidden');
      });
    }

    function setViewMode(mode) {
      var showNetwork = mode === 'network';
      if (gridPanel) {
        gridPanel.hidden = showNetwork;
        gridPanel.style.display = showNetwork ? 'none' : 'block';
      }
      if (networkPanel) {
        networkPanel.hidden = !showNetwork;
        networkPanel.style.display = showNetwork ? 'block' : 'none';
      }
    }

    function applyFilters() {
      var department = value(departmentInput);
      var teamType = value(teamTypeInput);
      var dependencies = value(dependenciesInput);
      var search = value(globalSearch);
      var visibleCount = 0;
      var visibleMembers = 0;

      cards.forEach(function (card) {
        var name = (card.getAttribute('data-team-name') || '').toLowerCase();
        var cardDepartment = (card.getAttribute('data-team-department') || '').toLowerCase();
        var cardType = (card.getAttribute('data-team-type') || '').toLowerCase();
        var cardDependencies = (card.getAttribute('data-team-dependencies') || '').toLowerCase();
        var memberCount = parseInt(card.getAttribute('data-team-members') || '0', 10);
        var matchesDepartment = !department || cardDepartment.indexOf(department) !== -1;
        var matchesTeamType = !teamType || cardType.indexOf(teamType) !== -1;
        var matchesDependencies = !dependencies || cardDependencies.indexOf(dependencies) !== -1;
        var searchHaystack = [name, cardDepartment, cardType, cardDependencies].join(' ');
        var matchesSearch = !search || searchHaystack.indexOf(search) !== -1;
        var isVisible = matchesDepartment && matchesTeamType && matchesDependencies && matchesSearch;

        card.classList.toggle('is-hidden', !isVisible);
        if (isVisible) {
          visibleCount += 1;
          visibleMembers += Number.isNaN(memberCount) ? 0 : memberCount;
        }
      });

      if (totalTeams) {
        totalTeams.textContent = String(visibleCount);
      }

      if (totalMembers) {
        totalMembers.textContent = String(visibleMembers);
      }

      if (emptyState) {
        emptyState.hidden = visibleCount !== 0;
      }

      if (grid) {
        grid.classList.toggle('is-empty', visibleCount === 0);
      }

      if (gridPanel) {
        gridPanel.hidden = getActiveView() === 'network';
      }

      if (networkPanel) {
        networkPanel.hidden = getActiveView() !== 'network';
      }

      updateExportLink();

      if (getActiveView() === 'network') {
        renderNetwork();
      } else {
        hideNetwork();
      }
    }

    function buildGraphData() {
      var visible = visibleCards();
      var nodes = visible.map(function (card) {
        return {
          id: card.getAttribute('data-team-name'),
          name: card.querySelector('h3') ? card.querySelector('h3').textContent : card.getAttribute('data-team-name'),
          members: parseInt(card.getAttribute('data-team-members') || '0', 10) || 0,
          department: card.getAttribute('data-team-department') || '',
          depsRaw: (card.getAttribute('data-team-dependencies') || '').trim(),
          el: card
        };
      });

      var nodeByName = {};
      nodes.forEach(function (node) {
        nodeByName[(node.id || '').toLowerCase()] = node;
      });

      var links = [];
      nodes.forEach(function (node) {
        if (!node.depsRaw) {
          return;
        }

        var parts = node.depsRaw.split('|||').map(function (part) {
          return part.trim();
        }).filter(Boolean);

        parts.forEach(function (part) {
          var pieces = part.split('::');
          var key = (pieces[0] || '').toLowerCase();
          var direction = (pieces[1] || 'upstream').toLowerCase();
          var type = (pieces[2] || 'dependency').toLowerCase();
          var target = nodeByName[key];
          if (target) {
            links.push({ source: node.id, target: target.id, direction: direction, type: type });
          }
        });
      });

      return { nodes: nodes, links: links };
    }

    function removeNetworkSvg() {
      if (!networkSvg) {
        return;
      }
      if (networkSvg.parentNode) {
        networkSvg.parentNode.removeChild(networkSvg);
      }
      networkSvg = null;
    }

    function getNodeLevels(nodes, links) {
      var outgoing = {};
      var memo = {};
      var visiting = {};

      nodes.forEach(function (node) {
        outgoing[node.id] = [];
      });

      links.forEach(function (link) {
        if (!outgoing[link.source]) {
          outgoing[link.source] = [];
        }
        outgoing[link.source].push(link.target);
      });

      function levelFor(nodeId) {
        if (memo[nodeId] !== undefined) {
          return memo[nodeId];
        }
        if (visiting[nodeId]) {
          return 0;
        }

        visiting[nodeId] = true;
        var deps = outgoing[nodeId] || [];
        var level = 0;

        if (deps.length) {
          var maxDepLevel = 0;
          deps.forEach(function (depId) {
            var depLevel = levelFor(depId);
            if (depLevel > maxDepLevel) {
              maxDepLevel = depLevel;
            }
          });
          level = maxDepLevel + 1;
        }

        visiting[nodeId] = false;
        memo[nodeId] = level;
        return level;
      }

      nodes.forEach(function (node) {
        node.level = levelFor(node.id);
      });

      return memo;
    }

    function renderInspector(node, nodes, links) {
      if (!inspectorBody) {
        return;
      }

      if (!node) {
        if (inspectorShell) {
          inspectorShell.hidden = true;
        }
        inspectorBody.hidden = true;
        return;
      }

      var upstream = [];
      var downstream = [];

      links.forEach(function (link) {
        var source = nodes.find(function (item) { return item.id === link.source; });
        var target = nodes.find(function (item) { return item.id === link.target; });
        if (!source || !target) {
          return;
        }

        if (link.source === node.id) {
          upstream.push({ name: target.name, type: link.type, direction: link.direction });
        }

        if (link.target === node.id) {
          downstream.push({ name: source.name, type: link.type, direction: link.direction });
        }
      });

      if (inspectorShell) {
        inspectorShell.hidden = false;
      }

      if (inspectorTitle) {
        inspectorTitle.textContent = node.name;
      }
      if (inspectorSubtitle) {
        inspectorSubtitle.textContent = 'Selected team network view';
      }
      if (inspectorMembers) {
        inspectorMembers.textContent = String(node.members);
      }
      if (inspectorDepartment) {
        inspectorDepartment.textContent = node.department || 'Team';
      }
      if (inspectorUpstreamCount) {
        inspectorUpstreamCount.textContent = String(upstream.length);
      }
      if (inspectorDownstreamCount) {
        inspectorDownstreamCount.textContent = String(downstream.length);
      }

      function fillList(listElement, items, emptyLabel) {
        if (!listElement) {
          return;
        }
        listElement.innerHTML = '';
        if (!items.length) {
          var emptyItem = document.createElement('li');
          emptyItem.textContent = emptyLabel;
          listElement.appendChild(emptyItem);
          return;
        }

        items.forEach(function (item) {
          var li = document.createElement('li');
          li.textContent = item.name + ' (' + item.type + ')';
          listElement.appendChild(li);
        });
      }

      fillList(inspectorUpstream, upstream, 'No upstream dependencies');
      fillList(inspectorDownstream, downstream, 'No downstream dependents');

      inspectorBody.hidden = false;
    }

    function highlightNeighborhood(selectedId, nodes, links) {
      selectedNodeId = selectedId;
      var neighborhood = {};
      neighborhood[selectedId] = true;

      links.forEach(function (link) {
        if (link.source === selectedId || link.target === selectedId) {
          neighborhood[link.source] = true;
          neighborhood[link.target] = true;
        }
      });

      Array.prototype.slice.call(networkSvg.querySelectorAll('[data-node-group]')).forEach(function (nodeGroup) {
        var nodeId = nodeGroup.getAttribute('data-node-id');
        nodeGroup.setAttribute('opacity', neighborhood[nodeId] ? '1' : '0.18');
      });

      Array.prototype.slice.call(networkSvg.querySelectorAll('[data-edge-link]')).forEach(function (edge) {
        var sourceId = edge.getAttribute('data-source-id');
        var targetId = edge.getAttribute('data-target-id');
        var relevant = neighborhood[sourceId] && neighborhood[targetId];
        edge.setAttribute('opacity', relevant ? '1' : '0.08');
        edge.setAttribute('stroke-width', relevant ? (edge.getAttribute('data-base-width') || '2.25') : '1.4');
      });

      renderInspector(nodes.find(function (node) { return node.id === selectedId; }), nodes, links);
    }

    function clearFocus(nodes, links) {
      selectedNodeId = null;
      if (!networkSvg) {
        return;
      }
      Array.prototype.slice.call(networkSvg.querySelectorAll('[data-node-group]')).forEach(function (nodeGroup) {
        nodeGroup.setAttribute('opacity', '1');
      });
      Array.prototype.slice.call(networkSvg.querySelectorAll('[data-edge-link]')).forEach(function (edge) {
        edge.setAttribute('opacity', '1');
        edge.setAttribute('stroke-width', edge.getAttribute('data-base-width') || '2.25');
      });
      renderInspector(null, nodes, links);
    }

    function applyZoom(nextZoom) {
      if (!networkSvg || !currentNetworkWidth || !currentNetworkHeight) {
        return;
      }
      zoomLevel = Math.max(zoomMin, Math.min(zoomMax, nextZoom));
      networkSvg.style.width = Math.round(currentNetworkWidth * zoomLevel) + 'px';
      networkSvg.style.height = Math.round(currentNetworkHeight * zoomLevel) + 'px';
      networkSvg.style.maxWidth = 'none';
    }

    function renderNetwork() {
      if (!networkPanel) {
        return;
      }

      cards.forEach(function (card) {
        card.style.display = 'none';
      });

      removeNetworkSvg();

      var svgNS = 'http://www.w3.org/2000/svg';
      var data = buildGraphData();
      var nodes = data.nodes;
      var links = data.links;
      var columnGap = 240;
      var rowGap = 150;
      var marginX = 100;
      var marginY = 100;

      getNodeLevels(nodes, links);

      var levelGroups = {};
      var maxLevel = 0;
      nodes.forEach(function (node) {
        if (!levelGroups[node.level]) {
          levelGroups[node.level] = [];
        }
        levelGroups[node.level].push(node);
        if (node.level > maxLevel) {
          maxLevel = node.level;
        }
      });

      var maxPerLevel = 1;
      Object.keys(levelGroups).forEach(function (key) {
        var groupSize = levelGroups[key].length;
        if (groupSize > maxPerLevel) {
          maxPerLevel = groupSize;
        }
      });

      var contentWidth = (maxLevel + 1) * columnGap + marginX * 2;
      var contentHeight = maxPerLevel * rowGap + marginY * 2;
      var width = contentWidth;
      var height = contentHeight;
      currentNetworkWidth = width;
      currentNetworkHeight = height;
      zoomLevel = 1;


      networkSvg = document.createElementNS(svgNS, 'svg');
      networkSvg.setAttribute('width', String(width));
      networkSvg.setAttribute('height', String(height));
      networkSvg.setAttribute('viewBox', '0 0 ' + width + ' ' + height);
      networkSvg.setAttribute('aria-label', 'Team dependency network');
      networkSvg.style.display = 'block';
      networkSvg.style.width = Math.round(width) + 'px';
      networkSvg.style.height = Math.round(height) + 'px';
      networkSvg.style.maxWidth = 'none';
      networkSvg.style.maxHeight = 'none';

      applyZoom(zoomLevel);
      networkSvg.addEventListener('click', function (event) {
        if (event.target === networkSvg) {
          clearFocus(nodes, links);
        }
      });
      networkPanel.appendChild(networkSvg);

      var defs = document.createElementNS(svgNS, 'defs');
      var marker = document.createElementNS(svgNS, 'marker');
      marker.setAttribute('id', 'arrowhead');
      marker.setAttribute('markerWidth', '10');
      marker.setAttribute('markerHeight', '7');
      marker.setAttribute('refX', '10');
      marker.setAttribute('refY', '3.5');
      marker.setAttribute('orient', 'auto');
      var path = document.createElementNS(svgNS, 'path');
      path.setAttribute('d', 'M0,0 L10,3.5 L0,7 z');
      path.setAttribute('fill', '#94a3b8');
      marker.appendChild(path);
      defs.appendChild(marker);
      networkSvg.appendChild(defs);

      var nodeTypeColors = {
        architecture: '#ef4444',
        frontend: '#60a5fa',
        backend: '#10b981',
        security: '#8b5cf6',
        qa: '#f97316',
        mobile: '#f59e0b',
        data: '#ec4899',
        devops: '#8b5cf6',
        api: '#14b8a6',
        general: '#27c5a6'
      };

      function edgeColor(type, direction) {
        var palette = {
          'infrastructure support': '#64748b',
          'bug resolution': '#f97316',
          'security fixes': '#8b5cf6',
          'agile coaching': '#10b981',
          'deployment pipeline': '#3b82f6',
          'encryption logic': '#f59e0b',
          'ci/cd infrastructure': '#0ea5e9',
          'cloud hosting services': '#22c55e'
        };
        var key = (type || 'dependency').toLowerCase();
        return palette[key] || (direction === 'downstream' ? '#60a5fa' : '#cbd5e1');
      }

      Object.keys(levelGroups).forEach(function (key) {
        levelGroups[key].sort(function (left, right) {
          return left.name.localeCompare(right.name);
        });
      });

      nodes.forEach(function (node) {
        var group = levelGroups[node.level] || [];
        var groupHeight = Math.max(1, group.length) * rowGap;
        var startY = Math.max(marginY, (height - groupHeight) / 2 + rowGap / 2);
        var indexInGroup = group.indexOf(node);
        node.x = marginX + node.level * columnGap;
        node.y = startY + indexInGroup * rowGap;
      });

      links.forEach(function (link) {
        var source = nodes.find(function (node) { return node.id === link.source; });
        var target = nodes.find(function (node) { return node.id === link.target; });
        if (!source || !target) {
          return;
        }

        var sourceX = source.x + 40;
        var sourceY = source.y;
        var targetX = target.x - 40;
        var targetY = target.y;
        var bendX = sourceX + ((targetX - sourceX) / 2);
        var pathData = 'M' + sourceX + ',' + sourceY + ' L' + bendX + ',' + sourceY + ' L' + bendX + ',' + targetY + ' L' + targetX + ',' + targetY;

        var edge = document.createElementNS(svgNS, 'path');
        edge.setAttribute('d', pathData);
        edge.setAttribute('fill', 'none');
        edge.setAttribute('stroke', edgeColor(link.type, link.direction));
        edge.setAttribute('stroke-width', '2.25');
        edge.setAttribute('marker-end', 'url(#arrowhead)');
        edge.setAttribute('stroke-linecap', 'round');
        edge.setAttribute('data-edge-link', 'true');
        edge.setAttribute('data-source-id', link.source);
        edge.setAttribute('data-target-id', link.target);
        edge.setAttribute('data-base-width', '2.25');
        networkSvg.appendChild(edge);
      });

      nodes.forEach(function (node) {
        var group = document.createElementNS(svgNS, 'g');
        group.setAttribute('transform', 'translate(' + node.x + ',' + node.y + ')');
        group.setAttribute('data-node-group', 'true');
        group.setAttribute('data-node-id', node.id);
        group.style.cursor = 'pointer';

        var departmentKey = (node.department || '').toLowerCase();
        var circleColor = nodeTypeColors[departmentKey] || nodeTypeColors.general;

        var circle = document.createElementNS(svgNS, 'circle');
        circle.setAttribute('r', 38);
        circle.setAttribute('fill', circleColor);
        circle.setAttribute('stroke', '#fff');
        circle.setAttribute('stroke-width', '3');
        circle.setAttribute('filter', 'drop-shadow(0 8px 16px rgba(15, 23, 42, 0.15))');
        group.appendChild(circle);

        var name = document.createElementNS(svgNS, 'text');
        name.setAttribute('x', 0);
        name.setAttribute('y', -2);
        name.setAttribute('text-anchor', 'middle');
        name.setAttribute('fill', '#fff');
        name.setAttribute('font-size', '11');
        name.setAttribute('font-weight', '700');
        name.textContent = node.name;
        group.appendChild(name);

        var members = document.createElementNS(svgNS, 'text');
        members.setAttribute('x', 0);
        members.setAttribute('y', 14);
        members.setAttribute('text-anchor', 'middle');
        members.setAttribute('fill', '#f0fffb');
        members.setAttribute('font-size', '10');
        members.textContent = node.members + ' members';
        group.appendChild(members);

        group.addEventListener('click', function (event) {
          event.stopPropagation();
          highlightNeighborhood(node.id, nodes, links);
          if (node.el && node.el.scrollIntoView) {
            node.el.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });
            node.el.classList.add('highlight');
            setTimeout(function () {
              node.el.classList.remove('highlight');
            }, 1800);
          }
        });

        networkSvg.appendChild(group);
      });

      if (selectedNodeId) {
        highlightNeighborhood(selectedNodeId, nodes, links);
      } else {
        renderInspector(null, nodes, links);
      }

      setViewMode('network');
    }

    function hideNetwork() {
      removeNetworkSvg();
      cards.forEach(function (card) {
        card.style.display = '';
      });
      selectedNodeId = null;
      if (inspectorShell) {
        inspectorShell.hidden = true;
      }
      if (inspectorBody) {
        inspectorBody.hidden = true;
      }
      setViewMode('grid');
    }

    function updateZoom(delta) {
      if (!networkSvg || !currentNetworkWidth || !currentNetworkHeight) {
        return;
      }
      applyZoom(zoomLevel + delta);
      if (selectedNodeId) {
        var data = buildGraphData();
        highlightNeighborhood(selectedNodeId, data.nodes, data.links);
      }
    }

    if (zoomOutButton) {
      zoomOutButton.addEventListener('click', function () {
        updateZoom(-zoomStep);
      });
    }

    if (zoomInButton) {
      zoomInButton.addEventListener('click', function () {
        updateZoom(zoomStep);
      });
    }

    if (zoomResetButton) {
      zoomResetButton.addEventListener('click', function () {
        updateZoom(1 - zoomLevel);
      });
    }

    [departmentInput, teamTypeInput, dependenciesInput, globalSearch].forEach(function (input) {
      if (!input) {
        return;
      }
      input.addEventListener('input', applyFilters);
    });

    viewButtons.forEach(function (button) {
      button.addEventListener('click', function () {
        var mode = button.getAttribute('data-org-view');
        viewButtons.forEach(function (item) {
          item.classList.toggle('is-active', item === button);
        });
        if (mode === 'network') {
          renderNetwork();
        } else {
          hideNetwork();
        }
        updateExportLink();
      });
    });

    window.addEventListener('resize', function () {
      if (getActiveView() === 'network') {
        renderNetwork();
      } else {
        hideNetwork();
      }
    });

    setViewMode(getActiveView());
    applyFilters();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupOrganisationFilters);
  } else {
    setupOrganisationFilters();
  }
})();
