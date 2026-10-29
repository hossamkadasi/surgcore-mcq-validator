"use strict";

(() => {
  const engine = window.SurgCoreValidator;
  if (!engine) throw new Error("Validator engine failed to load.");

  const $ = id => document.getElementById(id);
  const input = $("input"), drop = $("drop"), selection = $("selection");
  const mapping = $("mapping"), status = $("status"), run = $("run");
  const download = $("download"), issues = $("issues");

  let selected = null, report = null;
  const cleanDemo = [
    { id: "DEMO-01", stem: "Which property identifies the selected answer label?",
      options: { A: "source", B: "answer", C: "stem", D: "id" },
      answer: "B", explanation: "The answer field identifies the option label.", source: "Synthetic example" },
    { id: "DEMO-02", stem: "Which file extension commonly represents comma-separated values?",
      options: { A: ".csv", B: ".jpg", C: ".mp3", D: ".png" },
      answer: "A", explanation: "CSV is a plain-text table format.", source: "Synthetic example" }
  ];
  const flaggedDemo = [
    cleanDemo[0],
    cleanDemo[1],
    { ...cleanDemo[0], id: "DEMO-03", answer: "E", source: "" }
  ];

  function statusText(text, kind = "") {
    status.textContent = text;
    status.className = "status" + (kind ? " " + kind : "");
  }

  function reset() {
    report = null;
    download.disabled = true;
    for (const key of ["total", "valid", "errors", "warnings"]) $(key).textContent = "—";
    issues.replaceChildren();
    const empty = document.createElement("li");
    empty.className = "muted";
    empty.textContent = "Findings will appear here after validation.";
    issues.append(empty);
  }

  function useSample(label, questions) {
    selected = { name: label + ".json", text: JSON.stringify({ questions }, null, 2), format: "json" };
    input.value = "";
    mapping.value = "";
    selection.textContent = "Selected synthetic example: " + label;
    reset();
    statusText("Sample loaded locally. Select “Run local checks” to see the results.");
  }

  async function acceptFile(file) {
    reset();
    if (!file) {
      selected = null;
      selection.textContent = "No file selected";
      statusText("Choose a CSV or JSON file.", "error");
      return;
    }
    const ext = (file.name.split(".").pop() || "").toLowerCase();
    if (!["csv", "json"].includes(ext)) {
      selected = null;
      selection.textContent = "Unsupported format";
      statusText("Only .csv or .json files are supported.", "error");
      return;
    }
    if (file.size > engine.LIMIT_BYTES) {
      selected = null;
      selection.textContent = "File exceeds limit";
      statusText("The browser demo accepts files of up to 5 MiB.", "error");
      return;
    }
    try {
      const text = await file.text();
      selected = { name: file.name, text, format: ext };
      selection.textContent = file.name + " (" + file.size.toLocaleString() + " bytes)";
      statusText("File loaded into local browser memory. Select “Run local checks”.");
    } catch (_) {
      selected = null;
      selection.textContent = "File not loaded";
      statusText("Could not read that local file.", "error");
    }
  }

  function render(result) {
    $("total").textContent = result.summary.record_count.toLocaleString();
    $("valid").textContent = result.summary.schema_valid_record_count.toLocaleString();
    $("errors").textContent = result.summary.error_count.toLocaleString();
    $("warnings").textContent = result.summary.warning_count.toLocaleString();
    issues.replaceChildren();

    if (!result.issues.length) {
      const li = document.createElement("li");
      li.textContent = "No structural issues detected. Medical accuracy has NOT been reviewed.";
      issues.append(li);
    } else {
      for (const issue of result.issues) {
        const li = document.createElement("li");
        const heading = document.createElement("strong");
        heading.className = issue.severity === "error" ? "danger" : "warning";
        heading.textContent = issue.severity.toUpperCase() + " · " + issue.code;
        const detail = document.createElement("small");
        // Never interpolate user-supplied IDs into HTML.
        detail.textContent = "Record " + issue.record_index +
          (issue.question_id ? " · ID " + issue.question_id : "") +
          " — " + issue.message;
        li.append(heading, detail);
        issues.append(li);
      }
    }
  }

  input.addEventListener("change", () => { void acceptFile(input.files?.[0]); });
  drop.addEventListener("dragover", event => {
    event.preventDefault();
    drop.classList.add("drag");
  });
  drop.addEventListener("dragleave", event => {
    if (!drop.contains(event.relatedTarget)) drop.classList.remove("drag");
  });
  drop.addEventListener("drop", event => {
    event.preventDefault();
    drop.classList.remove("drag");
    void acceptFile(event.dataTransfer?.files?.[0]);
  });

  $("clean").addEventListener("click", () => useSample("valid-sample", cleanDemo));
  $("broken").addEventListener("click", () => useSample("flagged-sample", flaggedDemo));

  run.addEventListener("click", () => {
    reset();
    if (!selected) {
      statusText("Choose a local file or load a synthetic example first.", "error");
      return;
    }
    try {
      const config = engine.parseMapping(mapping.value);
      const parsed = engine.parseInput(selected.text, selected.format, config);
      const result = engine.validate(parsed);
      report = result;
      render(result);
      download.disabled = false;
      if (result.summary.error_count) {
        statusText("Checks finished. " + result.summary.error_count + " structural error(s) found. Review before import.", "error");
      } else if (result.summary.warning_count) {
        statusText("Checks finished. No structural errors; " + result.summary.warning_count + " warning(s) need review.", "ok");
      } else {
        statusText("Checks finished with no structural problems. This does NOT certify medical correctness.", "ok");
      }
    } catch (error) {
      report = null;
      statusText("Validation failed: " + (error instanceof Error ? error.message : "Unsupported input"), "error");
    }
  });

  download.addEventListener("click", () => {
    if (!report) return;
    const blob = new Blob([JSON.stringify(report, null, 2) + "\n"], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "surgcore-validation-report.json";
    document.body.append(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 2000);
  });
})();
