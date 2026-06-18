/** @jsxRuntime classic */
const { useMemo, useState } = React;

function Field({ label, children }) {
  return (
    <label className="adv-field">
      <span>{label}</span>
      {children}
    </label>
  );
}

function YesNo({ label, value, onChange, name }) {
  return (
    <div className="adv-radio-group">
      <p>{label}</p>
      <div>
        <label><input type="radio" name={name} checked={value === "True"} onChange={() => onChange("True")} /> Yes</label>
        <label><input type="radio" name={name} checked={value === "False"} onChange={() => onChange("False")} /> No</label>
      </div>
    </div>
  );
}

function PredictorApp() {
  const csrfToken = document.getElementById("csrfTokenHolder")?.value || "";
  const initialState = {
    name: "",
    age: "",
    gender: "",
    jaundice: "",
    abdominal_pain: "",
    weight_loss: "",
    fatigue: "",
    fever: "",
    bilirubin: "",
    alt: "",
    ast: "",
    alp: "",
    ca19_9: "",
    smoking: "",
    alcohol: "",
    diabetes: "",
    liver_disease_history: "",
    gallstones: ""
  };

  const [form, setForm] = useState(initialState);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  const riskTheme = useMemo(() => {
    if (!result) return "low";
    return result.risk_level;
  }, [result]);

  const updateField = (key, value) => setForm((s) => ({ ...s, [key]: value }));

  const allFilled = Object.values(form).every((v) => `${v}`.trim() !== "");

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setResult(null);
    if (!allFilled) {
      setError("Please fill all fields. Invalid input.");
      return;
    }
    setLoading(true);

    const body = new URLSearchParams(form);
    const response = await fetch("/api/predict/", {
      method: "POST",
      headers: { "X-CSRFToken": csrfToken, "Content-Type": "application/x-www-form-urlencoded" },
      body: body.toString()
    });
    const data = await response.json();
    setLoading(false);
    if (!response.ok || !data.ok) {
      setError(data.message || "Prediction failed.");
      return;
    }
    setResult(data.result);
  };

  return (
    <div className="adv-wrapper">
      <div className="adv-header">
        <h1>AI-Driven Cholangiocarcinoma Risk Assessment</h1>
        <p>Enter patient profile, symptoms, lab values, and risk factors for a predictive risk score.</p>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="adv-grid">
          <section className="adv-panel">
            <h3>Patient Details</h3>
            <Field label="Name"><input value={form.name} onChange={(e) => updateField("name", e.target.value)} /></Field>
            <Field label="Age"><input type="number" min="1" max="120" value={form.age} onChange={(e) => updateField("age", e.target.value)} /></Field>
            <Field label="Gender">
              <select value={form.gender} onChange={(e) => updateField("gender", e.target.value)}>
                <option value="">Select gender</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
              </select>
            </Field>
          </section>

          <section className="adv-panel emphasis-options">
            <h3>Symptoms</h3>
            <YesNo label="Jaundice" value={form.jaundice} onChange={(v) => updateField("jaundice", v)} name="jaundice" />
            <YesNo label="Abdominal pain" value={form.abdominal_pain} onChange={(v) => updateField("abdominal_pain", v)} name="abdominal_pain" />
            <YesNo label="Weight loss" value={form.weight_loss} onChange={(v) => updateField("weight_loss", v)} name="weight_loss" />
            <YesNo label="Fatigue" value={form.fatigue} onChange={(v) => updateField("fatigue", v)} name="fatigue" />
            <YesNo label="Fever" value={form.fever} onChange={(v) => updateField("fever", v)} name="fever" />
          </section>

          <section className="adv-panel emphasis-options">
            <h3>Lab Values</h3>
            <Field label="Bilirubin"><input type="number" min="0" step="any" value={form.bilirubin} onChange={(e) => updateField("bilirubin", e.target.value)} /></Field>
            <Field label="ALT"><input type="number" min="0" step="any" value={form.alt} onChange={(e) => updateField("alt", e.target.value)} /></Field>
            <Field label="AST"><input type="number" min="0" step="any" value={form.ast} onChange={(e) => updateField("ast", e.target.value)} /></Field>
            <Field label="ALP"><input type="number" min="0" step="any" value={form.alp} onChange={(e) => updateField("alp", e.target.value)} /></Field>
            <Field label="CA 19-9"><input type="number" min="0" step="any" value={form.ca19_9} onChange={(e) => updateField("ca19_9", e.target.value)} /></Field>
          </section>

          <section className="adv-panel emphasis-options">
            <h3>Risk Factors</h3>
            <YesNo label="Smoking" value={form.smoking} onChange={(v) => updateField("smoking", v)} name="smoking" />
            <YesNo label="Alcohol" value={form.alcohol} onChange={(v) => updateField("alcohol", v)} name="alcohol" />
            <YesNo label="Diabetes" value={form.diabetes} onChange={(v) => updateField("diabetes", v)} name="diabetes" />
            <YesNo label="Liver disease history" value={form.liver_disease_history} onChange={(v) => updateField("liver_disease_history", v)} name="liver_disease_history" />
            <YesNo label="Gallstones" value={form.gallstones} onChange={(v) => updateField("gallstones", v)} name="gallstones" />
          </section>
        </div>

        {error ? <div className="alert">{error}</div> : null}

        <div className="button-row">
          <button className="btn" type="submit" disabled={loading}>{loading ? "Predicting..." : "Submit Prediction"}</button>
          <button className="btn secondary" type="button" onClick={() => { setForm(initialState); setError(""); setResult(null); }}>Reset</button>
        </div>
      </form>

      {result ? (
        <section className={`adv-result ${riskTheme}`}>
          <h2>Prediction Result: {result.risk_level.toUpperCase()} RISK</h2>
          <p><strong>Patient:</strong> {result.name}</p>
          <p><strong>Probability:</strong> {result.probability_percent}%</p>
          <div className="progress-track">
            <div className={`progress-fill ${riskTheme}`} style={{ width: `${result.probability_percent}%` }}></div>
          </div>
          <p>{result.explanation}</p>
          <a className="btn" href="/report/">Download / Print Report</a>
        </section>
      ) : null}
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("predictApp")).render(<PredictorApp />);
