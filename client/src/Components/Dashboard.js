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
                    <h4>FQDN: <a href={"https://" + thisFqdn.fqdn}>{thisFqdn.fqdn}</a></h4>
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
                <div className="col-3">
                    <h4>Subdomain Count</h4>
                    <ul style={{listStyleType:"none", padding:"0", margin:"0"}}>
                        <li style={{paddingTop:"10px", paddingBottom:"10px", fontSize:"20px", fontWeight:"bold"}}>Amass: {thisFqdn.recon.subdomains.amass.length}</li>
                        <h5 style={{paddingTop:"10px", fontWeight:"600"}}>Web Scraping</h5>
                        <li>Sublist3r: {thisFqdn.recon.subdomains.sublist3r.length}</li>
                        <li>Assetfinder: {thisFqdn.recon.subdomains.assetfinder.length}</li>
                        <li>GetAllUrls (GAU): {thisFqdn.recon.subdomains.gau.length}</li>
                        <li>Certificate Transparency Logs (CTL): {thisFqdn.recon.subdomains.ctl.length}</li>
                        <li>Subfinder: {thisFqdn.recon.subdomains.subfinder.length}</li>
                        <h5 style={{paddingTop:"10px", fontWeight:"600"}}>Brute Force</h5>
                        <li>ShuffleDNS Standard: {thisFqdn.recon.subdomains.shuffledns.length}</li>
                        <li>ShuffleDNS CeWL: {thisFqdn.recon.subdomains.shufflednsCustom.length}</li>
                        <h5 style={{paddingTop:"10px", fontWeight:"600"}}>Link & JavaScript Discovery</h5>
                        <li>GoSpider: {thisFqdn.recon.subdomains.gospider.length}</li>
                        <li>Subdomainizer: {thisFqdn.recon.subdomains.subdomainizer.length}</li>
                        <h5 style={{paddingTop:"10px", fontWeight:"600"}}>Favicon & Marketing</h5>
                    </ul>
                </div>
                <div className="col-4">
                    <h5>Subdomains (New: {thisFqdn.recon.subdomains.consolidatedNew.length}/{thisFqdn.recon.subdomains.consolidated.length})</h5>
                    <div style={{width: '400px', height: '500px', padding: '5px', border: '1px solid black', overflowY: 'scroll'}}>
                        {
                            thisFqdn.recon.subdomains.consolidated.sort().map((subdomain, i) => {
                                return (
                                    thisFqdn.recon.subdomains.consolidatedNew.includes(subdomain) ?
                                    <a style={{display: "block", color: "red"}} href={"https://" + subdomain} key={i} target="_blank" rel="noreferrer">{subdomain}</a> :
                                    <a style={{display: "block"}} href={"https://" + subdomain} key={i} target="_blank" rel="noreferrer">{subdomain}</a>
                                )
                            })
                        }
                    </div>
                </div>
                <div className="col-4 ml-5">
                    <h5>Live URLs: (New: {thisFqdn.recon.subdomains.httprobeAdded.length}/{thisFqdn.recon.subdomains.httprobe.length})</h5>
                    <div style={{width: '400px', height: '500px', padding: '5px', border: '1px solid black', overflowY: 'scroll'}}>
                        {
                            thisFqdn.recon.subdomains.httprobe.sort().map((server, i) => {
                                return (
                                        thisFqdn.recon.subdomains.httprobeAdded.includes(server) ?
                                        <a style={{display: "block", color: "red"}} key={i} href={server} target="_blank" rel="noreferrer">{server}</a> :
                                        <a style={{display: "block"}} key={i} href={server} target="_blank" rel="noreferrer">{server}</a>
                                )
                            })
                        }
                    </div>
                </div>
            </div>
            <div className="row ml-5 pl-5">
            <div className="col-12 mt-3">
                    <h5>Infrastructure Map</h5>
                    <div style={{width: '1500px', height: '600px', padding: '5px', border: '1px solid black', overflowY: 'scroll'}}>
                        {
                            thisFqdn.asns.sort().map((record, i) => {
                                return (
                                    <div key={i}>
                                        <ul style={{listStyleType:"none", padding:"0", margin:"0"}}>
                                            <li key={i}>{record}
                                                <ul style={{listStyleType:"none", padding:"0", margin:"0"}}>
                                                    {
                                                        thisFqdn.subnets.sort().filter(subnet => subnet.includes(record.split(" ")[5])).map((subnet, j) => (
                                                            <li style={{paddingLeft:"100px"}} key={j}>{subnet}
                                                                <ul style={{listStyleType:"none", padding:"0", margin:"0"}}>
                                                                    {
                                                                        thisFqdn.dns.arecord.concat(thisFqdn.dns.aaaarecord).sort().filter(tempRecord => tempRecord.split(" ")[5] === subnet.split(" ")[5]).map((tempRecord, k) => (
                                                                            <li style={{paddingLeft:"100px"}} key={k}>{tempRecord} --- LINK: <a href={"https://" + tempRecord.split(" ")[0]} target="_blank" rel="noreferrer">{"https://" + tempRecord.split(" ")[0]}</a></li>
                                                                        ))
                                                                    }
                                                                </ul>
                                                            </li>
                                                        ))
                                                    }
                                                </ul>
                                                <br></br>
                                            </li>
                                        </ul>
                                    </div>
                                )
                            })
                        }
                    </div>
                </div>
            </div>
            <div className="row ml-5 pl-5">
                <div className="col-12 mt-3">
                    <h5>DNS Records</h5>
                    <div style={{width: '1500px', height: '300px', padding: '5px', border: '1px solid black', overflowY: 'scroll'}}>
                        {
                            thisFqdn.dns.cnamerecord.sort().map((record, i) => {
                                return (
                                    <div key={i}>
                                        <ul style={{listStyleType:"none", padding:"0", margin:"0"}}>
                                            <li key={i}><a href={"https://" + record.split(" ")[0]} target="_blank" rel="noreferrer">{record.split(" ")[0]} </a>{record.replace(record.split(" ")[0], '').replace(record.split(" ")[5], '')}<a href={"https://" + record.split(" ")[5]} target="_blank" rel="noreferrer"> {record.split(" ")[5]}</a></li>
                                        </ul>
                                    </div>
                                )
                            })
                        }
                        {
                            thisFqdn.dns.node.sort().map((record, i) => {
                                return (
                                    <div key={i}>
                                        <ul style={{listStyleType:"none", padding:"0", margin:"0"}}>
                                        <li key={i}><a href={"https://" + record.split(" ")[0]} target="_blank" rel="noreferrer">{record.split(" ")[0]} </a>{record.replace(record.split(" ")[0], '').replace(record.split(" ")[5], '')}<a href={"https://" + record.split(" ")[5]} target="_blank" rel="noreferrer"> {record.split(" ")[5]}</a></li>
                                        </ul>
                                    </div>
                                )
                            })
                        }
                        {
                            thisFqdn.dns.arecord.sort().map((record, i) => {
                                return (
                                    <div key={i}>
                                        <ul style={{listStyleType:"none", padding:"0", margin:"0"}}>
                                        <li key={i}><a href={"https://" + record.split(" ")[0]} target="_blank" rel="noreferrer">{record.split(" ")[0]} </a>{record.replace(record.split(" ")[0], '').replace(record.split(" ")[5], '')}<a href={"https://" + record.split(" ")[5]} target="_blank" rel="noreferrer"> {record.split(" ")[5]}</a></li>
                                        </ul>
                                    </div>
                                )
                            })
                        }
                                                {
                            thisFqdn.dns.aaaarecord.sort().map((record, i) => {
                                return (
                                    <div key={i}>
                                        <ul style={{listStyleType:"none", padding:"0", margin:"0"}}>
                                        <li key={i}><a href={"https://" + record.split(" ")[0]} target="_blank" rel="noreferrer">{record.split(" ")[0]} </a>{record.replace(record.split(" ")[0], '').replace(record.split(" ")[5], '')}<a href={"https://" + record.split(" ")[5]} target="_blank" rel="noreferrer"> {record.split(" ")[5]}</a></li>
                                        </ul>
                                    </div>
                                )
                            })
                        }
                                                {
                            thisFqdn.dns.mxrecord.sort().map((record, i) => {
                                return (
                                    <div key={i}>
                                        <ul style={{listStyleType:"none", padding:"0", margin:"0"}}>
                                        <li key={i}><a href={"https://" + record.split(" ")[0]} target="_blank" rel="noreferrer">{record.split(" ")[0]} </a>{record.replace(record.split(" ")[0], '').replace(record.split(" ")[5], '')}<a href={"https://" + record.split(" ")[5]} target="_blank" rel="noreferrer"> {record.split(" ")[5]}</a></li>
                                        </ul>
                                    </div>
                                )
                            })
                        }
                        {
                            thisFqdn.dns.nsrecord.sort().map((record, i) => {
                                return (
                                    <div key={i}>
                                        <ul style={{listStyleType:"none", padding:"0", margin:"0"}}>
                                        <li key={i}><a href={"https://" + record.split(" ")[0]} target="_blank" rel="noreferrer">{record.split(" ")[0]} </a>{record.replace(record.split(" ")[0], '').replace(record.split(" ")[5], '')}<a href={"https://" + record.split(" ")[5]} target="_blank" rel="noreferrer"> {record.split(" ")[5]}</a></li>
                                        </ul>
                                    </div>
                                )
                            })
                        }
                        {
                            thisFqdn.dns.ptrrecord.sort().map((record, i) => {
                                return (
                                    <div key={i}>
                                        <ul style={{listStyleType:"none", padding:"0", margin:"0"}}>
                                        <li key={i}><a href={"https://" + record.split(" ")[0]} target="_blank" rel="noreferrer">{record.split(" ")[0]} </a>{record.replace(record.split(" ")[0], '').replace(record.split(" ")[5], '')}<a href={"https://" + record.split(" ")[5]} target="_blank" rel="noreferrer"> {record.split(" ")[5]}</a></li>
                                        </ul>
                                    </div>
                                )
                            })
                        }
                        {
                            thisFqdn.dns.soarecord.sort().map((record, i) => {
                                return (
                                    <div key={i}>
                                        <ul style={{listStyleType:"none", padding:"0", margin:"0"}}>
                                        <li key={i}><a href={"https://" + record.split(" ")[0]} target="_blank" rel="noreferrer">{record.split(" ")[0]} </a>{record.replace(record.split(" ")[0], '').replace(record.split(" ")[5], '')}<a href={"https://" + record.split(" ")[5]} target="_blank" rel="noreferrer"> {record.split(" ")[5]}</a></li>
                                        </ul>
                                    </div>
                                )
                            })
                        }
                        {
                            thisFqdn.dns.spfrecord.sort().map((record, i) => {
                                return (
                                    <div key={i}>
                                        <ul style={{listStyleType:"none", padding:"0", margin:"0"}}>
                                        <li key={i}><a href={"https://" + record.split(" ")[0]} target="_blank" rel="noreferrer">{record.split(" ")[0]} </a>{record.replace(record.split(" ")[0], '').replace(record.split(" ")[5], '')}<a href={"https://" + record.split(" ")[5]} target="_blank" rel="noreferrer"> {record.split(" ")[5]}</a></li>
                                        </ul>
                                    </div>
                                )
                            })
                        }
                        {
                            thisFqdn.dns.srvrecord.sort().map((record, i) => {
                                return (
                                    <div key={i}>
                                        <ul style={{listStyleType:"none", padding:"0", margin:"0"}}>
                                        <li key={i}><a href={"https://" + record.split(" ")[0]} target="_blank" rel="noreferrer">{record.split(" ")[0]} </a>{record.replace(record.split(" ")[0], '').replace(record.split(" ")[5], '')}<a href={"https://" + record.split(" ")[5]} target="_blank" rel="noreferrer"> {record.split(" ")[5]}</a></li>
                                        </ul>
                                    </div>
                                )
                            })
                        }
                        {
                            thisFqdn.dns.txtrecord.sort().map((record, i) => {
                                return (
                                    <div key={i}>
                                        <ul style={{listStyleType:"none", padding:"0", margin:"0"}}>
                                        <li key={i}><a href={"https://" + record.split(" ")[0]} target="_blank" rel="noreferrer">{record.split(" ")[0]} </a>{record.replace(record.split(" ")[0], '').replace(record.split(" ")[5], '')}<a href={"https://" + record.split(" ")[5]} target="_blank" rel="noreferrer"> {record.split(" ")[5]}</a></li>
                                        </ul>
                                    </div>
                                )
                            })
                        }
                    </div>
                </div>
            </div>
        <div className="row ml-5 pl-5">
            <div className="col-12 mt-3">
                <h5>Impactful Nuclei Vulns: {impactfulVulnCount}/{vulnCount}</h5>
                <div style={{width: '1500px', height: '300px', padding: '5px', border: '1px solid black', overflowY: 'scroll', overflowX: 'hidden'}}>
                    {
                        impactfulVulnArray.sort().map((vuln, i) => {
                            return (
                                <div key={i}>
                                    <ul style={{listStyleType:"none", padding:"0", margin:"0"}}>
                                        <li key={i}>{vuln.info.name} --{'>'} <a href={"https://" + vuln.host} target="_blank" rel="noreferrer">{vuln.host}</a> ({vuln.info.severity.toUpperCase()}) --- Evidence: <a href={"https://" + vuln['matched-at']} target="_blank" rel="noreferrer">{vuln['matched-at']}</a> ({vuln.ip})</li>
                                    </ul>
                                </div>
                            )
                        })
                    }
                </div>
                </div>
            </div>
            <div className="row ml-5 pl-5">
            <div className="col-6 mt-3">
                    <h5>ASNs</h5>
                    <div style={{width: '600px', height: '300px', padding: '5px', border: '1px solid black', overflowY: 'scroll'}}>
                        {
                            thisFqdn.asns.sort().map((record, i) => {
                                return (
                                    <div key={i}>
                                        <ul style={{listStyleType:"none", padding:"0", margin:"0"}}>
                                            <li key={i}>{record}</li>
                                        </ul>
                                    </div>
                                )
                            })
                        }
                    </div>
                </div>
                <div className="col-6 mt-3">
                    <h5>Subnets</h5>
                    <div style={{width: '600px', height: '300px', padding: '5px', border: '1px solid black', overflowY: 'scroll'}}>
                        {
                            thisFqdn.subnets.sort().map((record, i) => {
                                return (
                                    <div key={i}>
                                        <ul style={{listStyleType:"none", padding:"0", margin:"0"}}>
                                            <li key={i}>{record}</li>
                                        </ul>
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