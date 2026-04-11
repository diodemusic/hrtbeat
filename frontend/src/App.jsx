import { useEffect, useState } from "react";
import "./App.css";
import SiteCard from "./components/SiteCard"

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
      <div className="max-w-2xl mx-auto px-6 py-16">
        <header className="mb-12">
          <h1 className="text-4xl font-bold tracking-tight mb-1">hrtbeat</h1>
          <p className="text-sm text-neutral-400">uptime monitoring</p>
        </header>

        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />

        <button type="submit" onClick={watchNewSite}>
          Add Site
        </button>

        <ul className="list-none p-0">
          {sites.map((site) =>
            <SiteCard key={site.id} site={site} />
          )}
        </ul>
      </div>
    </>
  );
}

export default App;
