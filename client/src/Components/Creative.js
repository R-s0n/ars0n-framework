import React, {useState} from 'react';

import '../Component.css';
import HopHeaders from './SubComponents/HopHeaders';
import CachePoisoning from './SubComponents/CachePoisoning';
import Cors from './SubComponents/Cors';
import CspBypass from './SubComponents/CspBypass';



const Creative = props => {
    const [currentStep, setCurrentStep] = useState(0);

    return (
        <div className="container-fluid">
            <div className="row">
        <div className="bg-secondary checklistStyle pt-2 ml-4 col-3">
            <h4 className="ml-3 pt-2">Creative Application Testing</h4>
            <ul>
                <li style={{fontWeight: "bold"}}>External Identify Access Management (IAM) Testing</li>
                <ul>
                    <li onClick={(e)=>setCurrentStep(0)}>OAuth Misconfiguration</li>
                    <li onClick={(e)=>setCurrentStep(1)}>SAML Misconfiguration</li>
                    <li onClick={(e)=>setCurrentStep(1)}>Google Firebase IAM Misconfiguration</li>
                    <li onClick={(e)=>setCurrentStep(1)}>Keycloak IAM Misconfiguration</li>
                </ul>
                <li style={{fontWeight: "bold"}}>Application Logic Testing</li>
                <ul>
                    <li onClick={(e)=>setCurrentStep(2)}>In-Direct Object Reference (IDOR) - Read/Write</li>
                    <li onClick={(e)=>setCurrentStep(3)}>In-Direct Object Reference (IDOR) - Read Only</li>
                    <li onClick={(e)=>setCurrentStep(2)}>Insufficient Access Controls - Read/Write</li>
                    <li onClick={(e)=>setCurrentStep(3)}>Insufficient Access Controls - Read Only</li>
                    <li onClick={(e)=>setCurrentStep(2)}>Bypass Access Controls - Read/Write</li>
                    <li onClick={(e)=>setCurrentStep(3)}>Bypass Access Controls - Read Only</li>
                    <li onClick={(e)=>setCurrentStep(3)}>2FA/MFA Bypass</li>
                    <li onClick={(e)=>setCurrentStep(3)}>Captcha Bypass</li>
                    <li onClick={(e)=>setCurrentStep(3)}>Rate Limiting/Brute-force Bypass</li>
                    <li onClick={(e)=>setCurrentStep(3)}>Bypass Registration Restrictions</li>
                    <li onClick={(e)=>setCurrentStep(3)}>Bypass Payment Process Restrictions</li>
                    <li onClick={(e)=>setCurrentStep(3)}>Bypass Password Reset Restrictions</li>
                    <li onClick={(e)=>setCurrentStep(3)}>Race Conditions</li>
                    <li onClick={(e)=>setCurrentStep(3)}>Username Enumeration</li>
                </ul>
                <li style={{fontWeight: "bold"}}>Public Repository & OSINT Testing</li>
                <ul>
                    <li onClick={(e)=>setCurrentStep(0)}>Internal Source Code on Public GitHub Repo</li>
                    <li onClick={(e)=>setCurrentStep(1)}>Internal/Priviledged Creds on Public GitHub Repo</li>
                    <li onClick={(e)=>setCurrentStep(1)}>Internal Source Code Found in Web Scraping</li>
                    <li onClick={(e)=>setCurrentStep(1)}>Internal/Priviledged Creds Found in Web Scraping</li>
                </ul>
            </ul>
        </div>
        <div className="bg-secondary workTableStyle col-8">
            {
                currentStep === 0 ?
                <HopHeaders thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 1 ?
                <CachePoisoning thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 8 ?
                <CspBypass thisFqdn={props.thisFqdn} /> :
                ''
            }
            {
                currentStep === 9 ?
                <Cors thisFqdn={props.thisFqdn} /> :
                ''
            }
        </div>
        </div>
        </div>
    )
}

export default Creative;