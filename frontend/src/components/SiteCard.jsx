function SiteCard({ site }) {
    return (
        <li className="border border-neutral-800 rounded-lg p-6 bg-neutral-900 mb-4">
            <div className="flex justify-between items-center">
                <span className="text-lg font-medium">{site.url}</span>
                <span className="text-sm text-neutral-400">{site.pings[0]?.latency}ms</span>

            </div>

            <div className="flex gap-1 mt-4">
                {site.pings.slice(0, 30).reverse().map((ping) => (
                    <div key={ping.timestamp} className={`flex-1 h-6 rounded-sm ${ping.status === "healthy" ? "bg-green-500" : "bg-red-500"}`} />
                ))}
            </div>
        </li >
    )
}

export default SiteCard;
