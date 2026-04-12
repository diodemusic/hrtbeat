import { useState } from "react";

function AddCard() {
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
    )
}

export default AddCard;
