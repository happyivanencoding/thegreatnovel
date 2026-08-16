(function () {
  "use strict";

  var approvalPhrase = "批准写入正史";
  var csrf = document.querySelector('meta[name="csrf-token"]');

  function errorMessage(payload) {
    if (payload && payload.error) {
      return payload.error.message || payload.error.code || "审批请求失败";
    }
    return "审批请求失败";
  }

  async function submit(button, endpoint, extraPayload) {
    var feedback = button && button.closest
      ? button.closest("article, section, form")?.querySelector("[data-approval-feedback]")
      : null;
    var payload = Object.assign(
      { confirmation: approvalPhrase },
      extraPayload || {},
    );
    button.disabled = true;
    try {
      var response = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRF-Token": csrf ? csrf.content : "",
        },
        body: JSON.stringify(payload),
      });
      var value = await response.json();
      if (!response.ok || value.error) throw new Error(errorMessage(value));
      if (feedback) {
        feedback.textContent = "已通过共享发布边界写入正史。";
        feedback.classList.remove("is-error");
      }
      return value;
    } catch (error) {
      button.disabled = false;
      if (feedback) {
        feedback.textContent = error.message || String(error);
        feedback.classList.add("is-error");
      }
      throw error;
    }
  }

  window.CodexApproval = { submit: submit, phrase: approvalPhrase };

  document.querySelectorAll("[data-approval-action]").forEach(function (button) {
    button.addEventListener("click", async function () {
      try {
        await submit(button, button.dataset.approvalEndpoint);
        button.textContent = "已写入正史";
      } catch (_error) {
        // The inline feedback contains the actionable server-side reason.
      }
    });
  });
})();
