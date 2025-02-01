import React from "react";

function Result({ result }) {
  return (
    <div>
      <h2>Analysis Result</h2>
      <h3>Key Phrases:</h3>
      <ul>
        {result.key_phrases.map((phrase, index) => (
          <li key={index}>{phrase}</li>
        ))}
      </ul>
      <h3>Improved Resume:</h3>
      <pre>{result.improved_resume}</pre>
      <button onClick={() => window.location.reload()}>Back</button>
    </div>
  );
}

export default Result;