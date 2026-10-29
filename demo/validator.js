/* SurgCore browser preview: offline, dependency-free structural checks.
 * This is not a medical answer-key review or a replacement for the Python CLI.
 */
(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.SurgCoreValidator = api;
})(typeof window === "object" ? window : null, function () {
  "use strict";

  const HEADERS = {
    id: ["id", "question_id"],
    stem: ["stem", "question", "question_text"],
    option_a: ["option_a", "a"],
    option_b: ["option_b", "b"],
    option_c: ["option_c", "c"],
    option_d: ["option_d", "d"],
    answer: ["answer", "correct_answer", "correct_option"],
    explanation: ["explanation", "rationale"],
    source: ["source", "reference"]
  };
  const LETTERS = ["A", "B", "C", "D"];
  const LIMIT_BYTES = 5 * 1024 * 1024;
  const LIMIT_RECORDS = 5000;

  function fail(message) { throw new Error(message); }
  function stringValue(value) { return value == null ? "" : String(value).trim(); }

  function keysLower(obj, position) {
    if (!obj || typeof obj !== "object" || Array.isArray(obj)) fail("Record " + position + " must be an object.");
    const out = Object.create(null);
    for (const key of Object.keys(obj)) {
      const normalized = key.trim().toLowerCase();
      if (!normalized || Object.hasOwn(out, normalized)) fail("Record " + position + ": empty or duplicated field name.");
      out[normalized] = obj[key];
    }
    return out;
  }

  function parseCsv(text) {
    if (typeof text !== "string") fail("CSV content must be text.");
    if (text.charCodeAt(0) === 0xFEFF) text = text.slice(1);
    const rows = [];
    let row = [], cell = "", inQuotes = false, endedWithNewline = false;
    for (let i = 0; i < text.length; i++) {
      const c = text[i];
      endedWithNewline = false;
      if (inQuotes) {
        if (c === '"') {
          if (text[i + 1] === '"') { cell += '"'; i++; }
          else inQuotes = false;
        } else {
          cell += c;
        }
      } else if (c === '"') {
        if (cell !== "") fail("Unexpected quote in CSV field.");
        inQuotes = true;
      } else if (c === ",") {
        row.push(cell);
        cell = "";
      } else if (c === "\n" || c === "\r") {
        if (c === "\r" && text[i + 1] === "\n") i++;
        row.push(cell);
        rows.push(row);
        row = [];
        cell = "";
        endedWithNewline = true;
      } else {
        cell += c;
      }
    }
    if (inQuotes) fail("Unclosed quoted CSV field.");
    if (!endedWithNewline || cell !== "" || row.length) { row.push(cell); rows.push(row); }
    if (!rows.length || rows[0].length === 1 && !rows[0][0].trim()) fail("CSV must contain a header.");
    const headings = rows.shift().map(x => x.trim().toLowerCase());
    if (headings.some(x => !x) || new Set(headings).size !== headings.length) fail("CSV headers must be unique and nonempty.");
    if (!rows.length) fail("Input contains no question records.");
    if (rows.length > LIMIT_RECORDS) fail("Browser preview supports at most 5,000 records.");
    return rows.map((values, i) => {
      if (values.length !== headings.length) fail("CSV row " + (i + 2) + " has " + values.length + " columns, expected " + headings.length + ".");
      const item = Object.create(null);
      headings.forEach((key, j) => { item[key] = values[j]; });
      return item;
    });
  }

  function parseMapping(text) {
    if (!text || !text.trim()) return Object.create(null);
    let parsed;
    try { parsed = JSON.parse(text); } catch (_) { fail("Mapping is not valid JSON."); }
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) fail("Mapping must be a JSON object.");
    const mapping = Object.create(null);
    const seen = new Set();
    for (const key of Object.keys(parsed)) {
      if (!Object.hasOwn(HEADERS, key)) fail("Unknown canonical mapping field: " + key);
      if (typeof parsed[key] !== "string" || !parsed[key].trim()) fail("Mapping column names must be nonempty strings.");
      const column = parsed[key].trim().toLowerCase();
      if (seen.has(column)) fail("Mapping source columns must be unique.");
      mapping[key] = column;
      seen.add(column);
    }
    return mapping;
  }

  function parseInput(text, format, mapping) {
    if (typeof text !== "string") fail("Select a text file.");
    if (new TextEncoder().encode(text).length > LIMIT_BYTES) fail("Browser preview supports files up to 5 MiB.");
    mapping = mapping || Object.create(null);
    let raw;
    if (format === "csv") raw = parseCsv(text);
    else if (format === "json") {
      let parsed;
      try { parsed = JSON.parse(text); } catch (_) { fail("File is not valid JSON."); }
      raw = Array.isArray(parsed) ? parsed : parsed && parsed.questions;
      if (!Array.isArray(raw)) fail('JSON must be a question array or an object containing "questions".');
    } else fail("Supported file formats: .csv and .json.");
    if (!raw.length) fail("Input contains no question records.");
    if (raw.length > LIMIT_RECORDS) fail("Browser preview supports at most 5,000 records.");

    return raw.map((original, i) => {
      const item = keysLower(original, i + 1);
      function field(name) {
        if (Object.hasOwn(mapping, name)) return stringValue(item[mapping[name]]);
        for (const alias of HEADERS[name]) if (Object.hasOwn(item, alias)) return stringValue(item[alias]);
        return "";
      }
      let options;
      const hasMappedOptions = LETTERS.some(letter => Object.hasOwn(mapping, "option_" + letter.toLowerCase()));
      if (hasMappedOptions) options = LETTERS.map(letter => field("option_" + letter.toLowerCase()));
      else if (Array.isArray(item.options)) {
        if (item.options.length !== 4) fail("Record " + (i + 1) + ": options array must contain exactly A-D.");
        options = item.options.map(stringValue);
      } else if (item.options != null) {
        const nested = keysLower(item.options, i + 1);
        if (Object.keys(nested).sort().join(",") !== "a,b,c,d") fail("Record " + (i + 1) + ": options object must contain exactly A-D.");
        options = LETTERS.map(letter => stringValue(nested[letter.toLowerCase()]));
      } else options = LETTERS.map(letter => field("option_" + letter.toLowerCase()));
      return {
        record_index: i + 1,
        question_id: field("id"), stem: field("stem"), options,
        answer: field("answer"), explanation: field("explanation"), source: field("source")
      };
    });
  }

  const STEM_RE = /[\p{L}\p{N}_]+(?:[.,]\d+)*|<=|>=|[≤≥≠±<>+\-−=/%°:]/gu;
  function normalizeStem(value) {
    return (String(value).normalize("NFKC").toLowerCase().match(STEM_RE) || []).join(" ");
  }
  function normalizeOption(value) {
    const cleaned = String(value).normalize("NFKC").toLowerCase().trim().replace(/\s+/g, " ");
    return cleaned.replace(/^[ .,!?:;"'“”‘’]+|[ .,!?:;"'“”‘’]+$/g, "") || cleaned;
  }

  function validate(questions) {
    if (!Array.isArray(questions)) fail("Expected parsed questions.");
    const issues = [], idSeen = new Map(), stemSeen = new Map(), invalidRows = new Set();
    function flag(q, severity, code, message, related) {
      const issue = { severity, code, record_index: q.record_index, question_id: q.question_id, message };
      if (related !== undefined) issue.related_record_index = related;
      issues.push(issue);
      if (severity === "error") invalidRows.add(q.record_index);
    }
    questions.forEach(q => {
      if (!q.question_id) flag(q, "error", "missing_id", "Question ID is missing.");
      else if (idSeen.has(q.question_id)) flag(q, "error", "duplicate_id", "Question ID duplicates an earlier record.", idSeen.get(q.question_id));
      else idSeen.set(q.question_id, q.record_index);
      const stem = normalizeStem(q.stem);
      if (!stem) flag(q, "error", "missing_stem", "Question stem is empty.");
      else if (stem.length < 12) flag(q, "warning", "short_stem", "Question stem is unusually short.");
      if (stem) {
        if (stemSeen.has(stem)) flag(q, "error", "duplicate_stem", "Question stem duplicates an earlier record.", stemSeen.get(stem));
        else stemSeen.set(stem, q.record_index);
      }
      const seen = new Map();
      LETTERS.forEach((letter, i) => {
        const value = normalizeOption(q.options[i] || "");
        if (!value) flag(q, "error", "missing_option", "Option " + letter + " is empty.");
        else if (seen.has(value)) flag(q, "error", "duplicate_option", "Option " + letter + " duplicates option " + seen.get(value) + ".");
        else seen.set(value, letter);
      });
      if (!q.answer) flag(q, "error", "missing_answer", "Correct answer label is missing.");
      else if (!LETTERS.includes(q.answer.toUpperCase())) flag(q, "error", "invalid_answer", "Correct answer must be A, B, C, or D.");
      if (!q.explanation) flag(q, "warning", "missing_explanation", "Explanation is missing.");
      if (!q.source) flag(q, "warning", "missing_source", "Source/reference is missing.");
    });
    const errors = issues.filter(x => x.severity === "error").length;
    return {
      schema_version: "1.0",
      summary: {
        record_count: questions.length,
        schema_valid_record_count: questions.length - invalidRows.size,
        error_count: errors,
        warning_count: issues.length - errors,
        passed_structural_checks: errors === 0
      },
      issues,
      disclaimer: "Structural checks only. No medical fact-checking or clinical certification. The browser preview does not run the Python CLI's heuristic near-duplicate scan."
    };
  }

  return { parseCsv, parseInput, parseMapping, normalizeStem, normalizeOption, validate, LIMIT_BYTES, LIMIT_RECORDS };
});
