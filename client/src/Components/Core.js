import React, {useState} from 'react';

import '../Component.css';
import HopHeaders from './SubComponents/HopHeaders';
import CachePoisoning from './SubComponents/CachePoisoning';
import Cors from './SubComponents/Cors';
import CspBypass from './SubComponents/CspBypass';



const Core = props => {
    const [currentStep, setCurrentStep] = useState(0);

    return (
        <div className="container-fluid">
            <div className="row">
        <div className="bg-secondary checklistStyle pt-2 ml-4 col-3">
            <h4 className="ml-3 pt-2">Core Application Testing</h4>
            <ul>
                <li style={{fontWeight: "bold"}}>Global Application Config Testing</li>
                <ul>
                    <li onClick={(e)=>setCurrentStep(0)}>Content Security Policy (CSP)</li>
                    <li onClick={(e)=>setCurrentStep(1)}>Cross-Origin Resource Sharing (CORS)</li>
                    <li onClick={(e)=>setCurrentStep(2)}>Dependency Confusion</li>
                    <li onClick={(e)=>setCurrentStep(3)}>JSON Web Token (JWT) Misconfiguration</li>
                    <li onClick={(e)=>setCurrentStep(4)}>File Inclusion / Path Traversal</li>
                </ul>
                <li style={{fontWeight: "bold"}}>Client-Side Codebase Testing</li>
                <ul>
                    <li onClick={(e)=>setCurrentStep(5)}>Reflected Cross-Site Scripting (XSS)</li>
                    <li onClick={(e)=>setCurrentStep(6)}>DOM-Based Cross-Site Scripting (XSS)</li>
                    <li onClick={(e)=>setCurrentStep(7)}>Client-Side Prototype Pollution (CSPP)</li>
                    <li onClick={(e)=>setCurrentStep(8)}>Client-Side Template Injection</li>
                    <li onClick={(e)=>setCurrentStep(9)}>PostMessage Vulnerabilities</li>
                    <li onClick={(e)=>setCurrentStep(10)}>Dangling Markup</li>
                    <li onClick={(e)=>setCurrentStep(11)}>Denial of Service (DoS)</li>
                    <li onClick={(e)=>setCurrentStep(12)}>Information Disclosure</li>
                    <li onClick={(e)=>setCurrentStep(13)}>Priviledged Credentials Exposed</li>
                    <li onClick={(e)=>setCurrentStep(14)}>DOM-Based Open Redirect</li>
                    <li onClick={(e)=>setCurrentStep(15)}>Content Injection</li>
                    <li onClick={(e)=>setCurrentStep(16)}>Insecure Data Storage</li>
                </ul>
                <li style={{fontWeight: "bold"}}>Server-Side Codebase Testing</li>
                <ul>
                    <li onClick={(e)=>setCurrentStep(19)}>Command Injection</li>
                    <li onClick={(e)=>setCurrentStep(20)}>Stored Cross-Site Scripting (XSS)</li>
                    <li onClick={(e)=>setCurrentStep(21)}>Blind Cross-Site Scripting (XSS)</li>
                    <li onClick={(e)=>setCurrentStep(22)}>Code Injection</li>
                    <li onClick={(e)=>setCurrentStep(23)}>Server-Side Prototype Pollution (SSPP)</li>
                    <li onClick={(e)=>setCurrentStep(24)}>Insecure Deserialization</li>
                    <li onClick={(e)=>setCurrentStep(25)}>LDAP Injection</li>
                    <li onClick={(e)=>setCurrentStep(26)}>Server-Side Request Forgery (SSRF)</li>
                    <li onClick={(e)=>setCurrentStep(27)}>File Inclusion / Path Traversal</li>
                    <li onClick={(e)=>setCurrentStep(28)}>XPATH Injection</li>
                    <li onClick={(e)=>setCurrentStep(29)}>Cross-Site Request Forgery (CSRF)</li>
                    <li onClick={(e)=>setCurrentStep(30)}>Unrestricted File Upload</li>
                    <li onClick={(e)=>setCurrentStep(31)}>Web Shell via File Upload</li>
                    <li onClick={(e)=>setCurrentStep(32)}>Server-Side Template Injection</li>
                    <li onClick={(e)=>setCurrentStep(33)}>XML External Entity (XEE)</li>
                    <li onClick={(e)=>setCurrentStep(34)}>WebSocket Injection</li>
                </ul>
                <li style={{fontWeight: "bold"}}>Database Operation Testing</li>
                <ul>
                    <li onClick={(e)=>setCurrentStep(35)}>SQL Injection</li>
                    <li onClick={(e)=>setCurrentStep(36)}>NoSQL Injection</li>
                    <li onClick={(e)=>setCurrentStep(37)}>GraphQL Injection</li>
                    <li onClick={(e)=>setCurrentStep(38)}>Denial of Service (DoS)</li>
                    <li onClick={(e)=>setCurrentStep(39)}>Information Disclosure</li>
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

export default Core;