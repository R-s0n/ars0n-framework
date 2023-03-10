import React, {useState} from 'react';

import '../Component.css';
import HopHeaders from './SubComponents/HopHeaders';
import CachePoisoning from './SubComponents/CachePoisoning';
import Cors from './SubComponents/Cors';
import CspBypass from './SubComponents/CspBypass';



const Input = props => {
    const [currentStep, setCurrentStep] = useState(0);

    return (
        <div className="container-fluid">
            <div className="row">
        <div className="bg-secondary checklistStyle pt-2 ml-4 col-3">
            <ul>
                <li>Reflected Value Testing</li>
                <ul>
                    <li onClick={(e)=>setCurrentStep(0)}>Client-Side Template Injection (CSTI)</li>
                    <li onClick={(e)=>setCurrentStep(1)}>Command Injection</li>
                    <li onClick={(e)=>setCurrentStep(2)}>Carriage Return / Line Feed (CLRF) Injection</li>
                    <li onClick={(e)=>setCurrentStep(3)}>Dangling Markup</li>
                    <li onClick={(e)=>setCurrentStep(4)}>File Inclusion / Path Traversal</li>
                    <li onClick={(e)=>setCurrentStep(5)}>Open Redirect</li>
                    <li onClick={(e)=>setCurrentStep(6)}>Prototype Pollution</li>
                    <li onClick={(e)=>setCurrentStep(7)}>Server-Side Inclusion (SSI)</li>
                    <li onClick={(e)=>setCurrentStep(8)}>Server-Side Request Forgery (SSRF)</li>
                    <li onClick={(e)=>setCurrentStep(9)}>Server-Side Template Injection (SSTI)</li>
                    <li onClick={(e)=>setCurrentStep(10)}>XSLT Server-Side Injection</li>
                    <li onClick={(e)=>setCurrentStep(11)}>HTML Injection (HTMLi)</li>
                    <li onClick={(e)=>setCurrentStep(12)}>Cross-Site Scripting (XSS)</li>
                    <li onClick={(e)=>setCurrentStep(13)}>Dom-Based Cross-Site Scripting (XSS)</li>
                </ul>
                <li>Injection Testing</li>
                <ul>
                    <li onClick={(e)=>setCurrentStep(14)}>SQL Injection</li>
                    <li onClick={(e)=>setCurrentStep(15)}>NoSQL Injection</li>
                    <li onClick={(e)=>setCurrentStep(16)}>LDAP Injection</li>
                    <li onClick={(e)=>setCurrentStep(17)}>XPath Injection</li>
                    <li onClick={(e)=>setCurrentStep(18)}>GraphQL Injection</li>
                </ul>
                <li>Forms / WebSockets</li>
                <ul>
                    <li onClick={(e)=>setCurrentStep(19)}>Cross-Site Request Forgery (CSRF)</li>
                    <li onClick={(e)=>setCurrentStep(20)}>Cross-Site WebSocket Hijacking</li>
                    <li onClick={(e)=>setCurrentStep(21)}>PostMessage Vulnerabilities</li>
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

export default Input;