import React, {useState, useEffect} from 'react';
import axios from 'axios';
import '../Component.css';

const Dashboard = props => {
    const [vulnCount, setVulnCount] = useState(0)
    const [impactfulVulnCount, setImpactfulVulnCount] = useState(0)
    const [impactfulVulnArray, setImpactfulVulnArray] = useState([])
    const thisFqdn = props.thisFqdn;
    const formatUpdated = thisFqdn.updatedAt.replace(/([A-Z])+/g, " ").replace(/(\.[0-9]+)/g, " GMT");
    
    useEffect(()=>{
        axios.post('http://localhost:8000/api/fqdn', {_id:props.thisFqdn._id})
            .then(res=>{
                if (res.data !== null){
                    let tempVulns = [];
                    if (res.data.vulns.length > 1){
                        tempVulns = res.data.vulns;
                    } else {
                        let tempVulnsA = res.data.vulnsSSL;
                        let tempVulnsB = tempVulnsA.concat(res.data.vulnsFile);
                        let tempVulnsC = tempVulnsB.concat(res.data.vulnsDNS);
                        let tempVulnsD = tempVulnsC.concat(res.data.vulnsVulns);
                        let tempVulnsE = tempVulnsD.concat(res.data.vulnsTech);
                        let tempVulnsF = tempVulnsE.concat(res.data.vulnsMisconfig);
                        let tempVulnsG = tempVulnsF.concat(res.data.vulnsCVEs);
                        let tempVulnsH = tempVulnsG.concat(res.data.vulnsCNVD);
                        let tempVulnsI = tempVulnsH.concat(res.data.vulnsExposed);
                        let tempVulnsJ = tempVulnsI.concat(res.data.vulnsExposure);
                        let tempVulnsK = tempVulnsJ.concat(res.data.vulnsMisc);
                        let tempVulnsL = tempVulnsK.concat(res.data.vulnsNetwork);
                        let tempVulnsM = tempVulnsL.concat(res.data.vulnsRs0n);
                        tempVulns = tempVulnsM.concat(res.data.vulnsHeadless);
                    }
                    let vulnCount = 0;
                    let impactfulVulnCount = 0;
                    let tempImpactfulVulnArray = []
                    for (let i=0; i<tempVulns.length; i++){
                        if (tempVulns[i].info.severity !== "foo"){
                            vulnCount++;
                        }
                        if (tempVulns[i].info.severity !== "foo" && tempVulns[i].info.severity !== "info"){
                            impactfulVulnCount++;
                            tempImpactfulVulnArray.push(tempVulns[i])
                        }
                    }
                    setImpactfulVulnArray(tempImpactfulVulnArray)
                    setVulnCount(vulnCount);
                    setImpactfulVulnCount(impactfulVulnCount);
                }
            })
    }, [props])

    console.log(`Impactful Vuln Count: ${impactfulVulnCount} -- Vuln Count: ${vulnCount}`);

    return (
        <div className="bg-secondary dashboard">
            <div className="row pl-5">
                <div className="col-4 mb-4">
                    <h4>FQDN: {thisFqdn.fqdn}</h4>
                </div>
                <div className="col-4 mb-4">
                    {
                        thisFqdn.targetUrls.length > 0 ? <h4>Target URL: {thisFqdn.targetUrls[0]}</h4> : <h4>Target URL: None</h4>
                    }
                </div>
                <div className="col-4 mb-4">
                    <h4>Data Last Updated: {formatUpdated}</h4>
                </div>
            </div>
            <div className="row ml-5 pl-5">
                <div className="col-4">
                    <h4>Subdomain Count:</h4>
                    <ul>
                        <li>amass: {thisFqdn.recon.subdomains.amass.length}</li>
                        <li>assetfinder: {thisFqdn.recon.subdomains.assetfinder.length}</li>
                        <li>ctl: {thisFqdn.recon.subdomains.ctl.length}</li>
                        <li>cloud-ranges: {thisFqdn.recon.subdomains.cloudRanges.length}</li>
                        <li>gau: {thisFqdn.recon.subdomains.gau.length}</li>
                        <li>github-search: {thisFqdn.recon.subdomains.githubSearch.length}</li>
                        <li>gospider: {thisFqdn.recon.subdomains.gospider.length}</li>
                        <li>hakrawler: {thisFqdn.recon.subdomains.hakrawler.length}</li>
                        <li>shosubgo: {thisFqdn.recon.subdomains.shosubgo.length}</li>
                        <li>shuffledns: {thisFqdn.recon.subdomains.shuffledns.length}</li>
                        <li>subdomainizer: {thisFqdn.recon.subdomains.subdomainizer.length}</li>
                        <li>subfinder: {thisFqdn.recon.subdomains.subfinder.length}</li>
                        <li>sublist3r: {thisFqdn.recon.subdomains.sublist3r.length}</li>
                    </ul>
                </div>
                <div className="col-4">
                    <h5>Total Unique Subdomains: {thisFqdn.recon.subdomains.consolidated.length}</h5>
                    <h5>New Unique Subdomains ({thisFqdn.recon.subdomains.consolidatedNew.length}):</h5>
                    <div style={{width: '300px', height: '300px', padding: '5px', border: '1px solid black', overflowY: 'scroll'}}>
                        {
                            thisFqdn.recon.subdomains.consolidatedNew.sort().map((subdomain, i) => {
                                return (
                                    <a style={{display: "block"}} href={subdomain} key={i} target="_blank" rel="noreferrer">{subdomain}</a>
                                )
                            })
                        }
                    </div>
                </div>
                <div className="col-4">
                    <h5>Live Domains: {thisFqdn.recon.subdomains.httprobe.length}</h5>
                    <div style={{width: '300px', height: '300px', padding: '5px', border: '1px solid black', overflowY: 'scroll'}}>
                        {
                            thisFqdn.recon.subdomains.httprobe.sort().map((server, i) => {
                                return (
                                    <div key={i}>
                                    <a href={server} className="m-0 mt-2" target="_blank" rel="noreferrer">{server}</a><br/>
                                    </div>
                                )
                            })
                        }
                    </div>
                </div>
            </div>
            <div className="row ml-5 pl-5">
                <div className="col-4">
                    <h5>Impactful Nuclei Vulns: {impactfulVulnCount}/{vulnCount}</h5>
                    <div style={{width: '300px', height: '300px', padding: '5px', border: '1px solid black', overflowY: 'scroll'}}>
                        {
                            impactfulVulnArray.sort().map((vuln, i) => {
                                return (
                                    <div key={i}>
                                        <ul style={{listStyleType:"none", padding:"0", margin:"0"}}>
                                            <li key={i}>{vuln.info.name} - {vuln.info.severity}</li>
                                        </ul>
                                    </div>
                                )
                            })
                        }
                    </div>
                </div>
                <div className="col-4">
                    <h5>Server IPs: ({thisFqdn.ips.length}):</h5>
                    <div style={{width: '300px', height: '130px', padding: '5px', border: '1px solid black', overflowY: 'scroll'}}>
                        {
                            thisFqdn.ips.sort((a, b) => a.ip - b.ip).map((ip, i) => {
                                return (
                                    <p style={{display: "block", margin: 0}} key={i}>{ip['ip']}</p>
                                )
                            })
                        }
                    </div>
                    <h5>AWS IPs: ({thisFqdn.recon.subdomains.cloudRanges.length}):</h5>
                    <div style={{width: '300px', height: '130px', padding: '5px', border: '1px solid black', overflowY: 'scroll'}}>
                        {
                            thisFqdn.recon.subdomains.cloudRanges.sort().map((subdomain, i) => {
                                return (
                                    <a style={{display: "block"}} href={subdomain} key={i} target="_blank" rel="noreferrer">{subdomain}</a>
                                )
                            })
                        }
                    </div>
                </div>
                <div className="col-4">
                    <h5>Servers/Ports: {thisFqdn.recon.subdomains.masscan.length}</h5>
                    <div style={{width: '300px', height: '300px', padding: '5px', border: '1px solid black', overflowY: 'scroll'}}>
                        {
                            thisFqdn.recon.subdomains.masscanAdded.sort().map((server, i) => {
                                return (
                                    <div key={i}>
                                    <a href={"http://"+server} className="m-0 mt-2" target="_blank" rel="noreferrer">{server}</a><br/>
                                    </div>
                                )
                            })
                        }
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Dashboard;