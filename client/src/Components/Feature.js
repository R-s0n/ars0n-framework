import React, {useState} from 'react';

import '../Component.css';
import HopHeaders from './SubComponents/HopHeaders';
import CachePoisoning from './SubComponents/CachePoisoning';
import Cors from './SubComponents/Cors';
import CspBypass from './SubComponents/CspBypass';



const Feature = props => {
    const [currentStep, setCurrentStep] = useState(0);

    return (
        <div className="container-fluid">
            <div className="row">
        <div className="bg-secondary checklistStyle pt-2 ml-4 col-3">
            <ul>
                <li>Structured Objects</li>
                <ul>
                    <li onClick={(e)=>setCurrentStep(0)}>Deserialization</li>
                    <ul>
                        <li onClick={(e)=>setCurrentStep(1)}>Java</li>
                        <li onClick={(e)=>setCurrentStep(2)}>.NET</li>
                        <li onClick={(e)=>setCurrentStep(3)}>PHP</li>
                        <li onClick={(e)=>setCurrentStep(4)}>Python</li>
                        <li onClick={(e)=>setCurrentStep(5)}>NodeJS</li>
                        <li onClick={(e)=>setCurrentStep(6)}>Ruby</li>
                    </ul>
                    <li onClick={(e)=>setCurrentStep(7)}>Json Web Tokens (JWT)</li>
                    <li onClick={(e)=>setCurrentStep(8)}>XML External Entity (XXE) Injection</li>
                </ul>
                <li>Files</li>
                <ul>
                    <li onClick={(e)=>setCurrentStep(9)}>File Upload</li>
                    <li onClick={(e)=>setCurrentStep(10)}>Formula Injection</li>
                    <li onClick={(e)=>setCurrentStep(11)}>PDF Injection</li>
                    <li onClick={(e)=>setCurrentStep(12)}>Server-Side XSS</li>
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

export default Feature;