import React, {useState, useEffect} from 'react';
import axios from 'axios';
import '../Component.css';
import NucleiScansFull from './SubComponents/NucleiScansFull';
import NucleiScansSSL from './SubComponents/NucleiScansSSL';
import NucleiScansFile from './SubComponents/NucleiScansFile';
import NucleiScansDNS from './SubComponents/NucleiScansDNS';
import NucleiScansVulns from './SubComponents/NucleiScansVulns';
import NucleiScansTech from './SubComponents/NucleiScansTech';
import NucleiScansMisconfigs from './SubComponents/NucleiScansMisconfigs';
import NucleiScansCVEs from './SubComponents/NucleiScansCVEs';
import NucleiScansCNVD from './SubComponents/NucleiScansCNVD';
import NucleiScansExposed from './SubComponents/NucleiScansExposed';
import NucleiScansExposure from './SubComponents/NucleiScansExposure';
import NucleiScansMisc from './SubComponents/NucleiScansMisc';
import NucleiScansNetwork from './SubComponents/NucleiScansNetwork';
import NucleiScansRs0n from './SubComponents/NucleiScansRs0n';
import NucleiScansHeadless from './SubComponents/NucleiScansHeadless';



const CveTesting = props => {
    const [currentStep, setCurrentStep] = useState(0);
    const [impactfulVulnCount, setImpactfulVulnCount] = useState(0)
    const [impactfulVulnCountSSL, setImpactfulVulnCountSSL] = useState(0)
    const [impactfulVulnCountFile, setImpactfulVulnCountFile] = useState(0)
    const [impactfulVulnCountDNS, setImpactfulVulnCountDNS] = useState(0)
    const [impactfulVulnCountVulns, setImpactfulVulnCountVulns] = useState(0)
    const [impactfulVulnCountTech, setImpactfulVulnCountTech] = useState(0)
    const [impactfulVulnCountMisconfig, setImpactfulVulnCountMisconfig] = useState(0)
    const [impactfulVulnCountCVEs, setImpactfulVulnCountCVEs] = useState(0)
    const [impactfulVulnCountCNVD, setImpactfulVulnCountCNVD] = useState(0)
    const [impactfulVulnCountExposed, setImpactfulVulnCountExposed] = useState(0)
    const [impactfulVulnCountExposure, setImpactfulVulnCountExposure] = useState(0)
    const [impactfulVulnCountMisc, setImpactfulVulnCountMisc] = useState(0)
    const [impactfulVulnCountNetwork, setImpactfulVulnCountNetwork] = useState(0)
    const [impactfulVulnCountRs0n, setImpactfulVulnCountRs0n] = useState(0)
    const [impactfulVulnCountHeadless, setImpactfulVulnCountHeadless] = useState(0)
    const [impactfulVulnFoundCount, setImpactfulVulnFoundCount] = useState(false)
    const [impactfulVulnFoundSSL, setImpactfulVulnFoundSSL] = useState(false)
    const [impactfulVulnFoundFile, setImpactfulVulnFoundFile] = useState(false)
    const [impactfulVulnFoundDNS, setImpactfulVulnFoundDNS] = useState(false)
    const [impactfulVulnFoundVulns, setImpactfulVulnFoundVulns] = useState(false)
    const [impactfulVulnFoundTech, setImpactfulVulnFoundTech] = useState(false)
    const [impactfulVulnFoundMisconfig, setImpactfulVulnFoundMisconfig] = useState(false)
    const [impactfulVulnFoundCVEs, setImpactfulVulnFoundCVEs] = useState(false)
    const [impactfulVulnFoundCNVD, setImpactfulVulnFoundCNVD] = useState(false)
    const [impactfulVulnFoundExposed, setImpactfulVulnFoundExposed] = useState(false)
    const [impactfulVulnFoundExposure, setImpactfulVulnFoundExposure] = useState(false)
    const [impactfulVulnFoundMisc, setImpactfulVulnFoundMisc] = useState(false)
    const [impactfulVulnFoundNetwork, setImpactfulVulnFoundNetwork] = useState(false)
    const [impactfulVulnFoundRs0n, setImpactfulVulnFoundRs0n] = useState(false)
    const [impactfulVulnFoundHeadless, setImpactfulVulnFoundHeadless] = useState(false)

    useEffect(()=>{
        axios.post('http://localhost:8000/api/fqdn', {_id:props.thisFqdn._id})
            .then(res=>{
                if (res.data !== null){
                    let counter = 0;
                    for (let i=0; i<res.data.vulns.length; i++){
                        if (res.data.vulns[i].info.severity !== "foo"){
                            counter++;
                        }
                    }
                    if (counter === 1){
                        counter = 0;
                    }
                    setImpactfulVulnCount(counter);
                    let counterSSL = 0;
                    for (let i=0; i<res.data.vulnsSSL.length; i++){
                        // console.log(res.data.vulnsSSL[i].info.severity)
                        if (res.data.vulnsSSL[i].info.severity !== "foo"){
                            counterSSL++;
                        }
                        if (res.data.vulnsSSL[i].info.severity !== "foo" && res.data.vulnsSSL[i].info.severity !== "info"){
                            console.log(res.data.vulnsSSL[i].info.severity)
                            setImpactfulVulnFoundSSL(true);
                        }
                    }
                    setImpactfulVulnCountSSL(counterSSL);
                    let counterFile = 0;
                    for (let i=0; i<res.data.vulnsFile.length; i++){
                        if (res.data.vulnsFile[i].info.severity !== "foo"){
                            counterFile++;
                        }
                        if (res.data.vulnsFile[i].info.severity !== "foo" && res.data.vulnsFile[i].info.severity !== "info"){
                            console.log(res.data.vulnsFile[i].info.severity)
                            setImpactfulVulnFoundFile(true);
                        }
                    }
                    setImpactfulVulnCountFile(counterFile);
                    let counterDNS = 0;
                    for (let i=0; i<res.data.vulnsDNS.length; i++){
                        if (res.data.vulnsDNS[i].info.severity !== "foo"){
                            counterDNS++;
                        }
                        if (res.data.vulnsDNS[i].info.severity !== "foo" && res.data.vulnsDNS[i].info.severity !== "info"){
                            console.log(res.data.vulnsDNS[i].info.severity)
                            setImpactfulVulnFoundDNS(true);
                        }
                    }
                    setImpactfulVulnCountDNS(counterDNS);
                    let counterVulns = 0;
                    for (let i=0; i<res.data.vulnsVulns.length; i++){
                        if (res.data.vulnsVulns[i].info.severity !== "foo"){
                            counterVulns++;
                        }
                        if (res.data.vulnsVulns[i].info.severity !== "foo" && res.data.vulnsVulns[i].info.severity !== "info"){
                            console.log(res.data.vulnsVulns[i].info.severity)
                            setImpactfulVulnFoundVulns(true);
                        }
                    }
                    setImpactfulVulnCountVulns(counterVulns);
                    let counterTech = 0;
                    for (let i=0; i<res.data.vulnsTech.length; i++){
                        if (res.data.vulnsTech[i].info.severity !== "foo"){
                            counterTech++;
                        }
                        if (res.data.vulnsTech[i].info.severity !== "foo" && res.data.vulnsTech[i].info.severity !== "info"){
                            console.log(res.data.vulnsTech[i].info.severity)
                            setImpactfulVulnFoundTech(true);
                        }
                    }
                    setImpactfulVulnCountTech(counterTech);
                    let counterMisconfig = 0;
                    for (let i=0; i<res.data.vulnsMisconfig.length; i++){
                        if (res.data.vulnsMisconfig[i].info.severity !== "foo"){
                            counterMisconfig++;
                        }
                        if (res.data.vulnsMisconfig[i].info.severity !== "foo" && res.data.vulnsMisconfig[i].info.severity !== "info"){
                            console.log(res.data.vulnsMisconfig[i].info.severity)
                            setImpactfulVulnFoundMisconfig(true);
                        }
                    }
                    setImpactfulVulnCountMisconfig(counterMisconfig);
                    let counterCVEs = 0;
                    for (let i=0; i<res.data.vulnsCVEs.length; i++){
                        if (res.data.vulnsCVEs[i].info.severity !== "foo"){
                            counterCVEs++;
                        }
                        if (res.data.vulnsCVEs[i].info.severity !== "foo" && res.data.vulnsCVEs[i].info.severity !== "info"){
                            console.log(res.data.vulnsCVEs[i].info.severity)
                            setImpactfulVulnFoundCVEs(true);
                        }
                    }
                    setImpactfulVulnCountCVEs(counterCVEs);
                    let counterCNVD = 0;
                    for (let i=0; i<res.data.vulnsCNVD.length; i++){
                        if (res.data.vulnsCNVD[i].info.severity !== "foo"){
                            counterCNVD++;
                        }
                        if (res.data.vulnsCNVD[i].info.severity !== "foo" && res.data.vulnsCNVD[i].info.severity !== "info"){
                            console.log(res.data.vulnsCNVD[i].info.severity)
                            setImpactfulVulnFoundCNVD(true);
                        }
                    }
                    setImpactfulVulnCountCNVD(counterCNVD);
                    let counterExposed = 0;
                    for (let i=0; i<res.data.vulnsExposed.length; i++){
                        if (res.data.vulnsExposed[i].info.severity !== "foo"){
                            counterExposed++;
                        }
                        if (res.data.vulnsExposed[i].info.severity !== "foo" && res.data.vulnsExposed[i].info.severity !== "info"){
                            console.log(res.data.vulnsExposed[i].info.severity)
                            setImpactfulVulnFoundExposed(true);
                        }
                    }
                    setImpactfulVulnCountExposed(counterExposed);
                    let counterExposure = 0;
                    for (let i=0; i<res.data.vulnsExposure.length; i++){
                        if (res.data.vulnsExposure[i].info.severity !== "foo"){
                            counterExposure++;
                        }
                        if (res.data.vulnsExposure[i].info.severity !== "foo" && res.data.vulnsExposure[i].info.severity !== "info"){
                            console.log(res.data.vulnsExposure[i].info.severity)
                            setImpactfulVulnFoundExposure(true);
                        }
                    }
                    setImpactfulVulnCountExposure(counterExposure);
                    let counterMisc = 0;
                    for (let i=0; i<res.data.vulnsMisc.length; i++){
                        if (res.data.vulnsMisc[i].info.severity !== "foo"){
                            counterMisc++;
                        }
                        if (res.data.vulnsMisc[i].info.severity !== "foo" && res.data.vulnsMisc[i].info.severity !== "info"){
                            console.log(res.data.vulnsMisc[i].info.severity)
                            setImpactfulVulnFoundMisc(true);
                        }
                    }
                    setImpactfulVulnCountMisc(counterMisc);
                    let counterNetwork = 0;
                    for (let i=0; i<res.data.vulnsNetwork.length; i++){
                        if (res.data.vulnsNetwork[i].info.severity !== "foo"){
                            counterNetwork++;
                        }
                        if (res.data.vulnsNetwork[i].info.severity !== "foo" && res.data.vulnsNetwork[i].info.severity !== "info"){
                            console.log(res.data.vulnsNetwork[i].info.severity)
                            setImpactfulVulnFoundNetwork(true);
                        }
                    }
                    setImpactfulVulnCountNetwork(counterNetwork);
                    let counterRs0n = 0;
                    for (let i=0; i<res.data.vulnsRs0n.length; i++){
                        if (res.data.vulnsRs0n[i].info.severity !== "foo"){
                            counterRs0n++;
                        }
                        if (res.data.vulnsRs0n[i].info.severity !== "foo" && res.data.vulnsRs0n[i].info.severity !== "info"){
                            console.log(res.data.vulnsRs0n[i].info.severity)
                            setImpactfulVulnFoundRs0n(true);
                        }
                    }
                    setImpactfulVulnCountRs0n(counterRs0n);
                    let counterHeadless = 0;
                    for (let i=0; i<res.data.vulnsHeadless.length; i++){
                        if (res.data.vulnsHeadless[i].info.severity !== "foo"){
                            counterHeadless++;
                        }
                        if (res.data.vulnsHeadless[i].info.severity !== "foo" && res.data.vulnsHeadless[i].info.severity !== "info"){
                            console.log(res.data.vulnsHeadless[i].info.severity)
                            setImpactfulVulnFoundHeadless(true);
                        }
                    }
                    setImpactfulVulnCountHeadless(counterHeadless);
                }
            })
    }, [props])

    return (
        <div className="container-fluid">
        <div className="row">
        <div className="bg-secondary checklistStyle pt-4 ml-4 col-3">
            <ul>
                <li>Third-Party Scanning</li>
                <ul>
                    <li onClick={(e)=>setCurrentStep(0)}>Nuclei Scan Results -- Full (Vuln Count: {impactfulVulnCount})</li>
                    {
                        impactfulVulnFoundSSL ?
                        <li style={{color:"red"}} onClick={(e)=>setCurrentStep(1)}>Nuclei Scan Results -- SSL (Vuln Count: {impactfulVulnCountSSL})</li> :
                        <li onClick={(e)=>setCurrentStep(1)}>Nuclei Scan Results -- SSL (Vuln Count: {impactfulVulnCountSSL})</li> 
                    }
                    {
                        impactfulVulnFoundFile ?
                        <li style={{color:"red"}} onClick={(e)=>setCurrentStep(2)}>Nuclei Scan Results -- File (Vuln Count: {impactfulVulnCountFile})</li> :
                        <li onClick={(e)=>setCurrentStep(2)}>Nuclei Scan Results -- File (Vuln Count: {impactfulVulnCountFile})</li>
                    }
                    {
                        impactfulVulnFoundDNS ?
                        <li style={{color:"red"}} onClick={(e)=>setCurrentStep(3)}>Nuclei Scan Results -- DNS (Vuln Count: {impactfulVulnCountDNS})</li> :
                        <li onClick={(e)=>setCurrentStep(3)}>Nuclei Scan Results -- DNS (Vuln Count: {impactfulVulnCountDNS})</li>
                    }
                    {
                        impactfulVulnFoundVulns ?
                        <li style={{color:"red"}} onClick={(e)=>setCurrentStep(4)}>Nuclei Scan Results -- Vulns (Vuln Count: {impactfulVulnCountVulns})</li> :
                        <li onClick={(e)=>setCurrentStep(4)}>Nuclei Scan Results -- Vulns (Vuln Count: {impactfulVulnCountVulns})</li>
                    }
                    {
                        impactfulVulnFoundTech ?
                        <li style={{color:"red"}} onClick={(e)=>setCurrentStep(5)}>Nuclei Scan Results -- Tech (Vuln Count: {impactfulVulnCountTech})</li> :
                        <li onClick={(e)=>setCurrentStep(5)}>Nuclei Scan Results -- Tech (Vuln Count: {impactfulVulnCountTech})</li>
                    }
                    {
                        impactfulVulnFoundMisconfig ?
                        <li style={{color:"red"}} onClick={(e)=>setCurrentStep(6)}>Nuclei Scan Results -- Misconfigs (Vuln Count: {impactfulVulnCountMisconfig})</li> :
                        <li onClick={(e)=>setCurrentStep(6)}>Nuclei Scan Results -- Misconfigs (Vuln Count: {impactfulVulnCountMisconfig})</li>
                    }
                    {
                        impactfulVulnFoundCVEs ?
                        <li style={{color:"red"}} onClick={(e)=>setCurrentStep(7)}>Nuclei Scan Results -- CVEs (Vuln Count: {impactfulVulnCountCVEs})</li> :
                        <li onClick={(e)=>setCurrentStep(7)}>Nuclei Scan Results -- CVEs (Vuln Count: {impactfulVulnCountCVEs})</li>
                    }
                    {
                        impactfulVulnFoundCNVD ?
                        <li style={{color:"red"}} onClick={(e)=>setCurrentStep(8)}>Nuclei Scan Results -- CNVD (Vuln Count: {impactfulVulnCountCNVD})</li> :
                        <li onClick={(e)=>setCurrentStep(8)}>Nuclei Scan Results -- CNVD (Vuln Count: {impactfulVulnCountCNVD})</li>
                    }
                    {
                        impactfulVulnFoundExposed ?
                        <li style={{color:"red"}} onClick={(e)=>setCurrentStep(9)}>Nuclei Scan Results -- Exposed (Vuln Count: {impactfulVulnCountExposed})</li> :
                        <li onClick={(e)=>setCurrentStep(9)}>Nuclei Scan Results -- Exposed (Vuln Count: {impactfulVulnCountExposed})</li>
                    }
                    {
                        impactfulVulnFoundExposure ?
                        <li style={{color:"red"}} onClick={(e)=>setCurrentStep(10)}>Nuclei Scan Results -- Exposure (Vuln Count: {impactfulVulnCountExposure})</li> :
                        <li onClick={(e)=>setCurrentStep(10)}>Nuclei Scan Results -- Exposure (Vuln Count: {impactfulVulnCountExposure})</li>
                    }
                    {
                        impactfulVulnFoundMisc ?
                        <li style={{color:"red"}} onClick={(e)=>setCurrentStep(11)}>Nuclei Scan Results -- Misc (Vuln Count: {impactfulVulnCountMisc})</li> :
                        <li onClick={(e)=>setCurrentStep(11)}>Nuclei Scan Results -- Misc (Vuln Count: {impactfulVulnCountMisc})</li>
                    }
                    {
                        impactfulVulnFoundNetwork ?
                        <li style={{color:"red"}} onClick={(e)=>setCurrentStep(12)}>Nuclei Scan Results -- Network (Vuln Count: {impactfulVulnCountNetwork})</li> :
                        <li onClick={(e)=>setCurrentStep(12)}>Nuclei Scan Results -- Network (Vuln Count: {impactfulVulnCountNetwork})</li>
                    }
                    {
                        impactfulVulnFoundRs0n ?
                        <li style={{color:"red"}} onClick={(e)=>setCurrentStep(13)}>Nuclei Scan Results -- Rs0n (Vuln Count: {impactfulVulnCountRs0n})</li> :
                        <li onClick={(e)=>setCurrentStep(13)}>Nuclei Scan Results -- Rs0n (Vuln Count: {impactfulVulnCountRs0n})</li>
                    }
                    {
                        impactfulVulnFoundHeadless ?
                        <li style={{color:"red"}} onClick={(e)=>setCurrentStep(14)}>Nuclei Scan Results -- Headless (Vuln Count: {impactfulVulnCountHeadless})</li> :
                        <li onClick={(e)=>setCurrentStep(14)}>Nuclei Scan Results -- Headless (Vuln Count: {impactfulVulnCountHeadless})</li>
                    }
                </ul>
                <li>Custom Scanning</li>
                <ul>
                    <li>CVE Scanning</li>
                    <ul>
                        <li onClick={(e)=>setCurrentStep(20)}>Add CVE</li>
                        <li onClick={(e)=>setCurrentStep(21)}>CVE Scan Results</li>
                    </ul>
                </ul>
            </ul>
        </div>
        <div className="bg-secondary workTableStyle col-8">
            {
                currentStep === 0 ?
                <NucleiScansFull thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 1 ?
                <NucleiScansSSL thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 2 ?
                <NucleiScansFile thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 3 ?
                <NucleiScansDNS thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 4 ?
                <NucleiScansVulns thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 5 ?
                <NucleiScansTech thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 6 ?
                <NucleiScansMisconfigs thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 7 ?
                <NucleiScansCVEs thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 8 ?
                <NucleiScansCNVD thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 9 ?
                <NucleiScansExposed thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 10 ?
                <NucleiScansExposure thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 11 ?
                <NucleiScansMisc thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 12 ?
                <NucleiScansNetwork thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 13 ?
                <NucleiScansRs0n thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 14 ?
                <NucleiScansHeadless thisFqdn={props.thisFqdn} /> :
                ''
            }
        </div>
        </div>
        </div>
    )
}

export default CveTesting;