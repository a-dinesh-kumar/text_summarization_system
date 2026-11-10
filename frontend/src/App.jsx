import { useMemo, useState } from "react";
import {
  AlertCircle,
  ArrowDownToLine,
  ArrowRight,
  Check,
  CheckCircle2,
  Clock3,
  Copy,
  FileText,
  FileUp,
  File as FileIcon,
  Gauge,
  Layers3,
  LoaderCircle,
  Sparkles,
  UploadCloud,
  X,
} from "lucide-react";
import { requestSummary } from "./api";

const MAX_UPLOAD_MB = Number(import.meta.env.VITE_MAX_UPLOAD_SIZE_MB || 15);
const ACCEPTED_EXTENSIONS = [".pdf", ".docx", ".txt"];
const MIN_MEANINGFUL_CHARACTERS = 50;

function countMeaningfulCharacters(value) {
  return (value.match(/[\p{L}\p{N}]/gu) || []).length;
}

function formatDuration(seconds) {
  if (typeof seconds !== "number") return "—";
  return seconds < 60
    ? `${seconds.toFixed(1)} sec`
    : `${Math.floor(seconds / 60)}m ${(seconds % 60).toFixed(0)}s`;
}

function formatNumber(value) {
  return typeof value === "number" ? value.toLocaleString() : "—";
}

function App() {
  const [mode, setMode] = useState("text");
  const [text, setText] = useState("");
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const githubUrl = import.meta.env.VITE_GITHUB_URL || "";
  const linkedinUrl = import.meta.env.VITE_LINKEDIN_URL || "";
  const [copied, setCopied] = useState(false);

  const characterCount = text.length;
  const meaningfulCharacterCount = countMeaningfulCharacters(text);
  const textIsValid = meaningfulCharacterCount >= MIN_MEANINGFUL_CHARACTERS;
  const canSubmit = mode === "text" ? textIsValid : Boolean(file);

  const selectedFileSize = useMemo(() => {
    if (!file) return "";
    return `${(file.size / (1024 * 1024)).toFixed(2)} MB`;
  }, [file]);

  function changeMode(nextMode) {
    setMode(nextMode);
    setError("");
    setResult(null);
  }

  function validateFile(candidate) {
    if (!candidate) return;
    const extension = `.${candidate.name.split(".").pop()}`.toLowerCase();

    if (!ACCEPTED_EXTENSIONS.includes(extension)) {
      setError("Unsupported file type. Please upload a PDF, DOCX or TXT file.");
      return;
    }
    if (candidate.size > MAX_UPLOAD_MB * 1024 * 1024) {
      setError(`The file exceeds the ${MAX_UPLOAD_MB} MB upload limit.`);
      return;
    }

    setError("");
    setResult(null);
    setFile(candidate);
  }

  async function handleSubmit(event) {
    event.preventDefault();
    if (loading) return;

    if (mode === "text" && !textIsValid) {
      setError(
        `Please enter at least ${MIN_MEANINGFUL_CHARACTERS} meaningful characters.`
      );
      return;
    }

    if (mode === "file" && !file) {
      setError("Please select a document to upload.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await requestSummary({
        text: mode === "text" ? text.trim() : "",
        file: mode === "file" ? file : null,
      });
      setResult(data);
    } catch (requestError) {
      setError(requestError.message || "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  async function copySummary() {
    if (!result?.summary) return;
    try {
      await navigator.clipboard.writeText(result.summary);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1800);
    } catch {
      setError("Clipboard access was blocked by the browser. You can select and copy the summary manually.");
    }
  }

  function downloadSummary() {
    if (!result?.summary) return;
    const blob = new Blob([result.summary], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = "summary.txt";
    anchor.click();
    URL.revokeObjectURL(url);
  }

  function resetAll() {
    setText("");
    setFile(null);
    setResult(null);
    setError("");
    setCopied(false);
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <a className="brand" href="/" aria-label="Text Summarization System home">
          <span className="brand-mark"><Sparkles size={19} /></span>
          <span>Text Summarization <strong>System</strong></span>
        </a>
        <nav className="social-links" aria-label="Social profiles">
          <a className="social-link" href={githubUrl || undefined} target="_blank" rel="noreferrer"
             aria-label="GitHub profile" title="GitHub" aria-disabled={!githubUrl}
             onClick={(event) => { if (!githubUrl) event.preventDefault(); }}>
            <img src="/icons/github.png" alt="" />
          </a>
          <a className="social-link" href={linkedinUrl || undefined} target="_blank" rel="noreferrer"
             aria-label="LinkedIn profile" title="LinkedIn" aria-disabled={!linkedinUrl}
             onClick={(event) => { if (!linkedinUrl) event.preventDefault(); }}>
            <img src="/icons/linkedin.png" alt="" />
          </a>
        </nav>
      </header>

      <main className="main-content">
        <section className="hero">
          <div className="eyebrow"><Sparkles size={14} /> AI-POWERED SUMMARIZATION</div>
          <h1>Less reading.<br /><span>More understanding.</span></h1>
          <p className="hero-copy">
            Turn lengthy text and documents into clear, focused summaries.
            Add your content and let the models do the heavy lifting.
          </p>
        </section>

        <section className="workspace">
          <div className="workspace-heading">
            <div>
              <h2>Create a summary</h2>
              <p>Choose how you want to provide your content.</p>
            </div>
          </div>

          <div className="mode-tabs" role="tablist" aria-label="Input type">
            <button
              className={`mode-tab ${mode === "text" ? "active" : ""}`}
              onClick={() => changeMode("text")}
              role="tab"
              aria-selected={mode === "text"}
              type="button"
            >
              <FileText size={17} /> Paste text
            </button>
            <button
              className={`mode-tab ${mode === "file" ? "active" : ""}`}
              onClick={() => changeMode("file")}
              role="tab"
              aria-selected={mode === "file"}
              type="button"
            >
              <FileUp size={17} /> Upload document
            </button>
          </div>

          <form onSubmit={handleSubmit}>
            {mode === "text" ? (
              <div className="text-input-wrap">
                <textarea
                  value={text}
                  onChange={(event) => {
                    setText(event.target.value);
                    setResult(null);
                    setError("");
                  }}
                  placeholder="Paste an article, research notes, a chapter or any text you want to summarize..."
                  aria-label="Text to summarize"
                />
                <div className="input-footer">
                  <span>
                    {characterCount.toLocaleString()} characters
                    {mode === "text" &&
                      ` · ${meaningfulCharacterCount}/${MIN_MEANINGFUL_CHARACTERS} meaningful characters`}
                  </span>

                  <span>
                    {mode === "text"
                      ? textIsValid
                        ? "Ready to summarize"
                        : "Enter at least 50 meaningful characters"
                      : "Paste your content above"}
                  </span>
                </div>
              </div>
            ) : (
              <div className="upload-area">
                {!file ? (
                  <label className="upload-prompt">
                    <input
                      type="file"
                      accept=".pdf,.docx,.txt,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document,text/plain"
                      onChange={(event) => validateFile(event.target.files?.[0])}
                    />
                    <span className="upload-icon"><UploadCloud size={25} /></span>
                    <strong>Choose a document to upload</strong>
                    <span>or browse files from your computer</span>
                    <small>PDF, DOCX or TXT · Maximum {MAX_UPLOAD_MB} MB</small>
                  </label>
                ) : (
                  <div className="selected-file">
                    <span className="file-icon"><FileIcon size={22} /></span>
                    <div className="file-details">
                      <strong>{file.name}</strong>
                      <span>{selectedFileSize}</span>
                    </div>
                    <button className="icon-button" type="button" onClick={() => setFile(null)} aria-label="Remove file">
                      <X size={18} />
                    </button>
                  </div>
                )}
              </div>
            )}

            {error && (
              <div className="error-message" role="alert">
                <AlertCircle size={17} /> <span>{error}</span>
              </div>
            )}

            <div className="submit-row">
              <p className="privacy-hint">Supported formats: {ACCEPTED_EXTENSIONS.join(", ").toUpperCase()}</p>
              <button className="primary-button" type="submit" disabled={!canSubmit || loading}>
                {loading ? (
                  <><LoaderCircle className="spin" size={17} /> Summarizing...</>
                ) : (
                  <>Generate summary <ArrowRight size={17} /></>
                )}
              </button>
            </div>
          </form>
        </section>

        {loading && (
          <section className="processing-card" aria-live="polite">
            <div className="processing-icon"><LoaderCircle className="spin" size={23} /></div>
            <div>
              <strong>Working on your summary</strong>
              <p>Your content is being processed. Longer documents may take a little more time.</p>
            </div>
          </section>
        )}

        {result && (
          <section className="result-section">
            <div className="result-heading">
              <div>
                <div className="eyebrow result-eyebrow"><CheckCircle2 size={14} /> SUMMARY GENERATED</div>
                <h2>Your summary</h2>
              </div>
              <div className="result-actions">
                <button className="secondary-button" onClick={copySummary} type="button">
                  {copied ? <Check size={16} /> : <Copy size={16} />}
                  {copied ? "Copied" : "Copy"}
                </button>
                <button className="secondary-button" onClick={downloadSummary} type="button">
                  <ArrowDownToLine size={16} /> Download
                </button>
              </div>
            </div>

            <article className="summary-card">
              <div className="summary-content">{result.summary}</div>
              <div className="summary-source">
                <span><FileText size={14} /> {result.source_name || "Pasted text"}</span>
                <span>{formatNumber(result.source_characters)} source characters</span>
              </div>
            </article>

            <div className="metrics-grid">
              <Metric icon={<Sparkles size={17} />} label="Model" value={result.model || result.model_key} />
              <Metric icon={<Clock3 size={17} />} label="Processing time" value={formatDuration(result.processing_time_seconds)} />
              <Metric icon={<Layers3 size={17} />} label="Input tokens" value={formatNumber(result.source_tokens)} />
              <Metric icon={<Gauge size={17} />} label="Generation chunks" value={formatNumber(result.total_generation_chunks)} />
            </div>

            <div className="technical-details">
              <span>Initial chunks: <strong>{formatNumber(result.initial_chunk_count)}</strong></span>
              <span>Reduction levels: <strong>{formatNumber(result.reduction_levels)}</strong></span>
              <span>Input type: <strong>{result.source_type}</strong></span>
            </div>
            <button className="start-over" onClick={resetAll} type="button">Start a new summary <ArrowRight size={15} /></button>
          </section>
        )}

        <section className="how-it-works">
          <div className="how-title">
            <span className="eyebrow">UNDER THE HOOD</span>
            <h2>From content to clarity</h2>
          </div>
          <div className="steps">
            <Step number="01" title="Provide content" description="Paste text or upload a PDF, DOCX or TXT document." />
            <Step number="02" title="AI processing" description="FastAPI prepares the content and runs the configured transformer model." />
            <Step number="03" title="Get your summary" description="Read, copy or download the generated summary." />
          </div>
        </section>
      </main>

      <footer className="footer">
        <span>Text Summarization System</span>
        <span>Built with React, FastAPI & Transformer models</span>
      </footer>
    </div>
  );
}

function Metric({ icon, label, value }) {
  return (
    <div className="metric-card">
      <span className="metric-icon">{icon}</span>
      <span className="metric-label">{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function Step({ number, title, description }) {
  return (
    <div className="step-card">
      <span className="step-number">{number}</span>
      <strong>{title}</strong>
      <p>{description}</p>
    </div>
  );
}

export default App;
