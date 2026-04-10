import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [url, setUrl] = useState("");
  const [sites, setSites] = useState([]);

  useEffect(() => {
    async function loadSites() {
      const response = await fetch("http://127.0.0.1:8000/site-watches", {
        method: "GET"
      });

      return response.json()
    };

    const site_watches = loadSites();
    site_watches.then((s) => { setSites(s) });
  }, []);

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
        <h1>hrtbeat</h1>
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
        <ul>
          {sites.map((site) => (
            <li key={site.id} className="site-watch-list">
              <div>URL: {site.url}</div>
              <div>Status: {site.status}</div>
              <div>Ping: {site.pings[0]?.latency}</div>
            </li>
          )
          )}
        </ul>
      </div>
    </>
  );
}

export default App;
