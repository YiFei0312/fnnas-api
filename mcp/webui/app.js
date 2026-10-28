/* 飞牛接口 MCP Server —— Web UI 逻辑（原生 JS，无构建步骤） */
(function () {
  "use strict";

  var state = { status: null, config: null, tab: "available", listLoaded: 0 };

  function $(id) { return document.getElementById(id); }
  function esc(text) {
    return String(text == null ? "" : text)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }
  function toast(msg, kind) {
    var el = $("toast");
    el.textContent = msg;
    el.className = "toast show " + (kind || "");
    clearTimeout(el._timer);
    el._timer = setTimeout(function () { el.className = "toast"; }, 2600);
  }
  function api(path, options) {
    return fetch(path, options).then(function (r) {
      return r.json().then(function (body) {
        if (!r.ok) { throw new Error(body.error || ("HTTP " + r.status)); }
        return body;
      });
    });
  }
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }
    var ta = document.createElement("textarea");
    ta.value = text; ta.style.position = "fixed"; ta.style.opacity = "0";
    document.body.appendChild(ta); ta.select();
    try { document.execCommand("copy"); } catch (e) { /* ignore */ }
    document.body.removeChild(ta);
    return Promise.resolve();
  }

  /* ---------------- 状态 ---------------- */
  function renderStatus() {
    var st = state.status;
    if (!st) { return; }
    var conn = st.connection || {};
    var stats = st.stats || {};

    $("kpiWs").innerHTML = (stats.ws_total || 0) + "<small> 个</small>";
    $("kpiWsOk").textContent = stats.ws_available || 0;
    $("kpiHttp").innerHTML = (stats.http_total || 0) + "<small> 个</small>";
    $("kpiHttpOk").textContent = stats.http_available || 0;
    $("kpiTools").textContent = stats.tools || 0;

    var pill = $("connPill");
    var ok = !!conn.connected;
    var configured = conn.configured !== false;
    pill.className = "pill " + (ok ? "ok" : (configured ? "err" : "warn"));
    $("connText").textContent = ok
      ? ("已连接 " + (conn.username || "") + " @ " + (conn.host || ""))
      : (configured ? "未连接 NAS" : "待配置账号");
    $("footConn").textContent = ok ? (conn.ws_url || "") : (conn.last_error || "未连接");

    // 首页「飞牛连接配置」里的状态灯与目标
    var target = $("connTarget");
    var pill2 = $("connPill2");
    if (target) {
      target.textContent = ok
        ? ((conn.username || "-") + " @ " + (conn.host || "-") + ":" + (conn.port || "-"))
        : (configured ? "未连接" : "未配置账号");
    }
    if (pill2) { pill2.className = "pill " + (ok ? "ok" : (configured ? "err" : "warn")); }
    var extra = $("connExtra");
    if (extra) {
      if (!configured) {
        extra.textContent = "还没有账号密码：填好下面的 IP / 账号 / 密码，点「保存并重连」";
      } else if (ok) {
        extra.textContent = "已连接 · 接口调用 " + (conn.calls || 0) +
          " 次 / 失败 " + (conn.calls_failed || 0) + " 次";
      } else {
        extra.textContent = "最后错误：" + (conn.last_error || "尚未连接");
      }
    }
    $("footVersion").textContent = "fnnas-mcp v" + ((st.server || {}).version || "?");
    $("footTotal").textContent = (stats.ws_total || 0) + " + " + (stats.http_total || 0);

    /* 两个传输开关 + 地址 */
    var mcp = st.mcp || {}, sse = st.sse || {};
    $("swMcp").checked = !!mcp.enabled;
    $("swSse").checked = !!sse.enabled;
    $("cardMcp").className = "transport " + (mcp.enabled ? "on" : "off");
    $("cardSse").className = "transport " + (sse.enabled ? "on" : "off");
    $("urlMcp").textContent = mcp.url || "/mcp";
    $("urlSse").textContent = sse.url || "/sse";

    var mcpUrl = mcp.url || (location.origin + "/mcp");
    var sseUrl = sse.url || (location.origin + "/sse");
    $("snippetMcp").textContent = JSON.stringify({
      mcpServers: {
        "fnnas-nas": { type: "http", url: mcpUrl }
      }
    }, null, 2);
    $("snippetSse").textContent = JSON.stringify({
      mcpServers: {
        "fnnas-nas-sse": { type: "sse", url: sseUrl }
      }
    }, null, 2);
    $("clientSample").textContent =
      "# Claude Code（命令行）\n" +
      "claude mcp add --transport http fnnas-nas " + mcpUrl + "\n\n" +
      "# 其它客户端（JSON 配置）\n" +
      JSON.stringify({
        mcpServers: {
          "fnnas-nas": { type: "http", url: mcpUrl },
          "fnnas-nas-sse": { type: "sse", url: sseUrl }
        }
      }, null, 2);
    $("docFrame").src = "/docs";
    $("tabCount").textContent = (stats.ws_available || 0) + (stats.http_available || 0);
    highlightSetupIfNeeded();
  }

  function loadStatus() {
    api("/api/status").then(function (st) {
      state.status = st;
      renderStatus();
    }).catch(function (err) {
      $("connPill").className = "pill err";
      $("connText").textContent = "服务异常";
      console.warn(err);
    });
  }

  /* ---------------- 配置 ---------------- */
  function highlightSetupIfNeeded() {
    var st = state.status;
    if (!st || !st.connection) { return; }
    var needed = st.connection.configured === false;
    var box = $("connBlock");
    if (box) { box.classList.toggle("need-setup", needed); }
  }

  function loadConfig() {
    api("/api/config").then(function (cfg) {
      state.config = cfg;
      var nas = cfg.nas || {};
      $("fHost").value = nas.host || "";
      $("fPort").value = nas.port || "";
      $("fBase").value = nas.base_url || "";
      $("fUser").value = nas.username || "";
      $("fPass").value = "";
      var hint = $("passHint");
      if (hint) {
        hint.textContent = nas.password_set
          ? "（已配置，留空表示不修改）"
          : "（还没配置，必须填）";
      }
      var tools = ((cfg.server || {}).tools) || {};
      $("swUnverified").checked = !!tools.include_unverified;
    }).catch(function (err) { toast("读取配置失败：" + err.message, "err"); });
  }

  function saveConfig(payload, okMessage) {
    return api("/api/config", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    }).then(function (resp) {
      state.config = resp.config;
      if ($("fPass")) { $("fPass").value = ""; }
      toast(okMessage || "已保存", "ok");
      loadStatus();
      loadConfig();
      return resp;
    }).catch(function (err) { toast("保存失败：" + err.message, "err"); });
  }

  function bindTransports() {
    $("swMcp").addEventListener("change", function (e) {
      saveConfig({ server: { mcp: { enabled: e.target.checked } } },
        "Streamable HTTP 已" + (e.target.checked ? "开启" : "关闭"))
        .then(function () { renderStatus(); });
    });
    $("swSse").addEventListener("change", function (e) {
      saveConfig({ server: { sse: { enabled: e.target.checked } } },
        "HTTP + SSE 已" + (e.target.checked ? "开启" : "关闭"))
        .then(function () { renderStatus(); });
    });
    $("swUnverified").addEventListener("change", function (e) {
      saveConfig({ server: { tools: { include_unverified: e.target.checked } } },
        "工具范围已更新");
    });
    var useLocal = $("useLocal");
    if (useLocal) {
      useLocal.addEventListener("click", function () {
        $("fHost").value = "127.0.0.1";
        $("fHost").focus();
        toast("已填 127.0.0.1（应用在 NAS 本机运行）");
      });
    }
    $("saveCfg").addEventListener("click", function () {
      saveConfig({
        nas: {
          host: $("fHost").value.trim(),
          port: $("fPort").value.trim(),
          base_url: $("fBase").value.trim(),
          username: $("fUser").value.trim(),
          password: $("fPass").value
        }
      }, "连接配置已保存，正在重连…");
    });
    $("testConn").addEventListener("click", function () {
      var btn = $("testConn");
      btn.disabled = true;
      $("connMsg").className = "msg";
      $("connMsg").textContent = "测试中…";
      api("/api/test", { method: "POST" }).then(function (r) {
        if (r.ok) {
          $("connMsg").className = "msg ok";
          var user = (r.user || {});
          $("connMsg").textContent = "连接成功：" + (user.name || "已登录") +
            (user.admin ? "（管理员）" : "") +
            " · " + (r.host || "") + ":" + (r.port || "") +
            "（" + r.elapsed_ms + "ms）";
        } else {
          $("connMsg").className = "msg err";
          $("connMsg").textContent = "连接失败：" + (r.error || "未知错误");
        }
        loadStatus();
      }).catch(function (err) {
        $("connMsg").className = "msg err";
        $("connMsg").textContent = "请求失败：" + err.message;
      }).finally(function () { btn.disabled = false; });
    });
  }

  /* ---------------- 可用接口列表 ---------------- */
  var searchTimer = null;

  function statusBadge(item) {
    if (item.verified) { return '<span class="badge-status ok">✅ 实测通过</span>'; }
    if (item.available) { return '<span class="badge-status warn">⚠ 需要参数</span>'; }
    return '<span class="badge-status dim">— 未实测</span>';
  }

  function loadInterfaces() {
    var q = $("q").value.trim();
    var proto = $("protoSel").value;
    var only = $("availSel").value;
    var url = "/api/interfaces?keyword=" + encodeURIComponent(q) +
      "&protocol=" + proto + "&only_available=" + only + "&limit=500";
    $("rows").innerHTML = '<tr><td colspan="6" class="muted">加载中…</td></tr>';
    api(url).then(function (resp) {
      state.listLoaded = resp.total;
      $("listCount").textContent = "共 " + resp.total + " 个" +
        (resp.total > resp.items.length ? "（显示前 " + resp.items.length + " 个）" : "");
      if (!resp.items.length) {
        $("rows").innerHTML = '<tr><td colspan="6" class="muted">没有匹配的接口</td></tr>';
        return;
      }
      var html = "";
      resp.items.forEach(function (it) {
        var protoCls = it.protocol === "ws" ? "ws" : "http";
        var protoText = it.protocol === "ws" ? "WS" : "HTTP";
        var name = esc(it.name);
        if (it.protocol === "http") { name = esc(it.method + " " + it.url); }
        html += "<tr>" +
          '<td><span class="badge-proto ' + protoCls + '">' + protoText + "</span></td>" +
          '<td class="name">' + name + "</td>" +
          '<td class="muted">' + esc(it.group) + "</td>" +
          '<td class="purpose">' + esc(it.purpose || "—") + "</td>" +
          '<td class="params">' + esc(it.params || "—") + "</td>" +
          "<td>" + statusBadge(it) + "</td>" +
          "</tr>";
      });
      $("rows").innerHTML = html;
    }).catch(function (err) {
      $("rows").innerHTML = '<tr><td colspan="6" class="muted">加载失败：' +
        esc(err.message) + "</td></tr>";
    });
  }

  function bindList() {
    $("q").addEventListener("input", function () {
      clearTimeout(searchTimer);
      searchTimer = setTimeout(loadInterfaces, 260);
    });
    $("protoSel").addEventListener("change", loadInterfaces);
    $("availSel").addEventListener("change", loadInterfaces);
    $("reloadList").addEventListener("click", loadInterfaces);
  }

  /* ---------------- 标签页 ---------------- */
  function bindTabs() {
    Array.prototype.forEach.call(document.querySelectorAll(".tab"), function (tab) {
      tab.addEventListener("click", function () {
        var name = tab.getAttribute("data-tab");
        state.tab = name;
        Array.prototype.forEach.call(document.querySelectorAll(".tab"), function (t) {
          t.classList.toggle("active", t === tab);
        });
        Array.prototype.forEach.call(document.querySelectorAll(".panel"), function (p) {
          p.classList.toggle("active", p.id === "panel-" + name);
        });
        if (name === "logs") { loadLogs(); }
        if (name === "docs") {
          var frame = $("docFrame");
          if (frame.getAttribute("src") === "about:blank") { frame.src = "/docs"; }
        }
      });
    });
  }

  /* ---------------- 日志 ---------------- */
  function loadLogs() {
    api("/api/logs").then(function (resp) {
      var lines = resp.lines || [];
      $("logs").textContent = lines.length ? lines.join("\n") : "（暂无日志）";
      $("logCount").textContent = lines.length + " 行";
      var el = $("logs");
      el.scrollTop = el.scrollHeight;
    }).catch(function (err) { $("logs").textContent = "读取失败：" + err.message; });
  }

  /* ---------------- 主题 ---------------- */
  function bindTheme() {
    var saved = localStorage.getItem("fnmcp-theme");
    if (saved === "light") { document.body.classList.add("light"); }
    $("themeBtn").addEventListener("click", function () {
      document.body.classList.toggle("light");
      localStorage.setItem("fnmcp-theme",
        document.body.classList.contains("light") ? "light" : "dark");
    });
  }

  /* ---------------- 复制 ---------------- */
  function bindCopy() {
    Array.prototype.forEach.call(document.querySelectorAll(".copy"), function (btn) {
      btn.addEventListener("click", function () {
        var target = $(btn.getAttribute("data-copy"));
        if (!target) { return; }
        copyText(target.textContent.trim()).then(function () {
          toast("已复制：" + target.textContent.trim(), "ok");
        });
      });
    });
  }

  /* ---------------- 启动 ---------------- */
  document.addEventListener("DOMContentLoaded", function () {
    bindTabs();
    bindTransports();
    bindList();
    bindTheme();
    bindCopy();
    $("refreshBtn").addEventListener("click", function () {
      loadStatus(); loadInterfaces(); toast("已刷新");
    });
    $("reloadLogs").addEventListener("click", loadLogs);

    loadStatus();
    loadConfig();
    loadInterfaces();
    setInterval(loadStatus, 5000);
  });
})();
