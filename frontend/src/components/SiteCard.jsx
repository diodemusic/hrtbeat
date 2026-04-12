function SiteCard({ site }) {
    const pingCount = site.pings.length;
    const placeholderPingCount = Math.max(0, 30 - pingCount);
    const placeholderPings = Array.from({ length: placeholderPingCount }, (_, i) => ({ placeholder: true }))
    const pings = [...placeholderPings, ...site.pings.slice(0, 30).reverse()]

    function getPingColor(ping) {
        if (ping.placeholder) return "bg-neutral-800"
        if (ping.status === "healthy") return "bg-green-500"
        if (ping.status === "down") return "bg-red-500"

        return "bg-neutral-800"
    }

    return (
        <li className="border border-neutral-800 rounded-lg p-6 bg-neutral-900 mb-4">
            <div className="flex justify-between items-center">
                <span className="text-lg font-medium">{site.url}</span>
                <span className="text-sm text-neutral-400">{site.pings[0]?.latency}ms</span>

            </div>

            <div className="flex gap-1 mt-4">
                {pings.map((ping, index) => (
                    <div key={ping.placeholder ? `placeholder-${index}` : ping.timestamp} className={`flex-1 h-6 rounded-sm ${getPingColor(ping)}`} />
                ))}
            </div>
        </li >
    )
}

export default SiteCard;
