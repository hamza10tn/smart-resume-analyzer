import React, { useState } from "react";

function ResumeForm({ onAnalyze }) {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    onAnalyze(resumeFile, jobDescription);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="resume">Upload Resume (PDF or Text):</label>
        <input
          type="file"
          id="resume"
          onChange={(e) => setResumeFile(e.target.files[0])}
          required
        />
      </div>
      <div>
        <label htmlFor="job_description">Paste Job Description:</label>
        <textarea
          id="job_description"
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          required
        />
      </div>
      <button type="submit">Analyze Resume</button>
    </form>
  );
}

export default ResumeForm;