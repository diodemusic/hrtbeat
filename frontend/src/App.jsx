import { useState } from "react";
import "./App.css";

function App() {
  const [url, setUrl] = useState("");

  async function watchNewSite() {
    const response = await fetch("http://127.0.0.1:8000/site-watch", {
      method: "POST",
      body: JSON.stringify({ url: url }),
      headers: { "Content-Type": "application/json" }
    });
    setUrl("");
    console.log(response);
  }

  return (
    <>
      <div>
        <h1>hellor</h1>
      </div>
      <div>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
        <button type="submit" onClick={watchNewSite}>
          Add Site
        </button>
      </div>
    </>
  );
}

export default App;
