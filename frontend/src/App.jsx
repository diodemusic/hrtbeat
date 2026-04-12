import { useEffect, useState } from "react";
import "./App.css";
import SiteCard from "./components/SiteCard"
import AddCard from "./components/AddSite";
import Header from "./components/Header";

function App() {
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

  return (
    <>
      <div className="max-w-2xl mx-auto px-6 py-16">
        <Header />

        <AddCard />

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
