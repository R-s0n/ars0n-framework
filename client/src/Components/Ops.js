import React, {useState} from 'react';
import {ToastProvider} from 'react-toast-notifications';
import '../Component.css';
import HopHeaders from './SubComponents/HopHeaders';
import CachePoisoning from './SubComponents/CachePoisoning';
import CacheDeception from './SubComponents/CacheDeception';
import Cors from './SubComponents/Cors';
import CspBypass from './SubComponents/CspBypass';
import HttpRequestSmuggling from './SubComponents/HttpRequestSmuggling';
import H2cSmuggling from './SubComponents/H2cSmuggling';
import H2cSmugglingTunneling from './SubComponents/H2cSmugglingTunneling';
import HostHeader from './SubComponents/HostHeader';



const Ops = props => {
    const [currentStep, setCurrentStep] = useState(0);

    return (
        <>
        <div className="bg-secondary checklistStyle pt-2 ml-4">
            <ul style={{listStyleType: "none"}}>
                <li>Reverse Proxy Testing</li>
                <ul style={{listStyleType: "none"}}>
                    <li onClick={(e)=>setCurrentStep(0)}>Abusing Hop-by-Hop Headers</li>
                    <li onClick={(e)=>setCurrentStep(1)}>Web Cache Poisoning</li>
                    <li onClick={(e)=>setCurrentStep(2)}>Web Cache Deception</li>
                    <li onClick={(e)=>setCurrentStep(3)}>HTTP Request Smuggling</li>
                    <li onClick={(e)=>setCurrentStep(4)}>H2C Smuggling</li>
                    <li onClick={(e)=>setCurrentStep(5)}>H2C Smuggling w/ Tunneling</li>
                </ul>
                <li>HTTP Header Testing</li>
                <ul style={{listStyleType: "none"}}>
                    <li onClick={(e)=>setCurrentStep(8)}>HTTP Host Header Attacks</li>
                    <li onClick={(e)=>setCurrentStep(9)}>Content Security Policy Bypass</li>
                    <li onClick={(e)=>setCurrentStep(10)}>CORS Misconfiguration/Bypass</li>
                </ul>
                <li>AWS Testing</li>
                <ul style={{listStyleType: "none"}}>
                    <li>Identity Access Management (IAM)</li>
                    <li>Key Management Service (KMS)</li>
                    <li>S3 Buckets</li>
                    <ul style={{listStyleType: "none"}}>
                        <li onClick={(e)=>setCurrentStep(22)}>Identify S3 Bucket</li>
                        <li onClick={(e)=>setCurrentStep(22)}>CRUD Tests</li>
                        <li onClick={(e)=>setCurrentStep(22)}>Extract Backup</li>
                        <li onClick={(e)=>setCurrentStep(22)}>Bucket Juicy Data (w/ SSRF)</li>
                    </ul>
                    <li>Hardware Security Module (HSM)</li>
                    <li>AWS CloudTrail</li>
                </ul>
                <li>IIS Testing (<i>https://www.youtube.com/watch?v=cqM-MdPkaWo</i>)</li>
                <ul style={{listStyleType: "none"}}>
                    <li onClick={(e)=>setCurrentStep(18)}>Find Hidden Applications 2:35</li>
                    <li onClick={(e)=>setCurrentStep(18)}>VHost Hopping 5:25</li>
                    <li onClick={(e)=>setCurrentStep(18)}>Local File Disclosure to DLLs 7:53</li>
                    <li onClick={(e)=>setCurrentStep(18)}>Local File Disclosure RCE 10:28</li>
                    <li onClick={(e)=>setCurrentStep(18)}>DNSpy 12:09</li>
                    <li onClick={(e)=>setCurrentStep(18)}>Complex XXE Vectors 14:05</li>
                </ul>
                <li>DNS Testing</li>
                <ul style={{listStyleType: "none"}}>
                    <li onClick={(e)=>setCurrentStep(23)}>DNS Rebinding</li>
                </ul>
            </ul>
        </div>
        <div className="bg-secondary workTableStyle">
            {
                currentStep === 0 ?
                <ToastProvider><HopHeaders thisFqdn={props.thisFqdn} /></ToastProvider> :
                ''
            }
            {
                currentStep === 1 ?
                <ToastProvider><CachePoisoning thisFqdn={props.thisFqdn} /></ToastProvider> :
                ''
            }
            {
                currentStep === 2 ?
                <ToastProvider><CacheDeception thisFqdn={props.thisFqdn} /></ToastProvider> :
                ''
            }
            {
                currentStep === 3 ?
                <ToastProvider><HttpRequestSmuggling thisFqdn={props.thisFqdn} /></ToastProvider> :
                ''
            }
            {
                currentStep === 4 ?
                <ToastProvider><H2cSmuggling thisFqdn={props.thisFqdn} /></ToastProvider> :
                ''
            }
            {
                currentStep === 5 ?
                <ToastProvider><H2cSmugglingTunneling thisFqdn={props.thisFqdn} /></ToastProvider> :
                ''
            }
            {
                currentStep === 8 ?
                <ToastProvider><HostHeader thisFqdn={props.thisFqdn} /></ToastProvider> :
                ''
            }
            {
                currentStep === 9 ?
                <ToastProvider><CspBypass thisFqdn={props.thisFqdn} /></ToastProvider> :
                ''
            }
            {
                currentStep === 10 ?
                <ToastProvider><Cors thisFqdn={props.thisFqdn} /></ToastProvider> :
                ''
            }
        </div>
        </>
    )
}

export default Ops;