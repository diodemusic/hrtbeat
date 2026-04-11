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
          <h1 className="text-4xl font-bold tracking-tight mb-1">uptide</h1>
          <p className="text-sm text-neutral-400">uptime monitoring</p>
        </header>

        <div className="flex gap-2 mb-8">
          <input
            className="flex-1 bg-neutral-900 border border-neutral-800 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-neutral-600"
            type="text"
            placeholder="example.com"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />

          <button className="bg-white text-black px-4 py-2 rounded-md font-medium hover:bg-neutral-200 cursor-pointer" type="submit" onClick={watchNewSite}>
            Add Site
          </button>
        </div>

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
