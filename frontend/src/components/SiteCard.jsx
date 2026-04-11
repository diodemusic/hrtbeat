function SiteCard({ site }) {
    return (
        <li className="border border-neutral-800 rounded-lg p-6 bg-neutral-900 mb-4">
            <div className="flex justify-between items-center">
                <span className="text-lg font-medium">{site.url}</span>
                <span className="text-sm text-neutral-400">{site.pings[0]?.latency}ms</span>

                {/* <div>Status: {site.status}</div> */}

            </div>
        </li>
    )
}

export default SiteCard;
