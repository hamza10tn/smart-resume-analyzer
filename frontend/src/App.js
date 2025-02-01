import React, { useState } from "react";
import ResumeForm from "./ResumeForm";
import Result from "./Result";

function App() {
  const [result, setResult] = useState(null);

  const handleAnalyze = async (resumeFile, jobDescription) => {
    const formData = new FormData();
    formData.append("resume", resumeFile);
    formData.append("job_description", jobDescription);

    const response = await fetch("http://localhost:5000/analyze", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    setResult(data);
  };

  return (
    <div className="App">
      <h1>AI-Powered Resume Analyzer</h1>
      {!result ? (
        <ResumeForm onAnalyze={handleAnalyze} />
      ) : (
        <Result result={result} />
      )}
    </div>
  );
}

export default App;